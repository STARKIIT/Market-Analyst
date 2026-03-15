import pytest
import pandas as pd
from unittest.mock import patch
from agents.portfolio_agent import run_portfolio_agent

def test_run_portfolio_agent_no_tickers():
    result = run_portfolio_agent([])
    assert "No tickers provided" in result

def test_run_portfolio_agent_no_data():
    with patch('agents.portfolio_agent.get_cached_history') as mock_fetch:
        mock_fetch.return_value = pd.DataFrame()
        result = run_portfolio_agent(["AAPL", "GOOG"])
        assert "Could not retrieve history for any tickers" in result

def test_run_portfolio_agent_success():
    with patch('agents.portfolio_agent.get_cached_history') as mock_fetch:
        # Create a mock dataframe that changes price -> 100 to 110 (10% return)
        mock_df1 = pd.DataFrame({'Close': [100.0, 105.0, 110.0]})
        mock_df2 = pd.DataFrame({'Close': [100.0, 95.0, 90.0]})
        
        # side_effect to return different df for AAPL and GOOG
        mock_fetch.side_effect = [mock_df1, mock_df2]
        
        result = run_portfolio_agent(["AAPL", "GOOG"])
        
        assert "Portfolio Performance" in result
        assert "Top performer: AAPL" in result
        assert "Weakest: GOOG" in result
