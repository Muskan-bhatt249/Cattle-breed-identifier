import os
import io
import json
from typing import Dict, List, Tuple
import difflib

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import torch
from torch import nn
from torchvision import models, transforms


# Prefer DirectML (AMD on Windows) > CUDA > CPU
try:
	import torch_directml  # type: ignore
	_DEVICE = torch_directml.device()
except Exception:
	_DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


CHECKPOINTS_DIR = os.path.join(os.getcwd(), "checkpoints")
ARTIFACTS_DIR = os.path.join(os.getcwd(), "artifacts")
# Search breed_info.json in common locations
_POSSIBLE_BREED_INFO_PATHS = [
	os.path.join(os.getcwd(), "breed_info.json"),
	os.path.join(ARTIFACTS_DIR, "breed_info.json"),
	os.path.join(os.getcwd(), "data", "breed_info.json"),
]


app = FastAPI(title="Cattle Breed Identifier API", version="1.0.0")

# Allow browser apps to call the API during development
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


_MODEL: nn.Module = None  # type: ignore
_IDX_TO_CLASS: Dict[int, str] = {}
_TRANSFORM = None
_IMAGE_SIZE: int = 224
_BREED_INFO: Dict[str, Dict] = {}
_BREED_INDEX: Dict[str, str] = {}


def _build_model(num_classes: int) -> nn.Module:
	model = models.resnet18(weights=None)
	in_features = model.fc.in_features
	model.fc = nn.Sequential(
		nn.Dropout(p=0.3),
		nn.Linear(in_features, 512),
		nn.ReLU(inplace=True),
		nn.Dropout(p=0.3),
		nn.Linear(512, num_classes),
	)
	return model


def _normalize_key(k: str) -> str:
	# lower case, replace underscores, remove common suffixes
	key = (k or "").strip().lower().replace("_", " ")
	for suffix in [" buffalo", " cattle", " cow", " breed"]:
		if key.endswith(suffix):
			key = key[: -len(suffix)]
	return " ".join(key.split())


def _load_artifacts() -> Tuple[nn.Module, Dict[int, str], transforms.Compose, int, Dict[str, Dict], Dict[str, str]]:
	idx_path = os.path.join(ARTIFACTS_DIR, "idx_to_class.json")
	ckpt_path = os.path.join(CHECKPOINTS_DIR, "best_model.pt")
	if not os.path.exists(idx_path) or not os.path.exists(ckpt_path):
		raise FileNotFoundError("Model artifacts not found. Ensure checkpoints/best_model.pt and artifacts/idx_to_class.json exist.")
	with open(idx_path, "r", encoding="utf-8") as f:
		idx_to_class: Dict[int, str] = json.load(f)
	ckpt = torch.load(ckpt_path, map_location="cpu")
	image_size: int = int(ckpt.get("image_size", 224))
	model = _build_model(len(idx_to_class))
	model.load_state_dict(ckpt["model_state"], strict=True)
	model.eval()
	transform = transforms.Compose([
		transforms.Resize(int(image_size * 1.15)),
		transforms.CenterCrop(image_size),
		transforms.ToTensor(),
		transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
	])
	breed_info: Dict[str, Dict] = {}
	for p in _POSSIBLE_BREED_INFO_PATHS:
		if os.path.exists(p):
			with open(p, "r", encoding="utf-8") as f:
				breed_info = json.load(f)
			break
	breed_index: Dict[str, str] = {_normalize_key(name): name for name in breed_info.keys()}
	return model.to(_DEVICE), idx_to_class, transform, image_size, breed_info, breed_index


def _ensure_loaded() -> None:
	global _MODEL, _IDX_TO_CLASS, _TRANSFORM, _IMAGE_SIZE, _BREED_INFO, _BREED_INDEX
	if _MODEL is None or _TRANSFORM is None or not _IDX_TO_CLASS:
		_MODEL, _IDX_TO_CLASS, _TRANSFORM, _IMAGE_SIZE, _BREED_INFO, _BREED_INDEX = _load_artifacts()


def _softmax(t: torch.Tensor) -> torch.Tensor:
	return torch.softmax(t, dim=1)


def _entropy(probabilities: torch.Tensor) -> float:
	# probabilities must sum to 1 along last dim
	eps = 1e-9
	p = probabilities.clamp(min=eps)
	h = -torch.sum(p * torch.log(p))
	return float(h.item())


def _predict_pil(image: Image.Image, top_k: int = 3) -> List[Dict]:
	image = image.convert("RGB")

	# Light TTA to stabilize predictions and measure uncertainty
	tta_transforms = [
		transforms.Compose([
			transforms.Resize(int(_IMAGE_SIZE * 1.15)),
			transforms.CenterCrop(_IMAGE_SIZE),
			transforms.ToTensor(),
			transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
		]),
		transforms.Compose([
			transforms.Resize(int(_IMAGE_SIZE * 1.15)),
			transforms.CenterCrop(_IMAGE_SIZE),
			transforms.RandomHorizontalFlip(p=1.0),
			transforms.ToTensor(),
			transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
		]),
		transforms.Compose([
			transforms.Resize(int(_IMAGE_SIZE * 1.15)),
			transforms.CenterCrop(_IMAGE_SIZE),
			transforms.ColorJitter(brightness=0.1, contrast=0.1),
			transforms.ToTensor(),
			transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
		]),
	]

	probs_list = []
	with torch.no_grad():
		for tform in tta_transforms:
			tensor = tform(image).unsqueeze(0).to(_DEVICE)
			logits = _MODEL(tensor)
			probs = _softmax(logits).squeeze(0)
			probs_list.append(probs)

	# Average probabilities across TTA
	avg_probs = torch.mean(torch.stack(probs_list, dim=0), dim=0)
	probs = avg_probs.cpu()

	# map to labels
	label_probs = [( _IDX_TO_CLASS[str(i)], float(probs[i]) ) for i in range(len(probs))]
	label_probs.sort(key=lambda kv: kv[1], reverse=True)

	# Uncertainty checks: top-1 margin and entropy
	best_prob = label_probs[0][1] if label_probs else 0.0
	second_prob = label_probs[1][1] if len(label_probs) > 1 else 0.0
	margin = best_prob - second_prob
	ent = _entropy(probs)

	# Heuristics tuned for open-set rejection
	is_non_cattle = (best_prob < 0.6) or (margin < 0.25) or (ent > 1.5)
	if is_non_cattle:
		return [{"label": "Not a cow or buffalo", "probability": 0.9}]

	return [ {"label": l, "probability": p} for l, p in label_probs[:top_k] ]


@app.get("/health")
def health() -> Dict[str, str]:
	return {"status": "ok", "model_loaded": "yes" if _MODEL is not None else "no"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)) -> JSONResponse:
	try:
		_ensure_loaded()
		data = await file.read()
		image = Image.open(io.BytesIO(data))
		preds = _predict_pil(image, top_k=3)
		best = preds[0] if preds else {"label": "", "probability": 0.0}
		# Robust lookup: case-insensitive + fuzzy + token normalized
		norm = _normalize_key(best["label"]) if best.get("label") else ""
		matched_key = _BREED_INDEX.get(norm)
		if matched_key is None and _BREED_INDEX:
			candidates = list(_BREED_INDEX.keys())
			close = difflib.get_close_matches(norm, candidates, n=1, cutoff=0.6)
			if close:
				matched_key = _BREED_INDEX.get(close[0])
		info = _BREED_INFO.get(matched_key) if matched_key else None
		return JSONResponse({
			"prediction": best,
			"topk": preds,
			"image_size": _IMAGE_SIZE,
			"info": info,
			"matched_key": matched_key,
			"available_breeds": list(_BREED_INFO.keys()),
		})
	except Exception as e:
		return JSONResponse({"error": str(e)}, status_code=400)


# Dev entrypoint: uvicorn Train.api:app --reload



