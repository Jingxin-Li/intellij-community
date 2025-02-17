import pytest
import pandas as pd
from app.services.industry_service import IndustryService
from app.services.openai_service import OpenAIService

@pytest.fixture
def industry_service():
    openai_service = OpenAIService()
    return IndustryService(openai_service)

@pytest.mark.asyncio
async def test_industry_board_data():
    """Test industry board data retrieval"""
    service = IndustryService(OpenAIService())
    df = await service.get_industry_data()
    
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    
    # Verify required columns
    required_columns = ["板块名称", "涨跌额", "换手率", "上涨家数", "下跌家数"]
    for col in required_columns:
        assert col in df.columns
    
    # Verify data types
    assert df["板块名称"].dtype == object  # string
    assert pd.api.types.is_numeric_dtype(df["涨跌额"])
    assert pd.api.types.is_numeric_dtype(df["换手率"])
    assert pd.api.types.is_numeric_dtype(df["上涨家数"])
    assert pd.api.types.is_numeric_dtype(df["下跌家数"])

@pytest.mark.asyncio
async def test_etf_flow_data():
    """Test ETF fund flow data retrieval"""
    service = IndustryService(OpenAIService())
    df = await service.get_etf_flows()
    
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    
    # Verify required columns
    required_columns = ["名称", "净流入"]
    for col in required_columns:
        assert col in df.columns
    
    # Verify data types
    assert df["名称"].dtype == object  # string
    assert pd.api.types.is_numeric_dtype(df["净流入"])
    
    # Verify fund flow values
    if not df.empty:
        assert not df["净流入"].isna().all()  # Should have some non-null values
        assert df["净流入"].abs().max() > 0  # Should have some non-zero flows

@pytest.mark.asyncio
async def test_industry_analysis_integration():
    """Test industry analysis with real market data"""
    service = IndustryService(OpenAIService())
    
    # Test analysis for a few key industries
    industries = ["人工智能", "机器人", "新能源车"]
    for industry in industries:
        result = await service.analyze_industry(industry)
        
        # Verify structure
        assert isinstance(result, dict)
        assert "sentiment" in result
        assert "market_data" in result
        assert "etf_data" in result
        assert "score" in result
        assert "analysis_time" in result
        
        # Verify score range
        assert 0 <= result["score"] <= 10
        
        # Verify market data
        if result["market_data"]:
            assert "换手率" in result["market_data"]
            assert "涨跌幅" in result["market_data"]
        
        # Verify ETF data
        if result["etf_data"]:
            assert "净流入" in result["etf_data"]

@pytest.mark.asyncio
async def test_error_handling_with_real_data():
    """Test error handling with real market data"""
    service = IndustryService(OpenAIService())
    
    # Test with invalid industry
    result = await service.analyze_industry("非存在行业")
    assert result["score"] == 0
    assert not result["market_data"]
    assert result["etf_data"] is None
    
    # Test with empty industry
    result = await service.analyze_industry("")
    assert result["score"] == 0
    assert not result["market_data"]
    assert result["etf_data"] is None
