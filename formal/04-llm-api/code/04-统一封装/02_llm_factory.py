"""
02_llm_factory.py
LLM 工厂 - 统一创建入口

运行前准备：
1. pip install openai anthropic python-dotenv
2. 在 .env 文件中添加相应的 API Key
"""
import os
from dotenv import load_dotenv
from typing import Union

# 导入统一接口
from unified_interface import BaseLLM, OpenAIAdapter, ClaudeAdapter, Message

load_dotenv()


class LLMFactory:
    """LLM 工厂类"""

    PRESETS = {
        # OpenAI 系列
        "gpt-4o": {"provider": "openai", "model": "gpt-4o"},
        "gpt-4o-mini": {"provider": "openai", "model": "gpt-4o-mini"},

        # Claude 系列
        "claude-sonnet": {"provider": "claude", "model": "claude-3-5-sonnet-20241022"},
        "claude-haiku": {"provider": "claude", "model": "claude-3-haiku-20240307"},

        # DeepSeek（使用 OpenAI 适配器）
        "deepseek": {
            "provider": "openai",
            "model": "deepseek-chat",
            "base_url": "https://api.deepseek.com",
            "api_key_env": "DEEPSEEK_API_KEY"
        },
        "deepseek-coder": {
            "provider": "openai",
            "model": "deepseek-coder",
            "base_url": "https://api.deepseek.com",
            "api_key_env": "DEEPSEEK_API_KEY"
        },

        # 通义千问
        "qwen-turbo": {
            "provider": "openai",
            "model": "qwen-turbo",
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "api_key_env": "DASHSCOPE_API_KEY"
        },
        "qwen-plus": {
            "provider": "openai",
            "model": "qwen-plus",
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "api_key_env": "DASHSCOPE_API_KEY"
        },

        # 智谱
        "glm-4-flash": {
            "provider": "openai",
            "model": "glm-4-flash",
            "base_url": "https://open.bigmodel.cn/api/paas/v4/",
            "api_key_env": "ZHIPU_API_KEY"
        },
    }

    @classmethod
    def create(cls, name_or_config: Union[str, dict]) -> BaseLLM:
        """
        创建 LLM 实例

        Args:
            name_or_config: 预设名称（如 "gpt-4o-mini"）或配置字典

        Returns:
            BaseLLM 实例
        """
        if isinstance(name_or_config, str):
            if name_or_config not in cls.PRESETS:
                raise ValueError(f"未知的预设: {name_or_config}，可用: {list(cls.PRESETS.keys())}")
            config = cls.PRESETS[name_or_config]
        else:
            config = name_or_config

        provider = config["provider"]
        model = config["model"]

        if provider == "openai":
            return OpenAIAdapter(
                model=model,
                api_key=os.getenv(config.get("api_key_env", "OPENAI_API_KEY")),
                base_url=config.get("base_url")
            )
        elif provider == "claude":
            return ClaudeAdapter(
                model=model,
                api_key=os.getenv(config.get("api_key_env", "ANTHROPIC_API_KEY"))
            )
        else:
            raise ValueError(f"未知的提供商: {provider}")

    @classmethod
    def list_presets(cls):
        """列出所有可用预设"""
        print("可用的模型预设：")
        for name, config in cls.PRESETS.items():
            print(f"  - {name}: {config['model']} ({config['provider']})")


if __name__ == "__main__":
    print("=" * 60)
    print("【LLM 工厂演示】")
    print("=" * 60)

    # 列出所有预设
    LLMFactory.list_presets()

    print("\n" + "-" * 60)
    print("测试各模型调用")
    print("-" * 60)

    messages = [Message(role="user", content="你好，介绍一下自己")]

    # 测试可用的模型
    test_models = []

    if os.getenv("OPENAI_API_KEY"):
        test_models.append("gpt-4o-mini")
    if os.getenv("DEEPSEEK_API_KEY"):
        test_models.append("deepseek")
    if os.getenv("DASHSCOPE_API_KEY"):
        test_models.append("qwen-turbo")
    if os.getenv("ZHIPU_API_KEY"):
        test_models.append("glm-4-flash")

    if not test_models:
        print("\n未配置任何 API Key，请在 .env 文件中配置")
    else:
        for model_name in test_models:
            print(f"\n--- {model_name} ---")
            try:
                llm = LLMFactory.create(model_name)
                response = llm.chat(messages, max_tokens=100)
                print(f"回复: {response.content[:100]}...")
            except Exception as e:
                print(f"错误: {e}")
