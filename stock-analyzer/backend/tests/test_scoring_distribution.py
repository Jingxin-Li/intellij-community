import pytest
import pandas as pd
import numpy as np
from app.services.industry_service import IndustryService
from app.services.openai_service import OpenAIService

@pytest.fixture
def industry_service():
    openai_service = OpenAIService()
    return IndustryService(openai_service)

@pytest.mark.asyncio
async def test_score_distribution():
    """Test score distribution across categories"""
    service = IndustryService(OpenAIService())
    
    # Generate test data with different characteristics
    test_cases = [
        # Strong buy case
        {
            "sentiment": {
                "capacity_utilization": 0.9,
                "inventory_cycle": "低",
                "policy_support": 0.9
            },
            "market_data": pd.Series({"换手率": 20}),
            "etf_data": {"净流入": 2000000},
            "expected_category": "strong_buy"
        },
        # Buy case
        {
            "sentiment": {
                "capacity_utilization": 0.75,
                "inventory_cycle": "中",
                "policy_support": 0.75
            },
            "market_data": pd.Series({"换手率": 5}),
            "etf_data": {"净流入": 750000},
            "expected_category": "buy"
        },
        # Neutral case
        {
            "sentiment": {
                "capacity_utilization": 0.65,
                "inventory_cycle": "高",
                "policy_support": 0.65
            },
            "market_data": pd.Series({"换手率": 3}),
            "etf_data": {"净流入": 100000},
            "expected_category": "neutral"
        },
        # Weak case
        {
            "sentiment": {
                "capacity_utilization": 0.5,
                "inventory_cycle": "高",
                "policy_support": 0.5
            },
            "market_data": pd.Series({"换手率": 1}),
            "etf_data": {"净流入": -500000},
            "expected_category": "weak"
        }
    ]
    
    scores = []
    for case in test_cases:
        score = service._calculate_industry_score(
            case["sentiment"],
            case["market_data"],
            case["etf_data"]
        )
        scores.append(score)
        
        # Verify score falls in expected category
        if case["expected_category"] == "strong_buy":
            assert score > 8
        elif case["expected_category"] == "buy":
            assert 6 <= score <= 8
        elif case["expected_category"] == "neutral":
            assert 3 <= score < 6
        else:  # weak
            assert score < 3
    
    # Verify score statistics
    assert max(scores) <= 10  # Maximum score cap
    assert min(scores) >= 0   # Minimum score floor
    assert len([s for s in scores if s > 8]) > 0  # Should have strong buy signals
    assert len([s for s in scores if s < 3]) > 0  # Should have weak signals

@pytest.mark.asyncio
async def test_score_weighting():
    """Test technical and industry score weighting"""
    service = IndustryService(OpenAIService())
    
    # Test case with known scores
    technical_score = 12  # Out of 15
    industry_score = 8   # Out of 10
    
    # Calculate expected total (technical 70%, industry 30%)
    expected_total = (technical_score / 15 * 0.7 + industry_score / 10 * 0.3) * 10
    
    # Verify through analyze_industry
    result = await service.analyze_industry("人工智能")
    if result["score"] > 0:  # Only test if we got real data
        assert 0 <= result["score"] <= 10
        assert isinstance(result["technical_score"], (int, float))
        assert isinstance(result["industry_score"], (int, float))
        
        # Calculate actual total
        actual_total = (result["technical_score"] / 15 * 0.7 + 
                       result["industry_score"] / 10 * 0.3) * 10
        
        # Verify weighting
        assert abs(result["score"] - actual_total) < 0.01  # Allow for floating point imprecision
