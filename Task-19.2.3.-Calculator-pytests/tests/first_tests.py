import pytest as pytest

from app.calculator import multiply, division, subtraction, adding


@pytest.mark.parametrize("a,b,expected_result", [(2, 2, 4),
                                                 (3, 2.5, 7.5),
                                                 (-3, 3, -9)])
def test_multiply_calculate_correctly(a, b, expected_result):  # позитивные тесты на правильность умножения
    assert multiply(a, b) == expected_result, "Unsuccessful"


@pytest.mark.parametrize("a,b,expected_result", [(6, 3, 2),
                                                 (-6, -3, 2),
                                                 (9, -3, -3)])
def test_division_calculate_correctly(a, b, expected_result):  # позитивные тесты на правильность деления
    assert division(a, b) == expected_result, "Unsuccessful"


@pytest.mark.parametrize("a,b,expected_result", [(7, 3, 4),
                                                 (-4, -2, -2),
                                                 (1, -4, 5)])
def test_subtraction_calculate_correctly(a, b, expected_result):  # позитивные тесты на правильность вычитания
    assert subtraction(a, b) == expected_result, "Unsuccessful"


@pytest.mark.parametrize("a,b,expected_result", [(2, 2, 4),
                                                 (-4, 2, -2),
                                                 (1, -4, -3)])
def test_adding_calculate_correctly(a, b, expected_result):  # позитивные тесты на правильность сложения
    assert adding(a, b) == expected_result, "Unsuccessful"


@pytest.mark.parametrize("expected_exception, a, b", [(ZeroDivisionError, 10, 0),
                                                      (TypeError, 10, "2"),
                                                      (TypeError, 10, "2"),
                                                      (TypeError, 10, "2")])
def test_with_invalid_data(expected_exception, a, b):  # негативные тесты, деление на 0 и тип str вместо int
    with pytest.raises(expected_exception):
        assert division(a, b)
        assert multiply(a, b)
        assert adding(a, b)
        assert subtraction(a, b)
