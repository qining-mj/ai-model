"""
01_text_splitter.py
文本分块器
"""
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
)


def recursive_split():
    """递归字符分块（推荐）"""
    print("=" * 60)
    print("【递归字符分块】")
    print("=" * 60)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=30,
        length_function=len,
        separators=["\n\n", "\n", "。", ".", " ", ""]
    )

    text = """
人工智能是计算机科学的一个重要分支。它致力于研究和开发能够模拟人类智能的系统。

机器学习是人工智能的核心技术之一。通过大量数据的训练，机器可以自动学习和改进。深度学习是机器学习的一个子集，使用多层神经网络来处理复杂的模式识别任务。

自然语言处理让计算机能够理解和生成人类语言。这是实现人机交互的关键技术。常见的 NLP 任务包括文本分类、命名实体识别、机器翻译等。

向量数据库是存储和检索高维向量的专用数据库。它是构建 RAG 系统的核心组件，支持语义搜索功能。
"""

    chunks = splitter.split_text(text)

    print(f"分成 {len(chunks)} 个块:\n")
    for i, chunk in enumerate(chunks):
        print(f"[{i}] ({len(chunk)} 字符)")
        print(f"  {chunk.strip()[:100]}...")
        print()

    return chunks


def character_split():
    """固定字符分块"""
    print("=" * 60)
    print("【固定字符分块】")
    print("=" * 60)

    splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=200,
        chunk_overlap=30
    )

    text = """第一段内容。这是一些关于人工智能的介绍文字。

第二段内容。这是一些关于机器学习的介绍文字。

第三段内容。这是一些关于深度学习的介绍文字。"""

    chunks = splitter.split_text(text)

    print(f"分成 {len(chunks)} 个块:")
    for i, chunk in enumerate(chunks):
        print(f"  [{i}] {chunk[:50]}...")

    return chunks


def compare_splitters():
    """对比不同分块器"""
    print("\n" + "=" * 60)
    print("【分块器对比】")
    print("=" * 60)

    text = "Python 是一种编程语言。它简洁易读。Python 广泛用于数据科学。"

    # 递归分块
    recursive = RecursiveCharacterTextSplitter(chunk_size=30, chunk_overlap=5)
    recursive_chunks = recursive.split_text(text)

    # 字符分块
    character = CharacterTextSplitter(separator="。", chunk_size=30, chunk_overlap=5)
    character_chunks = character.split_text(text)

    print(f"\n原文: {text}\n")
    print(f"递归分块 ({len(recursive_chunks)} 块):")
    for c in recursive_chunks:
        print(f"  - {c}")

    print(f"\n字符分块 ({len(character_chunks)} 块):")
    for c in character_chunks:
        print(f"  - {c}")


if __name__ == "__main__":
    recursive_split()
    character_split()
    compare_splitters()
