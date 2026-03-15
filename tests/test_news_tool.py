import pytest
from unittest.mock import patch, MagicMock
from tools.news_tool import search_news

def test_search_news_success():
    with patch('tools.news_tool.GNews') as mock_gnews:
        mock_instance = MagicMock()
        mock_instance.get_news.return_value = [{"title": "News 1", "description": "Body 1"}]
        mock_gnews.return_value = mock_instance
        
        result = search_news("AAPL", 1)
        
        assert len(result) == 1
        assert result[0]["title"] == "News 1"

def test_search_news_exception():
    with patch('tools.news_tool.GNews') as mock_gnews:
        mock_gnews.side_effect = Exception("API error")
        
        result = search_news("AAPL")
        
        assert result == []
