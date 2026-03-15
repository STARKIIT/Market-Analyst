import pytest
import os
import pandas as pd
from unittest.mock import patch, MagicMock
from services.data_fetcher import get_cached_history, get_cached_news

def test_get_cached_history_cache_hit(tmpdir):
    with patch('services.data_fetcher.PRICE_CACHE_DIR', str(tmpdir)):
        df = pd.DataFrame({'Close': [100, 101]})
        cache_path = os.path.join(str(tmpdir), "AAPL_1y_1d.csv")
        df.to_csv(cache_path)
        
        result = get_cached_history("AAPL")
        
        assert result is not None
        assert len(result) == 2
        assert 'Close' in result.columns

def test_get_cached_history_cache_miss(tmpdir):
    with patch('services.data_fetcher.PRICE_CACHE_DIR', str(tmpdir)):
        with patch('services.data_fetcher.fetch_stock_history') as mock_fetch:
            mock_df = pd.DataFrame({'Close': [100, 101, 102]})
            mock_fetch.return_value = mock_df
            
            result = get_cached_history("AAPL")
            
            assert result is not None
            assert len(result) == 3
            mock_fetch.assert_called_once_with("AAPL", "1y", "1d")
            
            # Verify it was saved to cache
            cache_path = os.path.join(str(tmpdir), "AAPL_1y_1d.csv")
            assert os.path.exists(cache_path)

def test_get_cached_news_cache_miss(tmpdir):
    with patch('services.data_fetcher.NEWS_CACHE_DIR', str(tmpdir)):
        with patch('services.data_fetcher.search_news') as mock_search:
            mock_news = [{"title": "News 1"}]
            mock_search.return_value = mock_news
            
            result = get_cached_news("AAPL", 5)
            
            assert result == mock_news
            mock_search.assert_called_once_with("AAPL stock news", 5)
