import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 05_fallback_retry.py
# with_fallbacks 回退机制 + with_retry 重试
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

load_dotenv()

# 可用的模型列表
primary = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0,
    max_retries=1,
    timeout=10,
)

# 模拟备用模型（如果有的话）
# backup = ChatOpenAI(
#     model="qwen-turbo",
#     base_url=os.getenv("QWEN_BASE_URL"),
#     api_key=os.getenv("QWEN_API_KEY"),
# )

# 带 fallback 的 LLM
# resilient_llm = primary.with_fallbacks([backup])
# 简化版：只用 primary
resilient_llm = primary

# 带重试（指数退避 + 随机抖动）
retry_llm = resilient_llm.with_retry(
    stop_after_attempt=3,
    wait_exponential_jitter=True,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是有用的助手。"),
    ("human", "{question}"),
])

chain = prompt | retry_llm | StrOutputParser()

print(chain.invoke({"question": "用一句话介绍 Python"}))
print("\nChain 执行成功！如果网络抖动会自动重试。")
