import pytest
from unittest.mock import patch, MagicMock
from streamlit.testing.v1 import AppTest
import pandas as pd

@patch('frontend.streamlit_app.requests.post')
@patch('frontend.streamlit_app.yf.Ticker')
def test_streamlit_app_success(mock_ticker, mock_post):
    at = AppTest.from_file("frontend/streamlit_app.py")
    
    # Mock the API payload
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "intent": "single_stock",
        "tickers": ["AAPL"],
        "fundamental_report": "Good fundamentals",
        "technical_report": "Bullish trend",
        "sentiment_report": "Positive sentiment",
        "final_report": "Buy AAPL"
    }
    mock_post.return_value = mock_response

    # Mock yfinance inside streamlit
    mock_stock = MagicMock()
    mock_stock.history.return_value = pd.DataFrame({'Close': [100.0, 101.0, 102.0]})
    mock_ticker.return_value = mock_stock

    # Run the app initially
    at.run()
    
    # Simulate user typing a query and pressing complete
    at.text_input[0].input("How is AAPL doing?").run()
    at.button[0].click().run()

    # Validate no unhandled exceptions crashed the UI
    assert not at.exception
    
    # Check elements generated
    successes = [s.value for s in at.success]
    assert any("Single Stock" in s for s in successes)
    
    infos = [i.value for i in at.info]
    assert any("AAPL" in i for i in infos)
    assert any("Buy AAPL" in i for i in infos)

@patch('frontend.streamlit_app.requests.post')
def test_streamlit_app_api_error(mock_post):
    at = AppTest.from_file("frontend/streamlit_app.py")
    
    # Mock API failure
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_post.return_value = mock_response

    at.run()
    at.text_input[0].input("How is AAPL doing?").run()
    at.button[0].click().run()

    # Check that error is appropriately caught and displayed
    assert not at.exception
    errors = [e.value for e in at.error]
    assert any("API Error (500)" in e for e in errors)

@patch('frontend.streamlit_app.requests.post')
def test_streamlit_app_connection_failed(mock_post):
    at = AppTest.from_file("frontend/streamlit_app.py")
    
    # Mock total connection failure
    mock_post.side_effect = Exception("Connection refused")

    at.run()
    at.text_input[0].input("How is AAPL doing?").run()
    at.button[0].click().run()

    assert not at.exception
    errors = [e.value for e in at.error]
    assert any("Failed to connect to backend" in e for e in errors)
