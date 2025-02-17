from typing import Dict, List, Optional
import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import asyncio

class MarketDataService:
    """Service for fetching real market data using akshare"""
    
    def __init__(self):
        self._cache = {}
        self._cache_timeout = 300  # 5 minutes
        
    async def get_stock_data(self, stock_code: str) -> Dict:
        """获取股票行情数据
        
        Args:
            stock_code: 股票代码（如：000001）
            
        Returns:
            Dict containing:
            - close: 收盘价
            - volume: 成交量
            - turnover: 换手率
            - ma5: 5日均线
            - ma10: 10日均线
            - ma20: 20日均线
            - ma30: 30日均线
            - ma120: 120日均线（半年线）
        """
        if not stock_code:
            return self._get_mock_data("000001")
            
        try:
            print(f"Fetching data for stock {stock_code}...")
            try:
                df = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: ak.stock_zh_a_hist(
                        symbol=stock_code,
                        period="daily",
                        start_date=(datetime.now() - timedelta(days=180)).strftime("%Y%m%d"),
                        end_date=datetime.now().strftime("%Y%m%d"),
                        adjust="qfq"  # 前复权
                    )
                )
                print(f"Successfully fetched data for stock {stock_code}")
            except Exception as e:
                print(f"Error fetching data for stock {stock_code}: {str(e)}")
                print("Using mock data due to API unavailability")
                return self._get_mock_data(stock_code)
            
            if df.empty:
                return self._get_mock_data(stock_code)
                
            # 计算均线
            df['ma5'] = df['收盘'].rolling(window=5).mean()
            df['ma10'] = df['收盘'].rolling(window=10).mean()
            df['ma20'] = df['收盘'].rolling(window=20).mean()
            df['ma30'] = df['收盘'].rolling(window=30).mean()
            df['ma120'] = df['收盘'].rolling(window=120).mean()
            
            # 检查DataFrame是否包含所需的列
            required_columns = ['收盘', '成交量', '换手率', '日期']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                print(f"Warning: Missing required columns: {missing_columns}")
                return self._get_mock_data(stock_code)
                
            # 获取最新数据并处理NaN值
            latest = df.iloc[-1]
            
            # 检查是否存在任何NaN值
            nan_columns = [col for col in df.columns if pd.isna(latest[col])]
            if nan_columns:
                print(f"Warning: Found NaN values in columns: {nan_columns}")
            
            # 处理均线计算中的NaN值
            for ma in ['ma5', 'ma10', 'ma20', 'ma30', 'ma120']:
                if pd.isna(df[ma]).any():
                    print(f"Warning: NaN values found in {ma} calculation")
                    # 使用更短的窗口重新计算
                    window = int(ma[2:])
                    if len(df) < window:
                        df[ma] = df['收盘'].rolling(window=len(df), min_periods=1).mean()
                    else:
                        df[ma] = df['收盘'].rolling(window=window, min_periods=1).mean()
                        
            def safe_float(value, column_name=None):
                """安全地转换数值，处理NaN、无穷大等特殊情况
                
                Args:
                    value: 要转换的值
                    column_name: 列名，用于日志记录
                
                Returns:
                    float: 转换后的数值，异常情况返回0.0
                """
                try:
                    if pd.isna(value) or pd.isnull(value):
                        if column_name:
                            print(f"Warning: NaN/null value found in column {column_name}")
                        return 0.0
                    
                    float_val = float(value)
                    if not np.isfinite(float_val):
                        if column_name:
                            print(f"Warning: Non-finite value {float_val} found in column {column_name}")
                        return 0.0
                        
                    return float_val
                except (ValueError, TypeError) as e:
                    if column_name:
                        print(f"Warning: Error converting value '{value}' in column {column_name}: {str(e)}")
                    return 0.0
            
            return {
                'close': safe_float(latest['收盘'], '收盘'),
                'volume': safe_float(latest['成交量'], '成交量'),
                'turnover': safe_float(latest.get('换手率', 0), '换手率'),
                'ma5': safe_float(latest['ma5'], 'ma5'),
                'ma10': safe_float(latest['ma10'], 'ma10'),
                'ma20': safe_float(latest['ma20'], 'ma20'),
                'ma30': safe_float(latest['ma30'], 'ma30'),
                'ma120': safe_float(latest['ma120'], 'ma120'),
                'date': str(latest['日期'])
            }
        except Exception as e:
            print(f"Error fetching stock data for {stock_code}: {e}")
            return self._get_empty_data()
            
    async def get_stock_list(self) -> List[Dict]:
        """获取A股股票列表"""
        try:
            # 使用asyncio.wait_for包装API调用
            async def fetch_list():
                df = await asyncio.get_event_loop().run_in_executor(None, ak.stock_info_a_code_name)
                return [
                    {
                        'code': str(row['code']),
                        'name': str(row['name']) if pd.notna(row['name']) else ''
                    }
                    for _, row in df.iterrows()
                    if pd.notna(row['code'])
                ]
            
            return await asyncio.wait_for(fetch_list(), timeout=10.0)
        except asyncio.TimeoutError:
            print("Timeout fetching stock list")
            return []
        except Exception as e:
            print(f"Error fetching stock list: {e}")
            return []
            
    async def get_realtime_quotes(self, stock_codes: List[str]) -> List[Dict]:
        """获取实时行情数据
        
        Args:
            stock_codes: 股票代码列表
            
        Returns:
            List of Dict containing:
            - code: 股票代码
            - name: 股票名称
            - price: 当前价格
            - change: 涨跌幅
            - volume: 成交量
            - turnover: 换手率
        """
        try:
            # 使用asyncio.wait_for包装API调用
            async def fetch_batch(batch):
                df = await asyncio.get_event_loop().run_in_executor(None, ak.stock_zh_a_spot_em)
                df = df[df['代码'].isin(batch)]
                def safe_float(value, column_name=None):
                    """安全地转换数值，处理NaN、无穷大等特殊情况"""
                    try:
                        if pd.isna(value) or pd.isnull(value):
                            if column_name:
                                print(f"Warning: NaN/null value found in column {column_name}")
                            return 0.0
                        
                        float_val = float(value)
                        if not np.isfinite(float_val):
                            if column_name:
                                print(f"Warning: Non-finite value {float_val} found in column {column_name}")
                            return 0.0
                            
                        return float_val
                    except (ValueError, TypeError) as e:
                        if column_name:
                            print(f"Warning: Error converting value '{value}' in column {column_name}: {str(e)}")
                        return 0.0

                return [
                    {
                        'code': str(row['代码']),
                        'name': str(row['名称']),
                        'price': safe_float(row['最新价'], '最新价'),
                        'change': safe_float(row['涨跌幅'], '涨跌幅'),
                        'volume': safe_float(row['成交量'], '成交量'),
                        'turnover': safe_float(row['换手率'], '换手率')
                    }
                    for _, row in df.iterrows()
                ]

            # 分批获取数据，每次最多50只股票
            batch_size = 50
            results = []
            
            for i in range(0, len(stock_codes), batch_size):
                batch = stock_codes[i:i+batch_size]
                try:
                    batch_results = await asyncio.wait_for(
                        fetch_batch(batch),
                        timeout=5.0
                    )
                    results.extend(batch_results)
                except asyncio.TimeoutError:
                    print(f"Timeout fetching batch {i//batch_size + 1}")
                    continue
                    
            return results
        except Exception as e:
            print(f"Error fetching realtime quotes: {e}")
            return []
            
    def _get_mock_data(self, stock_code: str) -> Dict:
        """返回模拟数据用于测试或API不可用时
        
        Args:
            stock_code: 股票代码，用于生成相对稳定的随机数
        """
        import random
        import hashlib
        
        # 使用股票代码作为随机数种子以保持相对稳定
        seed = int(hashlib.md5(stock_code.encode()).hexdigest()[:8], 16)
        random.seed(seed)
        
        base_price = 10 + random.uniform(0, 90)  # 基础价格在10-100之间
        
        # 生成合理的技术指标数据
        close = round(base_price * (1 + random.uniform(-0.05, 0.05)), 2)
        ma5 = round(close * (1 + random.uniform(-0.02, 0.02)), 2)
        ma10 = round(ma5 * (1 + random.uniform(-0.02, 0.02)), 2)
        ma20 = round(ma10 * (1 + random.uniform(-0.02, 0.02)), 2)
        ma30 = round(ma20 * (1 + random.uniform(-0.02, 0.02)), 2)
        ma120 = round(ma30 * (1 + random.uniform(-0.02, 0.02)), 2)
        
        return {
            'close': close,
            'volume': int(random.uniform(100000, 1000000)),
            'turnover': round(random.uniform(0.5, 5.0), 2),
            'ma5': ma5,
            'ma10': ma10,
            'ma20': ma20,
            'ma30': ma30,
            'ma120': ma120,
            'date': datetime.now().strftime("%Y-%m-%d")
        }
