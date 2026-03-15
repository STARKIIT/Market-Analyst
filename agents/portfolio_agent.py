import pandas as pd
from typing import List
from services.data_fetcher import get_cached_history
from utils.logger import get_logger

logger = get_logger(__name__)

def run_portfolio_agent(tickers: List[str]) -> str:
    logger.info(f"Portfolio Agent started for {tickers}")
    
    if not tickers:
        return "No tickers provided for portfolio analysis."
        
    portfolio_data = {}
    returns = {}
    
    for ticker in tickers:
        df = get_cached_history(ticker, period="1y", interval="1d")
        if df is not None and not df.empty:
            start_price = df['Close'].iloc[0]
            end_price = df['Close'].iloc[-1]
            ret = ((end_price - start_price) / start_price) * 100
            returns[ticker] = ret
            portfolio_data[ticker] = {
                "start_price": start_price,
                "end_price": end_price,
                "return_pct": ret,
                "volatility": df['Close'].pct_change().std() * (252 ** 0.5) * 100 # Annualized volatility
            }
            
    if not portfolio_data:
        logger.warning("Could not retrieve historical data for any tickers in portfolio.")
        return "Could not retrieve history for any tickers."
        
    # Basic calculations
    avg_return = sum(returns.values()) / len(returns)
    best_performer = max(returns, key=returns.get)
    worst_performer = min(returns, key=returns.get)
    
    # Calculate avg volatility
    vols = [data['volatility'] for data in portfolio_data.values()]
    avg_volatility = sum(vols) / len(vols)
    vol_str = "High" if avg_volatility > 30 else "Medium" if avg_volatility > 15 else "Low"
    
    report = [
        "Portfolio Performance",
        f"Return (1Y): {avg_return:.2f}%",
        f"Volatility: {vol_str} ({avg_volatility:.2f}%)",
        f"Top performer: {best_performer} ({returns[best_performer]:.2f}%)",
        f"Weakest: {worst_performer} ({returns[worst_performer]:.2f}%)"
    ]
    
    logger.info("Portfolio Agent completed successfully.")
    return "\n".join(report)
