import os
from typing import Dict, Any
import requests
import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class NvidiaService:
    def __init__(self):
        self.api_key = os.getenv("NVIDIA_NGC_API_KEY")
        self.api_url = os.getenv("NVIDIA_NGC_API_URL")
        self.models_path = os.getenv("MODELS_PATH")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    async def run_inference(self, model_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecuta inferencia usando un modelo de NVIDIA NGC
        
        Args:
            model_id: ID del modelo a usar
            input_data: Datos de entrada para el modelo
            
        Returns:
            Dict con los resultados de la inferencia
        """
        try:
            # Cargar modelo desde NGC o caché local
            model_path = os.path.join(self.models_path, model_id)
            if not os.path.exists(model_path):
                await self.download_model(model_id, model_path)
                
            # Cargar modelo y tokenizer
            model = AutoModelForCausalLM.from_pretrained(model_path).to(self.device)
            tokenizer = AutoTokenizer.from_pretrained(model_path)
            
            # Preparar input
            inputs = tokenizer(input_data["text"], return_tensors="pt").to(self.device)
            
            # Generar salida
            with torch.no_grad():
                outputs = model.generate(**inputs)
                
            # Decodificar resultado
            result = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            return {
                "model_id": model_id,
                "input": input_data["text"],
                "output": result,
                "device": self.device
            }
            
        except Exception as e:
            raise Exception(f"Error en inferencia: {str(e)}")
            
    async def download_model(self, model_id: str, target_path: str) -> None:
        """
        Descarga un modelo desde NVIDIA NGC
        
        Args:
            model_id: ID del modelo a descargar
            target_path: Ruta donde guardar el modelo
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Obtener URL de descarga
            response = requests.get(
                f"{self.api_url}/models/{model_id}/download",
                headers=headers
            )
            response.raise_for_status()
            download_url = response.json()["download_url"]
            
            # Descargar modelo
            os.makedirs(target_path, exist_ok=True)
            response = requests.get(download_url, stream=True)
            response.raise_for_status()
            
            model_file = os.path.join(target_path, "model.bin")
            with open(model_file, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
        except Exception as e:
            raise Exception(f"Error al descargar modelo: {str(e)}")
            
    async def get_model_info(self, model_id: str) -> Dict[str, Any]:
        """
        Obtiene información sobre un modelo
        
        Args:
            model_id: ID del modelo
            
        Returns:
            Dict con información del modelo
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(
                f"{self.api_url}/models/{model_id}",
                headers=headers
            )
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            raise Exception(f"Error al obtener información del modelo: {str(e)}")
            
    async def monitor_gpu_usage(self) -> Dict[str, Any]:
        """
        Monitorea el uso de GPU
        
        Returns:
            Dict con métricas de uso de GPU
        """
        try:
            if not torch.cuda.is_available():
                return {"status": "No GPU available"}
                
            return {
                "gpu_count": torch.cuda.device_count(),
                "current_device": torch.cuda.current_device(),
                "memory_allocated": torch.cuda.memory_allocated(),
                "memory_cached": torch.cuda.memory_cached(),
                "max_memory_allocated": torch.cuda.max_memory_allocated()
            }
            
        except Exception as e:
            raise Exception(f"Error al monitorear GPU: {str(e)}") 