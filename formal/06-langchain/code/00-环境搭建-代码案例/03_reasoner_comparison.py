import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 03_reasoner_comparison.py
# 对比 deepseek-chat vs deepseek-reasoner
import os, time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

question = "一个水池有进水管和出水管，进水管3小时注满，出水管5小时放完，两管同时开，几小时注满？"

models = {
    "deepseek-chat": ChatOpenAI(
        model="deepseek-chat",
        base_url=os.getenv("DEEPSEEK_BASE_URL"),
        api_key=os.getenv("DEEPSEEK_API_KEY"),
    ),
    "deepseek-reasoner": ChatOpenAI(
        model="deepseek-reasoner",
        base_url=os.getenv("DEEPSEEK_BASE_URL"),
        api_key=os.getenv("DEEPSEEK_API_KEY"),
    ),
}

for name, llm in models.items():
    print(f"\n{'='*40}")
    print(f"模型: {name}")
    start = time.time()
    response = llm.invoke(question)
    elapsed = time.time() - start
    print(f"回答: {response.content[:200]}...")
    print(f"耗时: {elapsed:.1f}s")
    if hasattr(response, "response_metadata"):
        tokens = response.response_metadata.get("token_usage", {})
        print(f"Token: {tokens}")
