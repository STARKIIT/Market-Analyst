import os
import json
import pandas as pd
from typing import Dict, Any, Optional, List
from utils.logger import get_logger
from tools.yahoo_finance_tool import fetch_stock_history, fetch_fundamentals
from tools.duckduckgo_tool import search_news

logger = get_logger(__name__)

PRICE_CACHE_DIR = "data/price_cache"
NEWS_CACHE_DIR = "data/news_cache"

# Ensure directories exist
os.makedirs(PRICE_CACHE_DIR, exist_ok=True)
os.makedirs(NEWS_CACHE_DIR, exist_ok=True)

def get_cached_history(ticker: str, period: str = "1y", interval: str = "1d") -> Optional[pd.DataFrame]:
    """Gets stock history from cache or fetches and caches it."""
    cache_path = os.path.join(PRICE_CACHE_DIR, f"{ticker}_{period}_{interval}.csv")
    
    if os.path.exists(cache_path):
        logger.info(f"Loading cached history for {ticker} from {cache_path}")
        try:
            return pd.read_csv(cache_path, index_col=0, parse_dates=True)
        except Exception as e:
            logger.error(f"Error reading cache for {ticker}: {str(e)}")
    
    logger.info(f"Cache miss for {ticker} history. Fetching from Yahoo Finance.")
    df = fetch_stock_history(ticker, period, interval)
    if df is not None and not df.empty:
        df.to_csv(cache_path)
        logger.info(f"Saved history cache for {ticker} to {cache_path}")
    return df

def get_cached_news(stock_name: str, max_results: int = 5) -> List[Dict[str, str]]:
    """Gets news from cache or fetches and caches it."""
    safe_name = stock_name.replace(" ", "_").lower()
    cache_path = os.path.join(NEWS_CACHE_DIR, f"{safe_name}_news.json")
    
    if os.path.exists(cache_path):
        logger.info(f"Loading cached news for {stock_name} from {cache_path}")
        try:
            with open(cache_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading news cache for {stock_name}: {str(e)}")
            
    logger.info(f"Cache miss for {stock_name} news. Fetching from DuckDuckGo.")
    query = f"{stock_name} stock news"
    news = search_news(query, max_results)
    
    if news:
        try:
            with open(cache_path, 'w') as f:
                json.dump(news, f, indent=2)
            logger.info(f"Saved news cache for {stock_name} to {cache_path}")
        except Exception as e:
            logger.error(f"Error saving news cache for {stock_name}: {str(e)}")
            
    return news
