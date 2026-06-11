import asyncio
from app.tools.news_sentiment import get_news_sentiment

async def test():
    print("=" * 60)
    print("Testing the news tool and analyzing sentiment")
    print("=" * 60)
    
    print("\n collect Apple data ...")
    result = await get_news_sentiment("Apple", "AAPL")
    
    if result.get("success"):
        print(f"\n It was fetched and analyzed {result['total_articles']} articles")
        print(f"\n sentiment analysis :")
        print(f"   - positive: {result['distribution']['positive']}")
        print(f"   - negative: {result['distribution']['negative']}")
        print(f"   - neutral: {result['distribution']['neutral']}")
        print(f"\n sentiment_score: {result['sentiment_score']} ( -1 - 1)")
        print(f" data source : {result['data_source']}")
        
        print(f"\n last updates :")
        for i, article in enumerate(result['articles'][:3], 1):
            print(f"   {i}. {article['title'][:80]}...")
            print(f"      sentiment: {article['sentiment']}")
    else:
        print(f"\n Error: {result.get('error_note', 'Unknown error')}")
        print(f" data sources : {result['data_source']}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    asyncio.run(test())



