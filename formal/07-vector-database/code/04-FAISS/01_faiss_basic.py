"""
01_faiss_basic.py
FAISS 基本使用
"""
import numpy as np
import faiss


def basic_usage():
    """FAISS 基本操作"""
    print("=" * 60)
    print("【FAISS 基本使用】")
    print("=" * 60)

    # 1. 准备数据
    d = 128  # 向量维度
    nb = 10000  # 数据库大小
    nq = 5  # 查询数量

    np.random.seed(42)
    xb = np.random.random((nb, d)).astype('float32')  # 数据库向量
    xq = np.random.random((nq, d)).astype('float32')  # 查询向量

    print(f"数据库: {nb} 个 {d} 维向量")
    print(f"查询: {nq} 个向量")

    # 2. 创建索引（Flat = 暴力搜索）
    index = faiss.IndexFlatL2(d)  # L2 距离

    # 3. 添加向量
    index.add(xb)
    print(f"\n索引中向量数: {index.ntotal}")

    # 4. 搜索
    k = 4  # 返回最近的 k 个
    distances, indices = index.search(xq, k)

    print(f"\n搜索 top-{k} 结果:")
    for i in range(min(3, nq)):  # 只显示前3个查询
        print(f"  查询 {i}:")
        print(f"    最近邻索引: {indices[i]}")
        print(f"    距离: {distances[i]}")

    # 5. 验证：搜索数据库中的向量
    print("\n验证（搜索数据库中的向量）:")
    D, I = index.search(xb[:3], k=1)
    print(f"  输入索引: [0, 1, 2]")
    print(f"  搜索结果: {I.flatten()}")
    print(f"  距离: {D.flatten()} (应该全为0)")


def index_with_ids():
    """带 ID 的索引"""
    print("\n" + "=" * 60)
    print("【带 ID 的索引】")
    print("=" * 60)

    d = 64
    n = 1000

    np.random.seed(42)
    xb = np.random.random((n, d)).astype('float32')

    # 自定义 ID（不是从0开始）
    ids = np.arange(1000, 1000 + n).astype('int64')

    # 创建支持 ID 的索引
    index = faiss.IndexFlatL2(d)
    index_with_ids = faiss.IndexIDMap(index)

    # 添加数据
    index_with_ids.add_with_ids(xb, ids)
    print(f"添加了 {index_with_ids.ntotal} 个向量")
    print(f"ID 范围: {ids[0]} - {ids[-1]}")

    # 搜索
    xq = np.random.random((1, d)).astype('float32')
    D, I = index_with_ids.search(xq, 3)

    print(f"\n搜索结果 ID: {I[0]}")
    print(f"距离: {D[0]}")


def different_metrics():
    """不同距离度量"""
    print("\n" + "=" * 60)
    print("【不同距离度量】")
    print("=" * 60)

    d = 64
    n = 1000

    np.random.seed(42)
    data = np.random.random((n, d)).astype('float32')
    query = np.random.random((1, d)).astype('float32')

    # L2 距离（欧氏距离）
    print("\n1. L2 距离（欧氏距离）:")
    index_l2 = faiss.IndexFlatL2(d)
    index_l2.add(data)
    D_l2, I_l2 = index_l2.search(query, 3)
    print(f"   最近邻: {I_l2[0]}")
    print(f"   距离: {D_l2[0]}")

    # 内积（点积）
    print("\n2. 内积（需要归一化才等价于余弦相似度）:")

    # 归一化数据
    data_normalized = data.copy()
    query_normalized = query.copy()
    faiss.normalize_L2(data_normalized)
    faiss.normalize_L2(query_normalized)

    index_ip = faiss.IndexFlatIP(d)  # Inner Product
    index_ip.add(data_normalized)
    D_ip, I_ip = index_ip.search(query_normalized, 3)
    print(f"   最近邻: {I_ip[0]}")
    print(f"   相似度: {D_ip[0]} (余弦相似度)")


if __name__ == "__main__":
    basic_usage()
    index_with_ids()
    different_metrics()
