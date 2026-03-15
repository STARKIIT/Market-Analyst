import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)

def run_aggregator_agent(ticker: str, fundamental_report: str, technical_report: str, sentiment_report: str) -> str:
    logger.info(f"Aggregator Agent started for {ticker}")
    
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "models", "prompts", "aggregator_prompt.txt")
    with open(prompt_path, "r") as f:
        template = f.read()
        
    prompt = PromptTemplate.from_template(template)
    
    formatted_prompt = prompt.format(
        ticker=ticker,
        fundamental_report=fundamental_report,
        technical_report=technical_report,
        sentiment_report=sentiment_report
    )
    
    try:
        llm = ChatGoogleGenerativeAI(google_api_key=settings.GEMINI_API_KEY, model="gemini-2.5-flash", temperature=0.1) # Aggregator gets better model
        response = llm.invoke(formatted_prompt)
        logger.info(f"Aggregator Agent completed for {ticker}")
        return response.content
    except Exception as e:
        logger.error(f"Aggregator Agent LLM error for {ticker}: {str(e)}")
        # Fallback
        return f"{ticker} Outlook:\n\nRecommendation:\nUnable to aggregate agent reports due to an error. See individual agent logs."
