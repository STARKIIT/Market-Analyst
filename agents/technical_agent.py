import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from config.settings import settings
from services.data_fetcher import get_cached_history
from services.indicator_calculator import get_technical_indicators
from utils.logger import get_logger

logger = get_logger(__name__)

def run_technical_agent(ticker: str) -> str:
    logger.info(f"Technical Agent started for {ticker}")
    
    df = get_cached_history(ticker, period="1y", interval="1d")
    if df is None or df.empty:
        logger.warning(f"No historical data found for {ticker}")
        return f"Could not retrieve historical data for {ticker}."
        
    indicators = get_technical_indicators(df)
    if not indicators:
        return f"Not enough data to calculate technical indicators for {ticker}."

    prompt_path = os.path.join(os.path.dirname(__file__), "..", "models", "prompts", "technical_prompt.txt")
    with open(prompt_path, "r") as f:
        template = f.read()
        
    prompt = PromptTemplate.from_template(template)
    formatted_prompt = prompt.format(
        ticker=ticker,
        indicators=str(indicators)
    )
    
    try:
        llm = ChatOpenAI(api_key=settings.OPENAI_API_KEY, model="gpt-4o-mini", temperature=0.1)
        response = llm.invoke(formatted_prompt)
        logger.info(f"Technical Agent completed for {ticker}")
        return response.content
    except Exception as e:
        logger.error(f"Technical Agent LLM error for {ticker}: {str(e)}")
        # Fallback
        return f"Trend: {indicators.get('trend')}\nRSI: {indicators.get('rsi')}\nMACD Crossover: {indicators.get('macd_crossover')}\nSupport: {indicators.get('support')}\nResistance: {indicators.get('resistance')}\n\nSignal:\nUnable to generate LLM summary due to an error."
