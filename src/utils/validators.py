"""
Validadores para diferentes tipos de entrada del sistema.
"""
from datetime import datetime
from typing import Optional


class DateValidator:
    """Valida formatos de fecha."""
    
    @staticmethod
    def validate_date(date_str: str) -> bool:
        """
        Valida que una cadena de fecha tenga el formato DD-MM correcto.
        
        Args:
            date_str: Cadena con formato DD-MM
            
        Returns:
            True si la fecha es válida, False en caso contrario
        """
        if not date_str:
            return False
        try:
            datetime.strptime(date_str, "%d-%m")
            return True
        except ValueError:
            return False


class LocomotiveValidator:
    """Valida números de locomotora."""
    
    @staticmethod
    def validate_locomotive_number(locomotive_str: str) -> bool:
        """
        Valida que un número de locomotora sea correcto.
        Acepta: G-0XX, AXXX, XX (2 dígitos), XXX (3 dígitos)
        
        Args:
            locomotive_str: Número de locomotora a validar
            
        Returns:
            True si es válido, False en caso contrario
        """
        clean_str = locomotive_str.strip().upper()
        
        # Formato ya formateado G-0XX
        if clean_str.startswith("G-0"):
            return clean_str[3:].isdigit() and len(clean_str[3:]) == 2
        
        # Formato AXXX
        if clean_str.startswith("A"):
            return clean_str[1:].isdigit() and len(clean_str[1:]) == 3
        
        # Números simples de 2 o 3 dígitos
        if clean_str.isdigit():
            return len(clean_str) in (2, 3)
        
        return False


class TrainValidator:
    """Valida números de tren."""
    
    @staticmethod
    def validate_train_number(train_str: str, min_val: int = 301, max_val: int = 310) -> bool:
        """
        Valida que un número de tren esté en el rango permitido.
        
        Args:
            train_str: Número de tren como cadena
            min_val: Valor mínimo permitido (default: 301)
            max_val: Valor máximo permitido (default: 310)
            
        Returns:
            True si el número es válido, False en caso contrario
        """
        clean_str = train_str.strip()
        
        if not clean_str.isdigit():
            return False
        
        if len(clean_str) != 3:
            return False
        
        train_num = int(clean_str)
        return min_val <= train_num <= max_val
