"""
Tests de integración para el renombrador de viajes LD.
"""
import pytest
import sys
from pathlib import Path

# Agregar src al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.validators import TrainValidator
from utils.formatters import FilenameFormatter, DateFormatter


class TestViajesLDWorkflow:
    """Tests de flujo completo para viajes LD."""
    
    def test_complete_viaje_ld_workflow(self):
        """Prueba flujo completo de viaje LD."""
        # Entrada del usuario
        train_input = "305"
        date_input = "0502"
        
        # Validar
        assert TrainValidator.validate_train_number(train_input) == True
        
        # Formatear fecha
        formatted_date = DateFormatter.format_date_input(date_input)
        assert formatted_date == "05-02"
        
        # Generar nombre final
        filename = FilenameFormatter.format_viaje_ld(formatted_date, train_input)
        assert filename == "05-02 MPN 305.pdf"
    
    def test_invalid_train_numbers(self):
        """Prueba números de tren inválidos."""
        assert TrainValidator.validate_train_number("300") == False
        assert TrainValidator.validate_train_number("311") == False
        assert TrainValidator.validate_train_number("999") == False
    
    def test_valid_train_range(self):
        """Prueba que todos los trenes del 301-310 sean válidos."""
        for train_num in range(301, 311):
            assert TrainValidator.validate_train_number(str(train_num)) == True
