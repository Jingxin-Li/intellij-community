import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import asyncio
import time

def test_stock_data():
    try:
        print("Starting akshare test...")
        start_date = (datetime.now() - timedelta(days=180)).strftime("%Y%m%d")
        end_date = datetime.now().strftime("%Y%m%d")
        print(f"Fetching data for 000001 from {start_date} to {end_date}")
        
        start_time = time.time()
        df = ak.stock_zh_a_hist(
            symbol="000001",
            period="daily",
            start_date=start_date,
            end_date=end_date,
            adjust="qfq"  # 前复权
        )
        end_time = time.time()
        
        print(f"\nFetch completed in {end_time - start_time:.2f} seconds")
        print("\nDataFrame info:")
        print(df.info())
        print("\nFirst 5 rows:")
        print(df.head())
        
        # Check for NaN values
        print("\nColumns with NaN values:")
        print(df.isna().sum())
        
        return True
    except Exception as e:
        print(f"Error: {type(e).__name__} - {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_stock_data()
