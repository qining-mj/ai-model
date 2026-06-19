"""
01_qwen_basic.py
通义千问基础调用示例

运行前准备：
1. pip install dashscope python-dotenv
2. 在 .env 文件中添加：DASHSCOPE_API_KEY=sk-xxx
3. 或者使用 OpenAI 兼容模式（见下方）
"""
import os
from dotenv import load_dotenv

load_dotenv()


def call_with_dashscope_sdk():
    """方式1：使用 DashScope 官方 SDK"""
    print("=" * 60)
    print("【方式1】DashScope 官方 SDK")
    print("=" * 60)

    import dashscope
    from dashscope import Generation

    dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

    response = Generation.call(
        model="qwen-turbo",  # 可选: qwen-turbo, qwen-plus, qwen-max
        messages=[
            {"role": "system", "content": "你是一个有帮助的助手"},
            {"role": "user", "content": "用一句话介绍通义千问"}
        ],
        result_format="message"  # 返回消息格式
    )

    if response.status_code == 200:
        print(f"\n回复: {response.output.choices[0].message.content}")
        print(f"\nToken 用量:")
        print(f"  输入: {response.usage.input_tokens}")
        print(f"  输出: {response.usage.output_tokens}")
    else:
        print(f"错误: {response.code} - {response.message}")


def call_with_openai_sdk():
    """方式2：使用 OpenAI SDK（推荐！）"""
    print("\n" + "=" * 60)
    print("【方式2】OpenAI 兼容模式（推荐）")
    print("=" * 60)

    from openai import OpenAI

    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )

    response = client.chat.completions.create(
        model="qwen-turbo",
        messages=[
            {"role": "system", "content": "你是一个有帮助的助手"},
            {"role": "user", "content": "用一句话介绍通义千问"}
        ],
        temperature=0.7
    )

    print(f"\n回复: {response.choices[0].message.content}")
    print(f"\nToken 用量:")
    print(f"  输入: {response.usage.prompt_tokens}")
    print(f"  输出: {response.usage.completion_tokens}")


def show_model_list():
    """展示通义千问模型列表"""
    print("\n" + "=" * 60)
    print("【通义千问模型列表】")
    print("=" * 60)

    models = """
    ┌─────────────────────┬──────────────┬─────────────────────────┐
    │  模型名称            │  上下文长度   │  特点                   │
    ├─────────────────────┼──────────────┼─────────────────────────┤
    │  qwen-turbo         │  128K        │  快速、便宜              │
    │  qwen-plus          │  128K        │  能力与成本均衡          │
    │  qwen-max           │  32K         │  最强能力                │
    │  qwen-max-longcontext│  28K        │  长文本处理              │
    │  qwen-coder-turbo   │  128K        │  代码生成专用            │
    │  qwen-vl-plus       │  -           │  多模态（图像理解）      │
    └─────────────────────┴──────────────┴─────────────────────────┘

    💡 推荐：
    - 日常对话：qwen-turbo
    - 复杂任务：qwen-plus
    - 代码生成：qwen-coder-turbo
    """
    print(models)


if __name__ == "__main__":
    show_model_list()

    # 如果有 DASHSCOPE_API_KEY，运行实际调用
    if os.getenv("DASHSCOPE_API_KEY"):
        # 方式1需要 dashscope 包
        try:
            call_with_dashscope_sdk()
        except ImportError:
            print("dashscope 未安装，跳过方式1")

        # 方式2只需要 openai 包
        call_with_openai_sdk()
    else:
        print("\n⚠️ 未设置 DASHSCOPE_API_KEY，跳过实际调用演示")
