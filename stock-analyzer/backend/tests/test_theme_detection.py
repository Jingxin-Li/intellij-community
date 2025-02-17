import pytest
from app.config.themes import (
    IndustryTheme,
    THEME_KEYWORDS,
    FOCUS_SECTORS,
    get_stock_themes,
    get_focus_sector
)

def test_ai_theme_detection():
    """Test AI theme detection"""
    # Test stock names
    assert IndustryTheme.AI in get_stock_themes("科大讯飞人工智能", "计算机应用")
    assert IndustryTheme.AI in get_stock_themes("AI芯片科技", "半导体")
    assert IndustryTheme.AI in get_stock_themes("普通公司", "人工智能")
    assert IndustryTheme.AI not in get_stock_themes("普通公司", "其他行业")

def test_robot_theme_detection():
    """Test robotics theme detection"""
    # Test stock names
    assert IndustryTheme.ROBOT in get_stock_themes("机器人科技", "智能制造")
    assert IndustryTheme.ROBOT in get_stock_themes("自动化设备", "机器人")
    assert IndustryTheme.ROBOT in get_stock_themes("普通公司", "智能制造")
    assert IndustryTheme.ROBOT not in get_stock_themes("普通公司", "其他行业")

def test_auto_theme_detection():
    """Test automotive theme detection"""
    # Test stock names
    assert IndustryTheme.AUTO in get_stock_themes("智能汽车科技", "汽车零部件")
    assert IndustryTheme.AUTO in get_stock_themes("新能源车企", "汽车制造")
    assert IndustryTheme.AUTO in get_stock_themes("普通公司", "自动驾驶")
    assert IndustryTheme.AUTO not in get_stock_themes("普通公司", "其他行业")

def test_semiconductor_theme_detection():
    """Test semiconductor theme detection"""
    # Test stock names
    assert IndustryTheme.SEMICONDUCTOR in get_stock_themes("半导体科技", "集成电路")
    assert IndustryTheme.SEMICONDUCTOR in get_stock_themes("芯片设计", "半导体")
    assert IndustryTheme.SEMICONDUCTOR in get_stock_themes("普通公司", "集成电路")
    assert IndustryTheme.SEMICONDUCTOR not in get_stock_themes("普通公司", "其他行业")

def test_defense_theme_detection():
    """Test defense theme detection"""
    # Test stock names
    assert IndustryTheme.DEFENSE in get_stock_themes("航空航天科技", "国防军工")
    assert IndustryTheme.DEFENSE in get_stock_themes("军工电子", "国防")
    assert IndustryTheme.DEFENSE in get_stock_themes("普通公司", "航空航天")
    assert IndustryTheme.DEFENSE not in get_stock_themes("普通公司", "其他行业")

def test_multiple_theme_detection():
    """Test detection of multiple themes"""
    themes = get_stock_themes("AI机器人科技", "智能制造")
    assert IndustryTheme.AI in themes
    assert IndustryTheme.ROBOT in themes
    assert len(themes) == 2

def test_focus_sector_detection():
    """Test focus sector detection"""
    # Test AI算力
    themes = get_stock_themes("AI算力科技", "人工智能")
    sector = get_focus_sector(themes)
    assert sector is not None
    assert sector["name"] == "AI算力"
    assert sector["policy_support"] > 0.8
    
    # Test 人形机器人
    themes = get_stock_themes("人形机器人科技", "机器人")
    sector = get_focus_sector(themes)
    assert sector is not None
    assert sector["name"] == "人形机器人"
    assert sector["market_potential"] > 0.8
    
    # Test 汽车智能化
    themes = get_stock_themes("智能驾驶科技", "汽车电子")
    sector = get_focus_sector(themes)
    assert sector is not None
    assert sector["name"] == "汽车智能化"
    assert all(k in sector["keywords"] for k in ["智能驾驶", "ADAS", "智能座舱"])
    
    # Test 低空经济
    themes = get_stock_themes("通航科技", "通用航空")
    sector = get_focus_sector(themes)
    assert sector is not None
    assert sector["name"] == "低空经济"
    assert sector["policy_support"] == 0.85
    assert sector["market_potential"] == 0.9
    assert all(k in sector["keywords"] for k in ["无人机", "通航", "低空旅游"])

def test_low_altitude_theme_detection():
    """Test low-altitude economy theme detection"""
    # Test stock names
    assert IndustryTheme.LOW_ALTITUDE in get_stock_themes("通航科技", "通用航空")
    assert IndustryTheme.LOW_ALTITUDE in get_stock_themes("无人机系统", "航空器械")
    assert IndustryTheme.LOW_ALTITUDE in get_stock_themes("普通公司", "低空旅游")
    assert IndustryTheme.LOW_ALTITUDE not in get_stock_themes("普通公司", "其他行业")

def test_defense_low_altitude_overlap():
    """Test defense and low-altitude theme overlap"""
    themes = get_stock_themes("军用无人机", "航空航天")
    assert IndustryTheme.DEFENSE in themes
    assert IndustryTheme.LOW_ALTITUDE in themes
    assert len(themes) == 2

def test_theme_keyword_completeness():
    """Test theme keyword configuration"""
    # Verify all themes have keywords
    for theme in IndustryTheme:
        assert theme in THEME_KEYWORDS
        assert len(THEME_KEYWORDS[theme]) >= 3  # At least 3 keywords per theme
        
    # Verify focus sectors configuration
    for sector_name, info in FOCUS_SECTORS.items():
        assert "theme" in info
        assert "keywords" in info
        assert "policy_support" in info
        assert "market_potential" in info
        assert isinstance(info["theme"], IndustryTheme)
        assert len(info["keywords"]) >= 3
