"""
03_long_context.py
Claude 长上下文处理示例

演示 Claude 200K 上下文窗口的优势
"""
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()


def demo_long_document():
    """长文档处理演示"""
    print("=" * 60)
    print("【演示】长文档处理")
    print("=" * 60)

    # 模拟一个长文档（实际应用中从文件读取）
    sample_paragraph = """
    人工智能（Artificial Intelligence，AI）是计算机科学的一个分支，
    它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。
    该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。
    """

    # 重复多次模拟长文档
    long_document = sample_paragraph * 50
    word_count = len(long_document)

    print(f"\n文档长度: {word_count} 字符（约 {word_count // 2} 个中文字）")

    # 使用 XML 标签包裹文档内容（Claude 最佳实践）
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": f"""请阅读以下文档并完成任务：

<document>
{long_document}
</document>

<tasks>
1. 用一句话总结这个文档的核心主题
2. 提取文档中提到的3个关键技术领域
3. 这个文档大约重复了多少次相同的内容？
</tasks>"""
            }
        ]
    )

    print(f"\n输入 Token: {message.usage.input_tokens}")
    print(f"输出 Token: {message.usage.output_tokens}")
    print(f"\n回复：\n{message.content[0].text}")


def demo_xml_tags():
    """XML 标签最佳实践"""
    print("\n" + "=" * 60)
    print("【演示】XML 标签的妙用")
    print("=" * 60)

    # Claude 对 XML 标签有特殊的处理能力
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": """
<task>分析以下代码的问题并给出修复建议</task>

<code language="python">
def divide(a, b):
    return a / b

def process_list(items):
    result = []
    for i in range(len(items)):
        result.append(items[i] * 2)
    return result

def read_file(path):
    f = open(path, 'r')
    content = f.read()
    return content
</code>

<requirements>
1. 指出每个函数的潜在问题
2. 给出修复后的代码
3. 解释每处修改的原因
</requirements>

<output_format>
对每个函数按以下格式输出：
### 函数名
- 问题：...
- 修复代码：...
- 原因：...
</output_format>"""
            }
        ]
    )

    print(message.content[0].text)


def demo_context_comparison():
    """上下文长度对比"""
    print("\n" + "=" * 60)
    print("【各模型上下文长度对比】")
    print("=" * 60)

    comparison = """
    ┌─────────────────────┬──────────────┬─────────────────────┐
    │  模型                │  上下文长度   │  约等于              │
    ├─────────────────────┼──────────────┼─────────────────────┤
    │  Claude 3 系列       │  200K tokens │  约 15 万中文字      │
    │  GPT-4o             │  128K tokens │  约 10 万中文字      │
    │  GPT-4 Turbo        │  128K tokens │  约 10 万中文字      │
    │  GPT-3.5 Turbo      │  16K tokens  │  约 1.2 万中文字     │
    │  Gemini 1.5 Pro     │  1M tokens   │  约 75 万中文字      │
    └─────────────────────┴──────────────┴─────────────────────┘

    💡 Claude 的长上下文优势场景：
    1. 整本书/长报告的分析和问答
    2. 大型代码库的理解和重构
    3. 长对话历史的保持
    4. 多文档综合分析
    """
    print(comparison)


def demo_reading_file():
    """从文件读取长文本"""
    print("\n" + "=" * 60)
    print("【实际应用】从文件读取长文本")
    print("=" * 60)

    # 示例代码（实际运行需要有对应文件）
    code_example = '''
def analyze_document(file_path: str, question: str) -> str:
    """
    分析长文档并回答问题

    Args:
        file_path: 文档路径（支持 .txt, .md 等文本文件）
        question: 要回答的问题
    """
    import anthropic

    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        document = f.read()

    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2000,
        messages=[
            {
                "role": "user",
                "content": f"""请基于以下文档回答问题。

<document>
{document}
</document>

<question>
{question}
</question>

请确保回答基于文档内容，如果文档中没有相关信息，请明确说明。"""
            }
        ]
    )

    return message.content[0].text

# 使用示例
# result = analyze_document("report.txt", "这份报告的主要结论是什么？")
    '''

    print(code_example)


if __name__ == "__main__":
    demo_long_document()
    demo_xml_tags()
    demo_context_comparison()
    demo_reading_file()
