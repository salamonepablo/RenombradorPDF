"""
Tests para los formateadores del sistema.
"""
import pytest
import sys
from pathlib import Path
from datetime import datetime

# Agregar src al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.formatters import DateFormatter, LocomotiveFormatter, FilenameFormatter


class TestDateFormatter:
    """Tests para el formateador de fechas."""
    
    def test_format_date_input(self):
        """Prueba el formateo de entrada de fecha."""
        assert DateFormatter.format_date_input("0102") == "01-02"
        assert DateFormatter.format_date_input("3112") == "31-12"
        assert DateFormatter.format_date_input("1506") == "15-06"
    
    def test_format_date_input_already_formatted(self):
        """Prueba entrada ya formateada."""
        assert DateFormatter.format_date_input("01-02") == "01-02"
    
    def test_format_date_input_invalid(self):
        """Prueba entrada inválida."""
        assert DateFormatter.format_date_input("123") == "123"
        assert DateFormatter.format_date_input("") == ""
    
    def test_get_today_formatted(self):
        """Prueba obtener fecha de hoy formateada."""
        today = DateFormatter.get_today_formatted()
        assert len(today) == 5
        assert today[2] == "-"
        # Verificar que coincide con la fecha real
        expected = datetime.now().strftime("%d-%m")
        assert today == expected


class TestLocomotiveFormatter:
    """Tests para el formateador de locomotoras."""
    
    def test_format_two_digit_locomotive(self):
        """Prueba formateo de locomotoras de 2 dígitos."""
        assert LocomotiveFormatter.format_locomotive_number("22") == "G-022"
        assert LocomotiveFormatter.format_locomotive_number("01") == "G-001"
        assert LocomotiveFormatter.format_locomotive_number("99") == "G-099"
    
    def test_format_three_digit_locomotive(self):
        """Prueba formateo de locomotoras de 3 dígitos."""
        assert LocomotiveFormatter.format_locomotive_number("107") == "A107"
        assert LocomotiveFormatter.format_locomotive_number("200") == "A200"
        assert LocomotiveFormatter.format_locomotive_number("999") == "A999"
    
    def test_format_exceptions(self):
        """Prueba excepciones 105 y 106."""
        assert LocomotiveFormatter.format_locomotive_number("105") == "105"
        assert LocomotiveFormatter.format_locomotive_number("106") == "106"
    
    def test_format_already_formatted(self):
        """Prueba locomotoras ya formateadas."""
        assert LocomotiveFormatter.format_locomotive_number("G-022") == "G-022"
        assert LocomotiveFormatter.format_locomotive_number("A107") == "A107"
    
    def test_format_with_whitespace(self):
        """Prueba formateo con espacios."""
        assert LocomotiveFormatter.format_locomotive_number("  22  ") == "G-022"
        assert LocomotiveFormatter.format_locomotive_number(" 107 ") == "A107"


class TestFilenameFormatter:
    """Tests para el formateador de nombres de archivo."""
    
    def test_format_checklist(self):
        """Prueba formato de checklist."""
        result = FilenameFormatter.format_checklist("05-02", "G-022")
        assert result == "05-02 CHECKLIST G-022.pdf"
    
    def test_format_alistamiento(self):
        """Prueba formato de alistamiento."""
        result = FilenameFormatter.format_alistamiento("05-02", "A107")
        assert result == "05-02 AL A107.pdf"
    
    def test_format_viaje_ld(self):
        """Prueba formato de viaje LD."""
        result = FilenameFormatter.format_viaje_ld("05-02", "305")
        assert result == "05-02 MPN 305.pdf"
    
    def test_format_with_exceptions(self):
        """Prueba formato con excepciones de locomotoras."""
        result1 = FilenameFormatter.format_checklist("05-02", "105")
        result2 = FilenameFormatter.format_alistamiento("10-03", "106")
        assert result1 == "05-02 CHECKLIST 105.pdf"
        assert result2 == "10-03 AL 106.pdf"
