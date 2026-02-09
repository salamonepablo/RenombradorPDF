"""
Formateadores para diferentes tipos de datos del sistema.
"""
from datetime import datetime
from typing import Optional


class DateFormatter:
    """Formatea fechas."""
    
    @staticmethod
    def format_date_input(date_str: str) -> str:
        """
        Formatea una entrada de fecha DDMM a DD-MM.
        
        Args:
            date_str: Cadena con formato DDMM
            
        Returns:
            Cadena formateada como DD-MM
        """
        if len(date_str) == 4 and date_str.isdigit():
            return f"{date_str[:2]}-{date_str[2:]}"
        return date_str
    
    @staticmethod
    def get_today_formatted() -> str:
        """
        Retorna la fecha de hoy en formato DD-MM.
        
        Returns:
            Fecha actual en formato DD-MM
        """
        return datetime.now().strftime("%d-%m")


class LocomotiveFormatter:
    """Formatea números de locomotora."""
    
    @staticmethod
    def format_locomotive_number(locomotive_str: str) -> str:
        """
        Formatea un número de locomotora según las reglas del negocio.
        - 2 dígitos: G-0XX (ej: 22 -> G-022)
        - 3 dígitos: AXXX (ej: 107 -> A107)
        - Excepciones: 105, 106 no llevan prefijo "A"
        
        Args:
            locomotive_str: Número de locomotora a formatear
            
        Returns:
            Número formateado según las reglas
        """
        clean_str = locomotive_str.strip().upper()
        
        # Si ya tiene formato, retornar como está
        if clean_str.startswith(("G-0", "A")):
            return clean_str
        
        # Aplicar formato según longitud
        if clean_str.isdigit():
            if len(clean_str) == 2:
                return f"G-0{clean_str}"
            elif len(clean_str) == 3:
                # Excepciones: 105 y 106 no llevan "A"
                if clean_str in ("105", "106"):
                    return clean_str
                return f"A{clean_str}"
        
        return locomotive_str


class FilenameFormatter:
    """Genera nombres de archivo según diferentes formatos."""
    
    @staticmethod
    def format_checklist(date: str, locomotive: str) -> str:
        """
        Genera nombre para checklist: DD-MM CHECKLIST LOC.pdf
        
        Args:
            date: Fecha en formato DD-MM
            locomotive: Número de locomotora formateado
            
        Returns:
            Nombre de archivo completo
        """
        return f"{date} CHECKLIST {locomotive}.pdf"
    
    @staticmethod
    def format_alistamiento(date: str, locomotive: str) -> str:
        """
        Genera nombre para alistamiento: DD-MM AL LOC.pdf
        
        Args:
            date: Fecha en formato DD-MM
            locomotive: Número de locomotora formateado
            
        Returns:
            Nombre de archivo completo
        """
        return f"{date} AL {locomotive}.pdf"
    
    @staticmethod
    def format_viaje_ld(date: str, train: str) -> str:
        """
        Genera nombre para viaje LD: DD-MM MPN TREN.pdf
        
        Args:
            date: Fecha en formato DD-MM
            train: Número de tren
            
        Returns:
            Nombre de archivo completo
        """
        return f"{date} MPN {train}.pdf"
