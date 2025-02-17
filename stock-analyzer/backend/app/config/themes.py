from enum import Enum
from typing import Dict, List

class IndustryTheme(Enum):
    """Industry themes for stock analysis"""
    AI = "人工智能"
    ROBOT = "人形机器人"
    AUTO = "智能汽车"
    SEMICONDUCTOR = "半导体"
    DEFENSE = "国防军工"
    LOW_ALTITUDE = "低空经济"

THEME_KEYWORDS = {
    IndustryTheme.AI: ["算力", "大模型", "人工智能", "AI", "深度学习", "机器学习"],
    IndustryTheme.ROBOT: ["机器人", "自动化", "智能制造", "工业4.0", "智能装备"],
    IndustryTheme.AUTO: ["智能汽车", "新能源车", "自动驾驶", "车联网", "智能座舱", "智能驾驶", "汽车电子", "车规级"],
    IndustryTheme.SEMICONDUCTOR: ["半导体", "芯片", "集成电路", "晶圆", "封装测试"],
    IndustryTheme.DEFENSE: ["国防", "军工", "航空航天", "卫星", "导航"],
    IndustryTheme.LOW_ALTITUDE: ["无人机", "通用航空", "低空旅游", "航空运动", "通航", "直升机", "低空物流"]
}

# 主题投资重点领域
FOCUS_SECTORS = {
    "AI算力": {
        "theme": IndustryTheme.AI,
        "keywords": ["算力", "GPU", "AI芯片", "数据中心", "服务器"],
        "policy_support": 0.9,  # 政策支持度
        "market_potential": 0.95  # 市场潜力
    },
    "人形机器人": {
        "theme": IndustryTheme.ROBOT,
        "keywords": ["人形机器人", "仿生", "机器视觉", "机器人关节", "伺服系统"],
        "policy_support": 0.85,
        "market_potential": 0.9
    },
    "汽车智能化": {
        "theme": IndustryTheme.AUTO,
        "keywords": ["智能驾驶", "ADAS", "智能座舱", "车规级芯片", "车联网"],
        "policy_support": 0.8,
        "market_potential": 0.85
    },
    "低空经济": {
        "theme": IndustryTheme.LOW_ALTITUDE,
        "keywords": ["无人机", "通航", "低空旅游", "直升机", "低空物流"],
        "policy_support": 0.85,  # 政策支持度较高，国家支持通航产业发展
        "market_potential": 0.9   # 市场潜力大，低空旅游和物流需求增长
    }
}

def get_stock_themes(stock_name: str, industry_name: str) -> List[IndustryTheme]:
    """根据股票名称和行业名称判断所属主题"""
    themes = set()
    
    # 检查股票名称和行业名称是否匹配主题关键词
    for theme, keywords in THEME_KEYWORDS.items():
        for keyword in keywords:
            if keyword in stock_name or keyword in industry_name:
                themes.add(theme)
                break
    
    return list(themes)

def get_focus_sector(themes: List[IndustryTheme]) -> Dict:
    """判断股票是否属于重点关注领域"""
    for sector_name, sector_info in FOCUS_SECTORS.items():
        if sector_info["theme"] in themes:
            return {
                "name": sector_name,
                **sector_info
            }
    return None
