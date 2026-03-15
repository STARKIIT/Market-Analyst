from gnews import GNews
from typing import List, Dict
from utils.logger import get_logger
from config.settings import settings

logger = get_logger(__name__)

def search_news(query: str, max_results: int = None) -> List[Dict[str, str]]:
    """Searches news using Google News based on the query."""
    max_res = max_results or settings.NEWS_MAX_RESULTS
    logger.info(f"Searching Google News for query: '{query}' with max {max_res} results")
    try:
        google_news = GNews(max_results=max_res)
        articles = google_news.get_news(query)
        
        results = []
        for r in articles:
            results.append({
                "title": r.get('title', ''),
                "body": r.get('description', ''),  # GNews calls the main snippet 'description'
                "url": r.get('url', ''),
                "date": r.get('published date', ''), # GNews uses 'published date'
                "source": r.get('publisher', {}).get('title', '') if isinstance(r.get('publisher'), dict) else ''
            })
            
        logger.info(f"Found {len(results)} news items for query: '{query}'")
        return results
    except Exception as e:
        logger.error(f"Error searching news for '{query}': {str(e)}")
        return []
