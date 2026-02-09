"""
Configuraciones centralizadas del sistema.
"""
import os
from pathlib import Path


class Settings:
    """Configuraciones generales de la aplicación."""
    
    # Información de la aplicación
    APP_NAME = "RenombradorPDF"
    APP_VERSION = "2.0.0"
    
    # Rutas por defecto
    DEFAULT_PATH = r"g:/Material Rodante/.ISO 9001- 2 - Coordinación General Técnica/08 - Programación/05 - Archivo/2026/"
    
    # Configuraciones de UI
    WINDOW_WIDTH = 400
    WINDOW_HEIGHT = 280
    
    # Configuraciones de previsualización de PDF
    PREVIEW_WIDTH = 800
    PREVIEW_DPI = 200
    PREVIEW_CLIP_FRACTION = 0.33  # Mostrar primer tercio de la página
    
    # Validaciones
    TRAIN_NUMBER_MIN = 301
    TRAIN_NUMBER_MAX = 310
    
    # Rangos de locomotoras
    LOCOMOTIVE_2_DIGIT_RANGE = (1, 99)
    LOCOMOTIVE_3_DIGIT_RANGE = (100, 999)
    LOCOMOTIVE_EXCEPTIONS = ["105", "106"]  # No llevan prefijo "A"
    
    @classmethod
    def get_project_root(cls) -> Path:
        """Retorna la ruta raíz del proyecto."""
        return Path(__file__).parent.parent.parent
    
    @classmethod
    def path_exists(cls, path: str) -> bool:
        """Verifica si una ruta existe."""
        return os.path.exists(path)
