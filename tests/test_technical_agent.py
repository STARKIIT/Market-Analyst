import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from agents.technical_agent import run_technical_agent

def test_run_technical_agent_no_data():
    with patch('agents.technical_agent.get_cached_history') as mock_fetch:
        mock_fetch.return_value = None
        result = run_technical_agent("AAPL")
        assert "Could not retrieve" in result

def test_run_technical_agent_success():
    with patch('agents.technical_agent.get_cached_history') as mock_fetch:
        with patch('agents.technical_agent.get_technical_indicators') as mock_ind:
            with patch('agents.technical_agent.ChatGoogleGenerativeAI') as mock_llm:
                mock_fetch.return_value = pd.DataFrame({'Close': [100, 101, 102]})
                mock_ind.return_value = {"trend": "Bullish", "rsi": 60}
                
                mock_instance = MagicMock()
                mock_instance.invoke.return_value.content = "Mocked Technical Analysis"
                mock_llm.return_value = mock_instance
                
                result = run_technical_agent("AAPL")
                
                assert result == "Mocked Technical Analysis"
                mock_fetch.assert_called_once_with("AAPL", period="1y", interval="1d")
                mock_ind.assert_called_once()
                mock_instance.invoke.assert_called_once()
