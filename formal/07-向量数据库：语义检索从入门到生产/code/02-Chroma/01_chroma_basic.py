"""
01_chroma_basic.py
Chroma 基本操作
"""
import chromadb


def basic_operations():
    """基本 CRUD 操作"""
    print("=" * 60)
    print("【Chroma 基本操作】")
    print("=" * 60)

    # 1. 创建内存客户端
    client = chromadb.Client()

    # 2. 创建集合
    collection = client.create_collection(
        name="demo_collection",
        metadata={"description": "演示集合"}
    )
    print(f"创建集合: {collection.name}")

    # 3. 添加数据
    collection.add(
        documents=[
            "Python 是一种编程语言",
            "机器学习需要大量数据",
            "深度学习使用神经网络",
            "JavaScript 用于网页开发",
            "向量数据库存储高维向量",
        ],
        metadatas=[
            {"category": "programming", "lang": "python"},
            {"category": "ai", "topic": "ml"},
            {"category": "ai", "topic": "dl"},
            {"category": "programming", "lang": "javascript"},
            {"category": "database", "topic": "vector"},
        ],
        ids=["doc1", "doc2", "doc3", "doc4", "doc5"]
    )
    print(f"添加了 {collection.count()} 个文档")

    # 4. 查询
    print("\n" + "-" * 40)
    print("查询: '人工智能技术'")
    results = collection.query(
        query_texts=["人工智能技术"],
        n_results=3
    )

    for i, (doc, dist, meta) in enumerate(zip(
        results['documents'][0],
        results['distances'][0],
        results['metadatas'][0]
    )):
        print(f"  {i+1}. [{dist:.4f}] {doc}")
        print(f"       metadata: {meta}")

    # 5. 获取特定文档
    print("\n" + "-" * 40)
    print("获取 doc1:")
    doc = collection.get(ids=["doc1"])
    print(f"  内容: {doc['documents'][0]}")
    print(f"  元数据: {doc['metadatas'][0]}")

    # 6. 更新文档
    collection.update(
        ids=["doc1"],
        documents=["Python 是最流行的编程语言之一"],
        metadatas=[{"category": "programming", "lang": "python", "updated": True}]
    )
    print("\n已更新 doc1")

    # 7. 删除文档
    collection.delete(ids=["doc4"])
    print(f"删除后文档数: {collection.count()}")

    # 8. 列出所有集合
    print("\n所有集合:")
    for col in client.list_collections():
        print(f"  - {col.name}")

    # 9. 删除集合
    client.delete_collection("demo_collection")
    print("\n已删除集合 demo_collection")


def metadata_filter():
    """元数据过滤"""
    print("\n" + "=" * 60)
    print("【元数据过滤】")
    print("=" * 60)

    client = chromadb.Client()
    collection = client.create_collection("filter_demo")

    # 添加数据
    collection.add(
        documents=[
            "Python 基础教程",
            "Python 高级编程",
            "JavaScript 入门",
            "机器学习实战",
            "深度学习入门",
        ],
        metadatas=[
            {"category": "programming", "level": "beginner", "year": 2023},
            {"category": "programming", "level": "advanced", "year": 2024},
            {"category": "programming", "level": "beginner", "year": 2023},
            {"category": "ai", "level": "intermediate", "year": 2024},
            {"category": "ai", "level": "beginner", "year": 2024},
        ],
        ids=["1", "2", "3", "4", "5"]
    )

    # 等值过滤
    print("\n1. category = 'ai':")
    results = collection.query(
        query_texts=["学习"],
        n_results=5,
        where={"category": "ai"}
    )
    for doc in results['documents'][0]:
        print(f"  - {doc}")

    # AND 条件
    print("\n2. category='programming' AND level='beginner':")
    results = collection.query(
        query_texts=["教程"],
        n_results=5,
        where={
            "$and": [
                {"category": "programming"},
                {"level": "beginner"}
            ]
        }
    )
    for doc in results['documents'][0]:
        print(f"  - {doc}")

    # 比较运算
    print("\n3. year >= 2024:")
    results = collection.get(
        where={"year": {"$gte": 2024}}
    )
    for doc in results['documents']:
        print(f"  - {doc}")


if __name__ == "__main__":
    basic_operations()
    metadata_filter()
