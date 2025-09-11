How to RUN::
pip install -r requirements.txt
2-> make sure you have Python version 3.10 
3-> Run FastAPI inference server (serves /predict)
.\.venv\Scripts\python.exe -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload
4->open you index.html




# Test the API (PowerShell)
$file = "sample\\cattle-breed-identifier\\UI\\images\\cow.avif"
Invoke-WebRequest -Uri http://127.0.0.1:8000/predict -Method Post -InFile $file -ContentType "image/jpeg"

# Frontend wiring
# The web UI in final_project/identify.html will call http://127.0.0.1:8000 by default.
# To override, open the browser console before identifying and set:
# window.__IDENTIFY_API__ = "http://<your-ip>:8000";