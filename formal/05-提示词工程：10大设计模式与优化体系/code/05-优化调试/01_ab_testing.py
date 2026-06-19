"""
01_ab_testing.py
Prompt A/B 测试框架
"""
import os
import time
from typing import List, Dict, Callable
from dataclasses import dataclass
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


@dataclass
class TestCase:
    """测试用例"""
    input: str
    expected: str
    tags: List[str] = None


@dataclass
class TestResult:
    """测试结果"""
    prompt_name: str
    input: str
    expected: str
    output: str
    is_correct: bool
    latency_ms: float


class PromptTester:
    """Prompt 测试器"""

    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.results: List[TestResult] = []

    def test_prompt(
        self,
        prompt_template: str,
        prompt_name: str,
        test_cases: List[TestCase],
        evaluator: Callable[[str, str], bool] = None
    ) -> Dict:
        """测试单个 Prompt"""

        if evaluator is None:
            evaluator = lambda output, expected: expected.lower() in output.lower()

        correct = 0
        total_latency = 0
        prompt_results = []

        print(f"\n测试 Prompt: {prompt_name}")
        print("-" * 40)

        for case in test_cases:
            prompt = prompt_template.format(input=case.input)

            start = time.time()
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=50
            )
            latency = (time.time() - start) * 1000

            output = response.choices[0].message.content.strip()
            is_correct = evaluator(output, case.expected)

            if is_correct:
                correct += 1
                status = "✓"
            else:
                status = "✗"

            print(f"{status} 输入: {case.input[:25]:25} | 预期: {case.expected:6} | 输出: {output[:15]}")

            result = TestResult(
                prompt_name=prompt_name,
                input=case.input,
                expected=case.expected,
                output=output,
                is_correct=is_correct,
                latency_ms=latency
            )
            prompt_results.append(result)
            self.results.append(result)
            total_latency += latency

        accuracy = correct / len(test_cases)
        avg_latency = total_latency / len(test_cases)

        print(f"\n准确率: {accuracy:.1%} ({correct}/{len(test_cases)})")
        print(f"平均延迟: {avg_latency:.0f}ms")

        return {
            "prompt_name": prompt_name,
            "accuracy": accuracy,
            "correct": correct,
            "total": len(test_cases),
            "avg_latency_ms": avg_latency,
            "results": prompt_results
        }

    def compare_prompts(
        self,
        prompts: Dict[str, str],
        test_cases: List[TestCase],
        evaluator: Callable = None
    ) -> Dict:
        """对比多个 Prompt"""
        results = {}

        for name, template in prompts.items():
            results[name] = self.test_prompt(
                template, name, test_cases, evaluator
            )

        # 打印对比结果
        print("\n" + "=" * 60)
        print("【A/B 测试结果对比】")
        print("=" * 60)
        print(f"{'Prompt':<20} {'准确率':<10} {'延迟(ms)':<10}")
        print("-" * 40)

        for name, stats in sorted(results.items(), key=lambda x: -x[1]['accuracy']):
            print(f"{name:<20} {stats['accuracy']:.1%}      {stats['avg_latency_ms']:.0f}")

        # 找出最佳 Prompt
        best = max(results.items(), key=lambda x: x[1]['accuracy'])
        print(f"\n推荐使用: {best[0]} (准确率 {best[1]['accuracy']:.1%})")

        return results


# 自定义评估函数
def exact_match(output: str, expected: str) -> bool:
    """精确匹配"""
    return output.strip() == expected.strip()


def contains_match(output: str, expected: str) -> bool:
    """包含匹配"""
    return expected.lower() in output.lower()


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("请设置 OPENAI_API_KEY")
        exit()

    # 定义测试用例
    test_cases = [
        TestCase("这个产品太棒了！", "正面"),
        TestCase("质量差，不推荐", "负面"),
        TestCase("还行吧，一般般", "中性"),
        TestCase("超出预期，非常满意", "正面"),
        TestCase("浪费钱，后悔购买", "负面"),
        TestCase("性价比还可以", "中性"),
        TestCase("物流很快，好评", "正面"),
        TestCase("包装破损，差评", "负面"),
    ]

    # 定义要对比的 Prompt
    prompts = {
        "baseline": "判断情感：{input}",

        "with_options": """判断以下文本的情感（正面/负面/中性）：
{input}
情感：""",

        "few_shot": """判断情感。

示例：
"非常好用" → 正面
"太差了" → 负面
"一般" → 中性

判断："{input}" →""",

        "detailed": """你是情感分析专家。
分析以下评论的情感倾向，只输出"正面"、"负面"或"中性"。

评论：{input}
情感：""",
    }

    # 运行 A/B 测试
    tester = PromptTester()
    results = tester.compare_prompts(prompts, test_cases, contains_match)
