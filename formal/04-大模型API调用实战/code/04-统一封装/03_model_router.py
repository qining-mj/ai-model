"""
03_model_router.py
智能模型路由器

根据任务类型、优先级等因素自动选择最佳模型
"""
import os
from typing import List
from dotenv import load_dotenv

from unified_interface import BaseLLM, Message, ChatResponse
from llm_factory import LLMFactory

load_dotenv()


class ModelRouter:
    """根据任务特征选择最佳模型"""

    def __init__(self):
        self.llms = {}
        self._init_available_llms()

    def _init_available_llms(self):
        """初始化可用的模型"""
        # 按优先级定义模型槽位
        model_slots = {
            "fast": ["gpt-4o-mini", "deepseek", "qwen-turbo", "glm-4-flash"],
            "smart": ["gpt-4o", "claude-sonnet", "qwen-plus"],
            "code": ["deepseek-coder", "gpt-4o", "claude-sonnet"],
            "cheap": ["deepseek", "glm-4-flash", "qwen-turbo"],
            "chinese": ["qwen-turbo", "glm-4-flash", "deepseek"],
        }

        for slot, candidates in model_slots.items():
            for model_name in candidates:
                try:
                    llm = LLMFactory.create(model_name)
                    self.llms[slot] = llm
                    print(f"  {slot}: {model_name}")
                    break
                except Exception:
                    continue

    def route(
        self,
        messages: List[Message],
        task_type: str = "general",
        priority: str = "balanced"
    ) -> BaseLLM:
        """
        根据任务类型和优先级选择模型

        Args:
            messages: 消息列表
            task_type: 任务类型 (general/code/chinese/complex)
            priority: 优先级 (speed/quality/cost)

        Returns:
            选择的 LLM 实例
        """
        # 基于任务类型的路由
        if task_type == "code" and "code" in self.llms:
            return self.llms["code"]
        elif task_type == "chinese" and "chinese" in self.llms:
            return self.llms["chinese"]
        elif task_type == "complex" and "smart" in self.llms:
            return self.llms["smart"]

        # 基于优先级的路由
        if priority == "speed" and "fast" in self.llms:
            return self.llms["fast"]
        elif priority == "cost" and "cheap" in self.llms:
            return self.llms["cheap"]
        elif priority == "quality" and "smart" in self.llms:
            return self.llms["smart"]

        # 默认返回第一个可用的
        return next(iter(self.llms.values()))

    def chat(
        self,
        messages: List[Message],
        task_type: str = "general",
        priority: str = "balanced",
        **kwargs
    ) -> ChatResponse:
        """智能路由并调用"""
        llm = self.route(messages, task_type, priority)
        print(f"[路由选择] task={task_type}, priority={priority} -> {llm.model_name}")
        return llm.chat(messages, **kwargs)


if __name__ == "__main__":
    print("=" * 60)
    print("【智能模型路由器演示】")
    print("=" * 60)

    print("\n初始化可用模型：")
    router = ModelRouter()

    if not router.llms:
        print("\n未配置任何 API Key，请在 .env 文件中配置")
        exit()

    print("\n" + "-" * 60)
    print("测试路由选择")
    print("-" * 60)

    # 测试不同的路由场景
    test_cases = [
        {"task_type": "code", "priority": "balanced", "message": "实现快速排序"},
        {"task_type": "chinese", "priority": "balanced", "message": "写一首关于春天的诗"},
        {"task_type": "general", "priority": "speed", "message": "你好"},
        {"task_type": "general", "priority": "cost", "message": "介绍一下自己"},
        {"task_type": "complex", "priority": "quality", "message": "分析一下人工智能的发展趋势"},
    ]

    for case in test_cases:
        print(f"\n场景: task={case['task_type']}, priority={case['priority']}")
        print(f"问题: {case['message']}")

        try:
            response = router.chat(
                [Message(role="user", content=case["message"])],
                task_type=case["task_type"],
                priority=case["priority"],
                max_tokens=100
            )
            print(f"回复: {response.content[:100]}...")
        except Exception as e:
            print(f"错误: {e}")
