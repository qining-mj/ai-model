"""
04_fallback_chain.py
故障转移链

主模型失败时自动切换到备用模型
"""
import os
import time
from typing import List
from dotenv import load_dotenv

from unified_interface import BaseLLM, Message, ChatResponse
from llm_factory import LLMFactory

load_dotenv()


class FallbackChain:
    """故障转移链 - 主模型失败时自动切换到备用模型"""

    def __init__(self, llms: List[BaseLLM], max_retries: int = 2):
        """
        Args:
            llms: LLM 实例列表，按优先级排序
            max_retries: 每个模型的最大重试次数
        """
        self.llms = llms
        self.max_retries = max_retries
        self.health_status = {llm.model_name: True for llm in llms}
        self.failure_counts = {llm.model_name: 0 for llm in llms}

    def mark_healthy(self, model_name: str):
        """标记模型为健康"""
        self.health_status[model_name] = True
        self.failure_counts[model_name] = 0

    def mark_unhealthy(self, model_name: str):
        """标记模型为不健康"""
        self.health_status[model_name] = False
        print(f"  [健康状态] {model_name} 标记为不健康")

    def get_healthy_llms(self) -> List[BaseLLM]:
        """获取健康的 LLM 列表"""
        return [llm for llm in self.llms if self.health_status.get(llm.model_name, True)]

    def chat(self, messages: List[Message], **kwargs) -> ChatResponse:
        """带故障转移的调用"""
        last_error = None
        healthy_llms = self.get_healthy_llms()

        if not healthy_llms:
            # 所有模型都不健康，重置状态重试
            print("  [故障恢复] 所有模型都不健康，重置状态")
            for llm in self.llms:
                self.mark_healthy(llm.model_name)
            healthy_llms = self.llms

        for llm in healthy_llms:
            for attempt in range(self.max_retries):
                try:
                    print(f"  [调用] {llm.model_name} (第{attempt+1}次)")
                    response = llm.chat(messages, **kwargs)
                    self.mark_healthy(llm.model_name)
                    return response

                except Exception as e:
                    last_error = e
                    self.failure_counts[llm.model_name] += 1
                    print(f"  [失败] {llm.model_name}: {e}")

                    if attempt < self.max_retries - 1:
                        wait_time = 2 ** attempt
                        print(f"  [等待] {wait_time}秒后重试...")
                        time.sleep(wait_time)

            # 该模型重试失败，标记为不健康
            self.mark_unhealthy(llm.model_name)
            print(f"  [切换] 尝试下一个模型...")

        raise Exception(f"所有模型都失败: {last_error}")

    def status(self) -> dict:
        """获取状态摘要"""
        return {
            "total_models": len(self.llms),
            "healthy_models": sum(1 for v in self.health_status.values() if v),
            "health_status": dict(self.health_status),
            "failure_counts": dict(self.failure_counts)
        }


if __name__ == "__main__":
    print("=" * 60)
    print("【故障转移链演示】")
    print("=" * 60)

    # 收集可用的模型
    available_llms = []
    model_names = ["gpt-4o-mini", "deepseek", "qwen-turbo", "glm-4-flash"]

    print("\n初始化模型链：")
    for name in model_names:
        try:
            llm = LLMFactory.create(name)
            available_llms.append(llm)
            print(f"  + {name}")
        except Exception as e:
            print(f"  - {name} (不可用: {e})")

    if not available_llms:
        print("\n未配置任何 API Key，请在 .env 文件中配置")
        exit()

    # 创建故障转移链
    fallback = FallbackChain(available_llms, max_retries=2)

    print("\n" + "-" * 60)
    print("测试正常调用")
    print("-" * 60)

    try:
        response = fallback.chat([Message(role="user", content="你好")])
        print(f"\n回复: {response.content}")
        print(f"使用模型: {response.model}")
    except Exception as e:
        print(f"错误: {e}")

    print("\n" + "-" * 60)
    print("查看状态")
    print("-" * 60)

    status = fallback.status()
    print(f"总模型数: {status['total_models']}")
    print(f"健康模型数: {status['healthy_models']}")
    print(f"健康状态: {status['health_status']}")
