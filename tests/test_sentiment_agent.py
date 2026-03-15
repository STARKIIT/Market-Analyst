import pytest
from unittest.mock import patch, MagicMock
from agents.sentiment_agent import run_sentiment_agent

def test_run_sentiment_agent_no_data():
    with patch('agents.sentiment_agent.get_cached_news') as mock_fetch:
        mock_fetch.return_value = []
        result = run_sentiment_agent("AAPL")
        assert "Could not retrieve" in result

def test_run_sentiment_agent_success():
    with patch('agents.sentiment_agent.get_cached_news') as mock_fetch:
        with patch('agents.sentiment_agent.analyze_sentiment') as mock_sa:
            with patch('agents.sentiment_agent.ChatGoogleGenerativeAI') as mock_llm:
                mock_fetch.return_value = [{"title": "Good News"}]
                mock_sa.return_value = {"overall_score": 0.5, "overall_sentiment": "Bullish", "details": []}
                
                mock_instance = MagicMock()
                mock_instance.invoke.return_value.content = "Mocked Sentiment Analysis"
                mock_llm.return_value = mock_instance
                
                result = run_sentiment_agent("AAPL")
                
                assert result == "Mocked Sentiment Analysis"
                mock_fetch.assert_called_once()
                mock_sa.assert_called_once()
                mock_instance.invoke.assert_called_once()
