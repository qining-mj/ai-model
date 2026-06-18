"""
05_cost_tracker.py
成本追踪器

追踪 API 调用成本，生成统计报告
"""
import os
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass, field
from dotenv import load_dotenv

from unified_interface import Message, ChatResponse
from llm_factory import LLMFactory

load_dotenv()


@dataclass
class CallRecord:
    """调用记录"""
    timestamp: datetime
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    cost_cny: float


class CostTracker:
    """API 调用成本追踪"""

    # 价格配置（美元/1M tokens）
    PRICING_USD = {
        "gpt-4o": {"input": 2.5, "output": 10},
        "gpt-4o-mini": {"input": 0.15, "output": 0.6},
        "claude-3-5-sonnet-20241022": {"input": 3, "output": 15},
        "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25},
        "deepseek-chat": {"input": 0.14, "output": 0.28},
        "deepseek-coder": {"input": 0.14, "output": 0.28},
        "qwen-turbo": {"input": 0.3, "output": 0.6},
        "qwen-plus": {"input": 0.8, "output": 2},
        "glm-4-flash": {"input": 0.1, "output": 0.1},  # 有免费额度
        "glm-4": {"input": 1, "output": 1},
    }

    # 默认汇率
    USD_TO_CNY = 7.2

    def __init__(self):
        self.records: List[CallRecord] = []

    def record(self, response: ChatResponse) -> CallRecord:
        """记录一次调用"""
        pricing = self.PRICING_USD.get(
            response.model,
            {"input": 1, "output": 2}  # 默认价格
        )

        input_cost = response.usage["input_tokens"] * pricing["input"] / 1_000_000
        output_cost = response.usage["output_tokens"] * pricing["output"] / 1_000_000
        total_usd = input_cost + output_cost

        record = CallRecord(
            timestamp=datetime.now(),
            model=response.model,
            input_tokens=response.usage["input_tokens"],
            output_tokens=response.usage["output_tokens"],
            cost_usd=total_usd,
            cost_cny=total_usd * self.USD_TO_CNY
        )

        self.records.append(record)
        return record

    @property
    def total_cost_usd(self) -> float:
        return sum(r.cost_usd for r in self.records)

    @property
    def total_cost_cny(self) -> float:
        return sum(r.cost_cny for r in self.records)

    def summary(self) -> dict:
        """生成统计摘要"""
        by_model = {}
        for r in self.records:
            if r.model not in by_model:
                by_model[r.model] = {
                    "calls": 0,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "cost_usd": 0,
                    "cost_cny": 0
                }
            by_model[r.model]["calls"] += 1
            by_model[r.model]["input_tokens"] += r.input_tokens
            by_model[r.model]["output_tokens"] += r.output_tokens
            by_model[r.model]["cost_usd"] += r.cost_usd
            by_model[r.model]["cost_cny"] += r.cost_cny

        return {
            "total_calls": len(self.records),
            "total_input_tokens": sum(r.input_tokens for r in self.records),
            "total_output_tokens": sum(r.output_tokens for r in self.records),
            "total_cost_usd": self.total_cost_usd,
            "total_cost_cny": self.total_cost_cny,
            "by_model": by_model
        }

    def print_report(self):
        """打印成本报告"""
        summary = self.summary()

        print("\n" + "=" * 60)
        print("【成本报告】")
        print("=" * 60)

        print(f"\n总调用次数: {summary['total_calls']}")
        print(f"总输入 Token: {summary['total_input_tokens']:,}")
        print(f"总输出 Token: {summary['total_output_tokens']:,}")
        print(f"总成本: ${summary['total_cost_usd']:.6f} (约 ¥{summary['total_cost_cny']:.4f})")

        if summary['by_model']:
            print("\n按模型统计:")
            print("-" * 60)
            for model, stats in summary['by_model'].items():
                print(f"\n  {model}:")
                print(f"    调用次数: {stats['calls']}")
                print(f"    Token: {stats['input_tokens']:,} 输入 / {stats['output_tokens']:,} 输出")
                print(f"    成本: ${stats['cost_usd']:.6f} (约 ¥{stats['cost_cny']:.4f})")


# 全局 tracker 实例
_global_tracker = None


def get_tracker() -> CostTracker:
    """获取全局 tracker"""
    global _global_tracker
    if _global_tracker is None:
        _global_tracker = CostTracker()
    return _global_tracker


if __name__ == "__main__":
    print("=" * 60)
    print("【成本追踪器演示】")
    print("=" * 60)

    tracker = CostTracker()

    # 测试可用的模型
    test_models = []
    if os.getenv("OPENAI_API_KEY"):
        test_models.append("gpt-4o-mini")
    if os.getenv("DEEPSEEK_API_KEY"):
        test_models.append("deepseek")
    if os.getenv("DASHSCOPE_API_KEY"):
        test_models.append("qwen-turbo")

    if not test_models:
        print("\n未配置任何 API Key，请在 .env 文件中配置")
        exit()

    print(f"\n测试模型: {test_models}")

    messages = [Message(role="user", content="写一首关于编程的短诗，不超过50字")]

    for model_name in test_models:
        print(f"\n调用 {model_name}...")
        try:
            llm = LLMFactory.create(model_name)
            response = llm.chat(messages, max_tokens=100)
            record = tracker.record(response)

            print(f"  回复: {response.content[:50]}...")
            print(f"  Token: {record.input_tokens} 输入 / {record.output_tokens} 输出")
            print(f"  成本: ${record.cost_usd:.6f}")
        except Exception as e:
            print(f"  错误: {e}")

    # 打印报告
    tracker.print_report()
