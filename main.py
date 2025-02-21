from fastapi import FastAPI
import subprocess

app = FastAPI()

# Start Streamlit as a subprocess
@app.on_event("startup")
def start_streamlit():
    subprocess.Popen(
        ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
    )

@app.get("/")
def read_root():
    return {"message": "FastAPI is running. Streamlit is available at /streamlit"}

@app.get("/streamlit")
def redirect_streamlit():
    return {"streamlit_url": "http://localhost:8501"}

