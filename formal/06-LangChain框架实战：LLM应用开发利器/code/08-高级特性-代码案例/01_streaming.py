import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 01_streaming.py
# 流式输出 + astream_events
import os, asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.7,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是 Python 专家，用中文回答。"),
    ("human", "{question}"),
])

chain = prompt | llm | StrOutputParser()

# === 1. 同步 stream ===
print("=== stream() 打字机效果 ===")
for chunk in chain.stream({"question": "简单介绍什么是装饰器"}):
    print(chunk, end="", flush=True)
print()

# === 2. 异步 astream ===
async def astream_demo():
    print("\n=== astream() 异步流式 ===")
    async for chunk in chain.astream({"question": "Python 的 GIL 是什么？"}):
        print(chunk, end="", flush=True)

asyncio.run(astream_demo())

# === 3. astream_events（能看到中间步骤） ===
async def astream_events_demo():
    print("\n\n=== astream_events() 带事件的流式 ===")
    async for event in chain.astream_events(
        {"question": "解释什么是列表推导式"},
        version="v2",
    ):
        kind = event["event"]
        name = event.get("name", "")

        if kind == "on_chat_model_start":
            print(f"\n[{name}] 开始生成...")
        elif kind == "on_chat_model_stream":
            print(event["data"]["chunk"].content, end="", flush=True)
        elif kind == "on_chat_model_end":
            print(f"\n[{name}] 生成完成")

asyncio.run(astream_events_demo())
