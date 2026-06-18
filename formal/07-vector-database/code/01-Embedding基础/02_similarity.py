"""
02_similarity.py
向量相似度计算
"""
import numpy as np
from typing import List


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    余弦相似度
    范围: [-1, 1]
    1 = 完全相同方向
    0 = 正交
    -1 = 完全相反
    """
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)


def euclidean_distance(vec1: List[float], vec2: List[float]) -> float:
    """
    欧氏距离
    范围: [0, +∞)
    越小越相似
    """
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.linalg.norm(vec1 - vec2)


def dot_product(vec1: List[float], vec2: List[float]) -> float:
    """
    点积（内积）
    对于归一化向量，等价于余弦相似度
    """
    return np.dot(vec1, vec2)


def normalize(vec: List[float]) -> np.ndarray:
    """L2 归一化"""
    vec = np.array(vec)
    return vec / np.linalg.norm(vec)


def demo_similarity():
    """相似度演示"""
    print("=" * 60)
    print("【向量相似度计算】")
    print("=" * 60)

    # 创建测试向量
    vec1 = [1.0, 2.0, 3.0]
    vec2 = [1.0, 2.0, 3.1]  # 与 vec1 非常相似
    vec3 = [-1.0, -2.0, -3.0]  # 与 vec1 完全相反
    vec4 = [3.0, -1.0, 2.0]  # 与 vec1 正交（近似）

    print("\n测试向量:")
    print(f"  vec1 = {vec1}")
    print(f"  vec2 = {vec2} (相似)")
    print(f"  vec3 = {vec3} (相反)")
    print(f"  vec4 = {vec4} (不同方向)")

    # 余弦相似度
    print("\n【余弦相似度】(范围 -1 到 1)")
    print(f"  vec1 vs vec2: {cosine_similarity(vec1, vec2):.4f}")
    print(f"  vec1 vs vec3: {cosine_similarity(vec1, vec3):.4f}")
    print(f"  vec1 vs vec4: {cosine_similarity(vec1, vec4):.4f}")

    # 欧氏距离
    print("\n【欧氏距离】(越小越相似)")
    print(f"  vec1 vs vec2: {euclidean_distance(vec1, vec2):.4f}")
    print(f"  vec1 vs vec3: {euclidean_distance(vec1, vec3):.4f}")
    print(f"  vec1 vs vec4: {euclidean_distance(vec1, vec4):.4f}")

    # 归一化后的点积
    print("\n【归一化后点积】(等价于余弦相似度)")
    vec1_norm = normalize(vec1)
    vec2_norm = normalize(vec2)
    print(f"  vec1 vs vec2: {dot_product(vec1_norm, vec2_norm):.4f}")


def demo_with_openai():
    """使用 OpenAI Embedding 测试相似度"""
    import os
    from openai import OpenAI

    if not os.getenv("OPENAI_API_KEY"):
        print("\n跳过 OpenAI 演示（未设置 API Key）")
        return

    print("\n" + "=" * 60)
    print("【OpenAI Embedding 相似度测试】")
    print("=" * 60)

    client = OpenAI()

    texts = [
        "我喜欢吃苹果",
        "我爱吃水果",
        "今天天气真好",
        "Python 是编程语言",
    ]

    # 获取 Embedding
    response = client.embeddings.create(
        input=texts,
        model="text-embedding-3-small"
    )
    embeddings = [item.embedding for item in response.data]

    # 计算相似度矩阵
    print("\n相似度矩阵:")
    print(f"{'':20}", end="")
    for i, t in enumerate(texts):
        print(f"[{i}]{t[:6]:8}", end="")
    print()

    for i, t1 in enumerate(texts):
        print(f"[{i}] {t1[:15]:15}", end="")
        for j, t2 in enumerate(texts):
            sim = cosine_similarity(embeddings[i], embeddings[j])
            print(f"{sim:8.3f}", end="  ")
        print()


if __name__ == "__main__":
    demo_similarity()
    demo_with_openai()
