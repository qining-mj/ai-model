import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 04_production_config.py
# 生产环境配置管理
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.caches import InMemoryCache
from langchain_core.globals import set_llm_cache
from langchain_core.rate_limiters import InMemoryRateLimiter

load_dotenv()

class ProductionConfig:
    """统一管理 LLM 配置"""

    # DeepSeek
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

    # LangSmith
    LANGCHAIN_TRACING = os.getenv("LANGCHAIN_TRACING_V2", "false") == "true"

    # 性能
    CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true") == "true"
    RATE_LIMIT_RPS = int(os.getenv("RATE_LIMIT_RPS", "5"))

    # LLM 池
    @classmethod
    def get_default_llm(cls, temperature=0.0):
        """日常任务"""
        return ChatOpenAI(
            model="deepseek-chat",
            base_url=cls.DEEPSEEK_BASE_URL,
            api_key=cls.DEEPSEEK_API_KEY,
            temperature=temperature,
            rate_limiter=InMemoryRateLimiter(
                requests_per_second=cls.RATE_LIMIT_RPS,
            ),
        )

    @classmethod
    def get_reasoner(cls):
        """复杂推理"""
        return ChatOpenAI(
            model="deepseek-reasoner",
            base_url=cls.DEEPSEEK_BASE_URL,
            api_key=cls.DEEPSEEK_API_KEY,
        )

    @classmethod
    def setup_cache(cls):
        if cls.CACHE_ENABLED:
            set_llm_cache(InMemoryCache())

    @classmethod
    def validate(cls):
        if not cls.DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY 未配置")

# 应用启动时
ProductionConfig.validate()
ProductionConfig.setup_cache()

# 使用时
llm = ProductionConfig.get_default_llm()
reasoner = ProductionConfig.get_reasoner()

print("生产配置加载成功")
print(f"  缓存: {'启用' if ProductionConfig.CACHE_ENABLED else '关闭'}")
print(f"  限流: {ProductionConfig.RATE_LIMIT_RPS} req/s")
print(f"  LangSmith: {'启用' if ProductionConfig.LANGCHAIN_TRACING else '关闭'}")
