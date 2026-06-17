import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# define_tools.py
# 定义工具：@tool 装饰器 + StructuredTool
import json
from langchain_core.tools import tool, StructuredTool
from pydantic import BaseModel, Field
from typing import Optional

# === 方式 1：@tool 装饰器（推荐） ===

@tool
def get_weather(city: str) -> str:
    """查询指定城市的当前天气。

    Args:
        city: 城市名称，如 "北京"、"上海"
    """
    weather_data = {
        "北京": "晴，25°C，湿度40%",
        "上海": "阴，28°C，湿度70%",
        "深圳": "阵雨，30°C，湿度85%",
    }
    return weather_data.get(city, f"未找到 {city} 的天气信息")

@tool
def calculator(expression: str) -> str:
    """计算数学表达式。

    Args:
        expression: 数学表达式，如 "2 + 3 * 4"
    """
    try:
        result = eval(expression)
        return f"计算结果: {result}"
    except Exception as e:
        return f"计算失败: {e}"

@tool
def search_knowledge_base(query: str) -> str:
    """搜索公司知识库，查找相关文档和信息。

    Args:
        query: 搜索关键词
    """
    kb = {
        "年假": "员工入职满1年享5天年假，满3年享10天年假。",
        "加班": "工作日加班1.5倍工资，周末2倍，法定假日3倍。",
        "报销": "差旅住宿一线城市400元/晚，其他300元/晚。",
    }
    for key, val in kb.items():
        if key in query:
            return val
    return f"未找到关于 '{query}' 的相关信息"

# === 方式 2：StructuredTool ===

class SendEmailInput(BaseModel):
    to: str = Field(description="收件人邮箱地址")
    subject: str = Field(description="邮件主题")
    body: str = Field(description="邮件正文")

def send_email_func(to: str, subject: str, body: str) -> str:
    """发送邮件（模拟）。"""
    return f"邮件已发送: 收件人={to}, 主题={subject}"

send_email = StructuredTool.from_function(
    func=send_email_func,
    name="send_email",
    description="发送电子邮件给指定收件人",
    args_schema=SendEmailInput,
)

# 工具列表
tools = [get_weather, calculator, search_knowledge_base, send_email]

# 测试
def test():
    print("get_weather:", get_weather.invoke({"city": "北京"}))
    print("calculator:", calculator.invoke({"expression": "3.14 * 10"}))
    print("search:", search_knowledge_base.invoke({"query": "年假"}))
    print("send_email:", send_email.invoke({"to": "hr@company.com", "subject": "请假", "body": "..."}))

if __name__ == "__main__":
    test()
