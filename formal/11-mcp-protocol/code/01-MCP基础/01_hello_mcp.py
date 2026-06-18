"""
01_hello_mcp.py
Hello MCP Server
"""
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio


server = Server("hello-mcp")


@server.list_tools()
async def list_tools():
    """列出可用工具"""
    return [
        Tool(
            name="hello",
            description="向指定的人打招呼",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "要打招呼的人名"
                    }
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="add",
            description="两数相加",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "第一个数"},
                    "b": {"type": "number", "description": "第二个数"}
                },
                "required": ["a", "b"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """调用工具"""
    if name == "hello":
        person_name = arguments.get("name", "World")
        return [TextContent(type="text", text=f"Hello, {person_name}!")]

    elif name == "add":
        a = arguments.get("a", 0)
        b = arguments.get("b", 0)
        return [TextContent(type="text", text=f"{a} + {b} = {a + b}")]

    raise ValueError(f"Unknown tool: {name}")


async def main():
    """主函数"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
