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
