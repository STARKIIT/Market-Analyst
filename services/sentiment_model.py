from typing import List, Dict, Any
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from utils.logger import get_logger

logger = get_logger(__name__)

# Initialize analyzer globally to avoid recreating it
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(news_items: List[Dict[str, str]]) -> Dict[str, Any]:
    """Analyzes sentiment of news articles using VADER."""
    logger.info(f"Analyzing sentiment for {len(news_items)} news items")
    
    if not news_items:
        return {
            "overall_score": 0.0,
            "overall_sentiment": "Neutral",
            "details": []
        }
        
    scores = []
    details = []
    
    try:
        for item in news_items:
            # Combine title and body for Better context
            text = f"{item.get('title', '')}. {item.get('body', '')}"
            
            # Get polarity scores
            sentiment = analyzer.polarity_scores(text)
            compound_score = sentiment['compound']
            scores.append(compound_score)
            
            classification = (
                "Positive" if compound_score >= 0.05 else
                "Negative" if compound_score <= -0.05 else
                "Neutral"
            )
            
            details.append({
                "title": item.get("title", ""),
                "score": compound_score,
                "classification": classification
            })
            
        avg_score = sum(scores) / len(scores) if scores else 0.0
        
        overall_sentiment = (
            "Bullish" if avg_score >= 0.15 else
            "Bearish" if avg_score <= -0.15 else
            "Neutral"
        )
        
        result = {
            "overall_score": round(avg_score, 2),
            "overall_sentiment": overall_sentiment,
            "details": details
        }
        
        logger.info(f"Calculated overall sentiment score: {result['overall_score']} ({result['overall_sentiment']})")
        return result
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {str(e)}")
        return {
            "overall_score": 0.0,
            "overall_sentiment": "Neutral",
            "error": str(e)
        }
