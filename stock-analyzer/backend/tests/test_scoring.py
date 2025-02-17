import pytest
import pandas as pd
from app.services.industry_service import IndustryService
from app.services.openai_service import OpenAIService

@pytest.fixture
def industry_service():
    openai_service = OpenAIService()
    return IndustryService(openai_service)

def test_industry_score_calculation(industry_service):
    """Test industry score calculation with known cases"""
    # Test Case 1: High scores in all categories
    sentiment1 = {
        "capacity_utilization": 0.9,  # Should get 3 points
        "inventory_cycle": "低",      # Should get 2 points
        "policy_support": 0.9,       # Should get 3 points
    }
    market_data1 = pd.Series({"换手率": 20})  # Should get 2 points (20 * 0.1)
    etf_data1 = {"净流入": 2000000}  # Should get 2 points for strong inflow
    score1 = industry_service._calculate_industry_score(sentiment1, market_data1, etf_data1)
    assert score1 == 10  # Should be capped at 10 despite total being higher

    # Test Case 2: Medium scores
    sentiment2 = {
        "capacity_utilization": 0.75,  # Should get 2 points
        "inventory_cycle": "中",       # Should get 0 points
        "policy_support": 0.75,        # Should get 2 points
    }
    market_data2 = pd.Series({"换手率": 5})  # Should get 0.5 points
    etf_data2 = {"净流入": 750000}  # Should get 1 point for moderate inflow
    score2 = industry_service._calculate_industry_score(sentiment2, market_data2, etf_data2)
    assert score2 == 5.5

    # Test Case 3: Low scores
    sentiment3 = {
        "capacity_utilization": 0.6,  # Should get 0 points
        "inventory_cycle": "高",      # Should get 0 points
        "policy_support": 0.6,       # Should get 0 points
    }
    market_data3 = pd.Series({"换手率": 2})  # Should get 0.2 points
    etf_data3 = {"净流入": -500000}  # Should get 0 points for outflow
    score3 = industry_service._calculate_industry_score(sentiment3, market_data3, etf_data3)
    assert score3 == 0.2

    # Test Case 4: Missing market data
    sentiment4 = {
        "capacity_utilization": 0.8,  # Should get 2 points
        "inventory_cycle": "低",      # Should get 2 points
        "policy_support": 0.8,       # Should get 2 points
    }
    market_data4 = pd.Series({})  # Empty market data
    etf_data4 = None  # Missing ETF data
    score4 = industry_service._calculate_industry_score(sentiment4, market_data4, etf_data4)
    assert score4 == 6  # Should only include sentiment scores

def test_industry_score_error_handling(industry_service):
    """Test industry score calculation error handling"""
    # Test with empty sentiment
    score1 = industry_service._calculate_industry_score({}, pd.Series({}), None)
    assert score1 == 0

    # Test with None values
    score2 = industry_service._calculate_industry_score(None, None, None)
    assert score2 == 0

    # Test with invalid inventory cycle
    sentiment = {
        "capacity_utilization": 0.8,
        "inventory_cycle": "invalid",
        "policy_support": 0.8,
    }
    score3 = industry_service._calculate_industry_score(sentiment, pd.Series({}), None)
    assert score3 == 4  # Should only count valid scores
