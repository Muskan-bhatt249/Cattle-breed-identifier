import os
import json
import argparse
from typing import Dict

import torch
from torch import nn
from torchvision import models, transforms
from PIL import Image

# Prefer DirectML (AMD on Windows) > CUDA > CPU
try:
	import torch_directml  # type: ignore
	_DEVICE = torch_directml.device()
except Exception:
	_DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

CHECKPOINTS_DIR = os.path.join(os.getcwd(), "checkpoints")
ARTIFACTS_DIR = os.path.join(os.getcwd(), "artifacts")


def load_model(ckpt_path: str) -> nn.Module:
	with open(os.path.join(ARTIFACTS_DIR, "idx_to_class.json"), "r", encoding="utf-8") as f:
		idx_to_class: Dict[int, str] = json.load(f)

	model = models.resnet18(weights=None)
	in_features = model.fc.in_features
	model.fc = nn.Sequential(
		nn.Dropout(p=0.3),
		nn.Linear(in_features, 512),
		nn.ReLU(inplace=True),
		nn.Dropout(p=0.3),
		nn.Linear(512, len(idx_to_class)),
	)
	ckpt = torch.load(ckpt_path, map_location="cpu")
	model.load_state_dict(ckpt["model_state"], strict=True)
	model.eval()
	return model.to(_DEVICE), idx_to_class, ckpt.get("image_size", 224)


def predict(image_path: str, ckpt_path: str, use_tta: bool = True):
	model, idx_to_class, image_size = load_model(ckpt_path)
	
	# Base transform
	base_transform = transforms.Compose([
		transforms.Resize(int(image_size * 1.15)),
		transforms.CenterCrop(image_size),
		transforms.ToTensor(),
		transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
	])
	
	# TTA transforms for robustness
	tta_transforms = [
		transforms.Compose([
			transforms.Resize(int(image_size * 1.15)),
			transforms.CenterCrop(image_size),
			transforms.ToTensor(),
			transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
		]),
		transforms.Compose([
			transforms.Resize(int(image_size * 1.15)),
			transforms.CenterCrop(image_size),
			transforms.RandomHorizontalFlip(p=1.0),
			transforms.ToTensor(),
			transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
		]),
		transforms.Compose([
			transforms.Resize(int(image_size * 1.15)),
			transforms.CenterCrop(image_size),
			transforms.ColorJitter(brightness=0.1, contrast=0.1),
			transforms.ToTensor(),
			transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
		]),
	]
	
	image = Image.open(image_path).convert("RGB")
	
	if use_tta:
		# Test-time augmentation: average predictions from multiple transforms
		all_probs = []
		for transform in tta_transforms:
			tensor = transform(image).unsqueeze(0).to(_DEVICE)
			with torch.no_grad():
				logits = model(tensor)
				probs = torch.softmax(logits, dim=1)
				all_probs.append(probs)
		
		# Average the predictions
		avg_probs = torch.mean(torch.cat(all_probs, dim=0), dim=0).squeeze(0)
		probabilities = avg_probs.tolist()
	else:
		# Single prediction
		tensor = base_transform(image).unsqueeze(0).to(_DEVICE)
		with torch.no_grad():
			logits = model(tensor)
			probs = torch.softmax(logits, dim=1).squeeze(0)
			probabilities = probs.tolist()
	
	result = {idx_to_class[str(i)]: float(probabilities[i]) for i in range(len(probabilities))}
	return dict(sorted(result.items(), key=lambda kv: kv[1], reverse=True))


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("image", type=str, help="Path to input image")
	parser.add_argument("--ckpt", type=str, default=os.path.join(CHECKPOINTS_DIR, "best_model.pt"))
	args = parser.parse_args()
	preds = predict(args.image, args.ckpt)
	best = next(iter(preds.items()))
	print(f"Prediction: {best[0]} ({best[1]*100:.2f}%)")
	print("Top-3:")
	for i, (label, p) in enumerate(list(preds.items())[:3], start=1):
		print(f" {i}. {label}: {p*100:.2f}%")


if __name__ == "__main__":
	main()