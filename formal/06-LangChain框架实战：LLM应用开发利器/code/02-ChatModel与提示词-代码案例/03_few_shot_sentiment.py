import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 03_few_shot_sentiment.py
# Few-Shot Prompting：用范例引导模型
import os
from dotenv import load_dotenv
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0,
)

# 范例
examples = [
    {"input": "今天心情真好，阳光明媚", "output": "POSITIVE"},
    {"input": "堵车堵死了，烦死了", "output": "NEGATIVE"},
    {"input": "今天周三", "output": "NEUTRAL"},
    {"input": "这服务态度也太差了吧", "output": "NEGATIVE"},
]

example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{output}"),
])

few_shot_prompt = FewShotChatMessagePromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    input_variables=["input"],
)

final_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是情感分析器。只输出 POSITIVE / NEGATIVE / NEUTRAL。"),
    few_shot_prompt,
    ("human", "{input}"),
])

chain = final_prompt | llm | StrOutputParser()

tests = [
    "这部电影太精彩了",
    "等了两个小时还没轮到",
    "今天星期五",
]
for t in tests:
    print(f"{t} → {chain.invoke({'input': t})}")
