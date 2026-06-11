#  M.I.R.A. - Market Intelligence & Research Agent

An autonomous AI agent that monitors equity markets, performs deep research on publicly traded companies, and generates structured investment analysis reports.

##  Architecture Overview
<img width="722" height="340" alt="image" src="https://github.com/user-attachments/assets/4b1e469c-1359-4a6b-8f45-fcd5938fb013" />

##  Key Features

| Feature | Description |
|---------|-------------|
| **Async REST API** | `POST /analyze` returns `job_id` immediately, `GET /status/{job_id}` for results |
| **3 Real Data Tools** | Market Data (Finnhub), News & Sentiment (NewsAPI + VADER), Peer Correlation |
| **Reflection Loop** | Self-critique and re-planning if data quality is insufficient |
| **Long-Term Monitoring** | `POST /monitor_start` with 3 alert triggers |
| **Structured JSON Output** | Pydantic models with all required fields |
| **Docker Support** | Dockerfile and docker-compose.yml included |

##  Technology Stack

| Component | Technology |
|-----------|------------|
| Web Framework | FastAPI |
| Async Server | Uvicorn |
| Market Data | Finnhub API |
| News | NewsAPI |
| Sentiment Analysis | VADER |
| Container | Docker + docker-compose |


##  Quick Start

### Prerequisites
- Python 3.11+
- Docker (optional)

### 1. Clone the repository
```bash
git clone https://github.com/NadiaMoustafa/MIRA-Agent.git
cd MIRA-Agent
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
pip install -r requirements.txt

### 4. Set up API keys
cp .env.example .env


### And, Edit .env file and add your API keys:
FINNHUB_API_KEY=your_finnhub_key_here

NEWS_API_KEY=your_newsapi_key_here

### 5. Run the server
uvicorn app.main:app --reload

### 6. Test the API
Open http://localhost:8000/docs in your browser


---

### API Endpoints

```markdown
```
##  API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` or `/health` | Health check |
| POST | `/analyze` | Start analysis (returns job_id) |
| GET | `/status/{job_id}` | Get analysis result |
| GET | `/jobs` | List all jobs |
| POST | `/monitor_start` | Start long-term monitoring |
| GET | `/monitor_status/{ticker}` | Check monitoring status |
| POST | `/monitor_stop/{ticker}` | Stop monitoring |

### Example: Analyze a stock

```bash
# Start analysis
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "Analyze Apple Inc. (AAPL)"}'

# Response
{"job_id": "abc-123", "status": "pending"}

# Check status
curl http://localhost:8000/status/abc-123


---

## الجزء 7: Docker

```markdown
##  Docker

### Build and run with Docker
```bash
docker build -t mira-agent .
docker run -p 8000:8000 --env-file .env mira-agent
OR
docker-compose up --build


---

## الجزء 8: The 3 Tools

```markdown
##  The Three Tools

### Tool 1: Market Data (`market_data.py`)
- Fetches real-time stock data from Finnhub API
- Returns: price, daily change, volume, market cap, sector
- Auto-retry on timeout (3 attempts)

### Tool 2: News & Sentiment (`news_sentiment.py`)
- Fetches 5 most recent news articles from NewsAPI
- Analyzes sentiment using VADER (positive/negative/neutral)
- Returns sentiment score from -1 to 1

### Tool 3: Peer Correlation (`peer_correlation.py`)
- Identifies competitors based on sector
- Calculates correlation with S&P 500, sector ETF, and peers
- Returns correlation coefficients

##  Reflection Loop (Self-Correction)

The agent critiques its own data quality and triggers additional research when:

| Condition | Action |
|-----------|--------|
| Less than 3 news articles | Trigger: need more news |
| Sentiment is neutral (-0.2 to 0.2) | Trigger: need more context |
| Sector correlation > 0.95 | Trigger: need deeper peer analysis |
| Price = 0 | Trigger: data unavailable |

##  Long-Term Monitoring

### Start monitoring
```bash
POST /monitor_start?ticker=AAPL&interval_hours=24



