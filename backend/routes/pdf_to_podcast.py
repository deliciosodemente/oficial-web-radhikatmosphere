from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List, Dict
import tempfile
import os
from ..services.nim_service import NIMService
from ..auth.auth import get_current_user
from ..models.user import User

router = APIRouter()
nim_service = NIMService()

@router.post("/convert")
async def convert_pdf_to_podcast(
    file: UploadFile = File(...),
    voice_id: str = "default",
    speaking_rate: float = 1.0,
    pitch: float = 1.0,
    current_user: User = Depends(get_current_user)
):
    """
    Convierte un archivo PDF a podcast
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="El archivo debe ser un PDF"
        )

    try:
        # Guardar el archivo temporalmente
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name

        # Convertir el PDF
        result = await nim_service.convert_pdf_to_podcast(
            pdf_content=content,
            voice_id=voice_id,
            speaking_rate=speaking_rate,
            pitch=pitch
        )

        # Limpiar el archivo temporal
        os.unlink(temp_path)

        return JSONResponse(
            content={
                "status": "success",
                "data": result
            }
        )

    except Exception as e:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/voices")
async def get_available_voices(
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene la lista de voces disponibles
    """
    try:
        voices = await nim_service.get_available_voices()
        return JSONResponse(
            content={
                "status": "success",
                "data": voices
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/history")
async def get_conversion_history(
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene el historial de conversiones
    """
    try:
        history = await nim_service.get_conversion_history()
        return JSONResponse(
            content={
                "status": "success",
                "data": history
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 