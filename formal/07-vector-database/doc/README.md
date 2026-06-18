# 模块 7：向量数据库

> **学习目标**：掌握向量数据库的核心概念与实践，为 RAG 应用打下基础

---

## 模块概述

本模块深入讲解向量数据库技术，从 Embedding 基础到多种向量数据库的实战应用，帮助你构建高效的语义搜索系统。

---

## 章节目录

| 章节 | 标题 | 核心内容 | 时长 |
|------|------|---------|------|
| 第1章 | [向量与 Embedding 基础](第1章%20·%20向量与%20Embedding%20基础%20—%20理解语义表示的核心.md) | 向量概念、OpenAI Embedding、相似度计算 | 2h |
| 第2章 | [Chroma 向量数据库](第2章%20·%20Chroma%20向量数据库%20—%20轻量级入门首选.md) | CRUD 操作、元数据过滤、持久化、LangChain 集成 | 3h |
| 第3章 | [Milvus 向量数据库](第3章%20·%20Milvus%20向量数据库%20—%20企业级向量检索引擎.md) | Milvus Lite、Schema 设计、索引类型 | 3h |
| 第4章 | [FAISS 向量检索库](第4章%20·%20FAISS%20向量检索库%20—%20Facebook%20高性能检索方案.md) | Flat/IVF/PQ/HNSW 索引、性能优化 | 3h |
| 第5章 | [向量数据库实战应用](第5章%20·%20向量数据库实战应用%20—%20构建完整的语义搜索系统.md) | 文档处理、搜索引擎、结果重排序 | 4h |

**总时长**：约 15 小时

---

## 代码文件清单

### 01-Embedding基础
| 文件 | 说明 |
|------|------|
| `01_openai_embedding.py` | OpenAI Embedding 使用 |
| `02_similarity.py` | 相似度计算（余弦、欧氏、点积） |

### 02-Chroma
| 文件 | 说明 |
|------|------|
| `01_chroma_basic.py` | Chroma 基本 CRUD 操作 |
| `02_chroma_persistent.py` | 持久化存储 |

### 03-Milvus
| 文件 | 说明 |
|------|------|
| `01_milvus_lite.py` | Milvus Lite 快速入门 |

### 04-FAISS
| 文件 | 说明 |
|------|------|
| `01_faiss_basic.py` | FAISS 基本使用 |
| `02_faiss_index.py` | 索引类型对比（Flat/IVF/PQ/HNSW） |

### 05-实战应用
| 文件 | 说明 |
|------|------|
| `01_semantic_search.py` | 完整语义搜索引擎 |

---

## 技术选型指南

| 场景 | 推荐方案 | 理由 |
|------|---------|------|
| 本地开发/原型 | Chroma | 零配置、Python 原生 |
| 嵌入式应用 | FAISS | 纯库、高性能 |
| 生产环境 | Milvus | 分布式、企业级 |
| 快速测试 | Milvus Lite | 无需部署服务 |

---

## 依赖安装

```bash
# 基础依赖
pip install openai python-dotenv numpy

# Chroma
pip install chromadb

# Milvus
pip install pymilvus

# FAISS
pip install faiss-cpu  # 或 faiss-gpu
```

---

## 学习路径

```
向量基础 → Chroma 入门 → Milvus 进阶 → FAISS 优化 → 实战应用
   ↓           ↓            ↓           ↓          ↓
 理解原理   快速上手    企业场景    性能调优   完整系统
```

---

## 核心概念

### Embedding 维度对比

| 模型 | 维度 | 特点 |
|------|------|------|
| text-embedding-3-small | 1536 | 性价比高 |
| text-embedding-3-large | 3072 | 精度更高 |
| BGE-large-zh | 1024 | 中文优化 |

### 索引类型对比

| 索引 | 内存 | 速度 | 精度 | 场景 |
|------|------|------|------|------|
| Flat | 高 | 慢 | 100% | 小数据 |
| IVF | 中 | 快 | 95%+ | 通用 |
| PQ | 低 | 快 | 90%+ | 内存受限 |
| HNSW | 高 | 快 | 98%+ | 高精度 |

---

## 下一步

完成本模块后，继续学习：
- **模块8：RAG 高级技术** - 检索增强生成深入实践
