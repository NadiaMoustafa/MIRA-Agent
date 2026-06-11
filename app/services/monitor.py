import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any
from apscheduler.schedulers.background import BackgroundScheduler # type: ignore
from ..agent.core import MIRAAgent

# save the share status
monitoring_states: Dict[str, dict] = {}

# the agent
agent = MIRAAgent()

def start_monitoring(ticker: str, interval_hours: int = 24):
    """ start monitor specfic share """
    
    if ticker not in monitoring_states:
        monitoring_states[ticker] = {
            "ticker": ticker,
            "last_run": None,
            "last_price": None,
            "last_volume": None,
            "last_article_ids": [],
            "alerts": [],
            "active": True
        }
    
    # scheduling ..
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=lambda: check_and_analyze(ticker),
        trigger="interval",
        hours=interval_hours,
        id=f"monitor_{ticker}"
    )
    scheduler.start()
    
    return {"status": "started", "ticker": ticker, "interval_hours": interval_hours}


async def check_and_analyze(ticker: str):
    """look at the conditions"""
    
    print(f" Checking {ticker} for triggers...")
    
    # collect the data
    from ..tools.market_data import get_market_data
    from ..tools.news_sentiment import get_news_sentiment
    
    market_data = await get_market_data(ticker)
    news_data = await get_news_sentiment(ticker, ticker)
    
    state = monitoring_states.get(ticker, {})
    triggers = []
    
    # 1 : 5 pages
    current_article_ids = [a.get('url') for a in news_data.get('articles', [])]
    last_article_ids = state.get('last_article_ids', [])
    new_articles = [aid for aid in current_article_ids if aid not in last_article_ids]
    
    if len(new_articles) >= 5:
        triggers.append(f"{len(new_articles)} new articles published")
    
    # Condition 2: The price changed by more than 2 standard deviations (simulated)
    last_price = state.get('last_price')
    current_price = market_data.get('price', 0)
    
    if last_price and current_price:
        change_percent = abs((current_price - last_price) / last_price * 100)
        if change_percent > 5:  # Simplification: A 5% change is considered significant.
            triggers.append(f"Price changed by {change_percent:.1f}%")
    
    # Condition 3: Trading volume doubled (simulated)
    last_volume = state.get('last_volume')
    current_volume = market_data.get('volume', 0)
    
    if last_volume and current_volume > last_volume * 2:
        triggers.append(f"Volume spiked to {current_volume:,}")
    
    # if conditions are true? start ..
    if triggers:
        print(f" Triggers found for {ticker}: {triggers}")
        
        # M.I.R.A...
        result = await agent.analyze(f"Monitor alert for {ticker}", ticker)
        
        # save the alert 
        alert = {
            "timestamp": datetime.now().isoformat(),
            "triggers": triggers,
            "analysis": result
        }
        
        if "alerts" not in state:
            state["alerts"] = []
        state["alerts"].append(alert)
        
        print(f" Alert generated for {ticker}")
    else:
        print(f" No triggers for {ticker}")
    
    # update the status 
    state["last_run"] = datetime.now().isoformat()
    state["last_price"] = current_price
    state["last_volume"] = current_volume
    state["last_article_ids"] = current_article_ids
    
    monitoring_states[ticker] = state


def get_monitoring_status(ticker: str) -> Dict:
    """Bring the monitoring status to a specific stock"""
    state = monitoring_states.get(ticker, {})
    return {
        "ticker": ticker,
        "is_monitored": ticker in monitoring_states,
        "last_run": state.get("last_run"),
        "alert_count": len(state.get("alerts", [])),
        "alerts": state.get("alerts", [])[-5:]  
    }


def stop_monitoring(ticker: str) -> Dict:
    """stop monitoring"""
    if ticker in monitoring_states:
        monitoring_states[ticker]["active"] = False
        return {"status": "stopped", "ticker": ticker}
    return {"status": "not_found", "ticker": ticker}


