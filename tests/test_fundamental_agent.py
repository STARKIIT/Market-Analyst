import pytest
from unittest.mock import patch, MagicMock
from agents.fundamental_agent import run_fundamental_agent

def test_run_fundamental_agent_no_data():
    with patch('agents.fundamental_agent.fetch_fundamentals') as mock_fetch:
        mock_fetch.return_value = {}
        result = run_fundamental_agent("AAPL")
        assert "Could not retrieve" in result

def test_run_fundamental_agent_success():
    with patch('agents.fundamental_agent.fetch_fundamentals') as mock_fetch:
        with patch('agents.fundamental_agent.ChatOpenAI') as mock_llm:
            mock_fetch.return_value = {"revenue": 100, "eps": 5}
            
            mock_instance = MagicMock()
            mock_instance.invoke.return_value.content = "Mocked LLM Summary for AAPL"
            mock_llm.return_value = mock_instance
            
            result = run_fundamental_agent("AAPL")
            
            assert result == "Mocked LLM Summary for AAPL"
            mock_fetch.assert_called_once_with("AAPL")
            mock_instance.invoke.assert_called_once()
