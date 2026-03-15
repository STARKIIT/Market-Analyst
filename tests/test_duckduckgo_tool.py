import pytest
from unittest.mock import patch, MagicMock
from tools.duckduckgo_tool import search_news

def test_search_news_success():
    with patch('tools.duckduckgo_tool.DDGS') as mock_ddgs:
        mock_instance = MagicMock()
        mock_instance.news.return_value = [{"title": "News 1", "body": "Body 1"}]
        mock_ddgs.return_value.__enter__.return_value = mock_instance
        
        result = search_news("AAPL", 1)
        
        assert len(result) == 1
        assert result[0]["title"] == "News 1"

def test_search_news_exception():
    with patch('tools.duckduckgo_tool.DDGS') as mock_ddgs:
        mock_ddgs.side_effect = Exception("API error")
        
        result = search_news("AAPL")
        
        assert result == []
