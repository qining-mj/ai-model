"""
01_openai_embedding.py
使用 OpenAI 生成 Embedding
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def get_embedding(text: str, model: str = "text-embedding-3-small") -> list:
    """获取文本的 Embedding 向量"""
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding


def batch_embedding(texts: list, model: str = "text-embedding-3-small") -> list:
    """批量获取 Embedding"""
    response = client.embeddings.create(
        input=texts,
        model=model
    )
    return [item.embedding for item in response.data]


def demo_single():
    """单个文本 Embedding"""
    print("=" * 60)
    print("【单个文本 Embedding】")
    print("=" * 60)

    text = "人工智能正在改变世界"
    embedding = get_embedding(text)

    print(f"文本: {text}")
    print(f"向量维度: {len(embedding)}")
    print(f"向量前5个值: {embedding[:5]}")
    print(f"向量后5个值: {embedding[-5:]}")


def demo_batch():
    """批量 Embedding"""
    print("\n" + "=" * 60)
    print("【批量 Embedding】")
    print("=" * 60)

    texts = [
        "机器学习是AI的子领域",
        "深度学习使用神经网络",
        "自然语言处理理解人类语言",
        "今天天气很好"
    ]

    embeddings = batch_embedding(texts)

    for text, emb in zip(texts, embeddings):
        print(f"\n{text}")
        print(f"  维度: {len(emb)}, 前3值: {emb[:3]}")


def demo_model_comparison():
    """模型对比"""
    print("\n" + "=" * 60)
    print("【Embedding 模型对比】")
    print("=" * 60)

    text = "向量数据库用于存储和检索高维向量"

    models = [
        "text-embedding-3-small",
        "text-embedding-3-large",
    ]

    for model in models:
        try:
            emb = get_embedding(text, model)
            print(f"\n{model}:")
            print(f"  维度: {len(emb)}")
        except Exception as e:
            print(f"\n{model}: 错误 - {e}")


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("请设置 OPENAI_API_KEY 环境变量")
        exit()

    demo_single()
    demo_batch()
    demo_model_comparison()
