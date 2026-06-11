import asyncio
from app.tools.peer_correlation import get_peer_comparison

async def test():
    print("=" * 60)
    print(" Testing the comparison tool in the sector")
    print("=" * 60)
    
    print("\n Analyzing Apple...")
    result = await get_peer_comparison("AAPL")
    
    if result.get("success"):
        print(f"\n fetched the data of peers")
        print(f"\n correlation with S&P 500: {result['vs_sp500']}")
        print(f"  correlation with sectors : {result['vs_sector_etf']}")
        
        print(f"\n  vs peers :")
        for peer, corr in result['vs_peers'].items():
            print(f"   - {peer}: {corr}")
        
        print(f"\n data sources : {result['data_source']}")
    else:
        print(f"\n  Error: {result.get('error')}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    asyncio.run(test())


