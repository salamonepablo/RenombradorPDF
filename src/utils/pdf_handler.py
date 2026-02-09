"""
Manejador de archivos PDF para generación de previsualizaciones.
"""
import fitz
from PIL import Image, ImageTk
from typing import Optional, Tuple


class PDFPreviewGenerator:
    """Genera previsualizaciones de archivos PDF."""
    
    @staticmethod
    def generate_preview(
        pdf_path: str, 
        preview_width: int = 800,
        clip_fraction: float = 0.33,
        dpi: int = 200
    ) -> Tuple[Optional[ImageTk.PhotoImage], Optional[str]]:
        """
        Genera una previsualización de la primera página de un PDF.
        
        Args:
            pdf_path: Ruta al archivo PDF
            preview_width: Ancho deseado para la previsualización (px)
            clip_fraction: Fracción de la página a mostrar (0.33 = primer tercio)
            dpi: Resolución de renderizado
            
        Returns:
            Tupla (imagen_tk, mensaje_error). Si hay error, imagen_tk es None.
        """
        try:
            doc = fitz.open(pdf_path)
            page = doc.load_page(0)
            rect = page.rect
            
            # Recortar al tercio superior de la página
            clip_rect = fitz.Rect(rect.x0, rect.y0, rect.x1, rect.height * clip_fraction)
            
            # Renderizar el área recortada
            pix = page.get_pixmap(clip=clip_rect, dpi=dpi)
            
            # Convertir a PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Redimensionar manteniendo aspecto
            ratio = preview_width / img.width
            new_height = int(img.height * ratio)
            resized_img = img.resize((preview_width, new_height), Image.LANCZOS)
            
            # Convertir a formato Tkinter
            photo_img = ImageTk.PhotoImage(resized_img)
            
            doc.close()
            return photo_img, None
            
        except Exception as e:
            return None, f"Error al generar vista previa: {str(e)}"
