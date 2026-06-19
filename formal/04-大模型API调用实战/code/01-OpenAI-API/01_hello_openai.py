"""
01_hello_openai.py
第一个 OpenAI API 调用示例

运行前准备：
1. pip install openai python-dotenv
2. 在项目根目录创建 .env 文件，添加：
   OPENAI_API_KEY=sk-proj-your-api-key-here
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv()

# 创建客户端
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
)

# 发起请求
response = client.chat.completions.create(
    model="gpt-4o-mini",           # 模型名称（性价比之王）
    messages=[
        {"role": "user", "content": "用一句话介绍什么是 API"}
    ]
)

# 提取回复
print("=" * 50)
print("模型回复：")
print(response.choices[0].message.content)

print("\n" + "=" * 50)
print("Token 用量统计：")
print(f"  输入 Token: {response.usage.prompt_tokens}")
print(f"  输出 Token: {response.usage.completion_tokens}")
print(f"  总计 Token: {response.usage.total_tokens}")

# 计算成本（gpt-4o-mini 价格：输入 $0.15/M，输出 $0.6/M）
input_cost = response.usage.prompt_tokens * 0.15 / 1_000_000
output_cost = response.usage.completion_tokens * 0.6 / 1_000_000
total_cost = input_cost + output_cost
print(f"\n预估成本: ${total_cost:.6f}")
