"""
01_retrieval_strategies.py
检索策略对比
"""
import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings


def create_vectorstore():
    """创建示例向量存储"""
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    texts = [
        "Python 是一种通用编程语言",
        "Python 语法简洁易读",
        "Python 适合初学者学习",
        "Python 广泛用于数据科学",
        "Java 是企业级开发语言",
        "JavaScript 是网页开发语言",
        "机器学习经常使用 Python",
        "深度学习需要大量计算资源",
    ]

    return Chroma.from_texts(texts, embeddings)


def similarity_search_demo(vectorstore):
    """相似度搜索"""
    print("=" * 60)
    print("【相似度搜索】")
    print("=" * 60)

    query = "Python 编程"

    # 基本搜索
    results = vectorstore.similarity_search(query, k=4)
    print(f"\n查询: {query}")
    print("\n结果:")
    for i, doc in enumerate(results, 1):
        print(f"  {i}. {doc.page_content}")

    # 带分数的搜索
    results_with_scores = vectorstore.similarity_search_with_score(query, k=4)
    print("\n带分数的结果:")
    for doc, score in results_with_scores:
        print(f"  [{score:.4f}] {doc.page_content}")


def mmr_search_demo(vectorstore):
    """MMR 搜索（增加多样性）"""
    print("\n" + "=" * 60)
    print("【MMR 搜索 - 增加多样性】")
    print("=" * 60)

    query = "Python"

    # 普通搜索
    print(f"\n查询: {query}")
    print("\n普通相似度搜索 (可能结果相似):")
    results = vectorstore.similarity_search(query, k=4)
    for doc in results:
        print(f"  - {doc.page_content}")

    # MMR 搜索
    print("\nMMR 搜索 (增加多样性):")
    results = vectorstore.max_marginal_relevance_search(
        query,
        k=4,
        fetch_k=8,
        lambda_mult=0.5  # 0=最大多样性, 1=纯相似度
    )
    for doc in results:
        print(f"  - {doc.page_content}")


def filter_search_demo(vectorstore):
    """带元数据过滤的搜索"""
    print("\n" + "=" * 60)
    print("【带过滤的搜索】")
    print("=" * 60)

    # 创建带元数据的向量存储
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    texts = [
        "Python 基础教程",
        "Python 高级编程",
        "Java 入门指南",
        "机器学习实战",
    ]

    metadatas = [
        {"category": "programming", "level": "beginner"},
        {"category": "programming", "level": "advanced"},
        {"category": "programming", "level": "beginner"},
        {"category": "ai", "level": "intermediate"},
    ]

    vs = Chroma.from_texts(texts, embeddings, metadatas=metadatas)

    query = "编程学习"

    print(f"\n查询: {query}")

    # 无过滤
    print("\n无过滤:")
    for doc in vs.similarity_search(query, k=3):
        print(f"  - {doc.page_content}")

    # 带过滤
    print("\n过滤 (level=beginner):")
    for doc in vs.similarity_search(query, k=3, filter={"level": "beginner"}):
        print(f"  - {doc.page_content}")


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("请设置 OPENAI_API_KEY")
        exit()

    vectorstore = create_vectorstore()
    similarity_search_demo(vectorstore)
    mmr_search_demo(vectorstore)
    filter_search_demo(vectorstore)
