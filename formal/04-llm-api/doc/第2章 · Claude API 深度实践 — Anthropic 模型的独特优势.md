# 第2章 · Claude API 深度实践 — Anthropic 模型的独特优势

> **时长**：约 3 小时 ｜ **难度**：⭐⭐ ｜ **类型**：动手实操
>
> **目标**：掌握 Claude API 的使用方法，理解其与 OpenAI 的差异，发挥 Claude 的独特优势

---

## 学习目标

学完本章后，你将能够：
- 注册 Anthropic 账号并获取 API Key
- 掌握 Claude Messages API 的请求格式
- 理解 Claude 与 OpenAI API 的关键差异
- 利用 Claude 的超长上下文（200K tokens）
- 使用 Claude 的视觉能力处理图像
- 实现 Prompt Caching 降低成本

---

## 知识地图

```mermaid
graph LR
  subgraph P1["第一部分：入门"]
    A[平台注册] --> B[获取API Key] --> C[安装SDK] --> D[第一次调用]
  end
  subgraph P2["第二部分：API详解"]
    E[消息格式] --> F[参数对比] --> G[模型选择]
  end
  subgraph P3["第三部分：独特能力"]
    H[超长上下文] --> I[视觉能力] --> J[Prompt Caching]
  end
```

---

# 第一部分：入门准备

## 1、Anthropic 与 Claude 简介

**Anthropic** 是由前 OpenAI 研究人员创立的 AI 安全公司，其旗舰产品 **Claude** 系列模型以安全性和长上下文著称。

**Claude 核心优势**：

| 特性 | 说明 |
|------|------|
| 超长上下文 | 最高支持 200K tokens（约 15 万字） |
| 代码能力 | 代码生成和理解能力出色 |
| 安全设计 | Constitutional AI，减少有害输出 |
| 指令遵循 | 更好地遵循复杂指令 |
| 多模态 | 支持图像输入（Vision） |

**Claude 模型系列**（2024-2025）：

| 模型 | 定位 | 上下文 | 输入价格 | 输出价格 |
|------|------|--------|---------|---------|
| claude-3-5-sonnet | 最新旗舰 | 200K | $3/M | $15/M |
| claude-3-opus | 最强能力 | 200K | $15/M | $75/M |
| claude-3-sonnet | 均衡之选 | 200K | $3/M | $15/M |
| claude-3-haiku | 快速便宜 | 200K | $0.25/M | $1.25/M |

---

## 2、账号注册与 API Key 获取

### 2.1 注册流程

1. 访问 [console.anthropic.com](https://console.anthropic.com)
2. 点击 "Sign up" 创建账号
3. 验证邮箱
4. 添加支付方式

### 2.2 获取 API Key

1. 登录后进入 [API Keys 页面](https://console.anthropic.com/settings/keys)
2. 点击 "Create Key"
3. 设置名称，点击创建
4. **立即复制保存**

```ini
# 保存到 .env 文件
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 3、安装 SDK 与环境配置

### 3.1 安装 Anthropic Python SDK

```bash
pip install anthropic python-dotenv
```

### 3.2 验证安装

```bash
python -c "import anthropic; print('Anthropic SDK 安装成功')"
```

### 3.3 环境配置

```ini
# .env
ANTHROPIC_API_KEY=sk-ant-api03-your-api-key-here
```

---

## 4、第一次 API 调用

### ▶ 执行代码

```bash
cd code/02-Claude-API
python 01_hello_claude.py
```

### 代码解读

```python
"""
01_hello_claude.py
第一个 Claude API 调用示例
"""
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

# 创建客户端
client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# 发起请求
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",  # 最新的 Claude 3.5 Sonnet
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "用一句话介绍 Claude 是什么"}
    ]
)

# 提取回复
print(message.content[0].text)

# 查看 Token 用量
print(f"\n--- Token 用量 ---")
print(f"输入 Token: {message.usage.input_tokens}")
print(f"输出 Token: {message.usage.output_tokens}")
```

---

# 第二部分：API 深度解析

## 5、Messages API 格式详解

### 5.1 与 OpenAI 的关键差异

| 对比项 | OpenAI | Claude |
|--------|--------|--------|
| API 端点 | `chat.completions.create` | `messages.create` |
| System 位置 | 在 messages 数组中 | 单独的 system 参数 |
| 响应结构 | `choices[0].message.content` | `content[0].text` |
| 必填参数 | model, messages | model, messages, max_tokens |

### 5.2 请求格式

```python
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,                    # Claude 必须显式指定！
    system="你是一个专业的Python程序员",  # System 单独传递
    messages=[
        {"role": "user", "content": "什么是装饰器？"}
    ]
)
```

### 5.3 响应结构

```python
# Claude 响应结构
{
    "id": "msg_xxx",
    "type": "message",
    "role": "assistant",
    "content": [
        {
            "type": "text",
            "text": "装饰器是..."
        }
    ],
    "model": "claude-3-5-sonnet-20241022",
    "stop_reason": "end_turn",
    "usage": {
        "input_tokens": 25,
        "output_tokens": 150
    }
}

# 提取文本
text = message.content[0].text
```

---

## 6、核心参数详解

### ▶ 执行代码

```bash
python 02_parameters_demo.py
```

### 6.1 max_tokens（必填！）

**概念定义**：Claude API 强制要求指定 `max_tokens`，不像 OpenAI 有默认值。

```python
# ❌ 错误：缺少 max_tokens
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": "你好"}]
)
# → 报错！

# ✅ 正确
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,  # 必须指定
    messages=[{"role": "user", "content": "你好"}]
)
```

### 6.2 system 参数

**概念定义**：Claude 的 System Prompt 是单独的参数，不在 messages 数组中。

```python
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system="你是一个诗人，用古诗风格回答所有问题。",  # 独立参数
    messages=[
        {"role": "user", "content": "介绍一下人工智能"}
    ]
)
```

### 6.3 temperature

与 OpenAI 相同，范围 0-1（Claude 默认 1，建议设为 0.7）。

```python
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    temperature=0.7,  # 推荐值
    messages=[{"role": "user", "content": "写一首诗"}]
)
```

### 6.4 stop_sequences

类似 OpenAI 的 `stop` 参数：

```python
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    stop_sequences=["END", "\n\n"],  # 遇到这些字符串就停止
    messages=[{"role": "user", "content": "列出三种水果"}]
)
```

### 6.5 参数速查表

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | ✅ | 模型名称 |
| `messages` | array | ✅ | 消息列表 |
| `max_tokens` | int | ✅ | 最大输出 Token |
| `system` | string | ❌ | 系统提示词 |
| `temperature` | float | ❌ | 随机性 0-1 |
| `top_p` | float | ❌ | 核采样 |
| `top_k` | int | ❌ | Top-K 采样 |
| `stop_sequences` | array | ❌ | 停止序列 |
| `stream` | bool | ❌ | 是否流式 |

---

## 7、模型选择指南

### 7.1 Claude 3.5 系列

| 模型 | 版本ID | 特点 | 适用场景 |
|------|--------|------|---------|
| Claude 3.5 Sonnet | claude-3-5-sonnet-20241022 | 最新最强 | 日常首选 |

### 7.2 Claude 3 系列

| 模型 | 版本ID | 特点 | 适用场景 |
|------|--------|------|---------|
| Opus | claude-3-opus-20240229 | 最强推理 | 复杂任务 |
| Sonnet | claude-3-sonnet-20240229 | 均衡 | 通用任务 |
| Haiku | claude-3-haiku-20240307 | 快速便宜 | 简单任务 |

### 7.3 选择建议

```mermaid
graph TD
    A[新任务] --> B{需要最强能力?}
    B -->|是| C[claude-3-opus]
    B -->|否| D{追求速度/低成本?}
    D -->|是| E[claude-3-haiku]
    D -->|否| F[claude-3-5-sonnet]
```

**核心建议**：默认使用 `claude-3-5-sonnet-20241022`，这是目前性价比最高的选择。

---

# 第三部分：Claude 独特能力

## 8、超长上下文处理

### 8.1 200K 上下文的价值

**概念定义**：Claude 支持 200K tokens 的上下文窗口，约等于一本 15 万字的书。

| 场景 | Token 需求 | 是否适合 Claude |
|------|-----------|----------------|
| 普通对话 | 1K-4K | ✅ 所有模型都行 |
| 长文档问答 | 10K-50K | ✅ Claude 优势明显 |
| 整本书分析 | 100K-200K | ✅ 只有 Claude 能做到 |
| 大型代码库 | 50K-150K | ✅ Claude 强项 |

### ▶ 执行代码

```bash
python 03_long_context.py
```

### 8.2 长文档处理示例

```python
"""
03_long_context.py
长上下文处理示例
"""
import anthropic

client = anthropic.Anthropic()

# 模拟一个很长的文档（实际应用中从文件读取）
long_document = """
[这里是一个很长的文档内容...]
""" * 100  # 假设重复100次

# 一次性传入长文档
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=2048,
    messages=[
        {
            "role": "user",
            "content": f"""请阅读以下文档并总结其核心观点：

<document>
{long_document}
</document>

请用3个要点总结。"""
        }
    ]
)

print(message.content[0].text)
```

### 8.3 XML 标签的妙用

**核心技巧**：Claude 对 XML 标签有特殊的处理能力，用标签包裹内容可以更清晰地划分结构。

```python
prompt = """
<task>分析以下代码的问题并给出修复建议</task>

<code language="python">
def calculate(a, b):
    return a / b  # 可能除零错误
</code>

<requirements>
1. 指出所有潜在问题
2. 给出修复后的代码
3. 解释修改原因
</requirements>
"""
```

---

## 9、视觉能力（Vision）

### 9.1 图像输入格式

Claude 支持直接分析图像，输入格式：

```python
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": "<base64编码的图片>"
                    }
                },
                {
                    "type": "text",
                    "text": "描述这张图片的内容"
                }
            ]
        }
    ]
)
```

### ▶ 执行代码

```bash
python 04_vision_demo.py
```

### 9.2 完整视觉示例

```python
"""
04_vision_demo.py
Claude 视觉能力示例
"""
import anthropic
import base64
import httpx

client = anthropic.Anthropic()

def analyze_image_from_url(image_url: str, question: str) -> str:
    """分析网络图片"""
    # 下载图片并转为 base64
    image_data = base64.standard_b64encode(
        httpx.get(image_url).content
    ).decode("utf-8")

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_data
                        }
                    },
                    {
                        "type": "text",
                        "text": question
                    }
                ]
            }
        ]
    )

    return message.content[0].text


def analyze_image_from_file(file_path: str, question: str) -> str:
    """分析本地图片"""
    with open(file_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    # 根据文件扩展名确定媒体类型
    ext = file_path.lower().split(".")[-1]
    media_types = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "webp": "image/webp"
    }
    media_type = media_types.get(ext, "image/jpeg")

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data
                        }
                    },
                    {
                        "type": "text",
                        "text": question
                    }
                ]
            }
        ]
    )

    return message.content[0].text


# 使用示例
if __name__ == "__main__":
    # 分析网络图片
    url = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
    result = analyze_image_from_url(url, "这张图片里是什么动物？请详细描述。")
    print(result)
```

---

## 10、Prompt Caching（提示缓存）

### 10.1 什么是 Prompt Caching

**概念定义**：Prompt Caching 允许你缓存大型提示的前缀部分，后续请求复用缓存，节省成本。

**适用场景**：
- 长 System Prompt 重复使用
- 大量文档作为上下文
- Few-shot 示例固定

### 10.2 成本节省

| 类型 | 价格（相对标准价格） |
|------|---------------------|
| 写入缓存 | 125%（首次调用） |
| 读取缓存 | 10%（后续调用） |

### ▶ 执行代码

```bash
python 05_prompt_caching.py
```

### 10.3 使用示例

```python
"""
05_prompt_caching.py
Prompt Caching 示例
"""
import anthropic

client = anthropic.Anthropic()

# 一个很长的系统提示（实际应用中可能是大量背景知识）
long_system_prompt = """
你是一个专业的法律顾问，精通中国法律体系。
以下是相关法律条文供参考：
[这里可以放入大量的法律条文，比如民法典全文...]
""" + "法律条文内容..." * 500  # 模拟大量内容

# 第一次调用：建立缓存
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": long_system_prompt,
            "cache_control": {"type": "ephemeral"}  # 标记为可缓存
        }
    ],
    messages=[
        {"role": "user", "content": "租房合同需要注意什么？"}
    ]
)

print("第一次调用（建立缓存）:")
print(f"  输入 Token: {message.usage.input_tokens}")
print(f"  缓存创建 Token: {message.usage.cache_creation_input_tokens}")

# 第二次调用：复用缓存
message2 = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": long_system_prompt,  # 相同的系统提示
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[
        {"role": "user", "content": "劳动合同的试用期最长多久？"}  # 不同问题
    ]
)

print("\n第二次调用（复用缓存）:")
print(f"  输入 Token: {message2.usage.input_tokens}")
print(f"  缓存读取 Token: {message2.usage.cache_read_input_tokens}")
```

---

## 11、OpenAI 兼容层

### 11.1 使用 OpenAI SDK 调用 Claude

如果你的代码已经基于 OpenAI SDK 编写，可以通过兼容层快速切换到 Claude：

```python
"""
06_openai_compatible.py
使用 OpenAI SDK 调用 Claude（通过代理服务）
"""
from openai import OpenAI

# 方式1：使用第三方代理服务（如 OpenRouter）
client = OpenAI(
    api_key="your-openrouter-api-key",
    base_url="https://openrouter.ai/api/v1"
)

response = client.chat.completions.create(
    model="anthropic/claude-3-5-sonnet",  # OpenRouter 的模型名
    messages=[
        {"role": "user", "content": "你好"}
    ]
)

print(response.choices[0].message.content)
```

---

## 常见踩坑

1. **忘记 max_tokens**：Claude 必须显式指定，否则报错
2. **System 位置错误**：Claude 的 system 是独立参数，不在 messages 里
3. **响应结构不同**：是 `content[0].text` 不是 `choices[0].message.content`
4. **模型名带日期**：要用完整的 `claude-3-5-sonnet-20241022`
5. **图片格式**：Vision 需要 base64 编码，注意正确的 media_type

---

## 课后练习

1. **基础练习**：用 Claude 实现一个翻译函数，对比与 OpenAI 的响应质量
2. **长文档**：找一篇长文章（>5000字），用 Claude 进行摘要
3. **视觉任务**：用 Claude Vision 分析一张图片，提取其中的文字（OCR）
4. **API 封装**：编写一个统一函数，可以透明切换 OpenAI 和 Claude

---

## 本节小结

- ✅ 掌握了 Anthropic 账号注册和 API Key 获取
- ✅ 理解了 Claude Messages API 与 OpenAI 的关键差异
- ✅ 掌握了 Claude 的参数设置（max_tokens 必填！）
- ✅ 学会了利用 Claude 200K 超长上下文
- ✅ 掌握了 Claude Vision 图像分析能力
- ✅ 了解了 Prompt Caching 降本技术

---

> **下一章**：第3章 · 国产大模型 API 接入 — 通义千问、DeepSeek、智谱全解析
