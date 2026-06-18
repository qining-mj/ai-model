"""
01_semantic_search.py
完整的语义搜索系统
"""
import os
from typing import List
from dataclasses import dataclass
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()


@dataclass
class SearchResult:
    """搜索结果"""
    content: str
    score: float
    metadata: dict


class SemanticSearchEngine:
    """语义搜索引擎"""

    def __init__(
        self,
        collection_name: str = "documents",
        persist_directory: str = "./search_db"
    ):
        self.client = chromadb.PersistentClient(path=persist_directory)

        # 根据是否有 OpenAI API Key 选择 Embedding 函数
        if os.getenv("OPENAI_API_KEY"):
            self.embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
                api_key=os.getenv("OPENAI_API_KEY"),
                model_name="text-embedding-3-small"
            )
        else:
            # 使用默认的 sentence-transformer
            self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn
        )

    def add_documents(
        self,
        documents: List[str],
        metadatas: List[dict] = None,
        ids: List[str] = None
    ):
        """添加文档"""
        if ids is None:
            start_id = self.collection.count()
            ids = [f"doc_{start_id + i}" for i in range(len(documents))]

        if metadatas is None:
            metadatas = [{}] * len(documents)

        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"已添加 {len(documents)} 个文档，总数: {self.collection.count()}")

    def search(
        self,
        query: str,
        n_results: int = 5,
        where: dict = None
    ) -> List[SearchResult]:
        """搜索"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where
        )

        search_results = []
        if results['documents'] and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                search_results.append(SearchResult(
                    content=results['documents'][0][i],
                    score=1 - results['distances'][0][i],
                    metadata=results['metadatas'][0][i] if results['metadatas'] else {}
                ))

        return search_results

    def delete_collection(self):
        """删除集合"""
        self.client.delete_collection(self.collection.name)
        print(f"已删除集合: {self.collection.name}")


def demo():
    """演示"""
    print("=" * 60)
    print("【语义搜索引擎演示】")
    print("=" * 60)

    # 创建搜索引擎
    engine = SemanticSearchEngine(
        collection_name="demo_search",
        persist_directory="./demo_search_db"
    )

    # 示例文档
    documents = [
        "Python 是一种广泛使用的高级编程语言，以简洁易读著称",
        "机器学习是人工智能的核心技术，通过数据训练模型",
        "深度学习使用多层神经网络处理复杂任务",
        "自然语言处理让计算机理解人类语言",
        "向量数据库是实现语义搜索的关键基础设施",
        "大语言模型如 GPT 可以生成高质量的文本内容",
        "RAG 技术结合检索和生成，提升 AI 应用效果",
        "JavaScript 是网页开发的主要编程语言",
        "Docker 容器技术简化了应用部署",
        "Kubernetes 是容器编排的行业标准",
    ]

    metadatas = [
        {"category": "programming", "topic": "python"},
        {"category": "ai", "topic": "ml"},
        {"category": "ai", "topic": "dl"},
        {"category": "ai", "topic": "nlp"},
        {"category": "database", "topic": "vector"},
        {"category": "ai", "topic": "llm"},
        {"category": "ai", "topic": "rag"},
        {"category": "programming", "topic": "javascript"},
        {"category": "devops", "topic": "docker"},
        {"category": "devops", "topic": "kubernetes"},
    ]

    # 添加文档（如果集合为空）
    if engine.collection.count() == 0:
        engine.add_documents(documents, metadatas)

    # 搜索测试
    queries = [
        ("人工智能技术", None),
        ("编程语言", None),
        ("容器技术", None),
        ("AI 应用", {"category": "ai"}),
    ]

    for query, where in queries:
        print(f"\n{'='*50}")
        filter_info = f" (过滤: {where})" if where else ""
        print(f"搜索: '{query}'{filter_info}")
        print("-" * 50)

        results = engine.search(query, n_results=3, where=where)

        if results:
            for i, r in enumerate(results, 1):
                print(f"{i}. [相似度: {r.score:.3f}] {r.content[:50]}...")
                print(f"   元数据: {r.metadata}")
        else:
            print("  无结果")


if __name__ == "__main__":
    demo()
