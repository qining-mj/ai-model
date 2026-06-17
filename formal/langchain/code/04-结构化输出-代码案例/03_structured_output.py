import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 03_structured_output.py
# with_structured_output：最推荐的结构化输出方式
# 注意：DeepSeek 需要 method="json_mode"，且 prompt 中需包含 "JSON" 关键词
import os
import sys
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import Literal

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0,
)

# === 方式 1：Pydantic Schema ===
class Person(BaseModel):
    name: str = Field(description="姓名")
    age: int = Field(description="年龄")
    skills: list[str] = Field(description="技能列表")

pydantic_llm = llm.with_structured_output(Person, method="json_mode")
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个信息提取助手。请将用户描述提取为 JSON 对象。"),
    ("human", "{text}"),
])
chain = prompt | pydantic_llm
resume = chain.invoke({"text": "王五，25岁，精通 Python 和 React"})
print(f"Pydantic: {resume.name}, {resume.age}岁, 技能={resume.skills}")

# === 方式 2：Pydantic Schema（轻量定义） ===
class Sentiment(BaseModel):
    sentiment: Literal["POSITIVE", "NEGATIVE", "NEUTRAL"] = Field(description="情感分类")
    confidence: float = Field(description="置信度，0~1 之间")
    reason: str = Field(description="判断理由")

sentiment_llm = llm.with_structured_output(Sentiment, method="json_mode")
prompt2 = ChatPromptTemplate.from_messages([
    ("system", "你是一个情感分析助手。分析评论的情感，输出 JSON 对象，包含 sentiment（POSITIVE/NEGATIVE/NEUTRAL）、confidence（0~1小数）、reason（字符串）三个字段。"),
    ("human", "{text}"),
])
chain2 = prompt2 | sentiment_llm
result = chain2.invoke({"text": "服务态度特别好，下次还来！"})
print(f"\nPydantic: {result.sentiment}, 置信度={result.confidence}")
print(f"理由: {result.reason}")

# === 方式 3：JSON Schema（最灵活） ===
json_schema = {
    "title": "Book",
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "author": {"type": "string"},
        "year": {"type": "integer"},
    },
    "required": ["title", "author", "year"],
}

book_llm = llm.with_structured_output(json_schema, method="json_mode")
prompt3 = ChatPromptTemplate.from_messages([
    ("system", "你是一个图书信息提取助手。请将提取结果输出为 JSON 对象。"),
    ("human", "{text}"),
])
chain3 = prompt3 | book_llm
book = chain3.invoke({"text": "《三体》是刘慈欣写的，2008年出版"})
print(f"\nJSON Schema: {book['title']} - {book['author']} ({book['year']})")
