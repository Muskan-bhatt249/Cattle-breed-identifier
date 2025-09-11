# Cattle Breed Identifier API (FastAPI)

This project identifies cattle/buffalo breeds from images using a fine-tuned ResNet18 model and provides breed-specific information.

- FastAPI service for programmatic predictions

## Prerequisites

- Windows 10/11
- Python 3.10 installed and available as `py` or `python`
- Internet access for first-time dependency installation

## Clone and Navigate

```powershell
cd "C:\Cattle AII\cattle-breed-identifier\Train"
```

If your path is different, open PowerShell in the repo root and `cd` into `cattle-breed-identifier\Train`.

## Create a Virtual Environment (recommended)

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
```

You can activate it (optional):

```powershell
.\.venv\Scripts\activate
```

> You can always run the venv Python directly without activation using `.\.venv\Scripts\python.exe`.

## Model Artifacts

Make sure these files exist (already present in this repo):

- `Train\checkpoints\best_model.pt`
- `Train\artifacts\idx_to_class.json`

If they are missing, the API will return an error indicating the artifacts are not found.

## Run the FastAPI Service

Install minimal dependencies required by the API and start the server:

```powershell
.\.venv\Scripts\python.exe -m pip install fastapi==0.116.1 uvicorn[standard]==0.35.0 pillow==11.3.0 torch==2.4.1 torchvision==0.19.1
.\.venv\Scripts\python.exe -m uvicorn api:app --host 127.0.0.1 --port 8000 --reload
```

- API base: `http://127.0.0.1:8000`
- Docs (Swagger UI): `http://127.0.0.1:8000/docs`
- Health check: `GET /health`
- Prediction: `POST /predict` with form-data file field named `file`

See `docs/API.md` for response formats and examples.

## Project Structure

```
cattle-breed-identifier/
├─ Train/
│  ├─ api.py                # FastAPI app
│  ├─ train.py              # Training script
│  ├─ infer.py              # Local inference helper
│  ├─ requirements.txt      # Python deps
│  ├─ artifacts/
│  │  └─ idx_to_class.json  # Class index mapping
│  └─ checkpoints/
│     └─ best_model.pt      # Trained model weights
└─ docs/
   ├─ API.md
   └─ TROUBLESHOOTING.md
```

## Notes

- GPU on Windows: If `torch_directml` is installed, the API will prefer DirectML (AMD). Otherwise it will use CUDA if available, else CPU.
- Security: Do not expose the API publicly without authentication and CORS hardening.

## Troubleshooting

- The term `.\.venv\Scripts\python.exe` is not recognized
  - Create the venv first: `py -3 -m venv .venv`
  - Then use the full path or activate it: `.\.venv\Scripts\activate`
- `No trained model found` / artifacts missing
  - Ensure `Train\checkpoints\best_model.pt` and `Train\artifacts\idx_to_class.json` exist
- `ModuleNotFoundError: No module named 'uvicorn'`
  - Install FastAPI/Uvicorn in the venv (see commands above)
- `Form data requires "python-multipart"`
  - Install: `.\.venv\Scripts\python.exe -m pip install python-multipart`
- Port already in use
  - Uvicorn: change `--port 8001`

## License

Internal / for demo use.





