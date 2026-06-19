import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 04_streaming_output.py
# 流式输出示例（打字机效果）
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

print("打字机效果输出：")
for chunk in llm.stream("写一首关于编程的五言绝句"):
    content = chunk.content
    if content:
        print(content, end="", flush=True)
print()
