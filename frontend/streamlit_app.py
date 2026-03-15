import streamlit as st
import requests
import json
import pandas as pd
import yfinance as yf

# Configuration
API_URL = "http://localhost:8000/api/analyze"

st.set_page_config(
    page_title="Market Scholar",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎓 Market Scholar")
st.markdown("A minimalist, multi-agent financial researcher powered by Google Gemini.")

# Sidebar
with st.sidebar:
    st.header("About Market Scholar")
    st.markdown("This application uses a team of highly specialized AI agents to autonomously research and analyze the stock market before aggregating a final conclusion.")
    
    st.divider()
    
    with st.expander("🤖 The Multi-Agent Architecture", expanded=False):
        st.markdown('''
        * **Master Agent**: Routes your query to the correct pipeline.
        * **Fundamental Agent**: Analyzes revenues, P/E ratios, and debt structures.
        * **Technical Agent**: Calculates MACD, RSI, and support/resistance zones.
        * **Sentiment Agent**: Scrapes breaking news to gauge market mood.
        * **Aggregator Agent**: Synthesizes the data into one cohesive recommendation.
        ''')
        
    st.divider()
    
    st.subheader("💡 Example Queries")
    st.markdown('''
    - "How is AAPL doing right now?"
    - "Analyze my portfolio: TSLA, MSFT, and NVDA"
    - "Give me a technical breakdown of INFY.NS"
    ''')
    
    st.divider()
    st.caption("🟢 System Services: **Online**")
    
# Main UI
with st.form("search_form"):
    query = st.text_input("Ask Market Scholar:", placeholder="e.g. How is Reliance doing? or Analyze my portfolio AAPL MSFT")
    submit_pressed = st.form_submit_button("Analyze")

if submit_pressed and query:
    with st.spinner("Scholar Agents are researching the market..."):
        try:
            response = requests.post(API_URL, json={"query": query})
            
            if response.status_code == 200:
                data = response.json()
                
                # Top section: Intent classification (Minimalist)
                intent = data.get("intent", "Unknown")
                tickers = data.get("tickers", [])
                
                # Subtle metadata rather than massive alerts
                st.caption(f"🧠 **Pipeline Routed**: {intent.replace('_', ' ').title()} &nbsp;&nbsp;|&nbsp;&nbsp; 🎯 **Tickers Scoped**: {', '.join(tickers) if tickers else 'None'}")
                st.write("") # small padding
                
                # Display Results based on Intent
                if intent == "portfolio" and data.get("portfolio_report"):
                    st.subheader("📊 Portfolio Analysis")
                    st.markdown(data["portfolio_report"])
                    
                else: 
                    # Single Stock or Comparison
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        # Highlighted minimalist final output container
                        st.subheader("Executive Summary")
                        with st.container(border=True):
                            st.markdown(data.get("final_report", "No final report generated."))
                        
                        st.divider()
                        
                        # Tabs for agent logs (Explainable AI)
                        st.markdown("*(Optional) Internal Agent Reasoning Logs:*")
                        tab1, tab2, tab3 = st.tabs(["Fundamental", "Technical", "Sentiment"])
                        
                        with tab1:
                            st.info(data.get("fundamental_report") or "No fundamental report generated.")
                        with tab2:
                            st.info(data.get("technical_report") or "No technical report generated.")
                        with tab3:
                            st.info(data.get("sentiment_report") or "No sentiment report generated.")
                            
                    with col2:
                        # Simple charts
                        if tickers:
                            st.subheader("Recent Price Action")
                            for ticker in tickers:
                                try:
                                    # Fallback logic for Indian stocks
                                    tickers_to_try = [f"{ticker}.NS", ticker] if "." not in ticker else [ticker]
                                    df = pd.DataFrame()
                                    plot_ticker = ticker
                                    
                                    for t in tickers_to_try:
                                        stock = yf.Ticker(t)
                                        temp_df = stock.history(period="1mo")
                                        if not temp_df.empty:
                                            df = temp_df
                                            plot_ticker = t
                                            break
                                            
                                    if not df.empty:
                                        st.line_chart(df['Close'])
                                        st.caption(f"{plot_ticker} - 1 Month Price")
                                except:
                                    pass
            else:
                st.error(f"API Error ({response.status_code}): {response.text}")
                
        except Exception as e:
            st.error(f"Failed to connect to backend: {str(e)}\n\nIs the FastAPI server running?")
