import streamlit as st
import requests
import json
import pandas as pd
import yfinance as yf

# Configuration
API_URL = "http://localhost:8000/api/analyze"

st.set_page_config(
    page_title="Multi-Agent Market Analyst",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Multi-Agent Stock Market Analyst")
st.markdown("Powered by LangGraph and specialized AI Agents")

# Sidebar
with st.sidebar:
    st.header("Settings")
    st.markdown("This application uses multiple AI agents to gather fundamentals, technicals, and sentiment before aggregating a final recommendation.")
    
# Main UI
query = st.text_input("Ask the Market Analyst AI:", placeholder="e.g. How is Reliance doing? or Analyze my portfolio AAPL MSFT")

if st.button("Analyze") and query:
    with st.spinner("Agents are analyzing the market..."):
        try:
            response = requests.post(API_URL, json={"query": query})
            
            if response.status_code == 200:
                data = response.json()
                
                # Top section: Intent classification
                intent = data.get("intent", "Unknown")
                tickers = data.get("tickers", [])
                
                st.success(f"**Intent Recognized**: {intent.replace('_', ' ').title()}")
                if tickers:
                    st.info(f"**Tickers Identified**: {', '.join(tickers)}")
                
                # Display Results based on Intent
                if intent == "portfolio" and data.get("portfolio_report"):
                    st.subheader("📊 Portfolio Analysis")
                    st.markdown(data["portfolio_report"])
                    
                else: 
                    # Single Stock or Comparison
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.subheader("🧠 Aggregator Final Output")
                        st.info(data.get("final_report", "No final report generated."))
                        
                        st.divider()
                        
                        # Tabs for agent logs (Explainable AI)
                        st.subheader("Agent Reasoning Logs")
                        tab1, tab2, tab3 = st.tabs(["Fundamental Agent", "Technical Agent", "Sentiment Agent"])
                        
                        with tab1:
                            st.text(data.get("fundamental_report") or "No fundamental report generated.")
                        with tab2:
                            st.text(data.get("technical_report") or "No technical report generated.")
                        with tab3:
                            st.text(data.get("sentiment_report") or "No sentiment report generated.")
                            
                    with col2:
                        # Simple charts
                        if tickers:
                            st.subheader("Recent Price Action")
                            for ticker in tickers:
                                try:
                                    stock = yf.Ticker(ticker)
                                    df = stock.history(period="1mo")
                                    if not df.empty:
                                        st.line_chart(df['Close'])
                                        st.caption(f"{ticker} - 1 Month Price")
                                except:
                                    pass
            else:
                st.error(f"API Error ({response.status_code}): {response.text}")
                
        except Exception as e:
            st.error(f"Failed to connect to backend: {str(e)}\n\nIs the FastAPI server running?")
