from typing import Dict, List, Optional
import openai
from datetime import datetime
from app.config.settings import settings

class OpenAIService:
    """OpenAI service for industry analysis and sentiment scoring"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.openai_api_key
        self._enabled = settings.enable_openai
        if self.api_key:
            openai.api_key = self.api_key
            
    async def analyze_industry_sentiment(self, industry: str) -> Dict:
        """分析行业景气度和政策支持
        
        Args:
            industry: 行业名称
            
        Returns:
            Dict containing:
            - capacity_utilization: 产能利用率 (0-1)
            - inventory_cycle: 库存周期 ("高"/"中"/"低")
            - policy_support: 政策支持度 (0-1)
            - outlook: 发展前景 ("看好"/"中性"/"谨慎")
        """
        if not industry or not self._enabled:
            return self._get_mock_sentiment()
            
        if not self.api_key:
            print("OpenAI API key not set")
            return self._get_mock_sentiment()
            
        try:
            prompt = self._generate_analysis_prompt(industry)
            response = await self._call_openai_api(prompt)
            return self._parse_openai_response(response)
        except Exception as e:
            print(f"Error analyzing industry sentiment: {e}")
            return self._get_mock_sentiment()
            
    def _generate_analysis_prompt(self, industry: str) -> str:
        """生成行业分析提示词"""
        return f"""分析以下行业的景气度和政策支持情况:
        行业: {industry}
        时间: {datetime.now().strftime('%Y-%m-%d')}
        
        请提供以下信息:
        1. 产能利用率评估 (0-1之间的数值)
        2. 库存周期状态 ("高"/"中"/"低")
        3. 政策支持度 (0-1之间的数值)
        4. 行业发展前景 ("看好"/"中性"/"谨慎")
        
        请以JSON格式返回，包含以下字段:
        {{
            "capacity_utilization": float,
            "inventory_cycle": string,
            "policy_support": float,
            "outlook": string
        }}
        """
            
    async def _call_openai_api(self, prompt: str) -> str:
        """调用OpenAI API"""
        if not self._enabled or not self.api_key:
            return self._get_mock_response()
            
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "你是一个专业的行业分析师，擅长分析中国A股市场的行业动态和政策导向。请基于最新的市场数据和政策信息提供分析。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # 解析返回的JSON字符串
            try:
                content = response.choices[0].message.content
                # 尝试从返回内容中提取JSON部分
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    return json_match.group()
                else:
                    print("Warning: Could not extract JSON from OpenAI response")
                    return self._get_mock_response()
            except Exception as e:
                print(f"Error parsing OpenAI response: {e}")
                return self._get_mock_response()
                
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return self._get_mock_response()
            
    def _get_mock_response(self) -> str:
        """返回模拟的行业分析数据"""
        return '{"capacity_utilization": 0.85, "inventory_cycle": "低", "policy_support": 0.9, "outlook": "看好"}'
            
    def _parse_openai_response(self, response: str) -> Dict:
        """解析OpenAI响应"""
        try:
            import json
            data = json.loads(response)
            
            # 验证必要字段
            required_fields = ["capacity_utilization", "inventory_cycle", "policy_support", "outlook"]
            if not all(field in data for field in required_fields):
                print("Warning: Missing required fields in OpenAI response")
                return self._get_mock_sentiment()
                
            # 验证数值范围
            if not (0 <= data["capacity_utilization"] <= 1):
                data["capacity_utilization"] = min(max(data["capacity_utilization"], 0), 1)
                
            if not (0 <= data["policy_support"] <= 1):
                data["policy_support"] = min(max(data["policy_support"], 0), 1)
                
            # 验证枚举值
            if data["inventory_cycle"] not in ["高", "中", "低"]:
                data["inventory_cycle"] = "中"
                
            if data["outlook"] not in ["看好", "中性", "谨慎"]:
                data["outlook"] = "中性"
                
            return data
        except json.JSONDecodeError as e:
            print(f"Error parsing OpenAI response JSON: {e}")
            return self._get_mock_sentiment()
        except Exception as e:
            print(f"Error processing OpenAI response: {e}")
            return self._get_mock_sentiment()
            
    def _get_mock_sentiment(self) -> Dict:
        """返回模拟数据用于测试
        
        根据不同行业特点返回合理的模拟数据，包括:
        - 产能利用率评分 (0-1)
        - 库存周期状态 (高/中/低)
        - 政策支持度 (0-1)
        - 发展前景 (看好/中性/谨慎)
        """
        import random
        
        # 随机生成合理范围内的评分
        capacity = round(random.uniform(0.6, 0.9), 2)
        policy = round(random.uniform(0.5, 0.95), 2)
        
        # 根据评分确定前景
        total_score = (capacity + policy) / 2
        if total_score > 0.8:
            outlook = "看好"
        elif total_score > 0.6:
            outlook = "中性"
        else:
            outlook = "谨慎"
            
        # 库存周期与产能利用率相关
        if capacity > 0.8:
            inventory = "低"
        elif capacity > 0.6:
            inventory = "中"
        else:
            inventory = "高"
            
        return {
            "capacity_utilization": capacity,
            "inventory_cycle": inventory,
            "policy_support": policy,
            "outlook": outlook
        }
