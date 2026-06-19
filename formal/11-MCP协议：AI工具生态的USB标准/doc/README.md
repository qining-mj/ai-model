# 模块 11：MCP 协议

> **学习目标**：掌握 MCP 协议，实现 AI 系统互操作

---

## 模块概述

本模块讲解 MCP (Model Context Protocol) 协议，帮助你构建标准化的 AI 工具服务。

---

## 章节目录

| 章节 | 标题 | 核心内容 | 时长 |
|------|------|---------|------|
| 第1章 | [MCP 协议基础](第1章%20·%20MCP%20协议基础%20—%20理解%20AI%20系统互操作标准.md) | 协议概念、架构、快速开始 | 2h |
| 第2章 | [MCP Server 开发](第2章%20·%20MCP%20Server%20开发%20—%20构建自定义工具服务.md) | Tools、Resources、Prompts | 3h |
| 第3章 | [MCP Client 集成](第3章%20·%20MCP%20Client%20集成%20—%20在应用中使用%20MCP%20服务.md) | Client 开发、LangChain 集成 | 3h |

**总时长**：约 8 小时

---

## 代码文件清单

### 01-MCP基础
| 文件 | 说明 |
|------|------|
| `01_hello_mcp.py` | Hello MCP Server |

### 02-Server开发
| 文件 | 说明 |
|------|------|
| `01_tools_server.py` | Tools Server 示例 |

### 03-Client集成
| 文件 | 说明 |
|------|------|
| `01_basic_client.py` | 基础 Client |

---

## MCP 架构

```
┌─────────────────────────────────────────────────────────┐
│                    MCP 架构                             │
├─────────────────────────────────────────────────────────┤
│  Client (AI 应用)  ←── JSON-RPC ──→  Server (工具服务)  │
│                                            │            │
│                         ┌──────────────────┼────────┐   │
│                         ↓                  ↓        ↓   │
│                     [Tools]          [Resources] [Prompts]│
└─────────────────────────────────────────────────────────┘
```

---

## 三种能力类型

| 类型 | 说明 | 示例 |
|------|------|------|
| **Tools** | 可执行的函数 | 搜索、计算、API 调用 |
| **Resources** | 可读取的数据 | 文件、数据库 |
| **Prompts** | 预定义的提示 | 代码审查、翻译 |

---

## 依赖安装

```bash
# Python SDK
pip install mcp

# 或使用 uv
uv pip install mcp
```

---

## Claude Desktop 配置

配置文件位置:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["/path/to/server.py"]
    }
  }
}
```

---

## 学习路径

```
协议基础 → Server 开发 → Client 集成
    ↓          ↓            ↓
 理解架构   开发工具    集成应用
```

---

## 下一步

完成本模块后，继续学习：
- **模块12：项目实战** - 综合运用所学构建完整应用
