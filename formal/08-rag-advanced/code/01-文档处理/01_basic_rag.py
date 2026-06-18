"""
01_basic_rag.py
基础 RAG 实现
"""
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


def basic_rag():
    """基础 RAG 示例"""
    print("=" * 60)
    print("【基础 RAG 实现】")
    print("=" * 60)

    # 准备示例文档
    documents = [
        "LangChain 是一个用于开发 LLM 应用的开源框架，由 Harrison Chase 于 2022 年创建。",
        "LangChain 的核心概念包括：Chain、Agent、Memory、Retriever 等。",
        "LCEL（LangChain Expression Language）是 LangChain 的声明式编排语法。",
        "RAG 是 Retrieval-Augmented Generation 的缩写，意为检索增强生成。",
        "向量数据库用于存储和检索高维向量，是 RAG 系统的核心组件。",
        "Chroma 是一个轻量级的向量数据库，适合本地开发和小规模应用。",
        "OpenAI 的 text-embedding-3-small 模型可以将文本转换为 1536 维向量。",
        "GPT-4 是 OpenAI 最强大的语言模型之一，支持 128K 上下文窗口。",
    ]

    # 创建向量存储
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma.from_texts(
        texts=documents,
        embedding=embeddings,
        collection_name="rag_demo"
    )

    # 创建检索器
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )

    # 创建 LLM
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # RAG Prompt
    template = """基于以下上下文回答问题。如果上下文中没有相关信息，请说明无法回答。

上下文：
{context}

问题：{question}

回答："""

    prompt = ChatPromptTemplate.from_template(template)

    # 构建 RAG Chain
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # 测试问题
    questions = [
        "什么是 LangChain？",
        "RAG 是什么意思？",
        "有哪些向量数据库可以使用？",
    ]

    for q in questions:
        print(f"\n问题: {q}")
        print("-" * 40)

        # 先看检索到的文档
        docs = retriever.invoke(q)
        print("检索到的文档:")
        for i, doc in enumerate(docs, 1):
            print(f"  {i}. {doc.page_content[:60]}...")

        # 生成回答
        answer = rag_chain.invoke(q)
        print(f"\n回答: {answer}")


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("请设置 OPENAI_API_KEY")
        exit()

    basic_rag()
