import asyncio
from app.agent.core import MIRAAgent

async def test():
    print("=" * 60)
    print("...test the MIRA...")
    print("=" * 60)
    
    agent = MIRAAgent()
    
    query = "Analyze Tesla, Inc. (TSLA)"
    ticker = "AAPL"  
    
    print(f"\n Query: {query}")
    print(f"Symbol: {ticker}")
    
    result = await agent.analyze(query, ticker)
    
    if "error" in result:
        print(f"\n Error: {result['error']}")
    else:
        print("\n" + "=" * 60)
        print("final report")
        print("=" * 60)
        print(f"\n company: {result['company_name']} ({result['company_ticker']})")
        print(f" summary: {result['analysis_summary']}")
        print(f" Sentiment degree: {result['sentiment_score']}")
        print(f"\n price: ${result['market_snapshot']['price']}")
        print(f" change: {result['market_snapshot']['daily_change_percent']}%")
        
        print(f"\n main points : ")
        for finding in result['key_findings']:
            print(f"   - {finding}")
        
        print(f"\n  used tools : {', '.join(result['tools_used'])}")
        print(f" Reflection triggered: {result.get('reflection_triggered', False)}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    asyncio.run(test())


    
    