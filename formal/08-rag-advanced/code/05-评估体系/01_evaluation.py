"""
01_evaluation.py
RAG 评估
"""
import os
import json
from typing import List, Set
import numpy as np
from openai import OpenAI


# ============ 检索评估 ============

def recall_at_k(retrieved: List[str], relevant: Set[str], k: int) -> float:
    """Recall@K"""
    retrieved_k = set(retrieved[:k])
    hits = len(retrieved_k & relevant)
    return hits / len(relevant) if relevant else 0.0


def precision_at_k(retrieved: List[str], relevant: Set[str], k: int) -> float:
    """Precision@K"""
    retrieved_k = set(retrieved[:k])
    hits = len(retrieved_k & relevant)
    return hits / k


def mrr(retrieved: List[str], relevant: Set[str]) -> float:
    """Mean Reciprocal Rank"""
    for i, doc_id in enumerate(retrieved, 1):
        if doc_id in relevant:
            return 1.0 / i
    return 0.0


def evaluate_retrieval(retrieved_ids: List[str], relevant_ids: Set[str]):
    """综合评估检索"""
    print("=" * 60)
    print("【检索评估】")
    print("=" * 60)

    print(f"\n检索结果: {retrieved_ids}")
    print(f"相关文档: {relevant_ids}")

    metrics = {
        "Recall@3": recall_at_k(retrieved_ids, relevant_ids, 3),
        "Recall@5": recall_at_k(retrieved_ids, relevant_ids, 5),
        "Precision@3": precision_at_k(retrieved_ids, relevant_ids, 3),
        "Precision@5": precision_at_k(retrieved_ids, relevant_ids, 5),
        "MRR": mrr(retrieved_ids, relevant_ids),
    }

    print("\n评估结果:")
    for name, value in metrics.items():
        print(f"  {name}: {value:.4f}")

    return metrics


# ============ 生成评估 ============

class GenerationEvaluator:
    """生成质量评估器"""

    def __init__(self):
        self.client = OpenAI()

    def evaluate_faithfulness(self, answer: str, context: str) -> dict:
        """评估忠实度"""
        prompt = f"""评估回答是否忠实于上下文（0-1分）。

上下文：{context}
回答：{answer}

返回 JSON: {{"score": 分数, "reason": "理由"}}"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    def evaluate_relevancy(self, question: str, answer: str) -> dict:
        """评估相关性"""
        prompt = f"""评估回答与问题的相关性（0-1分）。

问题：{question}
回答：{answer}

返回 JSON: {{"score": 分数, "reason": "理由"}}"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)


def evaluate_generation():
    """生成评估演示"""
    print("\n" + "=" * 60)
    print("【生成评估】")
    print("=" * 60)

    evaluator = GenerationEvaluator()

    question = "LangChain 是什么？"
    context = "LangChain 是一个用于开发 LLM 应用的开源框架。"
    answer = "LangChain 是一个帮助开发者构建大语言模型应用的框架。"

    print(f"\n问题: {question}")
    print(f"上下文: {context}")
    print(f"回答: {answer}")

    faithfulness = evaluator.evaluate_faithfulness(answer, context)
    relevancy = evaluator.evaluate_relevancy(question, answer)

    print("\n评估结果:")
    print(f"  忠实度: {faithfulness['score']:.2f} - {faithfulness['reason']}")
    print(f"  相关性: {relevancy['score']:.2f} - {relevancy['reason']}")


if __name__ == "__main__":
    # 检索评估演示
    retrieved = ["doc1", "doc3", "doc5", "doc2", "doc7"]
    relevant = {"doc1", "doc2", "doc4"}
    evaluate_retrieval(retrieved, relevant)

    # 生成评估演示
    if os.getenv("OPENAI_API_KEY"):
        evaluate_generation()
    else:
        print("\n跳过生成评估（需要 OPENAI_API_KEY）")
