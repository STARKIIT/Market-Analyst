from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from langchain_openai import ChatOpenAI
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)

class MasterAgentResponse(BaseModel):
    intent: Literal["single_stock", "portfolio", "comparison", "unknown"] = Field(description="The classified intent of the user query")
    tickers: List[str] = Field(description="A list of identified stock tickers in the query (e.g. ['AAPL', 'MSFT'])")

def run_master_agent(query: str) -> MasterAgentResponse:
    """Classifies user intent and extracts tickers from the query."""
    logger.info(f"Master Agent started for query: '{query}'")
    
    # Very rudimentary fallback standard for parsing if LLM is down
    if len(settings.OPENAI_API_KEY) < 5:
        logger.warning("No OpenAI key detected. Falling back to naive parsing.")
        intent = "single_stock"
        if "portfolio" in query.lower():
            intent = "portfolio"
        elif "compare" in query.lower() or "vs" in query.lower():
            intent = "comparison"
            
        words = query.split()
        tickers = [w.upper() for w in words if len(w) <= 5 and w.isalpha()]
        return MasterAgentResponse(intent=intent, tickers=tickers)

    try:
        llm = ChatOpenAI(api_key=settings.OPENAI_API_KEY, model="gpt-4o-mini", temperature=0)
        
        # Use Langchain's structured output
        structured_llm = llm.with_structured_output(MasterAgentResponse)
        
        system_prompt = (
            "You are a routing master agent for a stock market analysis system. "
            "Analyze the user's query and classify the intent into one of: 'single_stock', 'portfolio', 'comparison', 'unknown'. "
            "Also extract all stock tickers (symbols) mentioned in the query. If a company name is used (e.g., 'Apple', 'Reliance'), convert it to its ticker symbol (e.g., 'AAPL', 'RELIANCE.NS')."
        )
        
        response = structured_llm.invoke([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ])
        
        logger.info(f"Master Agent classified intent: {response.intent} with tickers: {response.tickers}")
        return response
    except Exception as e:
        logger.error(f"Master Agent LLM error: {str(e)}")
        # Fail safe
        return MasterAgentResponse(intent="unknown", tickers=[])
