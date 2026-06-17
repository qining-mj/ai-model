import warnings; warnings.filterwarnings('ignore', message='Core Pydantic V1 functionality')
# 04_error_handling_tools.py
# 工具错误处理与回退
from langchain_core.tools import tool

@tool
def risky_api_call(query: str) -> str:
    """调用可能失败的外部 API。"""
    try:
        if "fail" in query.lower():
            raise ConnectionError("API 连接超时")
        return f"API 返回: 关于 '{query}' 的查询结果"
    except Exception as e:
        return f"错误: {e}"

@tool
def fallback_search(query: str) -> str:
    """备用搜索工具，当主工具失败时使用。"""
    return f"备用搜索: '{query}' 的基本信息（缓存版本）"

@tool
def safe_divide(expression: str) -> str:
    """安全除法，处理除零错误。

    Args:
        expression: 格式为 "a / b"
    """
    try:
        parts = expression.split("/")
        if len(parts) == 2:
            a, b = float(parts[0]), float(parts[1])
            if b == 0:
                return "错误: 除数不能为零"
            return f"{a} / {b} = {a / b}"
        return "格式错误，请使用 'a / b' 格式"
    except Exception as e:
        return f"计算失败: {e}"

# 测试
print("=== 正常调用 ===")
print(risky_api_call.invoke({"query": "天气预报"}))

print("\n=== 失败调用 ===")
print(risky_api_call.invoke({"query": "test fail"}))

print("\n=== 备用工具 ===")
print(fallback_search.invoke({"query": "天气预报"}))

print("\n=== 安全除法 ===")
print(safe_divide.invoke({"expression": "10 / 3"}))
print(safe_divide.invoke({"expression": "10 / 0"}))
