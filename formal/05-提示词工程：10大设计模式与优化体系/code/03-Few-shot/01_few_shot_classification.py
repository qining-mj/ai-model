"""
01_few_shot_classification.py
Few-shot 分类任务示例
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def zero_shot_vs_few_shot():
    """对比 Zero-shot 和 Few-shot 效果"""

    test_cases = [
        "还行吧，不太满意也不太失望",
        "便宜是便宜，但质量一般",
        "包装精美，送货也快",
        "性价比不错，值得购买",
        "退货太麻烦了，差评",
    ]

    # Zero-shot Prompt
    zero_shot_prompt = """判断以下评论的情感倾向（正面/负面/中性）：

评论：{review}
情感："""

    # Few-shot Prompt
    few_shot_prompt = """判断评论的情感倾向。

示例1：
评论：非常满意，下次还会购买！
情感：正面

示例2：
评论：质量太差，申请退款了
情感：负面

示例3：
评论：一般般，没有惊喜也没有失望
情感：中性

示例4：
评论：性价比还可以，但包装有待提高
情感：中性

现在请判断：
评论：{review}
情感："""

    print("=" * 60)
    print("【Zero-shot vs Few-shot 效果对比】")
    print("=" * 60)

    for review in test_cases:
        print(f"\n评论: {review}")

        # Zero-shot
        r1 = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": zero_shot_prompt.format(review=review)}],
            max_tokens=10
        )
        zero_result = r1.choices[0].message.content.strip()

        # Few-shot
        r2 = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": few_shot_prompt.format(review=review)}],
            max_tokens=10
        )
        few_result = r2.choices[0].message.content.strip()

        print(f"  Zero-shot: {zero_result}")
        print(f"  Few-shot:  {few_result}")


def few_shot_entity_extraction():
    """Few-shot 实体提取"""

    prompt = """从文本中提取人名、地点和组织。

示例1：
文本：马云在杭州创立了阿里巴巴。
结果：人名=马云, 地点=杭州, 组织=阿里巴巴

示例2：
文本：雷军是小米公司的创始人，总部在北京。
结果：人名=雷军, 地点=北京, 组织=小米公司

示例3：
文本：昨天天气很好。
结果：人名=无, 地点=无, 组织=无

现在请提取：
文本：{text}
结果："""

    test_texts = [
        "张一鸣在北京创办了字节跳动。",
        "上海是中国最大的城市。",
        "任正非领导的华为公司总部在深圳。",
        "今天心情不错。",
    ]

    print("\n" + "=" * 60)
    print("【Few-shot 实体提取】")
    print("=" * 60)

    for text in test_texts:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt.format(text=text)}],
            max_tokens=50
        )
        print(f"\n文本: {text}")
        print(f"结果: {response.choices[0].message.content.strip()}")


def few_shot_format_conversion():
    """Few-shot 格式转换"""

    prompt = """将自然语言日期转换为标准格式（YYYY-MM-DD）。

示例1：
输入：明天
输出：{tomorrow}  # 假设今天是2024-03-15，则输出2024-03-16

示例2：
输入：下周一
输出：2024-03-18

示例3：
输入：三月底
输出：2024-03-31

示例4：
输入：2024年五月一日
输出：2024-05-01

现在转换（假设今天是2024-03-15）：
输入：{date_text}
输出："""

    test_dates = [
        "后天",
        "下个月初",
        "今年国庆节",
        "2024年元旦",
    ]

    print("\n" + "=" * 60)
    print("【Few-shot 日期格式转换】")
    print("=" * 60)

    for date_text in test_dates:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt.format(
                tomorrow="2024-03-16",
                date_text=date_text
            )}],
            max_tokens=20
        )
        print(f"\n输入: {date_text}")
        print(f"输出: {response.choices[0].message.content.strip()}")


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("请设置 OPENAI_API_KEY")
        exit()

    zero_shot_vs_few_shot()
    few_shot_entity_extraction()
    few_shot_format_conversion()
