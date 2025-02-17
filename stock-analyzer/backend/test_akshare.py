import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

def test_akshare():
    # Test basic akshare functionality
    print('Testing basic index data...')
    try:
        index_data = ak.stock_zh_index_spot()
        print(f'Successfully retrieved {len(index_data)} index records')
    except Exception as e:
        print(f'Error getting index data: {e}')

    # Test stock historical data
    print('\nTesting historical data...')
    try:
        end_date = datetime.now() - timedelta(days=1)
        start_date = end_date - timedelta(days=90)
        df = ak.stock_zh_a_hist(symbol='000001', 
                               start_date=start_date.strftime('%Y%m%d'),
                               end_date=end_date.strftime('%Y%m%d'),
                               adjust='qfq')
        print(f'Successfully retrieved {len(df)} historical records')
    except Exception as e:
        print(f'Error getting historical data: {e}')

if __name__ == '__main__':
    test_akshare()
