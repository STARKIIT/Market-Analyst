# Multi-Agent Stock Market Analyst - Build Plan & To-Do List

This document acts as a precise, step-by-step checklist for an AI agent to build the Stock Market Analyst application based on the specifications in `architecture.md`.

## Phase 1: Project Setup & Initialization
- [x] Initialize Python environment and dependency manager (e.g., `pip` with `requirements.txt`, `poetry`, or `uv`).
- [x] Instantiate the exact folder structure:
  - `backend/`
  - `agents/`
  - `tools/`
  - `services/`
  - `frontend/`
  - `models/prompts/`
  - `models/templates/`
  - `config/`
  - `tests/`
  - `data/price_cache/`
  - `data/news_cache/`
- [x] Create `config/settings.py` to handle environment configurations (API Keys for OpenAI, DuckDuckGo, etc.).
- [x] Create a `README.md` with instructions on how to run the API and Streamlit UI.

## Phase 2: Data Layer & Services
- [x] **Data Fetching (`tools/yahoo_finance_tool.py`)**:
  - Implement functions to fetch real-time and historical stock price data.
  - Implement functions to pull fundamental metrics.
- [x] **News Scraping (`tools/duckduckgo_tool.py`)**:
  - Implement functions to search DuckDuckGo for the latest news on standard query strings (e.g., "{Stock Name} stock news").
- [x] **Caching Layer (`services/data_fetcher.py`)**:
  - Implement a caching mechanism using local files in `data/price_cache/` and `data/news_cache/` to avoid rate limits and excessive API calls.
- [x] **Technical Calculators (`services/indicator_calculator.py`)**:
  - Add logic to calculate Moving Averages, RSI, MACD, Volume trends, Support, and Resistance levels based on historical data.
- [x] **Sentiment processing (`services/sentiment_model.py`)**:
  - Setup integration with a small transformer or a lightweight LLM call to classify news headlines as positive/negative/neutral to derive a sentiment score.

## Phase 3: Core Agents Implementation
Create appropriate LLM prompt files first under `models/prompts/` (e.g., `fundamental_prompt.txt`, `technical_prompt.txt`, `sentiment_prompt.txt`).
- [x] **Fundamental Agent (`agents/fundamental_agent.py`)**:
  - **Inputs**: Ticker/Company name.
  - **Task**: Use Yahoo Finance tool to retrieve Revenue, EPS, PE ratio, Market Cap, Debt, Free Cash Flow, ROE, Profit Margin. Evaluate and output a succinct summary on structure, valuation, and growth.
- [x] **Technical Agent (`agents/technical_agent.py`)**:
  - **Inputs**: Ticker historical data.
  - **Task**: Use Indicator Calculator service to find momentum signals (Bullish/Bearish, RSI status, MACD crosses).
- [x] **Sentiment Agent (`agents/sentiment_agent.py`)**:
  - **Inputs**: Ticker/Company name.
  - **Task**: Scrape recent news using DuckDuckGo, extract headlines, formulate sentiment score, and yield news highlights with total sentiment bias.
- [x] *(Optional)* **Portfolio Agent (`agents/portfolio_agent.py`)**:
  - **Inputs**: A list of tickers.
  - **Task**: Fetch prices, calculate 1-year returns, evaluate volatility/risk, compute diversification metrics, and report sector exposure.

## Phase 4: LangGraph Orchestration & Aggregator
- [x] **Aggregator Node / Agent (`agents/aggregator_agent.py` or within langgraph pipeline)**:
  - **Task**: Take the compiled outputs from the Fundamental, Technical, and Sentiment agents and use LLM reasoning to summarize into a final unified recommendation.
- [x] **Master Orchestrator (`agents/master_agent.py`)**:
  - **Task**: Perform intent classification (`single_stock`, `portfolio`, `comparison`) based on the user's string query.
- [x] **LangGraph Pipeline (`backend/langgraph_pipeline.py`)**:
  - Create the LangGraph structural `StateGraph`.
  - Wire the **Intent Classifier** routing to specific parallel executions (e.g., `run_parallel([fundamental, technical, sentiment])`).
  - Add the **Aggregator / Final Report** node at the end.
  - Implement streaming events to emit which agent is currently running.

## Phase 5: Backend API (FastAPI)
- [x] **API Router (`backend/router.py`)**:
  - Define Pydantic request and response models.
  - Expose API Endpoints: `POST /analyze-stock`, `POST /analyze-portfolio`, `POST /compare-stocks`, `POST /agent-debug`. (Note: condensed to a unified `/api/analyze` handling all intents dynamically)
- [x] **Server Initialization (`backend/main.py`)**:
  - Setup FastAPI app and integrate it to execute the `langgraph_pipeline`.
  - Implement Server-Sent Events (SSE) or WebSockets to stream agent logs back to the frontend in real-time.

## Phase 6: Frontend (Streamlit UI)
- [x] **User Interface (`frontend/streamlit_app.py`)**:
  - **Layout Constraints**: Implement Sidebar (Portfolio input, Timeframes) and Main Window.
  - **Core Feature - Search/Query**: Add form text input for user commands ("How is Reliance doing?").
  - **Core Feature - Log Streaming**: Build an interface to connect to FastAPI endpoint and display live logs ("technical analysis running..."). (Streamlined via Tabs for explainable AI)
  - **Core Feature - Results Display**: Render the final LLM synthesized recommendation and display relevant financial charts using Streamlit primitives.

## Phase 7: Testing & Verification
- [x] Run isolated tests for tools (`tests/test_tools.py`) ensuring external dependencies map correctly.
- [x] Run module tests for agents to guarantee structurally accurate string outputs.
- [x] Test the FastAPI API via cURL or docs page.
- [x] Review full end-to-end functionality via Streamlit.

## Phase 8: V3 Upgrades (Databases, React, MCP)
- [ ] **CLI Manager Script (`Makefile`)**:
  - Create a standard Unix `Makefile` to boot the application, replacing the need to keep multiple terminals open.
  - Commands should include `make run` (starts FastAPI + Streamlit concurrently) and `make init-db` (creates the SQLite tables).
- [ ] **Database Integration (SQLite)**:
  - Implement `SQLAlchemy` ORM and define models for `User`, `QueryHistory`, and `AnalysisResult`.
  - Restructure the FastAPI backend to store all final AI outputs into the `market_scholar.db`.
- [ ] **MCP Server (SQLite)**:
  - Create a Model Context Protocol tool that exposes the SQLite database so external AI (like Cursor/Claude) can query Market Scholar's historic research.
- [ ] **Input-to-Output Caching (Memoization)**:
  - Currently, we only cache raw datasets (prices/news). We must also cache the *final* AI generated reports.
  - Add logic in the FastAPI router to detect duplicated User Queries (e.g. "Analyze INFY") and immediately return the mapped `AnalysisResult` from the Database/Cache without ever booting up the LangGraph pipeline, dropping latency to 0.05s.
- [ ] **React Frontend Integration**:
  - Deprecate Streamlit for a `Next.js` or `Vite + React` application.
  - Rebuild the dashboard components using `TailwindCSS` and `TradingView Lightweight Charts`.

## Phase 9: V2 Upgrades (Indian Market Focus)
- [ ] **Interactive Candlestick Charts** (`frontend/streamlit_app.py`):
  - Add `plotly` or `lightweight-charts-python` to `requirements.txt`.
  - Replace the static `st.line_chart` with an interactive Candlestick chart displaying Open, High, Low, Close (OHLC).
  - Add quick-toggle buttons for different Indian market timeframes (1W, 1M, 6M, 1Y).
- [ ] **Financial Metrics KPI Dashboard** (`frontend/streamlit_app.py`):
  - Extract the core numeric data (PE Ratio, Debt, Margins) out of the Fundamental Agent's JSON response.
  - Render a clean horizontal row of `st.metric()` cards across the top of the Results screen for instant at-a-glance health checks.
- [ ] **Nifty 50 / Sensex Portfolio Benchmarking** (`agents/portfolio_agent.py` & `tools/yahoo_finance_tool.py`):
  - Add logic to fetch historical performance of `^NSEI` (Nifty 50) and `^BSESN` (Sensex).
  - Calculate the User's Portfolio 1-year returns and automatically plot a comparative benchmark chart against the indices.
- [ ] **Corporate Announcements & Earnings** (`tools/news_tool.py` or new `corporate_tool.py`):
  - Enhance the data fetcher to scrape localized financial websites (e.g., Screener, Moneycontrol, or NSE public feeds) for the latest quarterly earnings reports and official announcements for the requested ticker.
  - Pass this hard data to the Fundamental Agent.
- [ ] **FII / DII Institutional Activity Tracker**:
  - Implement a daily/weekly tracking tool to fetch Foreign and Domestic Institutional flow data for the broader Indian market or specific stocks.
  - Supply this institutional momentum data to the Technical/Aggregator agents.

## Phase 10: Deployment (Option 1 - Decoupled Architecture)
- [ ] **Step 1: Deploy Backend API to Render (Free)**
  - Go to Render.com and create a new **Web Service** tied to the GitHub repository.
  - Set the Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port 10000`
  - Add `GEMINI_API_KEY` to the Render Environment Variables.
  - Deploy and copy the resulting public API URL (e.g., `https://market-scholar-api.onrender.com`).
- [ ] **Step 2: Update Frontend Environment Variables**
  - Modify `frontend/streamlit_app.py` line 8 to accept dynamic API endpoints: `API_URL = os.environ.get("API_URL", "http://localhost:8000/api/analyze")`
- [ ] **Step 3: Deploy Frontend to Streamlit Community Cloud (Free)**
  - Go to share.streamlit.io and create a new app tied to the GitHub repository.
  - Set the Main file path to: `frontend/streamlit_app.py`.
  - In the Streamlit Advanced Settings -> Secrets, add the Render API URL: `API_URL = "https://market-scholar-api.onrender.com/api/analyze"`
  - Deploy the Streamlit application.
