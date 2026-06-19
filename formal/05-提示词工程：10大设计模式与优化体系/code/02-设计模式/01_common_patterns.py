"""
01_common_patterns.py
常用 Prompt 设计模式演示
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def instruction_pattern():
    """指令模式"""
    print("=" * 60)
    print("【模式1：指令模式】")
    print("=" * 60)

    prompt = """总结以下文章的要点，使用3-5个要点，每个要点不超过20字。

文章：
人工智能正在改变我们的生活方式。从智能手机上的语音助手，到自动驾驶汽车，
AI技术已经渗透到日常生活的方方面面。专家预测，未来十年AI将在医疗、教育、
金融等领域带来革命性的变化。然而，AI的发展也带来了一些担忧，包括就业影响、
隐私问题和伦理挑战。"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    print(response.choices[0].message.content)


def persona_pattern():
    """角色扮演模式"""
    print("\n" + "=" * 60)
    print("【模式2：角色扮演模式】")
    print("=" * 60)

    prompt = """你是一位有20年经验的投资顾问，擅长用通俗易懂的方式解释金融概念。
你总是会考虑风险因素，给出谨慎但有建设性的建议。

请回答：什么是复利？为什么说它是"世界第八大奇迹"？"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    print(response.choices[0].message.content)


def template_pattern():
    """模板填充模式"""
    print("\n" + "=" * 60)
    print("【模式3：模板填充模式】")
    print("=" * 60)

    prompt = """请为以下函数生成文档，按照此模板填充：

## 函数名
{函数名}

## 功能描述
{一句话描述}

## 参数说明
| 参数名 | 类型 | 说明 |
|--------|------|------|
{参数表格}

## 返回值
{返回值说明}

## 示例
```python
{使用示例}
```

待文档化的函数：
```python
def calculate_bmi(weight: float, height: float) -> float:
    return weight / (height ** 2)
```
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400
    )
    print(response.choices[0].message.content)


def constraint_pattern():
    """约束模式"""
    print("\n" + "=" * 60)
    print("【模式4：约束模式】")
    print("=" * 60)

    prompt = """请回答"什么是机器学习"。

约束条件：
✅ 必须：
- 回答长度：50-100字
- 包含一个具体的应用示例
- 使用通俗易懂的语言

❌ 禁止：
- 不要使用"可能"、"也许"等模糊词
- 不要使用专业术语（如需使用，必须解释）
- 不要超过100字"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    print(response.choices[0].message.content)


def decomposition_pattern():
    """分解模式"""
    print("\n" + "=" * 60)
    print("【模式5：分解模式】")
    print("=" * 60)

    prompt = """请按以下步骤分析这个业务需求：

Step 1: 需求理解
- 核心功能是什么？
- 目标用户是谁？

Step 2: 技术分析
- 需要哪些技术组件？
- 有哪些技术难点？

Step 3: 风险评估
- 可能的风险有哪些？
- 如何规避？

Step 4: 实施建议
- 推荐的实施方案
- 预估工时

请一步一步完成。

需求：开发一个在线教育平台，支持直播授课、录播回放、作业批改功能。"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600
    )
    print(response.choices[0].message.content)


def comparison_pattern():
    """对比模式"""
    print("\n" + "=" * 60)
    print("【模式6：对比模式】")
    print("=" * 60)

    prompt = """请对比 Python 和 JavaScript 这两种编程语言。

对比维度：
1. 语法特点
2. 主要应用场景
3. 学习难度
4. 生态系统
5. 性能

输出格式：
| 维度 | Python | JavaScript |
|------|--------|------------|

最后给出选择建议：什么情况选Python，什么情况选JavaScript。"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    print(response.choices[0].message.content)


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("请设置 OPENAI_API_KEY")
        exit()

    instruction_pattern()
    persona_pattern()
    template_pattern()
    constraint_pattern()
    decomposition_pattern()
    comparison_pattern()
