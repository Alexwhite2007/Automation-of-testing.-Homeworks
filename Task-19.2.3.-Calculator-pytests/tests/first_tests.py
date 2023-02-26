import pytest
from app.calculator import Calculator


class TestCalc:  # название класса обязательно начинается с Test
    def setup(self):  # определяем подготовительный метод setup
        self.calc = Calculator  # в котором мы будем создавать объект калькулятора
        # из импортированного класса (т.е мы подключаем тестируемый объект калькулятора)

    def test_multiply_calculate_correctly(self):          # тест на правильность умножения
        assert self.calc.multiply(self, 2, 2) == 4

    def test_division_calculate_correctly(self):          # тест на правильность деления
        assert self.calc.division(self, 6, 3) == 2

    def test_subtraction_calculate_correctly(self):       # тест на правильность вычитания
        assert self.calc.subtraction(self, 7, 3) == 4

    def test_adding_calculate_correctly(self):            # тест на правильность сложения
        assert self.calc.adding(self, 3, 5) == 8
