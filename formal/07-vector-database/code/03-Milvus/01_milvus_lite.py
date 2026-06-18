"""
01_milvus_lite.py
Milvus Lite 快速入门

Milvus Lite 是 Milvus 的轻量版本，无需部署服务器。
适合本地开发和测试。
"""
import random
from pymilvus import MilvusClient


def milvus_lite_demo():
    """Milvus Lite 演示"""
    print("=" * 60)
    print("【Milvus Lite 快速入门】")
    print("=" * 60)

    # 创建客户端（本地文件存储）
    client = MilvusClient("./milvus_lite_demo.db")

    collection_name = "demo_collection"

    # 删除已存在的集合
    if client.has_collection(collection_name):
        client.drop_collection(collection_name)
        print(f"已删除旧集合: {collection_name}")

    # 创建集合
    client.create_collection(
        collection_name=collection_name,
        dimension=128
    )
    print(f"创建集合: {collection_name}")

    # 准备数据
    data = [
        {
            "id": i,
            "vector": [random.random() for _ in range(128)],
            "text": f"这是第 {i} 个文档",
            "category": "A" if i % 2 == 0 else "B"
        }
        for i in range(100)
    ]

    # 插入数据
    client.insert(collection_name=collection_name, data=data)
    print(f"已插入 {len(data)} 条数据")

    # 搜索
    print("\n" + "-" * 40)
    print("向量搜索:")

    query_vector = [random.random() for _ in range(128)]
    results = client.search(
        collection_name=collection_name,
        data=[query_vector],
        limit=5,
        output_fields=["text", "category"]
    )

    for result in results[0]:
        print(f"  ID: {result['id']}, 距离: {result['distance']:.4f}")
        print(f"      text: {result['entity']['text']}")
        print(f"      category: {result['entity']['category']}")

    # 带过滤的搜索
    print("\n" + "-" * 40)
    print("带过滤的搜索 (category = 'A'):")

    results = client.search(
        collection_name=collection_name,
        data=[query_vector],
        filter="category == 'A'",
        limit=3,
        output_fields=["text", "category"]
    )

    for result in results[0]:
        print(f"  ID: {result['id']}, category: {result['entity']['category']}")

    # 查询（非向量查询）
    print("\n" + "-" * 40)
    print("标量查询 (id < 5):")

    results = client.query(
        collection_name=collection_name,
        filter="id < 5",
        output_fields=["id", "text", "category"]
    )

    for r in results:
        print(f"  {r}")

    # 删除数据
    client.delete(
        collection_name=collection_name,
        filter="category == 'B'"
    )
    print("\n已删除 category='B' 的数据")

    # 统计
    stats = client.get_collection_stats(collection_name)
    print(f"集合统计: {stats}")

    # 关闭客户端
    client.close()
    print("\n已关闭客户端")


if __name__ == "__main__":
    milvus_lite_demo()
