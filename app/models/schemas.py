from pydantic import BaseModel # type: ignore
from typing import List, Optional
from datetime import datetime

# 1. shape of market data will be : (Market Snapshot)
class MarketSnapshot(BaseModel):
    price: float                          # Current Price
    daily_change: float                   # Daily Change (USD)
    daily_change_percent: float           # Daily Change (Percentage)
    volume: int                           # Trading Volume
    market_cap: int                       # Market Capitalization
    pe_ratio: Optional[float]             # Price-to-Earnings Ratio (may not be available)
    week_52_high: float                   # 52-Week High
    week_52_low: float                    # 52-Week Low
    last_two_quarterly_revenues: List[float]  # Last 2 Quarters Revenue

# 2. shape of analysis of correlation will be (Correlation Analysis)
class CorrelationAnalysis(BaseModel):
    vs_sp500: float                       # Correlation with the S&P 500 Index
    vs_sector_etf: float                  # Correlation with a Sector Index Fund
    vs_peers: dict                        # Correlation with Competitors

# 3. shape of the final report (Analysis Report)
class AnalysisReport(BaseModel):
    company_ticker: str                   # Stock symbol (e.g., TSLA)
    company_name: str                     # Full company name
    analysis_summary: str                 # Analysis summary (one paragraph)
    sentiment_score: float                # Sentiment score between -1 and 1
    market_snapshot: MarketSnapshot       # Market data
    correlation_analysis: CorrelationAnalysis  # Correlation analysis
    key_findings: List[str]               # Top 3 key findings
    tools_used: List[str]                 # Tools used in order
    citation_sources: List[str]           # News sources
    generated_at: datetime                # Analysis completion time

# 4. the shape of user' request
class AnalyzeRequest(BaseModel):
    query: str                            # User question (example: "Analyze Tesla")

# 5. Task Status Format (for tracking progress)
class JobStatus(BaseModel):
    job_id: str                           # Job ID 
    status: str                           # pending, running, completed, failed
    result: Optional[AnalysisReport] = None  # Result (when completed)
    error: Optional[str] = None           # If there is an error
    created_at: datetime                  # Task start time
    updated_at: datetime                  # Last time updated



    