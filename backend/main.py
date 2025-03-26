from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn
import os

from services.davinci_service import DaVinciService
from services.unity_service import UnityService
from services.nvidia_ngc_service import NvidiaService
from services.gemini_service import GeminiService
from services.hostinger_service import HostingerService

# Cargar variables de entorno
load_dotenv()

app = FastAPI(
    title="Plataforma Integral Omniverse",
    description="API para integración de Unity, DaVinci Resolve, NVIDIA NGC/NIM y Hostinger",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar servicios
davinci_service = DaVinciService()
unity_service = UnityService()
nvidia_service = NvidiaService()
gemini_service = GeminiService()
hostinger_service = HostingerService()

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de la Plataforma Integral Omniverse"}

@app.post("/video/edit")
async def edit_video(project_id: str):
    try:
        result = await davinci_service.edit_video(project_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/unity/update")
async def update_unity_experience(experience_id: str, data: dict):
    try:
        result = await unity_service.update_experience(experience_id, data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ai/inference")
async def run_ai_inference(model_id: str, input_data: dict):
    try:
        result = await nvidia_service.run_inference(model_id, input_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/text/generate")
async def generate_text(prompt: str):
    try:
        result = await gemini_service.generate_text(prompt)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/hosting/status")
async def get_hosting_status():
    try:
        result = await hostinger_service.get_status()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 