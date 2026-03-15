from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from backend.langgraph_pipeline import run_pipeline
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    intent: str
    tickers: list[str]
    fundamental_report: Optional[str] = None
    technical_report: Optional[str] = None
    sentiment_report: Optional[str] = None
    portfolio_report: Optional[str] = None
    final_report: Optional[str] = None

@router.post("/analyze", response_model=QueryResponse)
async def analyze_query(request: QueryRequest):
    logger.info(f"Received query request: {request.query}")
    try:
        # Run the LangGraph Pipeline synchronously 
        result = run_pipeline(request.query)
        
        response = QueryResponse(
            intent=result.get("intent", "unknown"),
            tickers=result.get("tickers", []),
            fundamental_report=result.get("fundamental_report"),
            technical_report=result.get("technical_report"),
            sentiment_report=result.get("sentiment_report"),
            portfolio_report=result.get("portfolio_report"),
            final_report=result.get("final_report")
        )
        logger.info(f"Successfully processed query intent: {response.intent}")
        return response
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
