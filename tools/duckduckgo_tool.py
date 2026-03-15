from duckduckgo_search import DDGS
from typing import List, Dict
from utils.logger import get_logger
from config.settings import settings

logger = get_logger(__name__)

def search_news(query: str, max_results: int = None) -> List[Dict[str, str]]:
    """Searches news using DuckDuckGo based on the query."""
    max_res = max_results or settings.DUCKDUCKGO_MAX_RESULTS
    logger.info(f"Searching DuckDuckGo news for query: '{query}' with max {max_res} results")
    try:
        results = []
        with DDGS() as ddgs:
            ddgs_news_gen = ddgs.news(query, max_results=max_res)
            for r in ddgs_news_gen:
                results.append({
                    "title": r.get('title', ''),
                    "body": r.get('body', ''),
                    "url": r.get('url', ''),
                    "date": r.get('date', ''),
                    "source": r.get('source', '')
                })
        
        logger.info(f"Found {len(results)} news items for query: '{query}'")
        return results
    except Exception as e:
        logger.error(f"Error searching news for '{query}': {str(e)}")
        return []
