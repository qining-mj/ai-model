"""
01_hello_claude.py
第一个 Claude API 调用示例

运行前准备：
1. pip install anthropic python-dotenv
2. 在项目根目录创建 .env 文件，添加：
   ANTHROPIC_API_KEY=sk-ant-api03-your-api-key-here
"""
import os
from dotenv import load_dotenv
import anthropic

# 加载环境变量
load_dotenv()

# 创建客户端
client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# 发起请求
# 注意：Claude 必须显式指定 max_tokens！
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",  # 最新的 Claude 3.5 Sonnet
    max_tokens=1024,                      # 必填参数！
    messages=[
        {"role": "user", "content": "用一句话介绍 Claude 是什么"}
    ]
)

# 提取回复
# 注意：Claude 的响应结构与 OpenAI 不同
# OpenAI: response.choices[0].message.content
# Claude: message.content[0].text
print("=" * 50)
print("模型回复：")
print(message.content[0].text)

# 查看 Token 用量
print("\n" + "=" * 50)
print("Token 用量统计：")
print(f"  输入 Token: {message.usage.input_tokens}")
print(f"  输出 Token: {message.usage.output_tokens}")

# 计算成本（claude-3-5-sonnet 价格：输入 $3/M，输出 $15/M）
input_cost = message.usage.input_tokens * 3 / 1_000_000
output_cost = message.usage.output_tokens * 15 / 1_000_000
total_cost = input_cost + output_cost
print(f"\n预估成本: ${total_cost:.6f}")

# 查看完整响应结构
print("\n" + "=" * 50)
print("响应元数据：")
print(f"  ID: {message.id}")
print(f"  模型: {message.model}")
print(f"  停止原因: {message.stop_reason}")
