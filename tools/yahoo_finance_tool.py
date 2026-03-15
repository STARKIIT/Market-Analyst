import yfinance as yf
import pandas as pd
from typing import Dict, Any, Optional
from utils.logger import get_logger

logger = get_logger(__name__)

def fetch_stock_history(ticker: str, period: str = "1y", interval: str = "1d") -> Optional[pd.DataFrame]:
    """Fetches historical stock price data."""
    logger.info(f"Fetching stock history for {ticker} (period: {period}, interval: {interval})")
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)
        if df.empty:
            logger.warning(f"No historical data found for {ticker}")
            return None
        logger.info(f"Successfully fetched {len(df)} rows of data for {ticker}")
        return df
    except Exception as e:
        logger.error(f"Error fetching stock history for {ticker}: {str(e)}")
        return None

def fetch_fundamentals(ticker: str) -> Dict[str, Any]:
    """Fetches fundamental metrics for a stock."""
    logger.info(f"Fetching fundamentals for {ticker}")
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        fundamentals = {
            "revenue": info.get("totalRevenue"),
            "eps": info.get("trailingEps"),
            "pe_ratio": info.get("trailingPE"),
            "market_cap": info.get("marketCap"),
            "debt": info.get("totalDebt"),
            "free_cash_flow": info.get("freeCashflow"),
            "roe": info.get("returnOnEquity"),
            "profit_margin": info.get("profitMargins")
        }
        logger.info(f"Successfully fetched fundamentals for {ticker}")
        logger.debug(f"Fundamentals data: {fundamentals}")
        return fundamentals
    except Exception as e:
        logger.error(f"Error fetching fundamentals for {ticker}: {str(e)}")
        return {}
