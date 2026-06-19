"""
doc_assistant.py
多功能文档智能助手
"""
import os
from typing import List, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

load_dotenv()


# ============ 数据模型 ============

class Person(BaseModel):
    """人物信息"""
    name: str = Field(description="姓名")
    role: Optional[str] = Field(description="角色/职位", default=None)


class KeyInfo(BaseModel):
    """关键信息"""
    title: str = Field(description="文档标题或主题")
    summary: str = Field(description="一句话摘要")
    key_points: List[str] = Field(description="关键要点列表")
    people: List[Person] = Field(description="提及的人物", default_factory=list)
    dates: List[str] = Field(description="提及的日期", default_factory=list)


# ============ 文档摘要 ============

class DocumentSummarizer:
    """文档摘要生成器"""

    def __init__(self, model: str = "gpt-4o-mini"):
        self.llm = ChatOpenAI(model=model, temperature=0)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000,
            chunk_overlap=200
        )

    def summarize(
        self,
        text: str,
        style: str = "concise",
        max_length: int = 500
    ) -> str:
        """生成摘要"""
        styles = {
            "concise": "简洁的要点式摘要",
            "detailed": "详细的段落式摘要",
            "bullet": "要点列表形式的摘要",
        }

        style_desc = styles.get(style, styles["concise"])

        if len(text) < 4000:
            prompt = ChatPromptTemplate.from_template(f"""
请为以下文本生成{style_desc}，长度控制在{max_length}字以内。

文本：
{{text}}

摘要：
""")
            chain = prompt | self.llm
            return chain.invoke({"text": text}).content

        docs = [Document(page_content=chunk)
                for chunk in self.text_splitter.split_text(text)]

        chain = load_summarize_chain(self.llm, chain_type="map_reduce")
        return chain.invoke(docs)["output_text"]


# ============ 信息提取 ============

class InformationExtractor:
    """信息提取器"""

    def __init__(self, model: str = "gpt-4o-mini"):
        self.llm = ChatOpenAI(model=model, temperature=0)

    def extract_key_info(self, text: str) -> KeyInfo:
        """提取关键信息"""
        structured_llm = self.llm.with_structured_output(KeyInfo)

        prompt = ChatPromptTemplate.from_template("""
从以下文本中提取关键信息：

{text}

请提取：标题、摘要、关键要点、人物、日期等信息。
""")

        chain = prompt | structured_llm
        return chain.invoke({"text": text})

    def extract_action_items(self, text: str) -> List[str]:
        """提取待办事项"""
        prompt = ChatPromptTemplate.from_template("""
从以下会议记录/文档中提取待办事项和行动项：

{text}

以列表形式返回，每项一行。
""")

        chain = prompt | self.llm
        response = chain.invoke({"text": text})

        lines = response.content.strip().split("\n")
        return [line.strip("- ").strip() for line in lines if line.strip()]


# ============ 文档翻译 ============

class DocumentTranslator:
    """文档翻译器"""

    LANGUAGES = {
        "en": "English",
        "zh": "中文",
        "ja": "日本語",
        "ko": "한국어",
    }

    def __init__(self, model: str = "gpt-4o-mini"):
        self.llm = ChatOpenAI(model=model, temperature=0)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=100
        )

    def translate(
        self,
        text: str,
        target_lang: str,
        preserve_format: bool = True
    ) -> str:
        """翻译文本"""
        target = self.LANGUAGES.get(target_lang, target_lang)
        format_instruction = "保持原文的格式和结构。" if preserve_format else ""

        prompt = ChatPromptTemplate.from_template(f"""
将以下文本翻译成{target}。
{format_instruction}

原文：
{{text}}

翻译：
""")

        if len(text) < 2000:
            chain = prompt | self.llm
            return chain.invoke({"text": text}).content

        chunks = self.text_splitter.split_text(text)
        translated_chunks = []

        for chunk in chunks:
            chain = prompt | self.llm
            result = chain.invoke({"text": chunk})
            translated_chunks.append(result.content)

        return "\n\n".join(translated_chunks)


# ============ 格式转换 ============

class FormatConverter:
    """格式转换器"""

    def __init__(self, model: str = "gpt-4o-mini"):
        self.llm = ChatOpenAI(model=model, temperature=0)

    def to_markdown(self, text: str) -> str:
        """转换为 Markdown"""
        prompt = ChatPromptTemplate.from_template("""
将以下文本转换为格式良好的 Markdown 格式：

{text}

Markdown：
""")
        chain = prompt | self.llm
        return chain.invoke({"text": text}).content

    def to_outline(self, text: str) -> str:
        """转换为大纲"""
        prompt = ChatPromptTemplate.from_template("""
将以下文本转换为层级大纲格式：

{text}

大纲：
""")
        chain = prompt | self.llm
        return chain.invoke({"text": text}).content

    def to_table(self, text: str) -> str:
        """转换为表格"""
        prompt = ChatPromptTemplate.from_template("""
从以下文本中提取结构化数据，转换为 Markdown 表格格式：

{text}

表格：
""")
        chain = prompt | self.llm
        return chain.invoke({"text": text}).content


# ============ 综合助手 ============

class DocAssistant:
    """文档智能助手"""

    def __init__(self):
        self.summarizer = DocumentSummarizer()
        self.extractor = InformationExtractor()
        self.translator = DocumentTranslator()
        self.converter = FormatConverter()

    def process(self, text: str, task: str, **kwargs) -> str:
        """处理文档"""
        if task == "summarize":
            return self.summarizer.summarize(
                text,
                style=kwargs.get("style", "concise"),
                max_length=kwargs.get("max_length", 500)
            )
        elif task == "extract":
            info = self.extractor.extract_key_info(text)
            return f"标题: {info.title}\n摘要: {info.summary}\n要点: {info.key_points}"
        elif task == "translate":
            return self.translator.translate(
                text,
                target_lang=kwargs.get("target_lang", "en")
            )
        elif task == "to_markdown":
            return self.converter.to_markdown(text)
        elif task == "to_outline":
            return self.converter.to_outline(text)
        else:
            return f"未知任务: {task}"


def demo():
    """演示"""
    print("=" * 60)
    print("【文档智能助手】")
    print("=" * 60)

    if not os.getenv("OPENAI_API_KEY"):
        print("请设置 OPENAI_API_KEY")
        return

    sample_text = """
2024年第一季度项目总结

一、项目概述
本季度我们完成了 AI 助手产品的核心功能开发，包括：
1. 智能问答系统 - 支持多轮对话
2. 文档分析功能 - 支持 PDF、Word 格式
3. 知识库管理 - 向量化存储和检索

二、团队成员
- 张三：项目经理，负责整体协调
- 李四：技术负责人，负责架构设计
- 王五：前端开发，负责用户界面

三、后续计划
1. 4月15日前完成性能优化
2. 5月1日上线公测版本
3. 6月进行正式发布

会议结论：项目进展顺利，按计划推进。
"""

    assistant = DocAssistant()

    # 1. 摘要
    print("\n【任务1: 生成摘要】")
    result = assistant.process(sample_text, "summarize", style="bullet")
    print(result)

    # 2. 信息提取
    print("\n【任务2: 提取信息】")
    result = assistant.process(sample_text, "extract")
    print(result)

    # 3. 翻译
    print("\n【任务3: 翻译为英文】")
    result = assistant.process(sample_text[:200], "translate", target_lang="en")
    print(result)

    # 4. 转换为大纲
    print("\n【任务4: 转换为大纲】")
    result = assistant.process(sample_text, "to_outline")
    print(result)


if __name__ == "__main__":
    demo()
