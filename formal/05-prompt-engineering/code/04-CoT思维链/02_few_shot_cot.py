"""
02_few_shot_cot.py
Few-shot Chain-of-Thought 示例
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def few_shot_cot_math():
    """Few-shot CoT 数学问题"""

    prompt = """解决数学应用题，请展示推理过程。

问题1：食堂有 32 个苹果。如果用掉 20 个做果汁，又买入 15 个，现在有多少个？
推理：
1. 初始数量：32 个
2. 做果汁用掉：32 - 20 = 12 个
3. 买入新的：12 + 15 = 27 个
答案：27 个

问题2：停车场有 12 辆车。开走 5 辆，又来了 8 辆，现在有多少辆？
推理：
1. 初始数量：12 辆
2. 开走：12 - 5 = 7 辆
3. 新来：7 + 8 = 15 辆
答案：15 辆

问题3：图书馆有 50 本书，借出 23 本，归还 15 本，又购入 30 本，现在有多少本？
推理："""

    print("=" * 60)
    print("【Few-shot CoT 数学问题】")
    print("=" * 60)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )

    print(response.choices[0].message.content)


def few_shot_cot_logic():
    """Few-shot CoT 逻辑推理"""

    prompt = """解决逻辑推理问题。

问题1：A 比 B 高，B 比 C 高。谁最矮？
推理：
1. A 比 B 高 → A > B
2. B 比 C 高 → B > C
3. 因此：A > B > C
4. C 排在最后
答案：C 最矮

问题2：苹果比香蕉贵，香蕉比橘子贵，橘子比西瓜便宜。什么最贵？
推理：
1. 苹果 > 香蕉（价格）
2. 香蕉 > 橘子
3. 橘子 < 西瓜 → 西瓜 > 橘子
4. 目前确定：苹果 > 香蕉 > 橘子，西瓜 > 橘子
5. 但苹果和西瓜的关系不确定
答案：苹果或西瓜最贵（信息不足以确定）

问题3：小明比小红跑得快，小华比小明跑得慢，小红比小李跑得快。谁跑得最快？
推理："""

    print("\n" + "=" * 60)
    print("【Few-shot CoT 逻辑推理】")
    print("=" * 60)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )

    print(response.choices[0].message.content)


def few_shot_cot_code():
    """Few-shot CoT 代码分析"""

    prompt = """分析代码的时间复杂度。

代码1：
```python
for i in range(n):
    print(i)
```
分析：
1. 只有一个循环
2. 循环执行 n 次
3. 每次操作是 O(1)
复杂度：O(n)

代码2：
```python
for i in range(n):
    for j in range(n):
        print(i, j)
```
分析：
1. 外层循环 n 次
2. 每次外层循环，内层执行 n 次
3. 总操作次数：n × n = n²
复杂度：O(n²)

代码3：
```python
for i in range(n):
    for j in range(i):
        for k in range(j):
            print(i, j, k)
```
分析："""

    print("\n" + "=" * 60)
    print("【Few-shot CoT 代码复杂度分析】")
    print("=" * 60)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400
    )

    print(response.choices[0].message.content)


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("请设置 OPENAI_API_KEY")
        exit()

    few_shot_cot_math()
    few_shot_cot_logic()
    few_shot_cot_code()
