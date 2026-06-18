"""
02_chroma_persistent.py
Chroma 持久化存储
"""
import chromadb
from pathlib import Path


def persistent_demo():
    """持久化存储演示"""
    print("=" * 60)
    print("【Chroma 持久化存储】")
    print("=" * 60)

    # 创建持久化客户端
    db_path = "./chroma_persistent_db"
    client = chromadb.PersistentClient(path=db_path)

    # 获取或创建集合
    collection = client.get_or_create_collection(
        name="persistent_docs",
        metadata={"description": "持久化文档集合"}
    )

    # 检查是否已有数据
    if collection.count() == 0:
        print("首次运行，添加数据...")
        collection.add(
            documents=[
                "这是第一个持久化文档",
                "这是第二个持久化文档",
                "这是第三个持久化文档",
            ],
            metadatas=[
                {"type": "demo", "index": 1},
                {"type": "demo", "index": 2},
                {"type": "demo", "index": 3},
            ],
            ids=["p1", "p2", "p3"]
        )
        print(f"已添加 {collection.count()} 个文档")
    else:
        print(f"已存在 {collection.count()} 个文档")

    # 查询
    print("\n查询 '持久化':")
    results = collection.query(
        query_texts=["持久化"],
        n_results=2
    )
    for doc, dist in zip(results['documents'][0], results['distances'][0]):
        print(f"  [{dist:.4f}] {doc}")

    print(f"\n数据已保存到: {Path(db_path).absolute()}")


def list_all_collections():
    """列出所有集合"""
    print("\n" + "-" * 40)
    print("所有集合:")

    client = chromadb.PersistentClient(path="./chroma_persistent_db")
    for col in client.list_collections():
        collection = client.get_collection(col.name)
        print(f"  - {col.name}: {collection.count()} 个文档")


def add_more_data():
    """追加数据"""
    print("\n" + "-" * 40)
    print("追加数据:")

    client = chromadb.PersistentClient(path="./chroma_persistent_db")
    collection = client.get_collection("persistent_docs")

    # 获取当前最大 ID
    current_count = collection.count()
    new_id = f"p{current_count + 1}"

    # 检查 ID 是否存在
    existing = collection.get(ids=[new_id])
    if not existing['ids']:
        collection.add(
            documents=[f"这是追加的文档 #{current_count + 1}"],
            metadatas=[{"type": "demo", "index": current_count + 1}],
            ids=[new_id]
        )
        print(f"  已添加文档 {new_id}")
    else:
        print(f"  文档 {new_id} 已存在，跳过")

    print(f"  当前文档总数: {collection.count()}")


if __name__ == "__main__":
    persistent_demo()
    list_all_collections()
    add_more_data()

    print("\n提示: 再次运行程序，数据会被保留")
