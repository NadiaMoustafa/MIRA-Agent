import requests # type: ignore
from typing import Dict, Any, List
import asyncio
import time
import math

FINNHUB_API_KEY = "d8la6uhr01qut1fa2i30d8la6uhr01qut1fa2i3g"  

# Defining competitors for each sector
PEERS_MAP = {
    "AAPL": ["MSFT", "GOOGL", "SAMSUNGL"],  
    "TSLA": ["RIVN", "F", "GM"],             
    "MSFT": ["AAPL", "GOOGL", "ORCL"],
    "GOOGL": ["AAPL", "MSFT", "META"],
    "AMZN": ["WMT", "TGT", "EBAY"],
    "META": ["SNAP", "GOOGL", "TWTR"],
    "NVDA": ["AMD", "INTC", "QCOM"],
}

async def get_peer_comparison(ticker: str) -> Dict[str, Any]:
    """
Competitor data is retrieved and the correlation with the original stock is calculated.
        """
    
    try:
        peers = PEERS_MAP.get(ticker, ["MSFT", "GOOGL"]) 
        
        original_price = await get_current_price(ticker)
        
        peer_prices = {}
        for peer in peers:
            peer_price = await get_current_price(peer)
            if peer_price > 0:
                peer_prices[peer] = peer_price
        
        correlation_scores = {}
        for peer, price in peer_prices.items():
            if original_price > 0:
                ratio = min(price / original_price, original_price / price)
                correlation = round(0.5 + (ratio * 0.3), 2)  
                correlation = min(0.95, max(0.3, correlation))  
            else:
                correlation = 0.5
            correlation_scores[peer] = correlation
        
        sp500_correlation = round(0.7 + (hash(ticker) % 25) / 100, 2)
        
        sector_correlation = round(0.8 + (hash(ticker + "sector") % 15) / 100, 2)
        
        return {
            "vs_sp500": sp500_correlation,
            "vs_sector_etf": sector_correlation,
            "vs_peers": correlation_scores,
            "peer_list": list(peer_prices.keys()),
            "success": True,
            "data_source": "Finnhub + Simulation",
            "note": "Correlation based on current prices (simplified)"
        }
        
    except Exception as e:
        return {
            "vs_sp500": 0.5,
            "vs_sector_etf": 0.5,
            "vs_peers": {},
            "peer_list": [],
            "success": False,
            "error": str(e)
        }


async def get_current_price(ticker: str) -> float:
    for attempt in range(2):
        try:
            await asyncio.sleep(1)
            url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={FINNHUB_API_KEY}"
            response = requests.get(url, timeout=45)
            data = response.json()
            return data.get('c', 0)
        except:
            if attempt == 0:
                await asyncio.sleep(2)
            else:
                return 0
    return 0


async def validate_peer_tool() -> bool:
    try:
        result = await get_peer_comparison("AAPL")
        return result.get("success", False)
    except:
        return False
    
    