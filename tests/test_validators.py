"""
Tests para los validadores del sistema.
"""
import pytest
import sys
from pathlib import Path

# Agregar src al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.validators import DateValidator, LocomotiveValidator, TrainValidator


class TestDateValidator:
    """Tests para el validador de fechas."""
    
    def test_valid_dates(self):
        """Prueba fechas válidas."""
        assert DateValidator.validate_date("01-01") == True
        assert DateValidator.validate_date("31-12") == True
        assert DateValidator.validate_date("15-06") == True
    
    def test_invalid_dates(self):
        """Prueba fechas inválidas."""
        assert DateValidator.validate_date("32-01") == False
        assert DateValidator.validate_date("00-01") == False
        assert DateValidator.validate_date("15-13") == False
        assert DateValidator.validate_date("") == False
        assert DateValidator.validate_date("1-1") == False
        assert DateValidator.validate_date("15/06") == False


class TestLocomotiveValidator:
    """Tests para el validador de locomotoras."""
    
    def test_valid_two_digit_numbers(self):
        """Prueba números de 2 dígitos válidos."""
        assert LocomotiveValidator.validate_locomotive_number("22") == True
        assert LocomotiveValidator.validate_locomotive_number("01") == True
        assert LocomotiveValidator.validate_locomotive_number("99") == True
    
    def test_valid_three_digit_numbers(self):
        """Prueba números de 3 dígitos válidos."""
        assert LocomotiveValidator.validate_locomotive_number("105") == True
        assert LocomotiveValidator.validate_locomotive_number("106") == True
        assert LocomotiveValidator.validate_locomotive_number("107") == True
        assert LocomotiveValidator.validate_locomotive_number("999") == True
    
    def test_valid_formatted_numbers(self):
        """Prueba números ya formateados."""
        assert LocomotiveValidator.validate_locomotive_number("G-022") == True
        assert LocomotiveValidator.validate_locomotive_number("A107") == True
    
    def test_invalid_numbers(self):
        """Prueba números inválidos."""
        assert LocomotiveValidator.validate_locomotive_number("1") == False
        assert LocomotiveValidator.validate_locomotive_number("1234") == False
        assert LocomotiveValidator.validate_locomotive_number("") == False
        assert LocomotiveValidator.validate_locomotive_number("ABC") == False
        assert LocomotiveValidator.validate_locomotive_number("G-0222") == False


class TestTrainValidator:
    """Tests para el validador de trenes."""
    
    def test_valid_train_numbers(self):
        """Prueba números de tren válidos."""
        assert TrainValidator.validate_train_number("301") == True
        assert TrainValidator.validate_train_number("305") == True
        assert TrainValidator.validate_train_number("310") == True
    
    def test_invalid_train_numbers(self):
        """Prueba números de tren inválidos."""
        assert TrainValidator.validate_train_number("300") == False
        assert TrainValidator.validate_train_number("311") == False
        assert TrainValidator.validate_train_number("999") == False
        assert TrainValidator.validate_train_number("30") == False
        assert TrainValidator.validate_train_number("3001") == False
        assert TrainValidator.validate_train_number("") == False
        assert TrainValidator.validate_train_number("ABC") == False
    
    def test_custom_range(self):
        """Prueba validación con rango personalizado."""
        assert TrainValidator.validate_train_number("100", 100, 200) == True
        assert TrainValidator.validate_train_number("150", 100, 200) == True
        assert TrainValidator.validate_train_number("200", 100, 200) == True
        assert TrainValidator.validate_train_number("99", 100, 200) == False
        assert TrainValidator.validate_train_number("201", 100, 200) == False
