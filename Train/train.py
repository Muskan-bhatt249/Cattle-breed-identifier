import os
import json
import time
from typing import Tuple, Dict

import torch
from torch import nn
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, models, transforms
from tqdm import tqdm

# Prefer DirectML (AMD on Windows) > CUDA > CPU
try:
	import torch_directml  # type: ignore
	_DEVICE = torch_directml.device()
except Exception:
	_DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

DATASET_DIR = os.path.join(os.getcwd(), "Dataset")
CHECKPOINTS_DIR = os.path.join(os.getcwd(), "checkpoints")
ARTIFACTS_DIR = os.path.join(os.getcwd(), "artifacts")

os.makedirs(CHECKPOINTS_DIR, exist_ok=True)
os.makedirs(ARTIFACTS_DIR, exist_ok=True)


def build_dataloaders(dataset_dir: str, image_size: int = 224, batch_size: int = 32, val_split: float = 0.2, num_workers: int = 2) -> Tuple[DataLoader, DataLoader, Dict[int, str]]:
	train_transforms = transforms.Compose([
		transforms.RandomResizedCrop(image_size, scale=(0.7, 1.0), ratio=(0.75, 1.33)),
		transforms.RandomHorizontalFlip(),
		transforms.RandomRotation(15),
		transforms.ColorJitter(brightness=0.25, contrast=0.25, saturation=0.25, hue=0.1),
		transforms.RandomApply([transforms.GaussianBlur(kernel_size=3, sigma=(0.1, 2.0))], p=0.3),
		transforms.RandomApply([transforms.GaussianBlur(kernel_size=5, sigma=(0.1, 3.0))], p=0.2),
		transforms.ToTensor(),
		transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
	])
	val_transforms = transforms.Compose([
		transforms.Resize((image_size, image_size)),
		transforms.ToTensor(),
		transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
	])

	full_dataset = datasets.ImageFolder(root=dataset_dir, transform=train_transforms)
	class_to_idx = full_dataset.class_to_idx
	idx_to_class = {v: k for k, v in class_to_idx.items()}

	total_size = len(full_dataset)
	val_size = int(total_size * val_split)
	train_size = total_size - val_size

	train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])
	# Override transform for validation subset
	val_dataset.dataset.transform = val_transforms

	train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers, pin_memory=True)
	val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers, pin_memory=True)

	with open(os.path.join(ARTIFACTS_DIR, "idx_to_class.json"), "w", encoding="utf-8") as f:
		json.dump(idx_to_class, f, indent=2)

	return train_loader, val_loader, idx_to_class


def build_model(num_classes: int) -> nn.Module:
	model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
	for param in model.parameters():
		param.requires_grad = False
	# Unfreeze the last residual block for fine-tuning
	for param in model.layer4.parameters():
		param.requires_grad = True
	in_features = model.fc.in_features
	model.fc = nn.Sequential(
		nn.Dropout(p=0.3),
		nn.Linear(in_features, 512),
		nn.ReLU(inplace=True),
		nn.Dropout(p=0.3),
		nn.Linear(512, num_classes),
	)
	return model


def evaluate(model: nn.Module, data_loader: DataLoader, criterion: nn.Module, device) -> Tuple[float, float]:
	model.eval()
	loss_sum = 0.0
	correct = 0
	total = 0
	with torch.no_grad():
		for inputs, targets in data_loader:
			inputs = inputs.to(device)
			targets = targets.to(device)
			outputs = model(inputs)
			loss = criterion(outputs, targets)
			loss_sum += loss.item() * inputs.size(0)
			_, preds = torch.max(outputs, 1)
			correct += torch.sum(preds == targets).item()
			total += targets.size(0)
	avg_loss = loss_sum / max(total, 1)
	accuracy = correct / max(total, 1)
	return avg_loss, accuracy


def train(num_epochs: int = 15, batch_size: int = 32, lr: float = 3e-4, image_size: int = 224, val_split: float = 0.2, num_workers: int = 2):
	device = _DEVICE
	train_loader, val_loader, idx_to_class = build_dataloaders(DATASET_DIR, image_size, batch_size, val_split, num_workers)
	model = build_model(num_classes=len(idx_to_class))
	model.to(device)

	criterion = nn.CrossEntropyLoss()
	optimizer = AdamW(filter(lambda p: p.requires_grad, model.parameters()), lr=lr)
	scheduler = CosineAnnealingLR(optimizer, T_max=num_epochs)

	best_val_acc = 0.0
	best_ckpt_path = os.path.join(CHECKPOINTS_DIR, "best_model.pt")

	for epoch in range(1, num_epochs + 1):
		model.train()
		epoch_loss = 0.0
		epoch_correct = 0
		epoch_total = 0

		progress = tqdm(train_loader, desc=f"Epoch {epoch}/{num_epochs}", leave=False)
		for inputs, targets in progress:
			inputs = inputs.to(device)
			targets = targets.to(device)
			optimizer.zero_grad(set_to_none=True)
			outputs = model(inputs)
			loss = criterion(outputs, targets)
			loss.backward()
			optimizer.step()
			_, preds = torch.max(outputs, 1)
			epoch_loss += loss.item() * inputs.size(0)
			epoch_correct += torch.sum(preds == targets).item()
			epoch_total += targets.size(0)
			progress.set_postfix({"loss": f"{loss.item():.4f}"})

		train_loss = epoch_loss / max(epoch_total, 1)
		train_acc = epoch_correct / max(epoch_total, 1)
		val_loss, val_acc = evaluate(model, val_loader, criterion, device)
		scheduler.step()

		print(f"Epoch {epoch}/{num_epochs}: train_loss={train_loss:.4f} train_acc={train_acc:.4f} val_loss={val_loss:.4f} val_acc={val_acc:.4f}")

		if val_acc > best_val_acc:
			best_val_acc = val_acc
			torch.save({
				"model_state": model.state_dict(),
				"idx_to_class": idx_to_class,
				"image_size": image_size,
				"timestamp": int(time.time()),
			}, best_ckpt_path)
			print(f"Saved new best model to {best_ckpt_path} (val_acc={best_val_acc:.4f})")

	print(f"Best val accuracy: {best_val_acc:.4f}")


if __name__ == "__main__":
	train()
