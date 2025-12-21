"""Базовые тесты для проверки работоспособности CI/CD"""
import sys

def test_python_version():
    """Проверяем версию Python"""
    assert sys.version_info >= (3, 8)
    print(f"Python version: {sys.version}")

def test_imports():
    """Тест что необходимые модули импортируются"""
    try:
        import numpy
        import pandas
        import sklearn
        print("Все основные библиотеки импортируются успешно")
    except ImportError as e:
        print(f"Ошибка импорта: {e}")
        raise

def test_skip_app_tests():
    """Тест который пропускается если нет приложения"""
    try:
        import src.api.app
    except ImportError:
        import pytest
        pytest.skip("App not imported, skipping app tests")
