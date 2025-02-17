import pytest
from unittest.mock import patch
from app.services.openai_service import OpenAIService

@pytest.fixture
def openai_service():
    return OpenAIService()

@pytest.mark.asyncio
async def test_analyze_industry_sentiment_without_api_key(openai_service):
    """Test sentiment analysis without API key returns mock data"""
    result = await openai_service.analyze_industry_sentiment("人工智能")
    assert isinstance(result, dict)
    assert "capacity_utilization" in result
    assert "inventory_cycle" in result
    assert "policy_support" in result
    assert "outlook" in result
    
    # Verify value ranges
    assert 0 <= result["capacity_utilization"] <= 1
    assert result["inventory_cycle"] in ["高", "中", "低"]
    assert 0 <= result["policy_support"] <= 1
    assert result["outlook"] in ["看好", "中性", "谨慎"]

@pytest.mark.asyncio
async def test_analyze_industry_sentiment_with_empty_input(openai_service):
    """Test sentiment analysis with empty input returns mock data"""
    result = await openai_service.analyze_industry_sentiment("")
    assert isinstance(result, dict)
    assert result == openai_service._get_mock_sentiment()

@pytest.mark.asyncio
async def test_analyze_industry_sentiment_error_handling(openai_service):
    """Test error handling returns mock data"""
    result = await openai_service.analyze_industry_sentiment(None)
    assert isinstance(result, dict)
    assert result == openai_service._get_mock_sentiment()

@pytest.mark.asyncio
async def test_analyze_industry_sentiment_disabled():
    """Test sentiment analysis when OpenAI is disabled"""
    with patch("app.config.settings.settings.enable_openai", False):
        service = OpenAIService()
        result = await service.analyze_industry_sentiment("人工智能")
        assert isinstance(result, dict)
        assert "capacity_utilization" in result
        assert "inventory_cycle" in result
        assert "policy_support" in result
        assert result == service._get_mock_sentiment()
