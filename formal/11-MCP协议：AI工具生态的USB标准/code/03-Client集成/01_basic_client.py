"""
01_basic_client.py
基础 MCP Client
"""
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def demo_client():
    """演示 Client 功能"""
    print("=" * 60)
    print("【MCP Client 示例】")
    print("=" * 60)

    # 服务器参数（需要替换为实际路径）
    server_params = StdioServerParameters(
        command="python",
        args=["../02-Server开发/01_tools_server.py"]
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # 初始化
                await session.initialize()
                print("\n✓ 连接成功")

                # 列出工具
                print("\n【可用工具】")
                tools = await session.list_tools()
                for tool in tools.tools:
                    print(f"  - {tool.name}: {tool.description}")

                # 调用计算工具
                print("\n【调用 calculate 工具】")
                result = await session.call_tool(
                    "calculate",
                    {"expression": "2 + 3 * 4"}
                )
                print(f"  结果: {result.content[0].text}")

                # 调用天气工具
                print("\n【调用 get_weather 工具】")
                result = await session.call_tool(
                    "get_weather",
                    {"city": "北京"}
                )
                print(f"  结果: {result.content[0].text}")

                # 调用搜索工具
                print("\n【调用 search 工具】")
                result = await session.call_tool(
                    "search",
                    {"query": "Python", "limit": 3}
                )
                print(f"  结果:\n{result.content[0].text}")

    except FileNotFoundError:
        print("\n注意: 需要先启动 Server")
        print("请确保 01_tools_server.py 路径正确")
    except Exception as e:
        print(f"\n错误: {e}")


async def main():
    """主函数"""
    await demo_client()


if __name__ == "__main__":
    asyncio.run(main())
