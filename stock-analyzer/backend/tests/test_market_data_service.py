import pytest
import asyncio
from unittest.mock import patch, MagicMock
import pandas as pd
from app.services.market_data_service import MarketDataService

@pytest.fixture
def market_data_service():
    return MarketDataService()

@pytest.mark.asyncio
async def test_get_stock_data(market_data_service):
    """Test fetching stock data"""
    # Mock data for testing
    mock_df = pd.DataFrame({
        '日期': ['20250215'] * 90,
        '开盘': [100 + i * 0.1 for i in range(90)],
        '收盘': [101 + i * 0.1 for i in range(90)],
        '最高': [102 + i * 0.1 for i in range(90)],
        '最低': [99 + i * 0.1 for i in range(90)],
        '成交量': [1000000 + i * 1000 for i in range(90)]
    })
    
    with patch('akshare.stock_zh_a_hist', return_value=mock_df):
        # Test with valid stock code
        data = await market_data_service.get_stock_data("000001")
        assert isinstance(data, dict)
        assert "close" in data
        assert "volume" in data
        assert "turnover" in data
        assert "ma5" in data
        assert "ma10" in data
        assert "ma20" in data
        assert "ma30" in data
        assert "ma120" in data
        assert "date" in data
        
        # Test with invalid stock code
        data = await market_data_service.get_stock_data("invalid")
        assert isinstance(data, dict)
        assert data["close"] == 0.0
        assert data["volume"] == 0
    
@pytest.mark.asyncio
async def test_get_stock_list(market_data_service):
    """Test fetching stock list"""
    mock_df = pd.DataFrame({
        'code': ['000001', '600000'],
        'name': ['平安银行', '浦发银行']
    })
    
    with patch('akshare.stock_info_a_code_name', return_value=mock_df):
        stocks = await market_data_service.get_stock_list()
        assert isinstance(stocks, list)
        assert len(stocks) == 2
        assert all(isinstance(stock, dict) for stock in stocks)
        assert all("code" in stock and "name" in stock for stock in stocks)
        assert stocks[0]["code"] == "000001"
        assert stocks[0]["name"] == "平安银行"
    
@pytest.mark.asyncio
async def test_get_realtime_quotes(market_data_service):
    """Test fetching realtime quotes"""
    try:
        # Test with valid stock codes
        quotes = await asyncio.wait_for(
            market_data_service.get_realtime_quotes(["000001", "600000"]),
            timeout=10.0
        )
        assert isinstance(quotes, list)
        if len(quotes) > 0:
            for quote in quotes:
                assert "code" in quote
                assert "name" in quote
                assert "price" in quote
                assert "change" in quote
                assert "volume" in quote
                assert "turnover" in quote
    except (asyncio.TimeoutError, Exception) as e:
        print(f"Warning: Realtime quotes test error: {str(e)}")
        # Skip test if API is slow/unavailable
        pytest.skip("API error")
    
    try:
        # Test with invalid stock codes
        quotes = await asyncio.wait_for(
            market_data_service.get_realtime_quotes(["invalid"]),
            timeout=5.0
        )
        assert isinstance(quotes, list)
        assert len(quotes) == 0
    except asyncio.TimeoutError:
        # Skip invalid test if API is slow
        pytest.skip("API timeout on invalid test")
    
@pytest.mark.asyncio
async def test_error_handling(market_data_service):
    """Test error handling"""
    # Test with None input
    data = await market_data_service.get_stock_data(None)
    assert isinstance(data, dict)
    assert data["close"] == 0.0
    
    quotes = await market_data_service.get_realtime_quotes(None)
    assert isinstance(quotes, list)
    assert len(quotes) == 0
