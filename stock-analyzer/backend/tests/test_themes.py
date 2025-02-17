import pytest
from app.config.themes import (
    IndustryTheme,
    THEME_KEYWORDS,
    FOCUS_SECTORS,
    get_stock_themes,
    get_focus_sector
)

def test_get_stock_themes():
    """Test theme detection from stock and industry names"""
    # Test AI theme detection
    themes = get_stock_themes("科大讯飞人工智能", "计算机应用")
    assert IndustryTheme.AI in themes
    
    # Test multiple theme detection
    themes = get_stock_themes("智能机器人", "智能装备")
    assert IndustryTheme.ROBOT in themes
    
    # Test no theme match
    themes = get_stock_themes("普通公司", "其他行业")
    assert len(themes) == 0

def test_get_focus_sector():
    """Test focus sector detection"""
    # Test AI算力sector
    themes = [IndustryTheme.AI]
    sector = get_focus_sector(themes)
    assert sector is not None
    assert sector["name"] == "AI算力"
    
    # Test multiple themes
    themes = [IndustryTheme.ROBOT, IndustryTheme.AI]
    sector = get_focus_sector(themes)
    assert sector is not None
    
    # Test no focus sector match
    themes = [IndustryTheme.DEFENSE]
    sector = get_focus_sector(themes)
    assert sector is None

def test_theme_keywords():
    """Test theme keyword completeness"""
    for theme in IndustryTheme:
        assert theme in THEME_KEYWORDS
        assert isinstance(THEME_KEYWORDS[theme], list)
        assert len(THEME_KEYWORDS[theme]) > 0

def test_focus_sectors():
    """Test focus sector configuration"""
    for sector_name, info in FOCUS_SECTORS.items():
        assert "theme" in info
        assert "keywords" in info
        assert "policy_support" in info
        assert "market_potential" in info
        assert isinstance(info["theme"], IndustryTheme)
        assert 0 <= info["policy_support"] <= 1
        assert 0 <= info["market_potential"] <= 1
