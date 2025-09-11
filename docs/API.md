# API Guide

Base URL (local): `http://127.0.0.1:8000`

Start the server:

```
cd "C:\Users\Devesh\Desktop\SIH 2025\Train"
.\.venv\Scripts\python.exe -m uvicorn api:app --host 127.0.0.1 --port 8000 --reload
```

## Endpoints

### GET /health
Returns service liveness.

Response 200:
```
{"status":"ok"}
```

### POST /predict
Classifies an uploaded image and returns top-1 and top-3 predictions.

- Content type: `multipart/form-data`
- Field name: `file`

Request (cURL):
```
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample.jpg"
```

Response 200 (example):
```
{
  "prediction": {"label": "Sahiwal", "probability": 0.92},
  "topk": [
    {"label": "Sahiwal", "probability": 0.92},
    {"label": "Red_Sindhi", "probability": 0.05},
    {"label": "Gir", "probability": 0.02}
  ],
  "image_size": 224,
  "info": {
    "description": "...",
    "characteristics": ["..."],
    "fodder_requirements": ["..."],
    "government_schemes": ["..."],
    "best_practices": ["..."]
  }
}
```

## Model Artifacts

The API loads at startup and requires:

- `Train/checkpoints/best_model.pt`
- `Train/artifacts/idx_to_class.json`
- Optional: `Train/breed_info.json`

If missing, the API startup will fail with a clear error.

## Error Codes

- 200: Successful prediction
- 400: Invalid image or processing error (payload contains `{"error": "..."}`)

## CORS

Development CORS is wide-open (`allow_origins=["*"]`). For production, restrict to known frontends.





