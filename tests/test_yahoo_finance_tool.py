import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from tools.yahoo_finance_tool import fetch_stock_history, fetch_fundamentals

def test_fetch_stock_history_success():
    with patch('tools.yahoo_finance_tool.yf.Ticker') as mock_ticker:
        mock_df = pd.DataFrame({'Close': [100, 101, 102]})
        mock_instance = MagicMock()
        mock_instance.history.return_value = mock_df
        mock_ticker.return_value = mock_instance
        
        result = fetch_stock_history("AAPL")
        
        assert result is not None
        assert len(result) == 3
        mock_instance.history.assert_called_once()

def test_fetch_stock_history_empty():
    with patch('tools.yahoo_finance_tool.yf.Ticker') as mock_ticker:
        mock_df = pd.DataFrame()
        mock_instance = MagicMock()
        mock_instance.history.return_value = mock_df
        mock_ticker.return_value = mock_instance
        
        result = fetch_stock_history("INVALID")
        
        assert result is None

def test_fetch_fundamentals_success():
    with patch('tools.yahoo_finance_tool.yf.Ticker') as mock_ticker:
        mock_instance = MagicMock()
        mock_instance.info = {
            "totalRevenue": 1000,
            "trailingEps": 5.0,
        }
        mock_ticker.return_value = mock_instance
        
        result = fetch_fundamentals("AAPL")
        
        assert result.get("revenue") == 1000
        assert result.get("eps") == 5.0
