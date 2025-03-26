import os
from typing import Dict, Any
import DaVinciResolveScript as dvr

class DaVinciService:
    def __init__(self):
        self.resolve = dvr.scriptapp("Resolve")
        self.project_manager = self.resolve.GetProjectManager()
        self.api_key = os.getenv("DAVINCI_API_KEY")
        
    async def edit_video(self, project_id: str) -> Dict[str, Any]:
        """
        Edita un video usando DaVinci Resolve
        
        Args:
            project_id: ID del proyecto a editar
            
        Returns:
            Dict con el resultado de la edición
        """
        try:
            # Abrir proyecto
            project = self.project_manager.LoadProject(project_id)
            if not project:
                raise Exception(f"No se pudo cargar el proyecto {project_id}")
                
            # Obtener timeline
            timeline = project.GetCurrentTimeline()
            if not timeline:
                raise Exception("No se pudo obtener el timeline actual")
                
            # Ejemplo de automatización de edición
            # Aquí irían las operaciones específicas de edición
            result = {
                "project_id": project_id,
                "status": "success",
                "timeline_name": timeline.GetName(),
                "duration": timeline.GetDuration(),
                "frame_rate": timeline.GetSetting("frameRate")
            }
            
            return result
            
        except Exception as e:
            raise Exception(f"Error al editar video: {str(e)}")
            
    async def render_video(self, project_id: str, render_preset: str) -> Dict[str, Any]:
        """
        Renderiza un video usando un preset específico
        
        Args:
            project_id: ID del proyecto a renderizar
            render_preset: Nombre del preset de renderizado
            
        Returns:
            Dict con el resultado del renderizado
        """
        try:
            project = self.project_manager.LoadProject(project_id)
            if not project:
                raise Exception(f"No se pudo cargar el proyecto {project_id}")
                
            # Configurar renderizado
            project.SetRenderSettings({
                "SelectAllFrames": True,
                "TargetDir": os.getenv("RENDER_OUTPUT_PATH", "./output"),
                "CustomName": f"{project_id}_render",
                "RenderPreset": render_preset
            })
            
            # Iniciar renderizado
            project.StartRendering()
            
            # Esperar a que termine el renderizado
            while project.IsRenderingInProgress():
                await asyncio.sleep(1)
                
            return {
                "project_id": project_id,
                "status": "success",
                "output_path": os.path.join(os.getenv("RENDER_OUTPUT_PATH", "./output"), f"{project_id}_render.mp4")
            }
            
        except Exception as e:
            raise Exception(f"Error al renderizar video: {str(e)}")
            
    async def get_project_info(self, project_id: str) -> Dict[str, Any]:
        """
        Obtiene información sobre un proyecto
        
        Args:
            project_id: ID del proyecto
            
        Returns:
            Dict con la información del proyecto
        """
        try:
            project = self.project_manager.LoadProject(project_id)
            if not project:
                raise Exception(f"No se pudo cargar el proyecto {project_id}")
                
            timeline = project.GetCurrentTimeline()
            
            return {
                "project_id": project_id,
                "name": project.GetName(),
                "timeline_count": project.GetTimelineCount(),
                "current_timeline": timeline.GetName() if timeline else None,
                "frame_rate": project.GetSetting("timelineFrameRate"),
                "resolution": {
                    "width": project.GetSetting("timelineResolutionWidth"),
                    "height": project.GetSetting("timelineResolutionHeight")
                }
            }
            
        except Exception as e:
            raise Exception(f"Error al obtener información del proyecto: {str(e)}") 