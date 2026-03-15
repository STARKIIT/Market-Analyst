import pytest
from unittest.mock import patch, MagicMock
from agents.master_agent import run_master_agent

def test_run_master_agent_naive_fallback():
    with patch('agents.master_agent.settings') as mock_settings:
        mock_settings.OPENAI_API_KEY = "" # Force fallback
        
        result = run_master_agent("portfolio analysis")
        assert result.intent == "portfolio"
        assert len(result.tickers) == 0

def test_run_master_agent_success():
    with patch('agents.master_agent.settings') as mock_settings:
        mock_settings.GEMINI_API_KEY = "dummy-key-for-test-long-enough"
        
        with patch('agents.master_agent.ChatGoogleGenerativeAI') as mock_llm:
            mock_instance = MagicMock()
            
            # Setup mock for with_structured_output chain
            mock_structured_instance = MagicMock()
            mock_structured_instance.invoke.return_value = MagicMock(intent="single_stock", tickers=["AAPL"])
            
            mock_instance.with_structured_output.return_value = mock_structured_instance
            mock_llm.return_value = mock_instance
            
            result = run_master_agent("How is AAPL doing?")
            
            assert result.intent == "single_stock"
            assert result.tickers == ["AAPL"]
            mock_structured_instance.invoke.assert_called_once()
