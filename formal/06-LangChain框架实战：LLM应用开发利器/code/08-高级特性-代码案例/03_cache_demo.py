import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 03_cache_demo.py
# 缓存：避免重复 API 调用，节省成本
import os, time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.caches import InMemoryCache
from langchain_core.globals import set_llm_cache
from langchain_community.caches import SQLiteCache

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0,
)

# 先不用缓存
print("=== 无缓存 ===")
for i in range(3):
    start = time.time()
    r = llm.invoke("什么是 LangChain？")
    elapsed = time.time() - start
    print(f"  第{i+1}次: {elapsed:.2f}s")

# 启用内存缓存
set_llm_cache(InMemoryCache())
print("\n=== 启用 InMemoryCache ===")
for i in range(3):
    start = time.time()
    r = llm.invoke("什么是 LangChain？")
    elapsed = time.time() - start
    print(f"  第{i+1}次: {elapsed:.2f}s")

# 也可以启用 SQLite 持久化缓存
# set_llm_cache(SQLiteCache(database_path=".llm_cache.db"))
# print("\n启用 SQLiteCache，缓存已持久化到磁盘")
