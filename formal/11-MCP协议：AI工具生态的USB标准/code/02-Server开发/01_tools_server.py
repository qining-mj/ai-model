"""
01_tools_server.py
Tools Server 示例
"""
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio


server = Server("tools-demo")


@server.list_tools()
async def list_tools():
    """列出工具"""
    return [
        Tool(
            name="calculate",
            description="执行数学计算",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式"
                    }
                },
                "required": ["expression"]
            }
        ),
        Tool(
            name="get_weather",
            description="获取城市天气",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称"
                    }
                },
                "required": ["city"]
            }
        ),
        Tool(
            name="search",
            description="搜索信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "搜索关键词"},
                    "limit": {"type": "integer", "description": "结果数量", "default": 5}
                },
                "required": ["query"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """调用工具"""
    if name == "calculate":
        try:
            expression = arguments["expression"]
            allowed = set("0123456789+-*/.() ")
            if not all(c in allowed for c in expression):
                return [TextContent(type="text", text="错误: 不支持的字符")]
            result = eval(expression)
            return [TextContent(type="text", text=f"计算结果: {result}")]
        except Exception as e:
            return [TextContent(type="text", text=f"计算错误: {e}")]

    elif name == "get_weather":
        city = arguments["city"]
        weather_data = {
            "北京": "晴，25°C",
            "上海": "多云，28°C",
            "广州": "小雨，30°C",
        }
        weather = weather_data.get(city, "未知城市")
        return [TextContent(type="text", text=f"{city}天气: {weather}")]

    elif name == "search":
        query = arguments["query"]
        limit = arguments.get("limit", 5)
        results = [f"结果{i}: {query}相关内容" for i in range(1, min(limit, 5) + 1)]
        return [TextContent(type="text", text="\n".join(results))]

    raise ValueError(f"Unknown tool: {name}")


async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
