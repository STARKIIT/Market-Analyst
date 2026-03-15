from typing import Dict, TypedDict, Any, List
from langgraph.graph import StateGraph, START, END
from agents.master_agent import run_master_agent
from agents.fundamental_agent import run_fundamental_agent
from agents.technical_agent import run_technical_agent
from agents.sentiment_agent import run_sentiment_agent
from agents.portfolio_agent import run_portfolio_agent
from agents.aggregator_agent import run_aggregator_agent
from utils.logger import get_logger

logger = get_logger(__name__)

class GraphState(TypedDict):
    query: str
    intent: str
    tickers: List[str]
    fundamental_report: str
    technical_report: str
    sentiment_report: str
    portfolio_report: str
    final_report: str

def route_query(state: GraphState):
    logger.info("LangGraph Node: Routing Query")
    master_response = run_master_agent(state["query"])
    return {
        "intent": master_response.intent,
        "tickers": master_response.tickers
    }

def fundamental_node(state: GraphState):
    logger.info("LangGraph Node: Fundamental")
    if not state.get("tickers"):
        return {"fundamental_report": "No ticker provided."}
        
    ticker = state["tickers"][0] # simplified for single stock
    report = run_fundamental_agent(ticker)
    return {"fundamental_report": report}

def technical_node(state: GraphState):
    logger.info("LangGraph Node: Technical")
    if not state.get("tickers"):
        return {"technical_report": "No ticker provided."}
    ticker = state["tickers"][0]
    report = run_technical_agent(ticker)
    return {"technical_report": report}
    
def sentiment_node(state: GraphState):
    logger.info("LangGraph Node: Sentiment")
    if not state.get("tickers"):
        return {"sentiment_report": "No ticker provided."}
    ticker = state["tickers"][0]
    report = run_sentiment_agent(ticker)
    return {"sentiment_report": report}

def portfolio_node(state: GraphState):
    logger.info("LangGraph Node: Portfolio")
    tickers = state.get("tickers", [])
    report = run_portfolio_agent(tickers)
    return {"portfolio_report": report}

def aggregator_node(state: GraphState):
    logger.info("LangGraph Node: Aggregator")
    if not state.get("tickers"):
        return {"final_report": "No valid tickers found to aggregate."}
        
    ticker = state["tickers"][0]
    report = run_aggregator_agent(
        ticker=ticker,
        fundamental_report=state.get("fundamental_report", ""),
        technical_report=state.get("technical_report", ""),
        sentiment_report=state.get("sentiment_report", "")
    )
    return {"final_report": report}

# Define workflow paths
def should_continue(state: GraphState):
    intent = state.get("intent", "unknown")
    if intent == "single_stock":
        return ["fundamental", "technical", "sentiment"]
    elif intent == "portfolio":
        return ["portfolio"]
    elif intent == "comparison":
        # Simplified: Currently routing same as single stock conceptually in nodes
        return ["fundamental", "technical", "sentiment"]
    return END

# Build Graph
builder = StateGraph(GraphState)

builder.add_node("router", route_query)
builder.add_node("fundamental", fundamental_node)
builder.add_node("technical", technical_node)
builder.add_node("sentiment", sentiment_node)
builder.add_node("portfolio", portfolio_node)
builder.add_node("aggregator", aggregator_node)

builder.add_edge(START, "router")
builder.add_conditional_edges("router", should_continue, ["fundamental", "technical", "sentiment", "portfolio", END])
builder.add_edge("fundamental", "aggregator")
builder.add_edge("technical", "aggregator")
builder.add_edge("sentiment", "aggregator")
builder.add_edge("portfolio", END)
builder.add_edge("aggregator", END)

# Compile
graph = builder.compile()

def run_pipeline(query: str) -> Dict[str, Any]:
    logger.info(f"Starting pipeline execution for query: '{query}'")
    initial_state = {
        "query": query,
        "intent": "",
        "tickers": [],
        "fundamental_report": "",
        "technical_report": "",
        "sentiment_report": "",
        "portfolio_report": "",
        "final_report": ""
    }
    
    result = graph.invoke(initial_state)
    logger.info("Pipeline execution complete")
    return result
