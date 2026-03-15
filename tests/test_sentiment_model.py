import pytest
from services.sentiment_model import analyze_sentiment

def test_analyze_sentiment_empty():
    result = analyze_sentiment([])
    assert result["overall_score"] == 0.0
    assert result["overall_sentiment"] == "Neutral"

def test_analyze_sentiment_positive():
    news = [
        {"title": "Company X reports record profits", "body": "Profits are up 200% and outlook is fantastic."}
    ]
    result = analyze_sentiment(news)
    assert result["overall_score"] > 0
    assert result["overall_sentiment"] == "Bullish"
    assert result["details"][0]["classification"] == "Positive"

def test_analyze_sentiment_negative():
    news = [
        {"title": "Company X faces bankruptcy", "body": "Terrible losses and a horrible outlook."}
    ]
    result = analyze_sentiment(news)
    assert result["overall_score"] < 0
    assert result["overall_sentiment"] == "Bearish"
    assert result["details"][0]["classification"] == "Negative"
