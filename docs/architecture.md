1. System Overview
Goal

Build a Multi-Agent Stock Market Analyst capable of answering:

Single Stock Analysis

"How is Reliance doing?"

Portfolio Analysis

"How is my portfolio performing?"

Stock Comparison & Recommendation

"Compare Tata Motors vs Mahindra and which should I buy?"

2. High Level Architecture
                +----------------------+
                |      Streamlit UI    |
                |  (User Interaction)  |
                +----------+-----------+
                           |
                           v
                  +----------------+
                  |   FastAPI API  |
                  |  Query Router  |
                  +--------+-------+
                           |
                           v
                  +-------------------+
                  |  Master Agent     |
                  |  (LangGraph)      |
                  |  Orchestrator     |
                  +---------+---------+
                            |
        ------------------------------------------------
        |                 |               |             |
        v                 v               v             v
+---------------+  +--------------+  +-------------+  +----------------+
| Fundamental   |  | Technical    |  | Sentiment   |  | Portfolio      |
| Analyst Agent |  | Analyst      |  | Analyst     |  | Analyzer       |
+-------+-------+  +------+-------+  +------+------ +  +-------+--------+
        |                 |               |                  |
        v                 v               v                  v
 +-------------+   +-------------+  +-------------+   +---------------+
 | Yahoo       |   | Yahoo       |  | DuckDuckGo  |   | Yahoo Finance |
 | Finance API |   | Finance API |  | Search API  |   | Market Data   |
 +-------------+   +-------------+  +-------------+   +---------------+

                         |
                         v
                +-------------------+
                |  Result Synthesizer|
                |  (LLM reasoning)   |
                +-------------------+
3. Core Components
3.1 Streamlit UI

Purpose:

User interaction

Portfolio input

Visualization

Streaming agent responses

Features:

Stock query input

Portfolio input

Comparison interface

Charts

Agent explanation logs

Example UI elements:

Sidebar:
- Portfolio Input
- Select Timeframe

Main Window:
- Query box
- Agent reasoning logs
- Final recommendation
- Charts
4. Backend (FastAPI)

Acts as API gateway.

Endpoints:

POST /analyze-stock
POST /analyze-portfolio
POST /compare-stocks
POST /agent-debug

Example request:

{
 "query": "How is Reliance doing?"
}

FastAPI responsibilities:

validate request

call LangGraph pipeline

stream results

return structured response

5. LangGraph Agent Orchestration

LangGraph manages the multi-agent workflow.

Graph Structure
User Query
   |
   v
Intent Classifier
   |
   v
Master Orchestrator
   |
   |---- Fundamental Agent
   |---- Technical Agent
   |---- Sentiment Agent
   |---- Portfolio Agent (optional)
   |
   v
Aggregator Node
   |
   v
Final Report Generator
6. Master Agent (Orchestrator)

Role:

Understand query

Select which agents to activate

Run agents in parallel

Aggregate outputs

Example logic:

IF query contains "portfolio"
   -> run portfolio + sentiment + technical

IF query contains "compare"
   -> run all agents for both stocks

IF query contains "how is stock"
   -> run fundamental + technical + sentiment

Pseudo code:

if intent == "single_stock":
    run_parallel([fundamental, technical, sentiment])

if intent == "portfolio":
    run_parallel([portfolio_agent])

if intent == "comparison":
    run_parallel([
        fundamental(stockA),
        fundamental(stockB),
        technical(stockA),
        technical(stockB),
        sentiment(stockA),
        sentiment(stockB)
    ])
7. Agent Designs
7.1 Fundamental Analyst Agent

Purpose:
Analyze company financial health.

Data source:

Yahoo Finance

Metrics:

Revenue
EPS
PE ratio
Market cap
Debt
Free cash flow
ROE
Profit margin

Example output:

Reliance Fundamentals:

Revenue growth: +12%
PE Ratio: 24
Debt/Equity: 0.4
Net Profit Growth: 8%

Conclusion:
Financially stable large cap stock.
Moderate growth potential.
7.2 Technical Analyst Agent

Purpose:
Analyze price patterns and indicators.

Data source:

Yahoo Finance historical data

Indicators:

Moving averages
RSI
MACD
Volume trend
Support / resistance
Trend direction

Example output:

Trend: Bullish
RSI: 62 (not overbought)
MACD: Positive crossover
Support: ₹2650
Resistance: ₹2900

Signal:
Moderate buy momentum
7.3 Sentiment Analyst Agent

Purpose:
Analyze market sentiment from news.

Tools:

DuckDuckGo Search

News scraping

Steps:

1 Search news: "Reliance stock news"
2 Extract headlines
3 Sentiment classification
4 Aggregate sentiment score

Output example:

News Sentiment Score: +0.62

Positive:
- Reliance retail expansion

Negative:
- telecom tariff concerns

Overall sentiment: Slightly bullish
7.4 Portfolio Analyzer Agent

Input:

[Tata Motors, Infosys, M&M]

Tasks:

Fetch stock prices
Calculate returns
Calculate volatility
Compute diversification
Evaluate sector exposure

Output example:

Portfolio Performance

Return (1Y): 14%
Volatility: Medium
Top performer: Tata Motors
Weakest: Infosys

Sector risk:
High exposure to auto sector
8. Aggregator Agent

Combines outputs of all agents.

Example input:

Fundamental: Bullish
Technical: Neutral
Sentiment: Bullish

Final synthesis:

Reliance Outlook:

Fundamental strength: Strong
Technical trend: Neutral
Market sentiment: Positive

Recommendation:
Long term hold
Short term wait for breakout above ₹2900
9. Data Layer
/data
   price_cache
   news_cache

Caching avoids excessive API calls.

10. Project Folder Structure
market-analyst-ai/

backend/
    main.py
    router.py
    langgraph_pipeline.py

agents/
    fundamental_agent.py
    technical_agent.py
    sentiment_agent.py
    portfolio_agent.py
    master_agent.py

tools/
    yahoo_finance_tool.py
    duckduckgo_tool.py

services/
    data_fetcher.py
    indicator_calculator.py
    sentiment_model.py

frontend/
    streamlit_app.py

models/
    prompts/
    templates/

config/
    settings.py

tests/
11. Data Flow Example
Query
Compare Tata Motors and Mahindra

Flow:

User -> Streamlit
      -> FastAPI
      -> LangGraph

LangGraph:
Master agent

Parallel execution:
   fundamental(Tata)
   fundamental(Mahindra)
   technical(Tata)
   technical(Mahindra)
   sentiment(Tata)
   sentiment(Mahindra)

Aggregator
Final report
Return to UI
12. Recommended Models

LLM usage:

Agent reasoning → GPT-4o / GPT-4.1
Sentiment classification → small transformer

Prompt templates stored in:

/prompts/
   fundamental_prompt.txt
   technical_prompt.txt
   sentiment_prompt.txt
13. Key Features
Parallel Agent Execution

LangGraph supports:

map-reduce style agent execution
Streaming Responses

Stream results to UI:

agent started
technical analysis running
sentiment analysis running
Explainable AI

Show agent reasoning logs.

14. Optional Advanced Features

Future improvements:

Add Quant Agent
Factor models
Sharpe ratio
Alpha
Beta
Add Risk Agent
Value at Risk
Drawdown analysis
Add Earnings Call Analyzer
Transcribe earnings calls
LLM summarization