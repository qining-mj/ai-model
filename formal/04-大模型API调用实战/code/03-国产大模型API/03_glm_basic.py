"""
03_glm_basic.py
智谱 GLM 基础调用示例

运行前准备：
1. pip install zhipuai python-dotenv  # 或使用 OpenAI 兼容模式
2. 在 .env 文件中添加：ZHIPU_API_KEY=xxx.xxx
"""
import os
from dotenv import load_dotenv

load_dotenv()


def call_with_zhipuai_sdk():
    """方式1：使用智谱官方 SDK"""
    print("=" * 60)
    print("【方式1】智谱官方 SDK")
    print("=" * 60)

    from zhipuai import ZhipuAI

    client = ZhipuAI(api_key=os.getenv("ZHIPU_API_KEY"))

    response = client.chat.completions.create(
        model="glm-4-flash",  # 免费模型
        messages=[
            {"role": "user", "content": "用一句话介绍智谱GLM"}
        ]
    )

    print(f"\n回复: {response.choices[0].message.content}")
    print(f"\nToken 用量:")
    print(f"  输入: {response.usage.prompt_tokens}")
    print(f"  输出: {response.usage.completion_tokens}")


def call_with_openai_sdk():
    """方式2：使用 OpenAI SDK（兼容模式）"""
    print("\n" + "=" * 60)
    print("【方式2】OpenAI 兼容模式")
    print("=" * 60)

    from openai import OpenAI

    client = OpenAI(
        api_key=os.getenv("ZHIPU_API_KEY"),
        base_url="https://open.bigmodel.cn/api/paas/v4/"
    )

    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=[
            {"role": "user", "content": "用一句话介绍智谱GLM"}
        ]
    )

    print(f"\n回复: {response.choices[0].message.content}")


def web_search_demo():
    """联网搜索功能演示"""
    print("\n" + "=" * 60)
    print("【智谱 GLM 联网搜索】")
    print("=" * 60)

    from zhipuai import ZhipuAI

    client = ZhipuAI(api_key=os.getenv("ZHIPU_API_KEY"))

    response = client.chat.completions.create(
        model="glm-4-plus",  # 需要使用 plus 版本
        messages=[
            {"role": "user", "content": "2024年人工智能领域有哪些重要进展？"}
        ],
        tools=[
            {
                "type": "web_search",
                "web_search": {
                    "enable": True,
                    "search_result": True  # 返回搜索结果
                }
            }
        ]
    )

    print(f"\n回复: {response.choices[0].message.content}")


def show_model_list():
    """展示智谱模型列表"""
    print("=" * 60)
    print("【智谱 GLM 模型列表】")
    print("=" * 60)

    models = """
    ┌─────────────────┬─────────────────────────────────────────┐
    │  模型名称        │  特点                                   │
    ├─────────────────┼─────────────────────────────────────────┤
    │  glm-4-plus     │  旗舰模型，最强能力，支持联网搜索        │
    │  glm-4          │  标准模型，均衡之选                      │
    │  glm-4-flash    │  快速模型，速度快、成本低（有免费额度）  │
    │  glm-4-air      │  轻量模型，适合简单任务                  │
    │  glm-4v-plus    │  多模态模型，支持图像理解                │
    │  codegeex-4     │  代码模型，代码生成专用                  │
    └─────────────────┴─────────────────────────────────────────┘

    💡 特色功能：
    - 联网搜索：glm-4-plus 支持实时联网获取信息
    - 免费额度：glm-4-flash 有免费调用额度
    - 学术背景：清华大学孵化，中文能力强

    ⚠️ 注意事项：
    - API Key 格式：xxx.xxx（中间有个点）
    - 联网搜索需要使用 tools 参数
    """
    print(models)


if __name__ == "__main__":
    show_model_list()

    if os.getenv("ZHIPU_API_KEY"):
        try:
            call_with_zhipuai_sdk()
        except ImportError:
            print("zhipuai 未安装，跳过方式1")

        call_with_openai_sdk()

        # 联网搜索需要 plus 模型，可能需要付费
        # web_search_demo()
    else:
        print("\n⚠️ 未设置 ZHIPU_API_KEY，跳过实际调用演示")
