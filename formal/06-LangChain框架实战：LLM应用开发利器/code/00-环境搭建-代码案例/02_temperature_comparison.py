import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 02_temperature_comparison.py
# 对比 temperature 对输出的影响
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

prompt = "用一句话介绍人工智能"

for temp in [0, 0.5, 1.0]:
    llm = ChatOpenAI(
        model="deepseek-chat",
        base_url=os.getenv("DEEPSEEK_BASE_URL"),
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        temperature=temp,
    )
    print(f"\n--- temperature={temp} ---")
    for i in range(3):
        response = llm.invoke(prompt)
        print(f"  第{i+1}次: {response.content}")
