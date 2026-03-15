import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from config.settings import settings
from services.data_fetcher import get_cached_news
from services.sentiment_model import analyze_sentiment
from utils.logger import get_logger

logger = get_logger(__name__)

def run_sentiment_agent(ticker: str) -> str:
    logger.info(f"Sentiment Agent started for {ticker}")
    
    news = get_cached_news(ticker, max_results=5)
    if not news:
        logger.warning(f"No news found for {ticker}")
        return f"Could not retrieve news for {ticker}."
        
    sentiment_result = analyze_sentiment(news)
    
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "models", "prompts", "sentiment_prompt.txt")
    with open(prompt_path, "r") as f:
        template = f.read()
        
    prompt = PromptTemplate.from_template(template)
    formatted_prompt = prompt.format(
        company=ticker,
        sentiment_score=sentiment_result.get("overall_score"),
        overall_sentiment=sentiment_result.get("overall_sentiment"),
        news_details=json.dumps(sentiment_result.get("details", []), indent=2)
    )
    
    try:
        llm = ChatGoogleGenerativeAI(google_api_key=settings.GEMINI_API_KEY, model="gemini-2.5-flash", temperature=0.1)
        response = llm.invoke(formatted_prompt)
        logger.info(f"Sentiment Agent completed for {ticker}")
        return response.content
    except Exception as e:
        logger.error(f"Sentiment Agent LLM error for {ticker}: {str(e)}")
        # Fallback
        return f"News Sentiment Score: {sentiment_result.get('overall_score')}\n\nOverall sentiment: {sentiment_result.get('overall_sentiment')}"
