import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 00_hello_langchain.py
# LangChain 1.3.4 第一个程序
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.7,
)

response = llm.invoke("用一句话介绍 LangChain 是什么")
print(response.content)
print(f"\nToken 用量: {response.response_metadata}")
