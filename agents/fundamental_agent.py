import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from config.settings import settings
from tools.yahoo_finance_tool import fetch_fundamentals
from utils.logger import get_logger

logger = get_logger(__name__)

def run_fundamental_agent(ticker: str) -> str:
    logger.info(f"Fundamental Agent started for {ticker}")
    fundamentals = fetch_fundamentals(ticker)
    
    if not fundamentals:
        logger.warning(f"No fundamental data found for {ticker}")
        return f"Could not retrieve fundamental data for {ticker}."
    
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "models", "prompts", "fundamental_prompt.txt")
    with open(prompt_path, "r") as f:
        template = f.read()
        
    prompt = PromptTemplate.from_template(template)
    
    formatted_prompt = prompt.format(
        company=ticker,
        fundamentals=str(fundamentals)
    )
    
    try:
        llm = ChatOpenAI(api_key=settings.OPENAI_API_KEY, model="gpt-4o-mini", temperature=0.1)
        response = llm.invoke(formatted_prompt)
        logger.info(f"Fundamental Agent completed for {ticker}")
        return response.content
    except Exception as e:
        logger.error(f"Fundamental Agent LLM error for {ticker}: {str(e)}")
        # Fallback if no API key or LLM fails
        return f"{ticker} Fundamentals:\n\nRevenue: {fundamentals.get('revenue', 'N/A')}\nEPS: {fundamentals.get('eps', 'N/A')}\nPE Ratio: {fundamentals.get('pe_ratio', 'N/A')}\nDebt: {fundamentals.get('debt', 'N/A')}\n\nConclusion:\nUnable to generate LLM summary due to an error."
