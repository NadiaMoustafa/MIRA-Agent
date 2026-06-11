from fastapi import FastAPI, BackgroundTasks, HTTPException # type: ignore
from datetime import datetime
import uuid
from typing import Dict

from app.models.schemas import AnalyzeRequest, JobStatus, AnalysisReport
from app.services.monitor import start_monitoring, get_monitoring_status, stop_monitoring
from app.agent.core import MIRAAgent

app = FastAPI(title="M.I.R.A. Investment Agent", version="1.0.0")

jobs: Dict[str, dict] = {}

# Create M.I.R.A. agent instance
agent = MIRAAgent()

# ==================== Helper Functions ====================

def extract_ticker_from_query(query: str) -> str:
    """Extract stock ticker from user query"""
    tickers = ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN", "META", "NVDA"]
    query_upper = query.upper()
    for ticker in tickers:
        if ticker in query_upper:
            return ticker
    return "AAPL"  # Default fallback

# ==================== API Endpoints ====================

@app.post("/analyze")
async def analyze(request: AnalyzeRequest, background_tasks: BackgroundTasks):
    
    job_id = str(uuid.uuid4())
    
    jobs[job_id] = {
        "job_id": job_id,
        "status": "pending",                      
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "result": None,
        "error": None
    }
    
    background_tasks.add_task(run_analysis, job_id, request.query)
    
    return {"job_id": job_id, "status": "pending"}


@app.get("/status/{job_id}")
async def get_status(job_id: str):
    
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return jobs[job_id]


@app.get("/jobs")
async def get_all_jobs():
    return {"total_jobs": len(jobs), "jobs": jobs}


async def run_analysis(job_id: str, query: str):
    """Run M.I.R.A. agent analysis with real data"""
    
    try:
        jobs[job_id]["status"] = "running"
        jobs[job_id]["updated_at"] = datetime.now().isoformat()
        
        # Extract ticker from user query
        ticker = extract_ticker_from_query(query)
        
        # Run the real M.I.R.A. agent with real data from Finnhub and NewsAPI
        result = await agent.analyze(query, ticker)
        
        jobs[job_id]["result"] = result
        jobs[job_id]["status"] = "completed"
        
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
    
    finally:
        jobs[job_id]["updated_at"] = datetime.now().isoformat()


@app.get("/")
@app.get("/health")
async def health_check():
    return {"status": "alive", "service": "M.I.R.A.", "timestamp": datetime.now().isoformat()}


# ==================== Monitoring Endpoints ====================

@app.post("/monitor_start")
async def monitor_start(ticker: str, interval_hours: int = 24):
    result = start_monitoring(ticker.upper(), interval_hours)
    return result

@app.get("/monitor_status/{ticker}")
async def monitor_status(ticker: str):
    return get_monitoring_status(ticker.upper())

@app.post("/monitor_stop/{ticker}")
async def monitor_stop(ticker: str):
    return stop_monitoring(ticker.upper())

