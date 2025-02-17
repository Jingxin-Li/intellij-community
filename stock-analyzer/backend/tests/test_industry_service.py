import pytest
import pandas as pd
from app.services.industry_service import IndustryService
from app.services.openai_service import OpenAIService

@pytest.fixture
def industry_service():
    openai_service = OpenAIService()
    return IndustryService(openai_service)

@pytest.mark.asyncio
async def test_get_industry_data(industry_service):
    """Test industry data retrieval"""
    result = await industry_service.get_industry_data()
    assert isinstance(result, pd.DataFrame)
    if not result.empty:
        assert "板块名称" in result.columns

@pytest.mark.asyncio
async def test_get_etf_flows(industry_service):
    """Test ETF flow data retrieval"""
    result = await industry_service.get_etf_flows()
    assert isinstance(result, pd.DataFrame)
    if not result.empty:
        assert "名称" in result.columns

@pytest.mark.asyncio
async def test_analyze_industry(industry_service):
    """Test comprehensive industry analysis"""
    result = await industry_service.analyze_industry("人工智能")
    assert isinstance(result, dict)
    assert "sentiment" in result
    assert "market_data" in result
    assert "score" in result
    assert "analysis_time" in result
    
    # Verify score range
    assert 0 <= result["score"] <= 10

@pytest.mark.asyncio
async def test_analyze_industry_empty_input(industry_service):
    """Test industry analysis with empty input"""
    result = await industry_service.analyze_industry("")
    assert isinstance(result, dict)
    assert result == industry_service._get_empty_analysis()

@pytest.mark.asyncio
async def test_analyze_industry_error_handling(industry_service):
    """Test error handling in industry analysis"""
    result = await industry_service.analyze_industry(None)
    assert isinstance(result, dict)
    assert result == industry_service._get_empty_analysis()
