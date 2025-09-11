import os
import json
import io
import difflib

import streamlit as st
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

@st.cache_resource(show_spinner=False)
def load_model_and_metadata():
	idx_path = os.path.join(ARTIFACTS_DIR, "idx_to_class.json")
	ckpt_path = os.path.join(CHECKPOINTS_DIR, "best_model.pt")
	with open(idx_path, "r", encoding="utf-8") as f:
		idx_to_class = json.load(f)
	# Load breed info from common locations
	breed_info = {}
	possible_bi_paths = [
		os.path.join(os.getcwd(), "breed_info.json"),
		os.path.join(ARTIFACTS_DIR, "breed_info.json"),
		os.path.join(os.getcwd(), "data", "breed_info.json"),
	]
	for bi_path in possible_bi_paths:
		if os.path.exists(bi_path):
			with open(bi_path, "r", encoding="utf-8") as f:
				breed_info = json.load(f)
			break
	ckpt = torch.load(ckpt_path, map_location="cpu")
	image_size = ckpt.get("image_size", 224)
	model = models.resnet18(weights=None)
	in_features = model.fc.in_features
	model.fc = nn.Sequential(
		nn.Dropout(p=0.3),
		nn.Linear(in_features, 512),
		nn.ReLU(inplace=True),
		nn.Dropout(p=0.3),
		nn.Linear(512, len(idx_to_class)),
	)
	model.load_state_dict(ckpt["model_state"], strict=True)
	model.eval()
	transform = transforms.Compose([
		transforms.Resize((image_size, image_size)),
		transforms.ToTensor(),
		transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
	])

	# Build a case-insensitive index for breed lookup
	def _normalize_key(k: str) -> str:
		return (k or "").strip().lower().replace("_", " ")
	breed_index = {_normalize_key(name): name for name in breed_info.keys()}

	return model.to(_DEVICE), idx_to_class, transform, breed_info, breed_index


def predict_image(image: Image.Image, model, idx_to_class, transform, use_tta: bool = True):
	image = image.convert("RGB")
	
	if use_tta:
		# Test-time augmentation for better robustness
		tta_transforms = [
			transforms.Compose([
				transforms.Resize((224, 224)),
				transforms.CenterCrop(224),
				transforms.ToTensor(),
				transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
			]),
			transforms.Compose([
				transforms.Resize((224, 224)),
				transforms.CenterCrop(224),
				transforms.RandomHorizontalFlip(p=1.0),
				transforms.ToTensor(),
				transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
			]),
			transforms.Compose([
				transforms.Resize((224, 224)),
				transforms.CenterCrop(224),
				transforms.ColorJitter(brightness=0.1, contrast=0.1),
				transforms.ToTensor(),
				transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
			]),
		]
		
		all_probs = []
		for tta_transform in tta_transforms:
			tensor = tta_transform(image).unsqueeze(0).to(_DEVICE)
			with torch.no_grad():
				logits = model(tensor)
				probs = torch.softmax(logits, dim=1)
				all_probs.append(probs)
		
		# Average the predictions
		avg_probs = torch.mean(torch.cat(all_probs, dim=0), dim=0).squeeze(0)
		probabilities = avg_probs.tolist()
	else:
		# Single prediction
		tensor = transform(image).unsqueeze(0).to(_DEVICE)
		with torch.no_grad():
			probs = torch.softmax(model(tensor), dim=1).squeeze(0).tolist()
			probabilities = probs
	
	return {idx_to_class[str(i)]: float(probabilities[i]) for i in range(len(probabilities))}


st.set_page_config(page_title="Cattle Breed Identifier", page_icon="🐄", layout="centered")
st.title("Cattle Breed Identifier 🐄")
st.write("Upload an image of a cattle/buffalo to identify its breed and get best-practice guidance.")

if not os.path.exists(os.path.join(CHECKPOINTS_DIR, "best_model.pt")):
	st.warning("No trained model found. Train the model first by running: python train.py")
	st.stop()

model, idx_to_class, transform, breed_info, breed_index = load_model_and_metadata()

uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded is not None:
	image = Image.open(io.BytesIO(uploaded.read()))
	st.image(image, caption="Uploaded image", use_container_width=True)
	if st.button("Predict"):
		with st.spinner("Predicting..."):
			preds = predict_image(image, model, idx_to_class, transform)
			top = sorted(preds.items(), key=lambda kv: kv[1], reverse=True)
			label, p = top[0]
			st.subheader(f"Prediction: {label} ({p*100:.2f}%)")
			st.write("Top-3:")
			for i, (l, prob) in enumerate(top[:3], start=1):
				st.write(f"{i}. {l}: {prob*100:.2f}%")

			# Robust breed-info lookup (case-insensitive + fuzzy match)
			norm_label = label.strip().lower().replace("_", " ")
			original_key = breed_index.get(norm_label)
			if original_key is None and breed_index:
				candidates = list(breed_index.keys())
				close = difflib.get_close_matches(norm_label, candidates, n=1, cutoff=0.8)
				if close:
					original_key = breed_index.get(close[0])

			info = breed_info.get(original_key) if original_key else None
			if info:
				st.markdown("---")
				st.subheader("Breed Information")
				st.markdown(f"**Description**: {info.get('description', 'N/A')}")
				if info.get("characteristics"):
					st.markdown("**Characteristics**:")
					for c in info["characteristics"]:
						st.write(f"- {c}")
				if info.get("fodder_requirements"):
					st.markdown("**Fodder requirements**:")
					for f in info["fodder_requirements"]:
						st.write(f"- {f}")
				if info.get("government_schemes"):
					st.markdown("**Government schemes**:")
					for s in info["government_schemes"]:
						st.write(f"- {s}")
				if info.get("best_practices"):
					st.markdown("**Best practices**:")
					for b in info["best_practices"]:
						st.write(f"- {b}")
			else:
				if not breed_info:
					st.info("No 'breed_info.json' found. Place it in the project root or 'artifacts/'.")
				else:
					st.info("No detailed info found for this predicted breed. Check names/casing in 'breed_info.json'.")
					with st.expander("Show available breeds"):
						for name in sorted(breed_info.keys()):
							st.write(f"- {name}")
