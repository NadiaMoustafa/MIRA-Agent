import requests # type: ignore
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer # type: ignore
from typing import Dict, Any, List
import time
from app.config import config


analyzer = SentimentIntensityAnalyzer()

async def get_news_sentiment(company_name: str, ticker: str) -> Dict[str, Any]:
    """
   It answers and analyzes the last 5 news items about the company (positive/negative/neutral).

    """
    
    try:
        time.sleep(0.5)
        

        search_query = f'"{ticker}" AND (stock OR shares OR market OR earnings OR revenue)'
        
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": search_query,
            "sortBy": "publishedAt",
            "pageSize": 10,  
            "apiKey": config.NEWS_API_KEY,
            "language": "en"
        }
        
        response = requests.get(url, params=params, timeout=30)
        data = response.json()
        
        if data.get('status') == 'error':
            return generate_mock_news(company_name, data.get('message', 'API error'))
        
        articles = data.get('articles', [])
        
        filtered_articles = []
        for article in articles:
            title = article.get('title', '').lower()
            description = article.get('description', '').lower()
            text = f"{title} {description}"
            
            # make sure that the article is about the company
            company_related = (ticker.lower() in text) or (company_name.lower() in text)
            # make sure the article is financial
            financial_keywords = ['stock', 'share', 'earnings', 'revenue', 'profit', 'market', 'investor', 'quarter']
            is_financial = any(keyword in text for keyword in financial_keywords)
            
            if company_related and is_financial:
                filtered_articles.append(article)
            
            if len(filtered_articles) >= 5:
                break
        
        if len(filtered_articles) < 3:
            filtered_articles = articles[:5]
        
        if not filtered_articles:
            return generate_mock_news(company_name, "No relevant articles found")
        
        sentiment_results = []
        sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
        
        for article in filtered_articles[:5]: 
            title = article.get('title', '')
            description = article.get('description', '')
            text = f"{title} {description}"
            
            scores = analyzer.polarity_scores(text)
            compound = scores['compound']
            
            if compound >= 0.05:
                sentiment = "positive"
            elif compound <= -0.05:
                sentiment = "negative"
            else:
                sentiment = "neutral"
            
            sentiment_counts[sentiment] += 1
            sentiment_results.append({
                "title": title,
                "url": article.get('url'),
                "published_at": article.get('publishedAt'),
                "sentiment": sentiment,
                "score": compound
            })
        
        total = len(sentiment_results)
        if total > 0:
            total_score = (sentiment_counts["positive"] - sentiment_counts["negative"]) / total
        else:
            total_score = 0
        
        return {
            "sentiment_score": round(total_score, 3),
            "distribution": sentiment_counts,
            "articles": sentiment_results,
            "total_articles": total,
            "success": True,
            "data_source": "NewsAPI + VADER"
        }
        
    except Exception as e:
        return generate_mock_news(company_name, str(e))


def generate_mock_news(company_name: str, error_msg: str = "") -> Dict[str, Any]:
    """try data in case the NewsAPI is failed"""
    return {
        "sentiment_score": 0.3,
        "distribution": {"positive": 3, "negative": 1, "neutral": 1},
        "articles": [
            {"title": f"{company_name} reports strong earnings", "sentiment": "positive", "url": "https://example.com/1"},
            {"title": f"{company_name} stock rises on new product", "sentiment": "positive", "url": "https://example.com/2"},
            {"title": f"Analysts upgrade {company_name} stock", "sentiment": "positive", "url": "https://example.com/3"},
            {"title": f"{company_name} faces supply chain issues", "sentiment": "negative", "url": "https://example.com/4"},
            {"title": f"{company_name} announces expansion", "sentiment": "positive", "url": "https://example.com/5"},
        ],
        "total_articles": 5,
        "success": False,
        "data_source": "Mock Data (fallback)",
        "error_note": error_msg if error_msg else "Using mock data"
    }


async def validate_news_api() -> bool:
    """NewsAPI is oK! """
    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {"country": "us", "apiKey": config.NEWS_API_KEY, "pageSize": 1}
        response = requests.get(url, params=params, timeout=10)
        return response.json().get('status') == 'ok'
    except:
        return False
    


