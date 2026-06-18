"""
02_four_elements.py
Prompt 四要素模型演示

角色(Role) + 任务(Task) + 上下文(Context) + 格式(Format)
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def four_elements_prompt():
    """展示四要素完整 Prompt"""

    print("=" * 60)
    print("【Prompt 四要素模型】")
    print("=" * 60)

    # 完整的四要素 Prompt
    full_prompt = """
【角色】
你是一位资深的 Python 代码审查专家，有 10 年以上的开发经验，尤其擅长发现潜在的性能问题和安全漏洞。

【任务】
请审查以下代码，找出所有问题并提供改进建议。

【上下文】
这是一个生产环境的用户数据处理模块，每天处理约 100 万条记录。
当前团队反映该模块运行缓慢，需要优化。

【代码】
```python
def process_users(user_list):
    result = []
    for user in user_list:
        if user['age'] > 18:
            user_data = {
                'name': user['name'],
                'email': user['email'],
                'status': 'active' if user['is_active'] else 'inactive'
            }
            result.append(user_data)
    return result
```

【输出格式】
请按以下格式输出：

## 问题分析
| 问题 | 类型 | 严重程度 | 说明 |
|------|------|---------|------|

## 改进建议
1. 建议1
2. 建议2

## 优化后的代码
```python
# 优化后的代码
```

## 预期效果
- 性能提升：XX%
- 其他改进点
"""

    print("Prompt 结构：")
    print("-" * 40)
    print("1. 角色：资深 Python 代码审查专家")
    print("2. 任务：审查代码，找出问题")
    print("3. 上下文：生产环境，100万条/天")
    print("4. 格式：表格 + 列表 + 代码块")
    print("-" * 40)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": full_prompt}],
        max_tokens=1000
    )

    print("\n回复：")
    print(response.choices[0].message.content)


def element_comparison():
    """对比缺少要素的影响"""

    code = """
def calc(a, b):
    return a / b
"""

    prompts = {
        "只有任务": f"分析这段代码：{code}",

        "任务+格式": f"""分析这段代码：{code}

请按以下格式输出：
- 问题列表
- 修复建议""",

        "任务+角色+格式": f"""你是一位代码安全专家。

分析这段代码：{code}

请按以下格式输出：
- 安全问题
- 修复方案""",

        "完整四要素": f"""【角色】你是一位代码安全专家，专注于发现安全漏洞。

【任务】分析以下代码的安全性。

【上下文】这段代码用于处理用户输入的计算请求。

【代码】{code}

【格式要求】
## 安全问题
| 问题 | 风险等级 | 攻击方式 |

## 修复代码
```python
# 安全的代码
```
"""
    }

    print("\n" + "=" * 60)
    print("【要素缺失对比】")
    print("=" * 60)

    for name, prompt in prompts.items():
        print(f"\n--- {name} ---")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )

        print(response.choices[0].message.content[:200] + "...")


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("请设置 OPENAI_API_KEY")
        exit()

    four_elements_prompt()
    element_comparison()
