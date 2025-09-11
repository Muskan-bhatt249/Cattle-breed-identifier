# Cattle Breed Identifier (Streamlit + FastAPI)

This project identifies cattle/buffalo breeds from images using a fine-tuned ResNet18 model and provides breed-specific information. It includes:

- Streamlit web app for interactive uploads and results
- FastAPI service for programmatic predictions

## Prerequisites

- Windows 10/11
- Python 3.10+ installed
- Internet access for first-time dependency installation

## Quick Start (Streamlit App)

1) Open PowerShell and run:

```
cd "C:\Users\Devesh\Desktop\SIH 2025\Train"
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

- App URL: http://localhost:8501

If you see: "No trained model found", ensure these files exist:
- `checkpoints\best_model.pt`
- `artifacts\idx_to_class.json`

## Quick Start (FastAPI Service)

1) From the same folder:

```
cd "C:\Users\Devesh\Desktop\SIH 2025\Train"
.\.venv\Scripts\python.exe -m pip install fastapi "uvicorn[standard]" python-multipart
.\.venv\Scripts\python.exe -m uvicorn api:app --host 127.0.0.1 --port 8000 --reload
```

- API base: http://127.0.0.1:8000
- Health check: `GET /health`
- Prediction: `POST /predict` with form-data file field named `file`

See `docs/API.md` for full API details and examples.

## Project Structure

```
SIH 2025/
├─ Train/
│  ├─ app.py                # Streamlit UI
│  ├─ api.py                # FastAPI app
│  ├─ train.py              # Training script
│  ├─ infer.py              # Local inference helper
│  ├─ requirements.txt      # Python deps
│  ├─ breed_info.json       # Optional breed metadata
│  ├─ artifacts/
│  │  └─ idx_to_class.json  # Class index mapping
│  └─ checkpoints/
│     └─ best_model.pt      # Trained model weights
└─ docs/
   ├─ API.md
   └─ TROUBLESHOOTING.md
```

## Notes

- GPU: On Windows with AMD GPUs, `torch_directml` is used if available; otherwise CUDA or CPU.
- Port conflicts: Run Streamlit on a different port with `--server.port 8502`.
- Security: Do not expose the API publicly without authentication and CORS hardening.

## Troubleshooting

Common fixes are documented in `docs/TROUBLESHOOTING.md`. Highlights:
- `ModuleNotFoundError: No module named 'streamlit'` → install deps in the venv
- `No module named 'uvicorn'` → install FastAPI/Uvicorn in the venv
- `No module named 'Train'` → run `uvicorn api:app` from the `Train` folder, or add `__init__.py` and run as package
- `Form data requires "python-multipart"` → install `python-multipart`

## License

Internal / for SIH use.





