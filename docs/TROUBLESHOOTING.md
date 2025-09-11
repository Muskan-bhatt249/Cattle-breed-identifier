# Troubleshooting

## Environment / Installation

- "python is not recognized": Install Python and reopen PowerShell, or use full path `C:\Python310\python.exe`.
- Packages not found (e.g., streamlit/uvicorn): Ensure you are using the project venv:
  ```
  cd "C:\Users\Devesh\Desktop\SIH 2025\Train"
  .\.venv\Scripts\python.exe -m pip install -r requirements.txt
  ```

## Streamlit

- `ModuleNotFoundError: No module named 'streamlit'`
  - Install inside venv: `.\.venv\Scripts\python.exe -m pip install streamlit`
  - Run with: `.\.venv\Scripts\python.exe -m streamlit run app.py`

- Port 8501 busy
  - `.\.venv\Scripts\python.exe -m streamlit run app.py --server.port 8502`

## FastAPI / Uvicorn

- `No module named 'uvicorn'`
  - `.\.venv\Scripts\python.exe -m pip install fastapi "uvicorn[standard]"`

- `No module named 'Train'`
  - Run from the `Train` folder: `.\.venv\Scripts\python.exe -m uvicorn api:app --reload`
  - Or add `__init__.py` to make `Train` a package and run from parent: `uvicorn Train.api:app`

- `Form data requires "python-multipart"`
  - `.\.venv\Scripts\python.exe -m pip install python-multipart`

## Model Artifacts

- Streamlit shows "No trained model found" or API fails to load
  - Ensure both files exist:
    - `Train/checkpoints/best_model.pt`
    - `Train/artifacts/idx_to_class.json`

## Performance / Device

- CPU fallback or slow inference
  - Ensure GPU drivers are up to date
  - On Windows/AMD, `torch_directml` is preferred automatically when available





