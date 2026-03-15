import pytest
import pandas as pd
import numpy as np
from services.indicator_calculator import get_technical_indicators

def test_get_technical_indicators_insufficient_data():
    df = pd.DataFrame({'Close': [1, 2, 3]}) # Less than 50 rows
    result = get_technical_indicators(df)
    assert result == {}

def test_get_technical_indicators_success():
    # Create enough dummy data
    dates = pd.date_range("2020-01-01", periods=100)
    df = pd.DataFrame({
        'Close': np.linspace(10, 20, 100),
        'High': np.linspace(11, 21, 100),
        'Low': np.linspace(9, 19, 100),
        'Volume': np.random.randint(1000, 5000, 100)
    }, index=dates)
    
    result = get_technical_indicators(df)
    
    assert "current_price" in result
    assert "trend" in result
    assert "rsi" in result
    assert result["support"] is not None
    assert result["resistance"] is not None
