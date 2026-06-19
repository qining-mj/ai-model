"""
01_custom_tools.py
自定义工具
"""
from langchain_core.tools import tool, StructuredTool
from pydantic import BaseModel, Field
from typing import Optional


# 简单工具
@tool
def add(a: int, b: int) -> int:
    """将两个数字相加"""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """将两个数字相乘"""
    return a * b


# 带详细描述的工具
@tool
def translate(text: str, target_language: str = "英语") -> str:
    """
    翻译文本到指定语言。

    Args:
        text: 要翻译的文本
        target_language: 目标语言，默认为英语

    Returns:
        翻译后的文本
    """
    # 模拟翻译
    translations = {
        "你好": {"英语": "Hello", "日语": "こんにちは"},
        "谢谢": {"英语": "Thank you", "日语": "ありがとう"},
    }

    if text in translations and target_language in translations[text]:
        return translations[text][target_language]

    return f"[模拟翻译] {text} -> {target_language}"


# 结构化输入工具
class WeatherInput(BaseModel):
    """天气查询输入"""
    city: str = Field(description="城市名称")
    unit: str = Field(default="celsius", description="温度单位")


@tool(args_schema=WeatherInput)
def get_weather(city: str, unit: str = "celsius") -> str:
    """查询指定城市的天气"""
    weather_data = {
        "北京": {"temp": 25, "condition": "晴"},
        "上海": {"temp": 28, "condition": "多云"},
        "广州": {"temp": 32, "condition": "阵雨"},
    }

    data = weather_data.get(city, {"temp": 20, "condition": "未知"})
    temp = data["temp"] if unit == "celsius" else data["temp"] * 9/5 + 32
    unit_str = "°C" if unit == "celsius" else "°F"

    return f"{city}: {temp}{unit_str}, {data['condition']}"


# 使用 StructuredTool 类
class SearchInput(BaseModel):
    query: str = Field(description="搜索关键词")
    max_results: int = Field(default=5, description="最大结果数")


def search_function(query: str, max_results: int = 5) -> str:
    """搜索函数"""
    results = [f"结果{i}: {query}相关内容" for i in range(1, min(max_results, 3) + 1)]
    return "\n".join(results)


search_tool = StructuredTool.from_function(
    func=search_function,
    name="search",
    description="搜索信息",
    args_schema=SearchInput
)


def demo():
    """工具演示"""
    print("=" * 60)
    print("【自定义工具演示】")
    print("=" * 60)

    # 简单工具
    print("\n【简单工具】")
    print(f"add(1, 2) = {add.invoke({'a': 1, 'b': 2})}")
    print(f"multiply(3, 4) = {multiply.invoke({'a': 3, 'b': 4})}")

    # 翻译工具
    print("\n【翻译工具】")
    print(translate.invoke({"text": "你好", "target_language": "英语"}))
    print(translate.invoke({"text": "谢谢", "target_language": "日语"}))

    # 天气工具
    print("\n【天气工具】")
    print(get_weather.invoke({"city": "北京"}))
    print(get_weather.invoke({"city": "上海", "unit": "fahrenheit"}))

    # 搜索工具
    print("\n【搜索工具】")
    print(search_tool.invoke({"query": "Python", "max_results": 3}))

    # 工具信息
    print("\n【工具信息】")
    print(f"工具名称: {get_weather.name}")
    print(f"工具描述: {get_weather.description}")


if __name__ == "__main__":
    demo()
