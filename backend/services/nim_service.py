from typing import Dict, List, Optional
import os
import aiohttp
import asyncio
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class NIMService:
    def __init__(self):
        self.api_key = os.getenv("NVIDIA_NGC_API_KEY")
        self.base_url = os.getenv("NIM_URL", "https://api.nvcf.nvidia.com/v2/nvcf")
        self.model_id = os.getenv("NIM_MODEL_ID", "pdf-to-podcast")
        self.batch_size = int(os.getenv("NIM_BATCH_SIZE", "1"))
        self.max_retries = int(os.getenv("NIM_MAX_RETRIES", "3"))
        self.timeout = int(os.getenv("NIM_TIMEOUT", "300"))

    async def convert_pdf_to_podcast(
        self,
        pdf_content: bytes,
        voice_id: str = "default",
        speaking_rate: float = 1.0,
        pitch: float = 1.0
    ) -> Dict:
        """
        Convierte un PDF a podcast usando el servicio NIM
        """
        try:
            async with aiohttp.ClientSession() as session:
                # Subir el PDF
                upload_url = f"{self.base_url}/upload"
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/pdf"
                }
                
                async with session.post(
                    upload_url,
                    headers=headers,
                    data=pdf_content
                ) as response:
                    if response.status != 200:
                        raise HTTPException(
                            status_code=response.status,
                            detail="Error al subir el PDF"
                        )
                    upload_result = await response.json()
                    file_id = upload_result["file_id"]

                # Iniciar la conversión
                convert_url = f"{self.base_url}/convert"
                convert_payload = {
                    "file_id": file_id,
                    "voice_id": voice_id,
                    "speaking_rate": speaking_rate,
                    "pitch": pitch
                }

                async with session.post(
                    convert_url,
                    headers=headers,
                    json=convert_payload
                ) as response:
                    if response.status != 200:
                        raise HTTPException(
                            status_code=response.status,
                            detail="Error al iniciar la conversión"
                        )
                    convert_result = await response.json()
                    conversion_id = convert_result["conversion_id"]

                # Esperar y verificar el estado
                for _ in range(self.max_retries):
                    status_url = f"{self.base_url}/status/{conversion_id}"
                    async with session.get(
                        status_url,
                        headers=headers
                    ) as response:
                        if response.status != 200:
                            raise HTTPException(
                                status_code=response.status,
                                detail="Error al verificar el estado"
                            )
                        status_result = await response.json()
                        
                        if status_result["status"] == "completed":
                            return {
                                "audio_url": status_result["audio_url"],
                                "duration": status_result["duration"],
                                "word_count": status_result["word_count"]
                            }
                        elif status_result["status"] == "failed":
                            raise HTTPException(
                                status_code=500,
                                detail="La conversión falló"
                            )
                        
                        await asyncio.sleep(5)

                raise HTTPException(
                    status_code=408,
                    detail="Tiempo de espera agotado"
                )

        except Exception as e:
            logger.error(f"Error en la conversión: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error en el servicio NIM: {str(e)}"
            )

    async def get_available_voices(self) -> List[Dict]:
        """
        Obtiene la lista de voces disponibles
        """
        try:
            async with aiohttp.ClientSession() as session:
                voices_url = f"{self.base_url}/voices"
                headers = {
                    "Authorization": f"Bearer {self.api_key}"
                }
                
                async with session.get(
                    voices_url,
                    headers=headers
                ) as response:
                    if response.status != 200:
                        raise HTTPException(
                            status_code=response.status,
                            detail="Error al obtener las voces"
                        )
                    return await response.json()

        except Exception as e:
            logger.error(f"Error al obtener voces: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error en el servicio NIM: {str(e)}"
            )

    async def get_conversion_history(self) -> List[Dict]:
        """
        Obtiene el historial de conversiones
        """
        try:
            async with aiohttp.ClientSession() as session:
                history_url = f"{self.base_url}/history"
                headers = {
                    "Authorization": f"Bearer {self.api_key}"
                }
                
                async with session.get(
                    history_url,
                    headers=headers
                ) as response:
                    if response.status != 200:
                        raise HTTPException(
                            status_code=response.status,
                            detail="Error al obtener el historial"
                        )
                    return await response.json()

        except Exception as e:
            logger.error(f"Error al obtener historial: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error en el servicio NIM: {str(e)}"
            ) 