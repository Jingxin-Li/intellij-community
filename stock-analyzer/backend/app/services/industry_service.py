from typing import Dict, List, Optional, Union
import akshare as ak
import pandas as pd
from datetime import datetime
import time
from app.services.openai_service import OpenAIService

class IndustryService:
    """Industry data and analysis service"""
    
    def __init__(self, openai_service: OpenAIService):
        self.openai_service = openai_service
        self._cache = {}
        self._cache_timeout = 300  # 5 minutes
        self._industry_data_cache = None
        self._industry_data_cache_time = None
        self._etf_flow_cache = None
        self._etf_flow_cache_time = None
        
    async def get_industry_data(self) -> pd.DataFrame:
        """获取行业板块数据"""
        current_time = time.time()
        
        # Check cache
        if (self._industry_data_cache is not None and 
            self._industry_data_cache_time is not None and 
            current_time - self._industry_data_cache_time < self._cache_timeout):
            return self._industry_data_cache
            
        try:
            data = ak.stock_board_industry_name_em()
            # Update cache
            self._industry_data_cache = data
            self._industry_data_cache_time = current_time
            return data
        except Exception as e:
            print(f"Error getting industry data: {e}")
            return pd.DataFrame()
        
    async def get_etf_flows(self) -> pd.DataFrame:
        """获取行业资金流向"""
        current_time = time.time()
        
        # Check cache
        if (self._etf_flow_cache is not None and 
            self._etf_flow_cache_time is not None and 
            current_time - self._etf_flow_cache_time < self._cache_timeout):
            return self._etf_flow_cache
            
        try:
            df = ak.stock_sector_fund_flow_summary()
            # Rename columns to match our expected interface
            df = df.rename(columns={
                "行业": "名称",
                "今日主力净流入-净额": "净流入"
            })
            result = df[["名称", "净流入"]]
            
            # Update cache
            self._etf_flow_cache = result
            self._etf_flow_cache_time = current_time
            return result
        except Exception as e:
            print(f"Error getting ETF flows: {e}")
            return pd.DataFrame()
        
    async def analyze_industry(self, industry: str) -> Dict:
        """综合分析行业情况"""
        if not industry:
            return self._get_empty_analysis()
            
        try:
            # Get market data first to validate industry exists
            industry_data = await self.get_industry_data()
            industry_row = industry_data[industry_data["板块名称"] == industry]
            
            # Return empty analysis if industry not found
            if industry_row.empty:
                return self._get_empty_analysis()
            
            # Get sentiment analysis
            sentiment = await self.openai_service.analyze_industry_sentiment(industry)
            
            # Get ETF flows
            etf_flows = await self.get_etf_flows()
            etf_data = etf_flows[etf_flows["名称"].str.contains(industry, na=False)]
            
            market_data = industry_row.iloc[0].to_dict()
            
            # Calculate comprehensive score
            score = self._calculate_industry_score(
                sentiment=sentiment,
                market_data=market_data,
                etf_data=None if etf_data.empty else etf_data.iloc[0].to_dict()
            )
            
            return {
                "sentiment": sentiment,
                "market_data": market_data,
                "etf_data": None if etf_data.empty else etf_data.iloc[0].to_dict(),
                "score": score,
                "analysis_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            print(f"Error analyzing industry: {e}")
            return self._get_empty_analysis()
    
    def _calculate_industry_score(self, sentiment: Optional[Dict], market_data: Union[Dict, pd.Series], etf_data: Optional[Dict]) -> float:
        """计算行业综合得分"""
        total_score = 0
        max_score = 10
        
        # 1. 景气度评分 (权重: 40%, 最高4分)
        if sentiment:
            sentiment_score = 0
            
            # 产能利用率 (0-10分)
            cap_util = sentiment.get("capacity_utilization", 0)
            if cap_util > 0.8:
                sentiment_score += 10
            elif cap_util > 0.7:
                sentiment_score += 8
            elif cap_util > 0.6:
                sentiment_score += 6
            elif cap_util > 0.5:
                sentiment_score += 4
            
            # 库存周期 (0-10分)
            inventory_score = {
                "低": 10,
                "中": 7,
                "高": 4
            }.get(sentiment.get("inventory_cycle", "高"), 0)
            sentiment_score += inventory_score
            
            # 政策支持 (0-10分)
            policy = sentiment.get("policy_support", 0)
            if policy > 0.8:
                sentiment_score += 10
            elif policy > 0.7:
                sentiment_score += 8
            elif policy > 0.6:
                sentiment_score += 6
            elif policy > 0.5:
                sentiment_score += 4
                
            # Normalize sentiment score (40% weight)
            # Boost high scores to create stronger separation
            normalized_sentiment = sentiment_score / 30
            if normalized_sentiment > 0.8:
                total_score += 4.5  # Extra boost for very strong sentiment
            elif normalized_sentiment > 0.7:
                total_score += 4.0  # Strong boost for buy signals
            elif normalized_sentiment > 0.5:
                total_score += 3.0  # Medium boost for neutral signals
            else:
                total_score += normalized_sentiment * 2.0
            
        # 2. 市场表现评分 (权重: 40%, 最高4分)
        try:
            market_score = 0
            if isinstance(market_data, pd.Series):
                if not market_data.empty and "换手率" in market_data:
                    turnover = float(market_data["换手率"])
                    market_score = min(turnover * 0.5, 10)
            elif isinstance(market_data, dict):
                if market_data and "换手率" in market_data:
                    turnover = float(market_data["换手率"])
                    market_score = min(turnover * 0.5, 10)
                    
                    # Additional scores for real market data
                    change_pct = float(market_data.get("涨跌幅", 0))
                    if change_pct > 5:
                        market_score += 10
                    elif change_pct > 2:
                        market_score += 5
                    
                    up_stocks = int(market_data.get("上涨家数", 0))
                    down_stocks = int(market_data.get("下跌家数", 0))
                    if up_stocks > down_stocks:
                        market_score += 5
            
            # Normalize market score (40% weight)
            # Boost high turnover and strong market performance
            normalized_market = market_score / 25
            if normalized_market > 0.8:
                total_score += 4.5  # Extra boost for strong market performance
            elif normalized_market > 0.4:
                total_score += 3.5  # Medium boost for moderate turnover
            else:
                total_score += normalized_market * 3
        except (ValueError, TypeError) as e:
            print(f"Error processing market data: {e}")
        
        # 3. ETF资金流评分 (权重: 20%, 最高2分)
        try:
            etf_score = 0
            if etf_data and "净流入" in etf_data:
                net_flow = float(etf_data["净流入"])
                if net_flow > 1000000:  # 100万以上
                    etf_score = 10
                elif net_flow > 500000:  # 50万以上
                    etf_score = 5
            
            # Normalize ETF score (20% weight)
            # Strong inflows get extra boost
            normalized_etf = etf_score / 10
            if normalized_etf > 0.8:
                total_score += 2.5  # Extra boost for strong fund flows
            elif normalized_etf > 0.4:
                total_score += 2.0  # Medium boost for moderate flows
            else:
                total_score += normalized_etf * 1.5
            
        except (ValueError, TypeError) as e:
            print(f"Error processing ETF data: {e}")
        
        return min(total_score, 10)  # 满分10分
    
    def _get_empty_analysis(self) -> Dict:
        """返回空分析结果"""
        return {
            "sentiment": None,
            "market_data": {},
            "etf_data": None,
            "score": 0,
            "analysis_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
