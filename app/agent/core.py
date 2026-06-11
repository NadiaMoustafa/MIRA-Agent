from typing import Dict, Any, List
from datetime import datetime
import asyncio
from ..tools.market_data import get_market_data
from ..tools.news_sentiment import get_news_sentiment
from ..tools.peer_correlation import get_peer_comparison
from ..models.schemas import AnalysisReport, MarketSnapshot, CorrelationAnalysis

class MIRAAgent:
    def __init__(self):
        self.tools_called = []
        self.tool_count = 0
        self.reflection_count = 0
    
    async def analyze(self, query: str, ticker: str) -> Dict[str, Any]:
        """
        Implementing the MIRA 
        """
        
        print(f" M.I.R.A. Agent starting analysis for {ticker}")
        print(f" User query: {query}")
        
        # 1. Market data Tool
        print("\n Tool 1: Fetching market data...")
        market_data = await get_market_data(ticker)
        self.tools_called.append("market_data")
        
        if not market_data.get("success"):
            return {
                "error": f"Failed to get market data: {market_data.get('error')}",
                "tools_used": self.tools_called
            }
        
        company_name = market_data.get("company_name", ticker)
        print(f"    Got data for {company_name} at ${market_data.get('price', 0)}")
        
        # 2. news and sementit analysis tool
        print("\n Tool 2: Fetching news and analyzing sentiment...")
        news_data = await get_news_sentiment(company_name, ticker)
        self.tools_called.append("news_sentiment")
        print(f"    Sentiment score: {news_data.get('sentiment_score', 0)}")
        
        # 3. peer comparison tool
        print("\n Tool 3: Fetching peer comparison...")
        peer_data = await get_peer_comparison(ticker)
        self.tools_called.append("peer_correlation")
        print(f"    Found {len(peer_data.get('vs_peers', {}))} peers")
        
        # 4. Reflection: Analyzing data quality
        print("\n Reflection: Analyzing data quality...")
        reflection = await self._reflect(market_data, news_data, peer_data)
        
        if reflection["needs_more_research"]:
            print(f"    Reflection triggered: {reflection['missing_areas']}")
            self.reflection_count += 1
        else:
            print("    Data quality is sufficient")
        
        # 5. the final report
        print("\n Synthesizing final report...")
        report = await self._synthesize(query, market_data, news_data, peer_data, reflection)
        
        return report
    
    async def _reflect(self, market_data: Dict, news_data: Dict, peer_data: Dict) -> Dict[str, Any]:
        """Reflection loop - Reflection: Analyzing data quality"""
        
        needs_more = False
        missing_areas = []
        
        # old news or less?
        if news_data.get("total_articles", 0) < 3:
            needs_more = True
            missing_areas.append("no.of news is less than 3")
        
        # Condition 2: Feelings are very neutral
        sentiment = news_data.get("sentiment_score", 0)
        if -0.2 < sentiment < 0.2:
            needs_more = True
            missing_areas.append("Sentiment is neutral, needs more context")
        
        # Condition 3: Very high correlation with the sector
        sector_corr = peer_data.get("vs_sector_etf", 0)
        if sector_corr > 0.95:
            needs_more = True
            missing_areas.append("Need deeper comparison")
        
        # price = 0 ?!
        if market_data.get("price", 0) == 0:
            needs_more = True
            missing_areas.append("price is not available")
        
        return {
            "needs_more_research": needs_more,
            "missing_areas": missing_areas,
            "critique": self._generate_critique(market_data, news_data)
        }
    
    def _generate_critique(self, market_data: Dict, news_data: Dict) -> str:
        """generation the analysis"""
        sentiment = news_data.get("sentiment_score", 0)
        price = market_data.get("price", 0)
        
        if sentiment > 0.5:
            return f" the company is  in positive situation (sentiment={sentiment})، Good News"
        elif sentiment > 0.2:
            return f" the company is  in positive situation (sentiment={sentiment})، but we need more data to make sure"
        elif sentiment < -0.3:
            return f" the company has challenges (sentiment={sentiment})، bad news "
        else:
            return f" equal data (sentiment={sentiment})، need pay attention closly"
    
    async def _synthesize(self, query: str, market_data: Dict, news_data: Dict, 
                          peer_data: Dict, reflection: Dict) -> Dict[str, Any]:
        """the final report"""
        
        #  the Data
        sentiment = news_data.get("sentiment_score", 0)
        price = market_data.get("price", 0)
        change_percent = market_data.get("daily_change_percent", 0)
        company_name = market_data.get("company_name", "Unknown")
        ticker = market_data.get("symbol", "Unknown")
        
        # the sammary
        if sentiment > 0.5:
            summary = f"{company_name} ({ticker}) In a strongly positive position. The price is at ${price} with change {change_percent}%. The news is positive with a high degree of emotion. {sentiment}."
        elif sentiment > 0:
            summary = f"{company_name} ({ticker}) In a positive situation. Price ${price} with change {change_percent}%. The news tends to be positive. (sentiment={sentiment})."
        elif sentiment > -0.3:
            summary = f"{company_name} ({ticker}) In a neutral position. Price ${price}. The news is balanced, we need to follow up."
        else:
            summary = f"{company_name} ({ticker}) It faces challenges. Price ${price}. bad news (sentiment={sentiment})."
        
        # if reflection ?
        if reflection["needs_more_research"]:
            summary += f" note: {', '.join(reflection['missing_areas'])}."
        
        # generate the main points
        key_findings = [
            f"Share price: ${price} (change {change_percent}%)",
            f"Emotion analysis : {sentiment} (range -1 to 1)",
            f"correlation with S&P 500: {peer_data.get('vs_sp500', 0)}"
        ]
        
        # if there is a reflection
        if reflection["needs_more_research"]:
            key_findings.append(f"warning: {reflection['critique'][:100]}")
        
        return {
            "company_ticker": ticker,
            "company_name": company_name,
            "analysis_summary": summary,
            "sentiment_score": sentiment,
            "market_snapshot": {
                "price": price,
                "daily_change": market_data.get("daily_change", 0),
                "daily_change_percent": change_percent,
                "volume": market_data.get("volume", 0),
                "market_cap": market_data.get("market_cap", 0),
                "pe_ratio": market_data.get("pe_ratio"),
                "week_52_high": market_data.get("week_52_high", 0),
                "week_52_low": market_data.get("week_52_low", 0),
                "last_two_quarterly_revenues": market_data.get("last_two_quarterly_revenues", [])
            },
            "correlation_analysis": {
                "vs_sp500": peer_data.get("vs_sp500", 0.5),
                "vs_sector_etf": peer_data.get("vs_sector_etf", 0.5),
                "vs_peers": peer_data.get("vs_peers", {})
            },
            "key_findings": key_findings,
            "tools_used": self.tools_called,
            "citation_sources": [a.get("url") for a in news_data.get("articles", []) if a.get("url")],
            "generated_at": datetime.now().isoformat(),
            "reflection_triggered": reflection["needs_more_research"],
            "reflection_count": self.reflection_count
        }
    
    
