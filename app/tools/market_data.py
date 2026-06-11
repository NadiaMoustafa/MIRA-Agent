import requests # type: ignore
from typing import Dict, Any
import time
import asyncio
from app.config import config  

async def get_market_data(ticker: str) -> Dict[str, Any]:
    """
    Real market data from Finnhub 

    """
    
    # try 3 times
    for attempt in range(3):
        try:
            time.sleep(2) 

            quote_url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={config.FINNHUB_API_KEY}"
            quote_response = requests.get(quote_url, timeout=60) 
            quote = quote_response.json()
            
            profile_url = f"https://finnhub.io/api/v1/stock/profile2?symbol={ticker}&token={config.FINNHUB_API_KEY}"
            profile_response = requests.get(profile_url, timeout=60)
            profile = profile_response.json()
            
            price = quote.get('c', 0)
            
            if price > 0:
                return {
                    "symbol": ticker,
                    "company_name": profile.get('name', ticker),
                    "price": price,
                    "daily_change": quote.get('d', 0),
                    "daily_change_percent": quote.get('dp', 0),
                    "volume": quote.get('v', 0),
                    "market_cap": profile.get('marketCapitalization', 0),
                    "pe_ratio": None,
                    "week_52_high": 0,
                    "week_52_low": 0,
                    "sector": profile.get('finnhubIndustry', 'Unknown'),
                    "industry": profile.get('finnhubIndustry', 'Unknown'),
                    "last_two_quarterly_revenues": [],
                    "success": True,
                    "data_source": "Finnhub (real)"
                }
            else:
                return {
                    "symbol": ticker,
                    "success": False,
                    "error": f"No price data for {ticker}"
                }
                
        except requests.exceptions.Timeout:
            if attempt < 2: 
                print(f"    Finnhub timeout, retrying... (attempt {attempt + 2}/3)")
                await asyncio.sleep(3) 
                continue
            else:
                return {
                    "symbol": ticker,
                    "success": False,
                    "error": f"Finnhub timeout after 3 attempts"
                }
        except Exception as e:
            if attempt < 2:
                print(f"    Finnhub error, retrying... ({str(e)[:50]})")
                await asyncio.sleep(3)
                continue
            else:
                return {
                    "symbol": ticker,
                    "success": False,
                    "error": f"Finnhub error: {str(e)}"
                }
    
    return {
        "symbol": ticker,
        "success": False,
        "error": "All attempts failed"
    }


async def validate_ticker(ticker: str) -> bool:
    """Validate if ticker exists"""
    try:
        url = f"https://finnhub.io/api/v1/stock/profile2?symbol={ticker}&token={config.FINNHUB_API_KEY}"
        response = requests.get(url, timeout=30)
        data = response.json()
        return data.get('name') is not None
    except:
        return False
    



