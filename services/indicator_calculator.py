import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from utils.logger import get_logger

logger = get_logger(__name__)

def calculate_sma(df: pd.DataFrame, window: int) -> pd.Series:
    return df['Close'].rolling(window=window).mean()

def calculate_rsi(df: pd.DataFrame, periods: int = 14) -> pd.Series:
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)

    avg_gain = gain.rolling(window=periods, min_periods=1).mean()
    avg_loss = loss.rolling(window=periods, min_periods=1).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    fast_ema = df['Close'].ewm(span=fast, adjust=False).mean()
    slow_ema = df['Close'].ewm(span=slow, adjust=False).mean()
    macd_line = fast_ema - slow_ema
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    
    macd_df = pd.DataFrame({
        'MACD': macd_line,
        'Signal': signal_line,
        'Histogram': macd_line - signal_line
    })
    return macd_df

def calculate_support_resistance(df: pd.DataFrame, window: int = 20) -> tuple:
    if len(df) < window:
        return df['Low'].min(), df['High'].max()
    support = df['Low'].rolling(window=window).min().iloc[-1]
    resistance = df['High'].rolling(window=window).max().iloc[-1]
    return support, resistance

def get_technical_indicators(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculates all technical indicators for the given historical data."""
    logger.info("Calculating technical indicators")
    try:
        if df is None or len(df) < 50:
            logger.warning("Not enough data to calculate technical indicators")
            return {}

        df = df.copy()
        
        # Moving averages
        df['SMA_20'] = calculate_sma(df, 20)
        df['SMA_50'] = calculate_sma(df, 50)
        
        # RSI
        df['RSI'] = calculate_rsi(df)
        
        # MACD
        macd_df = calculate_macd(df)
        df = pd.concat([df, macd_df], axis=1)
        
        # Current trend (simple SMA cross)
        current_close = df['Close'].iloc[-1]
        sma_20 = df['SMA_20'].iloc[-1]
        sma_50 = df['SMA_50'].iloc[-1]
        
        trend = "Bullish" if current_close > sma_20 and sma_20 > sma_50 else "Bearish" if current_close < sma_20 and sma_20 < sma_50 else "Neutral"
        
        support, resistance = calculate_support_resistance(df)
        
        macd_cross = "Positive" if df['Histogram'].iloc[-1] > 0 and df['Histogram'].iloc[-2] <= 0 else \
                     "Negative" if df['Histogram'].iloc[-1] < 0 and df['Histogram'].iloc[-2] >= 0 else \
                     "None"

        indicators = {
            "current_price": float(current_close),
            "trend": trend,
            "rsi": float(df['RSI'].iloc[-1]),
            "macd_crossover": macd_cross,
            "support": float(support),
            "resistance": float(resistance),
            "volume_trend": "Increasing" if df['Volume'].iloc[-1] > df['Volume'].rolling(20).mean().iloc[-1] else "Decreasing"
        }
        
        logger.info(f"Calculated indicators: {indicators}")
        return indicators
    except Exception as e:
        logger.error(f"Error calculating technical indicators: {str(e)}")
        return {}
