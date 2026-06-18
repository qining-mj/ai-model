"""
qa_system.py
企业知识库问答系统 - 完整实现
"""
import os
from pathlib import Path
from typing import List, Tuple, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import (
    TextLoader, PyPDFLoader, Docx2txtLoader, UnstructuredMarkdownLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()


@dataclass
class Config:
    """配置"""
    LLM_MODEL: str = "gpt-4o-mini"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    COLLECTION_NAME: str = "knowledge_base"
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    RETRIEVAL_K: int = 4


config = Config()


class DocumentLoader:
    """文档加载器"""

    LOADERS = {
        ".txt": TextLoader,
        ".pdf": PyPDFLoader,
        ".docx": Docx2txtLoader,
        ".md": UnstructuredMarkdownLoader,
    }

    def load_file(self, file_path: str) -> List[Document]:
        """加载单个文件"""
        path = Path(file_path)
        ext = path.suffix.lower()

        if ext not in self.LOADERS:
            raise ValueError(f"不支持的文件类型: {ext}")

        loader_cls = self.LOADERS[ext]
        loader = loader_cls(str(path))
        documents = loader.load()

        for doc in documents:
            doc.metadata["source"] = path.name
            doc.metadata["file_type"] = ext

        return documents

    def load_directory(self, dir_path: str) -> List[Document]:
        """加载目录"""
        all_documents = []
        path = Path(dir_path)

        for ext in self.LOADERS.keys():
            for file_path in path.glob(f"**/*{ext}"):
                try:
                    docs = self.load_file(str(file_path))
                    all_documents.extend(docs)
                    print(f"  加载: {file_path.name} ({len(docs)} 个文档)")
                except Exception as e:
                    print(f"  跳过: {file_path.name} - {e}")

        return all_documents


class VectorStoreManager:
    """向量存储管理器"""

    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model=config.EMBEDDING_MODEL)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP
        )
        self._vectorstore: Optional[Chroma] = None

    @property
    def vectorstore(self) -> Chroma:
        if self._vectorstore is None:
            self._vectorstore = Chroma(
                collection_name=config.COLLECTION_NAME,
                embedding_function=self.embeddings,
                persist_directory=config.CHROMA_PERSIST_DIR
            )
        return self._vectorstore

    def add_documents(self, documents: List[Document]) -> int:
        """添加文档"""
        chunks = self.text_splitter.split_documents(documents)
        print(f"分块: {len(documents)} 个文档 -> {len(chunks)} 个块")
        self.vectorstore.add_documents(chunks)
        return len(chunks)

    def search(self, query: str, k: int = None) -> List[Document]:
        """搜索"""
        k = k or config.RETRIEVAL_K
        return self.vectorstore.similarity_search(query, k=k)

    def get_retriever(self):
        """获取检索器"""
        return self.vectorstore.as_retriever(
            search_kwargs={"k": config.RETRIEVAL_K}
        )


class QASystem:
    """问答系统"""

    def __init__(self):
        self.llm = ChatOpenAI(model=config.LLM_MODEL, temperature=0)
        self.vectorstore_manager = VectorStoreManager()
        self.doc_loader = DocumentLoader()
        self.chat_history: List[Tuple[str, str]] = []

        self.qa_prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个知识库问答助手。基于提供的上下文回答问题。

规则：
1. 只使用上下文中的信息回答
2. 如果上下文不足以回答，明确说明
3. 回答时引用来源（如：根据[文档名]...）
4. 保持回答简洁准确

上下文：
{context}"""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}")
        ])

    def index_directory(self, dir_path: str) -> int:
        """索引目录"""
        print(f"\n索引目录: {dir_path}")
        docs = self.doc_loader.load_directory(dir_path)
        if not docs:
            print("没有找到文档")
            return 0
        return self.vectorstore_manager.add_documents(docs)

    def _format_docs(self, docs) -> str:
        """格式化文档"""
        formatted = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source", "未知")
            formatted.append(f"[{i}] 来源: {source}\n{doc.page_content}")
        return "\n\n".join(formatted)

    def _get_chat_history(self):
        """获取对话历史"""
        messages = []
        for human, ai in self.chat_history[-5:]:
            messages.append(HumanMessage(content=human))
            messages.append(AIMessage(content=ai))
        return messages

    def ask(self, question: str) -> dict:
        """问答"""
        retriever = self.vectorstore_manager.get_retriever()
        docs = retriever.invoke(question)

        chain = (
            {
                "context": lambda x: self._format_docs(docs),
                "chat_history": lambda x: self._get_chat_history(),
                "question": RunnablePassthrough()
            }
            | self.qa_prompt
            | self.llm
            | StrOutputParser()
        )

        answer = chain.invoke(question)
        self.chat_history.append((question, answer))

        return {
            "question": question,
            "answer": answer,
            "sources": [
                {
                    "content": doc.page_content[:200] + "...",
                    "source": doc.metadata.get("source", "未知")
                }
                for doc in docs
            ]
        }

    def clear_history(self):
        """清除历史"""
        self.chat_history = []


def demo():
    """演示"""
    print("=" * 60)
    print("【企业知识库问答系统】")
    print("=" * 60)

    if not os.getenv("OPENAI_API_KEY"):
        print("请设置 OPENAI_API_KEY")
        return

    qa = QASystem()

    # 创建示例文档
    sample_dir = Path("./sample_docs")
    sample_dir.mkdir(exist_ok=True)

    sample_file = sample_dir / "langchain_intro.txt"
    if not sample_file.exists():
        sample_file.write_text("""
LangChain 简介

LangChain 是一个用于开发 LLM 应用的框架。

核心组件：
1. Models - 各种 LLM 的统一接口
2. Prompts - 提示词模板管理
3. Chains - 链式调用组合
4. Memory - 对话记忆管理
5. Agents - 智能代理系统

LangChain 支持多种 LLM 提供商，如 OpenAI、Anthropic 等。
通过 LCEL (LangChain Expression Language) 可以灵活组合各种组件。
        """, encoding="utf-8")
        print(f"\n创建示例文档: {sample_file}")

    # 索引
    count = qa.index_directory(str(sample_dir))
    print(f"\n索引完成: {count} 个文档块")

    # 问答
    questions = [
        "什么是 LangChain？",
        "LangChain 有哪些核心组件？",
        "LCEL 是什么？",
    ]

    for q in questions:
        print(f"\n问: {q}")
        result = qa.ask(q)
        print(f"答: {result['answer']}")
        print(f"来源: {[s['source'] for s in result['sources']]}")


if __name__ == "__main__":
    demo()
