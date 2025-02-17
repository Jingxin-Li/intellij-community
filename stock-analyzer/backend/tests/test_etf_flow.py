import pytest
import pandas as pd
from app.services.industry_service import IndustryService
from app.services.openai_service import OpenAIService

@pytest.fixture
def industry_service():
    openai_service = OpenAIService()
    return IndustryService(openai_service)

@pytest.mark.asyncio
async def test_get_etf_flows(industry_service):
    """Test ETF flow data retrieval"""
    result = await industry_service.get_etf_flows()
    assert isinstance(result, pd.DataFrame)
    if not result.empty:
        assert "名称" in result.columns
        assert "净流入" in result.columns

@pytest.mark.asyncio
async def test_etf_flow_integration(industry_service):
    """Test ETF flow integration with industry scoring"""
    # Test strong inflow
    sentiment = {
        "capacity_utilization": 0.8,
        "inventory_cycle": "低",
        "policy_support": 0.8,
    }
    market_data = pd.Series({"换手率": 5})
    etf_data = {"净流入": 2000000}  # Strong inflow > 1M
    score1 = industry_service._calculate_industry_score(sentiment, market_data, etf_data)
    
    # Test moderate inflow
    etf_data2 = {"净流入": 750000}  # Moderate inflow > 500K
    score2 = industry_service._calculate_industry_score(sentiment, market_data, etf_data2)
    
    # Test weak inflow
    etf_data3 = {"净流入": 100000}  # Weak inflow
    score3 = industry_service._calculate_industry_score(sentiment, market_data, etf_data3)
    
    # Verify ETF flow impact
    assert score1 > score2 > score3
    assert score1 - score2 == 1  # Strong flow adds 1 more point than moderate
    assert score2 - score3 == 1  # Moderate flow adds 1 more point than weak

@pytest.mark.asyncio
async def test_etf_flow_error_handling(industry_service):
    """Test ETF flow error handling"""
    # Test with missing ETF data
    sentiment = {
        "capacity_utilization": 0.8,
        "inventory_cycle": "低",
        "policy_support": 0.8,
    }
    market_data = pd.Series({"换手率": 5})
    score1 = industry_service._calculate_industry_score(sentiment, market_data, None)
    
    # Test with invalid ETF data
    score2 = industry_service._calculate_industry_score(sentiment, market_data, {"净流入": "invalid"})
    
    # Scores should be the same without ETF contribution
    assert score1 == score2
