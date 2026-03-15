import pytest
from unittest.mock import patch, MagicMock
from agents.aggregator_agent import run_aggregator_agent

def test_run_aggregator_agent_success():
    with patch('agents.aggregator_agent.ChatOpenAI') as mock_llm:
        mock_instance = MagicMock()
        mock_instance.invoke.return_value.content = "AAPL Outlook: Strong Buy"
        mock_llm.return_value = mock_instance
        
        result = run_aggregator_agent("AAPL", "Fund", "Tech", "Sent")
        
        assert "AAPL Outlook: Strong Buy" in result
        mock_instance.invoke.assert_called_once()
