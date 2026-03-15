import pytest
from unittest.mock import patch
from backend.langgraph_pipeline import run_pipeline

def test_run_pipeline_single_stock():
    with patch('backend.langgraph_pipeline.run_master_agent') as mock_master:
        with patch('backend.langgraph_pipeline.run_fundamental_agent') as mock_fund:
            with patch('backend.langgraph_pipeline.run_technical_agent') as mock_tech:
                with patch('backend.langgraph_pipeline.run_sentiment_agent') as mock_sent:
                    with patch('backend.langgraph_pipeline.run_aggregator_agent') as mock_aggregator:
                        
                        mock_master.return_value.intent = "single_stock"
                        mock_master.return_value.tickers = ["AAPL"]
                        
                        mock_fund.return_value = "Fund Report"
                        mock_tech.return_value = "Tech Report"
                        mock_sent.return_value = "Sent Report"
                        mock_aggregator.return_value = "Final Report"
                        
                        result = run_pipeline("How is AAPL doing?")
                        
                        assert result["intent"] == "single_stock"
                        assert result["tickers"] == ["AAPL"]
                        assert result["fundamental_report"] == "Fund Report"
                        assert result["final_report"] == "Final Report"

def test_run_pipeline_portfolio():
    with patch('backend.langgraph_pipeline.run_master_agent') as mock_master:
        with patch('backend.langgraph_pipeline.run_portfolio_agent') as mock_port:
            mock_master.return_value.intent = "portfolio"
            mock_master.return_value.tickers = ["AAPL", "GOOG"]
            
            mock_port.return_value = "Portfolio Report"
            
            result = run_pipeline("Analyze portfolio AAPL GOOG")
            
            assert result["intent"] == "portfolio"
            assert result["tickers"] == ["AAPL", "GOOG"]
            assert result["portfolio_report"] == "Portfolio Report"
