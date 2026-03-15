import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.main import app

client = TestClient(app)

def test_analyze_endpoint_success():
    with patch('backend.router.run_pipeline') as mock_pipeline:
        mock_pipeline.return_value = {
            "intent": "single_stock",
            "tickers": ["AAPL"],
            "fundamental_report": "Fund",
            "technical_report": "Tech",
            "sentiment_report": "Sent",
            "portfolio_report": "",
            "final_report": "Final"
        }
        
        response = client.post("/api/analyze", json={"query": "How is AAPL doing?"})
        
        assert response.status_code == 200
        data = response.json()
        assert data["intent"] == "single_stock"
        assert data["tickers"] == ["AAPL"]
        assert data["final_report"] == "Final"

def test_analyze_endpoint_error():
    with patch('backend.router.run_pipeline') as mock_pipeline:
        mock_pipeline.side_effect = Exception("Pipeline failure")
        
        response = client.post("/api/analyze", json={"query": "How is AAPL doing?"})
        
        assert response.status_code == 500
        assert "Pipeline failure" in response.json()["detail"]
