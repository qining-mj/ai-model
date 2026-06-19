# 模块4：大模型 API 调用实战

> **学习时长**：约 20 小时 ｜ **难度**：⭐⭐⭐ ｜ **状态**：✅ 已完成

---

## 模块简介

本模块系统讲解主流大模型 API 的使用方法，从 OpenAI、Claude 到国产大模型，全面覆盖。同时介绍多模型统一封装、流式输出、Function Calling 等核心工程能力。

---

## 学习目标

完成本模块后，你将能够：
- ✅ 熟练使用 OpenAI API 的各种功能
- ✅ 掌握 Claude API 的独特特性
- ✅ 接入国产大模型（通义千问、DeepSeek、智谱GLM）
- ✅ 设计多模型适配层，实现透明切换
- ✅ 实现流式输出和 SSE 协议
- ✅ 使用 Function Calling 让模型调用外部工具

---

## 章节目录

| 章节 | 标题 | 时长 | 难度 |
|------|------|------|------|
| 第1章 | [OpenAI API 完全指南](第1章%20·%20OpenAI%20API%20完全指南%20—%20从注册到精通.md) | 4h | ⭐⭐ |
| 第2章 | [Claude API 深度实践](第2章%20·%20Claude%20API%20深度实践%20—%20Anthropic%20模型的独特优势.md) | 3h | ⭐⭐ |
| 第3章 | [国产大模型 API 接入](第3章%20·%20国产大模型%20API%20接入%20—%20通义千问、DeepSeek、智谱全解析.md) | 4h | ⭐⭐ |
| 第4章 | [API 统一封装与切换](第4章%20·%20API%20统一封装与切换%20—%20多模型适配层设计.md) | 3h | ⭐⭐⭐ |
| 第5章 | [流式输出与实时响应](第5章%20·%20流式输出与实时响应%20—%20SSE%20协议深度实践.md) | 3h | ⭐⭐⭐ |
| 第6章 | [Function Calling 机制](第6章%20·%20Function%20Calling%20机制%20—%20让%20LLM%20调用外部工具.md) | 4h | ⭐⭐⭐ |

---

## 代码示例

```
code/
├── 01-OpenAI-API/               # OpenAI API 示例
│   ├── 01_hello_openai.py           # 基础调用
│   ├── 02_parameters_demo.py        # 参数演示
│   ├── 03_model_comparison.py       # 模型对比
│   ├── 04_multi_turn_chat.py        # 多轮对话
│   ├── 05_error_handling.py         # 错误处理
│   └── 06_token_counting.py         # Token 计数
│
├── 02-Claude-API/               # Claude API 示例
│   ├── 01_hello_claude.py           # 基础调用
│   ├── 02_parameters_demo.py        # 参数演示
│   ├── 03_long_context.py           # 长文本处理
│   └── 04_vision_demo.py            # 多模态示例
│
├── 03-国产大模型API/             # 国产模型示例
│   ├── 01_qwen_basic.py             # 通义千问
│   ├── 02_deepseek_basic.py         # DeepSeek
│   └── 03_glm_basic.py              # 智谱GLM
│
├── 04-统一封装/                 # 多模型适配层
│   ├── 01_unified_interface.py      # 统一接口定义
│   ├── 02_llm_factory.py            # 工厂方法
│   ├── 03_model_router.py           # 智能路由
│   ├── 04_fallback_chain.py         # 故障转移
│   └── 05_cost_tracker.py           # 成本追踪
│
├── 05-流式输出/                 # SSE 流式处理
│   ├── 01_stream_basic.py           # 基础流式
│   ├── 02_fastapi_stream.py         # FastAPI 服务
│   ├── 03_stream_error_handling.py  # 错误处理
│   └── 04_async_stream.py           # 异步流式
│
└── 06-Function-Calling/         # 工具调用
    ├── 01_tool_definition.py        # 工具定义
    ├── 02_function_calling_basic.py # 基础调用
    ├── 03_parallel_tool_calls.py    # 并行调用
    └── 04_multi_tool_agent.py       # 多工具Agent
```

---

## 环境准备

```bash
# 安装依赖
pip install openai anthropic python-dotenv tiktoken fastapi uvicorn

# 配置环境变量（.env 文件）
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-ant-xxx
DEEPSEEK_API_KEY=sk-xxx
DASHSCOPE_API_KEY=sk-xxx
ZHIPU_API_KEY=xxx.xxx
```

---

## 核心知识点

### API 调用对比

| 特性 | OpenAI | Claude | DeepSeek | 通义千问 |
|------|--------|--------|----------|---------|
| SDK | openai | anthropic | openai (兼容) | openai (兼容) |
| System 消息 | messages内 | 独立参数 | messages内 | messages内 |
| 流式输出 | ✅ | ✅ | ✅ | ✅ |
| Function Calling | ✅ | ✅ | ✅ | ✅ |
| 价格 (每M Token) | $2.5-$15 | $3-$15 | ¥1-2 | ¥0.3-2 |

### 统一封装架构

```
┌─────────────────────────────────────────┐
│              业务代码                    │
├─────────────────────────────────────────┤
│           统一 LLM 接口                  │
│  ┌─────┬─────┬─────┬─────┬─────┐       │
│  │OpenAI│Claude│DeepSeek│Qwen│GLM│       │
│  └─────┴─────┴─────┴─────┴─────┘       │
├─────────────────────────────────────────┤
│  路由策略 │ 故障转移 │ 成本追踪          │
└─────────────────────────────────────────┘
```

---

## 模块总结

完成本模块学习后，你将：

1. **熟练调用主流 API** - OpenAI、Claude、国产模型
2. **理解底层机制** - 参数含义、流式输出、Function Calling
3. **具备工程能力** - 错误处理、重试、统一封装
4. **能做技术选型** - 根据需求选择合适的模型和调用方式

---

## 下一步

完成本模块后，建议继续学习：
- **模块5：Prompt Engineering** - 提示词工程，与大模型高效沟通
- **模块6：LangChain 框架** - AI 应用开发框架（已完成）

---

> **版本**：v1.0 ｜ **更新日期**：2024年
