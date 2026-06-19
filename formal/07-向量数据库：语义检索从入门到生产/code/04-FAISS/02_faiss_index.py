"""
02_faiss_index.py
FAISS 索引类型
"""
import numpy as np
import faiss
import time


def flat_index():
    """Flat 索引（精确搜索）"""
    print("=" * 60)
    print("【Flat 索引 - 精确搜索】")
    print("=" * 60)

    d = 128
    nb = 100000

    np.random.seed(42)
    xb = np.random.random((nb, d)).astype('float32')
    xq = np.random.random((10, d)).astype('float32')

    # 创建 Flat 索引
    index = faiss.IndexFlatL2(d)
    index.add(xb)

    # 搜索
    start = time.time()
    D, I = index.search(xq, 5)
    elapsed = (time.time() - start) * 1000

    print(f"数据量: {nb}")
    print(f"搜索时间: {elapsed:.2f}ms")
    print(f"第一个查询结果: {I[0]}")


def ivf_index():
    """IVF 索引（倒排索引）"""
    print("\n" + "=" * 60)
    print("【IVF 索引 - 倒排索引】")
    print("=" * 60)

    d = 128
    nb = 100000

    np.random.seed(42)
    xb = np.random.random((nb, d)).astype('float32')
    xq = np.random.random((10, d)).astype('float32')

    # 创建 IVF 索引
    nlist = 100  # 聚类中心数
    quantizer = faiss.IndexFlatL2(d)
    index = faiss.IndexIVFFlat(quantizer, d, nlist)

    # 训练
    print("训练索引...")
    index.train(xb)

    # 添加数据
    index.add(xb)
    print(f"索引大小: {index.ntotal}")

    # 测试不同 nprobe 的效果
    print("\nnprobe 对比:")
    print(f"{'nprobe':<10} {'时间(ms)':<12} {'召回率':<10}")
    print("-" * 35)

    # 获取 Flat 索引结果作为基准
    flat_index = faiss.IndexFlatL2(d)
    flat_index.add(xb)
    D_flat, I_flat = flat_index.search(xq, 5)

    for nprobe in [1, 10, 50, 100]:
        index.nprobe = nprobe

        start = time.time()
        D, I = index.search(xq, 5)
        elapsed = (time.time() - start) * 1000

        # 计算召回率
        recall = np.mean([
            len(set(I[i]) & set(I_flat[i])) / 5
            for i in range(len(xq))
        ])

        print(f"{nprobe:<10} {elapsed:<12.2f} {recall:<10.2%}")


def pq_index():
    """PQ 索引（乘积量化 - 压缩存储）"""
    print("\n" + "=" * 60)
    print("【PQ 索引 - 压缩存储】")
    print("=" * 60)

    d = 128
    nb = 100000

    np.random.seed(42)
    xb = np.random.random((nb, d)).astype('float32')
    xq = np.random.random((10, d)).astype('float32')

    # 创建 IVF + PQ 索引
    nlist = 100
    m = 8  # 子向量数（d 必须能被 m 整除）

    quantizer = faiss.IndexFlatL2(d)
    index = faiss.IndexIVFPQ(quantizer, d, nlist, m, 8)

    # 训练
    print("训练索引...")
    index.train(xb)
    index.add(xb)

    # 内存对比
    flat_size = nb * d * 4  # float32 = 4 bytes
    pq_size = nb * m  # 每个向量只需 m bytes

    print(f"\n内存对比:")
    print(f"  Flat 索引: {flat_size / 1e6:.2f} MB")
    print(f"  IVF-PQ 索引: 约 {pq_size / 1e6:.2f} MB")
    print(f"  压缩比: {flat_size / pq_size:.1f}x")

    # 搜索
    index.nprobe = 10
    D, I = index.search(xq, 5)
    print(f"\n搜索结果（第一个查询）: {I[0]}")


def hnsw_index():
    """HNSW 索引（图索引 - 高召回）"""
    print("\n" + "=" * 60)
    print("【HNSW 索引 - 图索引】")
    print("=" * 60)

    d = 128
    nb = 100000

    np.random.seed(42)
    xb = np.random.random((nb, d)).astype('float32')
    xq = np.random.random((10, d)).astype('float32')

    # 创建 HNSW 索引
    M = 32  # 每层连接数
    index = faiss.IndexHNSWFlat(d, M)
    index.hnsw.efConstruction = 40

    # 添加数据
    print("构建索引...")
    start = time.time()
    index.add(xb)
    print(f"构建时间: {time.time() - start:.2f}s")

    # 测试不同 efSearch 的效果
    print("\nefSearch 对比:")

    flat_index = faiss.IndexFlatL2(d)
    flat_index.add(xb)
    D_flat, I_flat = flat_index.search(xq, 5)

    for ef in [16, 32, 64, 128]:
        index.hnsw.efSearch = ef

        start = time.time()
        D, I = index.search(xq, 5)
        elapsed = (time.time() - start) * 1000

        recall = np.mean([
            len(set(I[i]) & set(I_flat[i])) / 5
            for i in range(len(xq))
        ])

        print(f"  efSearch={ef}: 时间={elapsed:.2f}ms, 召回率={recall:.2%}")


if __name__ == "__main__":
    flat_index()
    ivf_index()
    pq_index()
    hnsw_index()
