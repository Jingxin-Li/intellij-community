import pytest
import pandas as pd
import time
from app.services.industry_service import IndustryService
from app.services.openai_service import OpenAIService

@pytest.fixture
def industry_service():
    openai_service = OpenAIService()
    return IndustryService(openai_service)

@pytest.mark.asyncio
async def test_large_stock_list_performance():
    """Test performance with large stock list"""
    service = IndustryService(OpenAIService())
    
    # Get all industries
    industry_data = await service.get_industry_data()
    industries = industry_data["板块名称"].tolist()
    
    # Measure performance
    start_time = time.time()
    results = []
    
    for industry in industries[:20]:  # Test with first 20 industries
        result = await service.analyze_industry(industry)
        results.append(result)
        
    end_time = time.time()
    processing_time = end_time - start_time
    
    # Verify results
    assert len(results) > 0
    assert all(isinstance(r, dict) for r in results)
    assert all("score" in r for r in results)
    
    # Performance assertions
    assert processing_time / len(results) < 2.0  # Average < 2 seconds per industry
    assert all(r["score"] >= 0 and r["score"] <= 10 for r in results)

@pytest.mark.asyncio
async def test_caching_performance():
    """Test caching implementation"""
    service = IndustryService(OpenAIService())
    
    # First request (uncached)
    start_time = time.time()
    result1 = await service.analyze_industry("人工智能")
    first_request_time = time.time() - start_time
    
    # Second request (should be cached)
    start_time = time.time()
    result2 = await service.analyze_industry("人工智能")
    cached_request_time = time.time() - start_time
    
    # Verify caching works
    assert cached_request_time < first_request_time
    assert result1["score"] == result2["score"]

@pytest.mark.asyncio
async def test_error_handling():
    """Test error handling for API calls"""
    service = IndustryService(OpenAIService())
    
    # Test with invalid industry
    result = await service.analyze_industry("非存在行业")
    assert result["score"] == 0
    assert result["market_data"] == {}
    
    # Test with empty input
    result = await service.analyze_industry("")
    assert result["score"] == 0
    assert result["market_data"] == {}
    
    # Test with None input
    result = await service.analyze_industry(None)
    assert result["score"] == 0
    assert result["market_data"] == {}

@pytest.mark.asyncio
async def test_concurrent_requests():
    """Test handling of concurrent requests"""
    service = IndustryService(OpenAIService())
    
    # Get test industries
    industry_data = await service.get_industry_data()
    test_industries = industry_data["板块名称"].tolist()[:5]
    
    # Run concurrent analysis
    import asyncio
    start_time = time.time()
    tasks = [service.analyze_industry(industry) for industry in test_industries]
    results = await asyncio.gather(*tasks)
    end_time = time.time()
    
    # Verify results
    assert len(results) == len(test_industries)
    assert all(isinstance(r, dict) for r in results)
    assert all("score" in r for r in results)
    
    # Performance assertions
    total_time = end_time - start_time
    assert total_time < len(test_industries) * 2  # Should be faster than sequential
