from typing import Dict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    enable_openai: bool = True  # 控制是否启用OpenAI分析服务
    openai_api_key: str = ""    # OpenAI API密钥

    class Config:
        env_file = ".env"
        env_prefix = "APP_"

settings = Settings()
