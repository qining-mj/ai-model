import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 01_temperature_demo.py
# temperature 参数对比实验
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

prompt = "写一首关于春天的小诗（4句）"

for temp in [0, 0.5, 1.0]:
    llm = ChatOpenAI(
        model="deepseek-chat",
        base_url=os.getenv("DEEPSEEK_BASE_URL"),
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        temperature=temp,
    )
    print(f"\n{'='*40}")
    print(f"temperature = {temp}")
    for i in range(3):
        r = llm.invoke(prompt)
        print(f"  第{i+1}次:\n{r.content}\n")
