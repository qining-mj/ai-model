# 第3章 · MCP Client 集成 — 在应用中使用 MCP 服务

> **时长**：约 3 小时 ｜ **难度**：⭐⭐⭐⭐ ｜ **类型**：实践
>
> **目标**：掌握 MCP Client 的开发和集成

---

## 学习目标

学完本章后，你将能够：
- 开发 MCP Client
- 连接和调用 MCP Server
- 在 LangChain 中集成 MCP
- 配置 Claude Desktop 使用 MCP

---

## 知识地图

```mermaid
graph LR
  subgraph Client["Client 集成"]
    A[Python Client]
    B[LangChain 集成]
    C[Claude Desktop]
  end
  subgraph Server["Server"]
    D[MCP Server]
  end
  A --> D
  B --> D
  C --> D
```

---

## 1、Python Client 开发

### 1.1 基础 Client

**概念定义**：`ClientSession` 是 MCP Python SDK 提供的 Client 端核心类，封装了与 Server 建立连接、发送请求、接收响应的完整流程。它通过 `initialize()` 方法完成协议握手，通过 `list_tools()`、`call_tool()`、`list_resources()`、`list_prompts()` 等方法调用 Server 的各项能力。`StdioServerParameters` 则定义了如何启动本地 Server 进程。

**核心定位**：ClientSession 是"AI 应用接入 MCP 世界的大门"。开发者不需要关心底层的 JSON-RPC 消息拼装和传输细节，只需创建一个 Session、调用 `initialize()` 完成初始化、然后直接调用业务方法即可。这种高层次的封装让 MCP Client 的开发门槛大幅降低——三行代码即可连接并使用任意 MCP Server。

```python
"""
01_basic_client.py
基础 MCP Client
"""
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """主函数"""
    print("=" * 60)
    print("【MCP Client 示例】")
    print("=" * 60)

    # 服务器参数
    server_params = StdioServerParameters(
        command="python",
        args=["path/to/your/server.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化
            await session.initialize()

            # 列出工具
            print("\n可用工具:")
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")

            # 调用工具
            print("\n调用工具:")
            result = await session.call_tool("hello", {"name": "World"})
            print(f"  结果: {result.content[0].text}")

            # 列出资源
            print("\n可用资源:")
            resources = await session.list_resources()
            for resource in resources.resources:
                print(f"  - {resource.uri}: {resource.name}")

            # 列出提示
            print("\n可用提示:")
            prompts = await session.list_prompts()
            for prompt in prompts.prompts:
                print(f"  - {prompt.name}: {prompt.description}")


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 2、与 LangChain 集成

### 2.1 MCP 工具转换

**概念定义**：`MCPTool` 是一个 LangChain 工具包装器，它将 MCP Server 暴露的 Tool 转换为 LangChain 的 `BaseTool` 接口。通过持有 MCP Session 引用，MCPTool 在调用时自动通过 `session.call_tool()` 将请求转发给 MCP Server，使 LangChain Agent 可以像调用普通 LangChain 工具一样使用 MCP 工具。

**核心定位**：MCPTool 是"打通 MCP 与 LangChain 生态的桥梁"。LangChain 拥有丰富的 Agent、Chain、Tool 生态系统，而 MCP 拥有标准化的 Server 实现。通过 MCPTool 适配器，开发者无需重写工具逻辑，直接将现有的 MCP Server 生态能力导入 LangChain，实现两个生态的无缝复用。当 MCP 社区新增一个 Server 时，LangChain 项目也能立即使用。

```python
"""
02_langchain_integration.py
LangChain 集成 MCP
"""
import asyncio
from typing import List, Any
from langchain_core.tools import BaseTool, ToolException
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from pydantic import Field


class MCPTool(BaseTool):
    """MCP 工具包装器"""

    name: str = Field(description="工具名称")
    description: str = Field(description="工具描述")
    mcp_session: Any = Field(description="MCP 会话")

    def _run(self, **kwargs) -> str:
        """同步调用"""
        return asyncio.run(self._arun(**kwargs))

    async def _arun(self, **kwargs) -> str:
        """异步调用"""
        try:
            result = await self.mcp_session.call_tool(self.name, kwargs)
            return result.content[0].text
        except Exception as e:
            raise ToolException(f"MCP 调用失败: {e}")


async def create_mcp_tools(session) -> List[MCPTool]:
    """从 MCP 会话创建 LangChain 工具"""
    tools_response = await session.list_tools()
    tools = []

    for tool in tools_response.tools:
        mcp_tool = MCPTool(
            name=tool.name,
            description=tool.description,
            mcp_session=session
        )
        tools.append(mcp_tool)

    return tools


async def langchain_mcp_agent():
    """LangChain + MCP Agent"""
    # 这里假设已有 MCP 会话
    # session = ...

    # 创建工具
    # tools = await create_mcp_tools(session)

    # 模拟工具（演示用）
    from langchain_core.tools import tool

    @tool
    def search(query: str) -> str:
        """搜索信息"""
        return f"搜索结果: {query}"

    tools = [search]

    # 创建 Agent
    llm = ChatOpenAI(model="gpt-4o-mini")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个助手，可以使用 MCP 工具。"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # 运行
    result = executor.invoke({"input": "搜索 Python 教程"})
    print(f"结果: {result['output']}")


if __name__ == "__main__":
    import os
    if os.getenv("OPENAI_API_KEY"):
        asyncio.run(langchain_mcp_agent())
    else:
        print("请设置 OPENAI_API_KEY")
```

---

## 3、Claude Desktop 配置

### 3.1 配置文件

**概念定义**：Claude Desktop 的 MCP 配置文件（`claude_desktop_config.json`）是一个 JSON 格式的声明文件，用于定义 Claude Desktop 启动时需要自动加载的 MCP Server 列表。每个 Server 配置包含启动命令（`command`）、命令行参数（`args`）和环境变量（`env`），Claude Desktop 在启动时会按照配置自动启动所有 Server 并与它们建立连接。

**核心定位**：配置文件是"普通用户零代码使用 MCP 的关键"。用户不需要编写任何 Python 代码，只需在 JSON 文件中声明想用的 Server，Claude Desktop 就会自动完成启动、连接和初始化的全过程。这种"配置即用"的设计将 MCP 工具的使用门槛降到最低，让非开发者也能享受 AI 工具的便利。

Claude Desktop 通过配置文件启用 MCP Server：

**配置文件位置**:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["/path/to/your/server.py"],
      "env": {
        "API_KEY": "your-api-key"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"]
    },
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "/path/to/database.db"]
    }
  }
}
```

### 3.2 常用 Server 配置

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "D:/projects"]
    },
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "D:/my-repo"]
    },
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"]
    }
  }
}
```

---

## 4、调试技巧

### 4.1 日志调试

```python
"""
03_debug_server.py
带调试的 Server
"""
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio
import logging
import sys

# 配置日志到文件（不是 stdout）
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp_server.log'),
    ]
)
logger = logging.getLogger(__name__)

server = Server("debug-server")


@server.list_tools()
async def list_tools():
    logger.debug("list_tools called")
    return [
        Tool(
            name="test",
            description="测试工具",
            inputSchema={
                "type": "object",
                "properties": {
                    "input": {"type": "string"}
                },
                "required": ["input"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    logger.info(f"call_tool: name={name}, args={arguments}")

    try:
        if name == "test":
            result = f"测试结果: {arguments.get('input', '')}"
            logger.debug(f"Result: {result}")
            return [TextContent(type="text", text=result)]
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        raise

    raise ValueError(f"Unknown tool: {name}")


async def main():
    logger.info("Server starting...")
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
```

### 4.2 MCP Inspector

**概念定义**：MCP Inspector 是 Anthropic 提供的官方调试工具，它是一个 Web 图形界面，可以连接到 MCP Server 并可视化地浏览和调用 Server 暴露的 Tools、Resources 和 Prompts。Inspector 会记录所有 JSON-RPC 通信日志，方便开发者检查请求和响应的详细信息。

**核心定位**：Inspector 解决了"Server 开发时无法直观验证"的问题。在没有 Inspector 时，开发者只能通过代码日志或 Client 调用来间接验证 Server 功能。Inspector 提供了所见即所得的调试体验——启动后打开浏览器就能看到所有工具列表、测试调用和查看返回结果，极大提升了 Server 开发效率。

使用官方 Inspector 工具调试：

```bash
# 安装
npm install -g @modelcontextprotocol/inspector

# 运行
npx @modelcontextprotocol/inspector python your_server.py
```

---

## 5、最佳实践

| 实践 | 说明 |
|------|------|
| 错误处理 | 返回有意义的错误信息 |
| 日志记录 | 记录到文件，不输出到 stdout |
| 输入验证 | 验证所有输入参数 |
| 超时处理 | 长操作设置超时 |
| 权限控制 | 限制敏感操作 |

---

## 常见踩坑

1. **Server 进程启动失败**：Client 连接 Server 时，如果 `StdioServerParameters` 中的 `command` 路径错误或依赖未安装，Server 进程会启动失败，而 Client 可能只收到一个模糊的超时错误。务必先手动运行启动命令验证 Server 能正常运行，再用 Client 连接。

2. **异步上下文管理不当导致资源泄露**：`stdio_client` 和 `ClientSession` 都使用了异步上下文管理器（`async with`），如果使用不当（如忘记 `await` 或上下文嵌套顺序错误），可能导致 Server 进程未能正确关闭，造成僵尸进程。始终使用 `async with stdio_client(...) as (read, write):` 和 `async with ClientSession(read, write) as session:` 的正确嵌套顺序。

3. **LangChain 中 `_run` 和 `_arun` 混用问题**：`MCPTool` 继承 LangChain 的 `BaseTool` 时，`_run`（同步）和 `_arun`（异步）必须同时实现。默认的 `_run` 调用 `asyncio.run()` 包装异步调用，但如果事件循环已经在运行中（如在 Jupyter Notebook 中），会抛出 `RuntimeError`。在异步环境中优先使用 Agent 的异步执行接口。

4. **Claude Desktop 配置 JSON 语法错误**：`claude_desktop_config.json` 是严格 JSON 格式，不支持注释、末尾逗号等非标准写法。一个常见的错误是在配置的末尾多加了逗号，导致 Claude Desktop 无法解析。使用 JSON 校验工具验证配置文件的格式正确性后再启动 Claude Desktop。

5. **网络环境导致 `npx` 或 `uvx` 安装失败**：配置 Claude Desktop 使用 `npx` 或 `uvx` 启动 Server 时，如果网络环境需要代理，`npx` 在首次运行时会自动下载包，下载失败会导致 Server 无法启动。确保终端中能正常执行 `npx` 命令，或先将包全局安装后再使用本地路径启动。

---

## 课后练习

1. 编写一个 Python Client，连接到第 2 章开发的天气查询 Server，依次调用其所有 Tool、读取 Resource 和获取 Prompt，打印每次调用的返回结果。

2. 实现一个 LangChain Agent，通过 `MCPTool` 包装一个文件操作 MCP Server，让 Agent 能够根据用户的自然语言指令读取、写入和列出文件。

3. 配置 Claude Desktop，添加一个自定义 MCP Server（使用第 2 章开发的计算器 Server），然后在对话中让 Claude 使用该 Server 进行计算。

4. 使用 MCP Inspector 连接任意一个 MCP Server，记录并分析一次完整的 `tools/call` 请求-响应流程的 JSON-RPC 消息格式。

---

## 本节小结

- ✅ 掌握了 Python MCP Client 开发
- ✅ 学会了 LangChain 集成 MCP
- ✅ 配置了 Claude Desktop 使用 MCP
- ✅ 了解了调试技巧和最佳实践

---

## 模块总结

恭喜完成 **模块11：MCP 协议**！

你已经掌握了：
- ✅ MCP 协议的核心概念
- ✅ Server 开发（Tools, Resources, Prompts）
- ✅ Client 开发与集成
- ✅ Claude Desktop 配置

---

> **下一模块**：模块12 · 项目实战 — 综合运用所学构建完整应用
