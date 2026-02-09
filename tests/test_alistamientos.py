"""
Tests de integración para el renombrador de alistamientos.
"""
import pytest
import sys
from pathlib import Path

# Agregar src al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.validators import LocomotiveValidator
from utils.formatters import LocomotiveFormatter, FilenameFormatter, DateFormatter


class TestAlistamientosWorkflow:
    """Tests de flujo completo para alistamientos."""
    
    def test_complete_checklist_workflow(self):
        """Prueba flujo completo de checklist."""
        # Entrada del usuario
        locomotive_input = "22"
        date_input = "0502"
        
        # Validar
        assert LocomotiveValidator.validate_locomotive_number(locomotive_input) == True
        
        # Formatear
        formatted_locomotive = LocomotiveFormatter.format_locomotive_number(locomotive_input)
        assert formatted_locomotive == "G-022"
        
        formatted_date = DateFormatter.format_date_input(date_input)
        assert formatted_date == "05-02"
        
        # Generar nombre final
        filename = FilenameFormatter.format_checklist(formatted_date, formatted_locomotive)
        assert filename == "05-02 CHECKLIST G-022.pdf"
    
    def test_complete_alistamiento_workflow(self):
        """Prueba flujo completo de alistamiento."""
        # Entrada del usuario
        locomotive_input = "107"
        date_input = "1003"
        
        # Validar
        assert LocomotiveValidator.validate_locomotive_number(locomotive_input) == True
        
        # Formatear
        formatted_locomotive = LocomotiveFormatter.format_locomotive_number(locomotive_input)
        assert formatted_locomotive == "A107"
        
        formatted_date = DateFormatter.format_date_input(date_input)
        assert formatted_date == "10-03"
        
        # Generar nombre final
        filename = FilenameFormatter.format_alistamiento(formatted_date, formatted_locomotive)
        assert filename == "10-03 AL A107.pdf"
    
    def test_workflow_with_exceptions(self):
        """Prueba flujo con locomotoras excepcionales."""
        locomotive_input = "105"
        date_input = "0101"
        
        assert LocomotiveValidator.validate_locomotive_number(locomotive_input) == True
        formatted_locomotive = LocomotiveFormatter.format_locomotive_number(locomotive_input)
        assert formatted_locomotive == "105"
        
        formatted_date = DateFormatter.format_date_input(date_input)
        filename = FilenameFormatter.format_checklist(formatted_date, formatted_locomotive)
        assert filename == "01-01 CHECKLIST 105.pdf"
