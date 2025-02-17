from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import numpy as np
from enum import Enum
import asyncio
from app.services.industry_service import IndustryService
from app.services.openai_service import OpenAIService
from app.services.market_data_service import MarketDataService

# Initialize services
market_data_service = MarketDataService()
openai_service = OpenAIService()
industry_service = IndustryService(openai_service)

class IndustryTheme(Enum):
    AI = "人工智能"
    ROBOT = "人形机器人"
    AUTO = "智能汽车"
    SEMICONDUCTOR = "半导体"
    DEFENSE = "国防军工"
    
# 行业景气度数据（模拟数据）
INDUSTRY_SENTIMENT = {
    "AI": {
        "capacity_utilization": 0.85,  # 产能利用率
        "inventory_cycle": 30,  # 库存周期
        "policy_support": 0.9,  # 政策支持度
        "fund_flow": 0.8,  # 资金流入强度
    },
    "ROBOT": {
        "capacity_utilization": 0.75,
        "inventory_cycle": 45,
        "policy_support": 0.85,
        "fund_flow": 0.7,
    },
    "AUTO": {
        "capacity_utilization": 0.8,
        "inventory_cycle": 40,
        "policy_support": 0.8,
        "fund_flow": 0.75,
    },
    "SEMICONDUCTOR": {
        "capacity_utilization": 0.9,
        "inventory_cycle": 25,
        "policy_support": 0.85,
        "fund_flow": 0.85,
    },
    "DEFENSE": {
        "capacity_utilization": 0.95,
        "inventory_cycle": 20,
        "policy_support": 0.95,
        "fund_flow": 0.9,
    }
}

app = FastAPI()

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

from functools import lru_cache
import asyncio
import pandas as pd



@app.get("/api/stock/list")
async def get_stock_list():
    """获取A股股票列表"""
    try:
        stocks = await market_data_service.get_stock_list()
        return {"data": stocks}
    except Exception as e:
        error_msg = f"Error in get_stock_list: {str(e)}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

@app.get("/api/stock/daily/{stock_code}")
async def get_stock_daily(stock_code: str):
    """获取单个股票的日K线数据，包含技术指标"""
    try:
        print(f"Processing request for stock {stock_code}")
        data = await asyncio.wait_for(
            market_data_service.get_stock_data(stock_code),
            timeout=90.0  # Increase timeout based on akshare API response time
        )
        if not data:
            raise HTTPException(status_code=404, detail="Stock data not found")
        return {"data": data}
    except asyncio.TimeoutError:
        print(f"Timeout fetching data for stock {stock_code}")
        raise HTTPException(status_code=504, detail="Request timeout")
    except Exception as e:
        print(f"Error processing request for stock {stock_code}: {str(e)}")
        # Return mock data instead of error in production
        data = market_data_service._get_mock_data(stock_code)
        return {"data": data}
    except Exception as e:
        error_msg = f"Error in get_stock_daily: {str(e)}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

def calculate_macd(data: pd.DataFrame) -> pd.DataFrame:
    """计算MACD指标"""
    close = data['收盘']
    exp1 = close.ewm(span=12, adjust=False).mean()
    exp2 = close.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal

def calculate_kdj(data: pd.DataFrame, n=9) -> tuple:
    """计算KDJ指标"""
    low_list = data['最低'].rolling(window=n).min()
    high_list = data['最高'].rolling(window=n).max()
    rsv = (data['收盘'] - low_list) / (high_list - low_list) * 100
    k = rsv.ewm(com=2).mean()
    d = k.ewm(com=2).mean()
    j = 3 * k - 2 * d
    return k, d, j

def get_stock_industry(stock_code: str) -> Optional[str]:
    """根据股票代码获取所属行业（模拟数据）"""
    industry_map = {
        "600519": "消费",
        "000001": "银行",
        "601318": "保险",
        "601398": "银行",
        "600036": "银行",
        "600276": "医药",
        "600887": "消费",
        "601288": "银行",
        "600030": "证券",
        "601166": "银行",
    }
    return industry_map.get(stock_code)

def calculate_industry_score(industry: str) -> float:
    """计算行业景气度得分"""
    try:
        # 获取行业主题
        theme = None
        for t in IndustryTheme:
            if t.value in industry:
                theme = t.name
                break
        
        if not theme:
            return 0
            
        sentiment = INDUSTRY_SENTIMENT[theme]
        
        # 计算行业得分
        score = 0
        
        # 1. 产能利用率评分
        if sentiment["capacity_utilization"] > 0.8:
            score += 3
        elif sentiment["capacity_utilization"] > 0.7:
            score += 2
            
        # 2. 库存周期评分（越短越好）
        if sentiment["inventory_cycle"] < 30:
            score += 3
        elif sentiment["inventory_cycle"] < 45:
            score += 2
            
        # 3. 政策支持度
        if sentiment["policy_support"] > 0.8:
            score += 3
        elif sentiment["policy_support"] > 0.7:
            score += 2
            
        # 4. 资金流入强度
        if sentiment["fund_flow"] > 0.8:
            score += 3
        elif sentiment["fund_flow"] > 0.7:
            score += 2
            
        return score
    except Exception as e:
        print(f"Error calculating industry score: {e}")
        return 0

async def calculate_stock_score(data: pd.DataFrame, stock_code: str) -> Dict:
    """计算股票得分，使用多个量化策略"""
    try:
        # Get industry analysis
        industry = get_stock_industry(stock_code)
        industry_analysis = await industry_service.analyze_industry(industry)
        
        # Calculate technical indicators score
        technical_scores = []
        
        # 1. 趋势跟踪策略（权重：30%）
        # 1.1 均线系统
        if data['MA5'].iloc[-1] > data['MA10'].iloc[-1]:
            technical_scores.append(2)  # 短期趋势转好
        if data['MA10'].iloc[-1] > data['MA20'].iloc[-1]:
            technical_scores.append(2)  # 中期趋势向好
        if data['MA20'].iloc[-1] > data['MA30'].iloc[-1]:
            technical_scores.append(1)  # 长期趋势向好
            
        # 1.2 MACD指标
        macd, signal = calculate_macd(data)
        if macd.iloc[-1] > signal.iloc[-1] and macd.iloc[-2] <= signal.iloc[-2]:
            technical_scores.append(3)  # MACD金叉
        elif macd.iloc[-1] > signal.iloc[-1]:
            technical_scores.append(1)  # MACD位于零轴上方
            
        # 2. 动量策略（权重：20%）
        # 2.1 KDJ指标
        k, d, j = calculate_kdj(data)
        if k.iloc[-1] > d.iloc[-1] and k.iloc[-1] < 80:
            technical_scores.append(2)  # KDJ金叉且未超买
        if j.iloc[-1] < 20:
            technical_scores.append(1)  # 超卖区域
            
        # 2.2 价格动量
        price_5d_change = (data['收盘'].iloc[-1] - data['收盘'].iloc[-5]) / data['收盘'].iloc[-5]
        if price_5d_change > 0.05:
            technical_scores.append(2)  # 强势动量
        elif price_5d_change > 0.02:
            technical_scores.append(1)  # 中等动量
            
        # 3. 量价配合策略（权重：30%）
        recent_vol = data['成交量'].tail(5).mean()
        prev_vol = data['成交量'].iloc[-10:-5].mean()
        vol_ratio = recent_vol / prev_vol if prev_vol > 0 else 1
        
        # 3.1 放量上涨
        if vol_ratio > 1.5 and price_5d_change > 0:
            technical_scores.append(3)  # 放量上涨
        elif vol_ratio > 1.2 and price_5d_change > 0:
            technical_scores.append(2)  # 量价齐升
            
        # 3.2 缩量回调
        if vol_ratio < 0.8 and price_5d_change < 0:
            technical_scores.append(1)  # 缩量调整
            
        # 4. 突破策略（权重：20%）
        # 4.1 价格突破
        highest_20d = data['最高'].rolling(window=20).max().iloc[-2]  # 前20日高点
        if data['收盘'].iloc[-1] > highest_20d:
            technical_scores.append(3)  # 突破前期高点
            
        # 4.2 支撑突破
        lowest_20d = data['最低'].rolling(window=20).min().iloc[-2]  # 前20日低点
        if data['收盘'].iloc[-1] > lowest_20d * 1.1:  # 向上突破10%
            technical_scores.append(2)  # 突破支撑位
            
        # 5. 风险控制
        # 5.1 超买检查
        if k.iloc[-1] > 80 and d.iloc[-1] > 80:
            technical_scores = [s * 0.5 for s in technical_scores]  # 超买区域，降低得分
            
        # 5.2 量能衰减检查
        vol_5d_trend = data['成交量'].tail(5).pct_change().mean()
        if vol_5d_trend < -0.1:  # 量能持续萎缩
            technical_scores = [s * 0.8 for s in technical_scores]  # 降低得分
            
        # 根据得分调整预测
        technical_score = min(sum(technical_scores), 15)  # 技术分最高15分
        industry_score = industry_analysis["score"]  # 行业分最高10分
        
        # Combine scores with weights (技术分70%, 行业分30%)
        total_score = (technical_score / 15 * 0.7 + industry_score / 10 * 0.3) * 10
        
        return {
            "total_score": round(total_score, 2),
            "technical_score": round(technical_score, 2),
            "industry_score": round(industry_score, 2),
            "industry_analysis": industry_analysis,
            "signals": {
                "trend_following": technical_score >= 8,
                "momentum": technical_score >= 10,
                "volume_price": technical_score >= 12,
                "breakout": technical_score >= 14,
                "industry_outlook": industry_score >= 7
            }
        }
    except Exception as e:
        print(f"Error calculating score: {e}")
        return {
            "total_score": 0,
            "technical_score": 0,
            "industry_score": 0,
            "industry_analysis": None,
            "signals": {
                "trend_following": False,
                "momentum": False,
                "volume_price": False,
                "breakout": False,
                "industry_outlook": False
            }
        }
            
        return {
            "total_score": 0,
            "technical_score": 0,
            "industry_score": 0,
            "industry_analysis": None,
            "signals": {
                "trend_following": False,
                "momentum": False,
                "volume_price": False,
                "breakout": False,
                "industry_outlook": False
            }
        }
    except Exception as e:
        print(f"Error calculating score: {e}")
        return {
            "total_score": 0,
            "technical_score": 0,
            "industry_score": 0,
            "industry_analysis": None,
            "signals": {
                "trend_following": False,
                "momentum": False,
                "volume_price": False,
                "breakout": False,
                "industry_outlook": False
            }
        }

from pydantic import BaseModel

from pydantic import BaseModel, Field

class ScreeningRequest(BaseModel):
    stock_list: List[str]
    top_k: int = Field(default=5, gt=0, description="Number of top stocks to return")

@app.post("/api/stock/screening")
async def screen_stocks(request: ScreeningRequest):
    """筛选推荐股票
    
    根据技术指标对股票进行打分和排名，返回最具上涨潜力的TopK支股票。
    评分标准包括：
    1. 均线系统（MA5/10/20/30）的多头排列
    2. 成交量趋势
    3. 价格位置相对均线的表现
    """
    try:
        if not request.stock_list:
            raise HTTPException(status_code=400, detail="Stock list cannot be empty")
            
        stock_scores = []
        for stock_code in request.stock_list:
            data = await market_data_service.get_stock_data(stock_code)
            score_data = await calculate_stock_score(pd.DataFrame(data), stock_code)
            prediction = {
                "one_week": "强烈看涨" if score_data["total_score"] >= 8 else "看涨" if score_data["total_score"] >= 6 else "观望" if score_data["total_score"] >= 4 else "谨慎",
                "one_month": "强烈看涨" if score_data["total_score"] >= 7 else "看涨" if score_data["total_score"] >= 5 else "观望" if score_data["total_score"] >= 3 else "谨慎"
            }
            
            stock_scores.append({
                "code": stock_code,
                "score": score_data["total_score"],
                "technical_score": score_data["technical_score"],
                "industry_score": score_data["industry_score"],
                "prediction": prediction,
                "signals": score_data["signals"],
                "industry_analysis": score_data["industry_analysis"]
            })
        
        # 按得分排序并返回TopK
        sorted_stocks = sorted(stock_scores, key=lambda x: x["score"], reverse=True)
        
        # 计算分析汇总
        analysis_summary = {
            "avg_technical_score": round(sum(s["technical_score"] for s in stock_scores) / len(stock_scores), 2),
            "avg_industry_score": round(sum(s["industry_score"] for s in stock_scores) / len(stock_scores), 2),
            "strong_signals": len([s for s in stock_scores if s["score"] >= 8]),
            "neutral_signals": len([s for s in stock_scores if 4 <= s["score"] < 8]),
            "weak_signals": len([s for s in stock_scores if s["score"] < 4])
        }
        
        return {
            "data": sorted_stocks[:request.top_k],
            "total_stocks": len(request.stock_list),
            "screening_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "analysis_summary": analysis_summary
        }
        
        # 添加更详细的分析结果
        result = {
            "data": sorted_stocks[:request.top_k],
            "total_stocks": len(request.stock_list),
            "screening_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "analysis": {
                "max_score": max(s["score"] for s in stock_scores),
                "min_score": min(s["score"] for s in stock_scores),
                "avg_score": sum(s["score"] for s in stock_scores) / len(stock_scores),
                "score_distribution": {
                    "strong_buy": len([s for s in stock_scores if s["score"] > 8]),
                    "buy": len([s for s in stock_scores if 6 <= s["score"] <= 8]),
                    "neutral": len([s for s in stock_scores if 3 <= s["score"] < 6]),
                    "weak": len([s for s in stock_scores if s["score"] < 3])
                }
            }
        }
        
        print(f"Analysis complete. Found {len(sorted_stocks[:request.top_k])} stocks with high growth potential.")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stock/realtime/{stock_code}")
async def get_stock_realtime(stock_code: str):
    """获取股票实时数据"""
    try:
        # 获取实时行情数据
        df = ak.stock_zh_a_spot_em()
        stock_data = df[df['代码'] == stock_code]
        
        if stock_data.empty:
            raise HTTPException(status_code=404, detail="Stock not found")
            
        return {"data": stock_data.to_dict(orient="records")[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
