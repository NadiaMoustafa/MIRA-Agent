import asyncio
from app.tools.market_data import get_market_data

async def test():
    print("=" * 50)
    print(" Testing real market data - Finnhub ")
    print("=" * 50)
    
    print("\n Fetching AAPL data...")
    result = await get_market_data("AAPL")
    
    if result.get("success"):
        print(f"\n  fetched data successfully  !")
        print(f" company name : {result['company_name']}")
        print(f"  the price: ${result['price']}")
        print(f"  daily change: {result['daily_change_percent']}%")
        print(f" volume: {result['volume']:,}")
        print(f"  market value: ${result['market_cap']:,}")
        print(f" sector: {result['sector']}")
        print(f"  data source : {result['data_source']}")
    else:
        print(f"\n Error: {result.get('error')}")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    asyncio.run(test())



