import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def analyze_stock_data_nan(stock_code: str):
    """分析股票数据中的NaN值"""
    print(f"\n=== 分析股票 {stock_code} 的NaN值 ===")
    try:
        # 获取数据
        start_date = (datetime.now() - timedelta(days=180)).strftime("%Y%m%d")
        end_date = datetime.now().strftime("%Y%m%d")
        print(f"获取数据时间范围: {start_date} 到 {end_date}")
        
        df = ak.stock_zh_a_hist(
            symbol=stock_code,
            period="daily",
            start_date=start_date,
            end_date=end_date,
            adjust="qfq"
        )
        
        # 分析原始数据中的NaN
        print("\n1. 原始数据NaN分析:")
        nan_cols = df.columns[df.isna().any()].tolist()
        if nan_cols:
            print("发现包含NaN的列:")
            for col in nan_cols:
                nan_count = df[col].isna().sum()
                print(f"  - {col}: {nan_count}个NaN值 ({(nan_count/len(df)*100):.2f}%)")
        else:
            print("原始数据中没有发现NaN值")
            
        # 计算技术指标并分析NaN
        print("\n2. 技术指标计算后的NaN分析:")
        df['ma5'] = df['收盘'].rolling(window=5).mean()
        df['ma10'] = df['收盘'].rolling(window=10).mean()
        df['ma20'] = df['收盘'].rolling(window=20).mean()
        df['ma30'] = df['收盘'].rolling(window=30).mean()
        df['ma120'] = df['收盘'].rolling(window=120).mean()
        
        tech_cols = ['ma5', 'ma10', 'ma20', 'ma30', 'ma120']
        for col in tech_cols:
            nan_count = df[col].isna().sum()
            print(f"  - {col}: {nan_count}个NaN值 ({(nan_count/len(df)*100):.2f}%)")
            
        # 分析无穷值
        print("\n3. 无穷值分析:")
        inf_cols = df.columns[np.isinf(df).any()].tolist()
        if inf_cols:
            print("发现包含无穷值的列:")
            for col in inf_cols:
                inf_count = np.isinf(df[col]).sum()
                print(f"  - {col}: {inf_count}个无穷值 ({(inf_count/len(df)*100):.2f}%)")
        else:
            print("数据中没有发现无穷值")
            
        return True
    except Exception as e:
        print(f"分析过程中出错: {str(e)}")
        return False

if __name__ == "__main__":
    # 分析几个代表性的股票
    test_stocks = ["000001", "600000", "300750"]
    for stock in test_stocks:
        analyze_stock_data_nan(stock)
        print("\n" + "="*50)
