# 第10章 · 生产化部署 — 容错、调试与 LangGraph Platform

> **时长**：约 3 小时 ｜ **难度**：⭐⭐⭐⭐ ｜ **类型**：讲解 + 动手
>
> **目标**：掌握 LangGraph 生产化部署所需的核心能力——容错机制、时间旅行调试、CLI 工具链、部署选项与监控集成

---

## 学习目标

学完本章后，你将能够：
- 理解 LangGraph 三层容错防护：RetryPolicy、TimeoutPolicy、ErrorHandler 及其组合规则
- 为图节点配置指数退避重试、条件重试和超时策略
- 用 ErrorHandler 实现 Saga 模式（补偿事务）
- 利用 Checkpoint 快照进行时间旅行调试：回溯、重放、分叉
- 使用 LangGraph CLI 和 LangGraph Studio v2 进行本地开发和可视化调试
- 对比四种部署选项并选择适合的方案
- 集成 LangSmith 进行生产环境追踪和监控
- 遵循生产部署清单，构建可投入实际业务的 LangGraph 应用

---

## 知识地图

```mermaid
graph TD
    subgraph P1["第一部分：容错机制（Fault Tolerance）"]
        A[三层防护模型] --> B[RetryPolicy 重试策略]
        A --> C[TimeoutPolicy 超时策略]
        A --> D[ErrorHandler 错误处理器]
        B --> E[指数退避 + Jitter]
        C --> F[run_timeout / idle_timeout]
        D --> G[Saga 补偿模式]
    end
    subgraph P2["第二部分：调试与工具链"]
        H[Time Travel 调试] --> I[Replay 重放]
        H --> J[Fork 分叉]
        K[LangGraph Studio v2] --> L[可视化 + 断点调试]
        M[LangGraph CLI] --> N[dev / up / deploy]
    end
    subgraph P3["第三部分：生产部署"]
        O[部署选项对比] --> P[本地开发]
        O --> Q[Docker 部署]
        O --> R[自托管]
        O --> S[LangGraph Cloud]
        T[LangSmith 监控] --> U[追踪 / 成本分析]
        V[生产清单] --> W[Postgres / 限时 / 重试 / 监控]
    end
    P1 --> P2
    P2 --> P3
```

---

## 第一部分：容错机制

## 1、三层防护模型

生产环境中，任何节点都可能失败：LLM 调用超时、API 限频、网络闪断、数据库连接丢失。LangGraph 提供了三层防护，自底向上依次拦截失败：

```mermaid
graph TD
    subgraph Layers["三层防护组合顺序"]
        T["第一层：TimeoutPolicy<br/>超时保护"]
        R["第二层：RetryPolicy<br/>自动重试"]
        E["第三层：ErrorHandler<br/>最后兜底"]
    end
    N["Node 执行"] --> T
    T -->|超时触发| R
    T -->|正常完成| OK["返回结果"]
    R -->|重试成功| OK
    R -->|重试耗尽| E
    E -->|处理或补偿| RECOVER["恢复 / 回滚"]
```

**组合规则**：当一个节点开始执行时，LangGraph 按以下顺序应用三层防护：

1. **TimeoutPolicy**：监控执行时间，超时则抛出 `NodeTimeoutError`
2. **RetryPolicy**：捕获 `NodeTimeoutError` 或其他指定异常，按配置重试
3. **ErrorHandler**：所有重试耗尽后，调用错误处理器做最终处理

这三层可以**单独配置**，也可以**叠加使用**，LangGraph 负责将它们组合为统一的执行逻辑。

> 💡 **设计哲学**：超时防止永久阻塞，重试处理瞬时故障，错误处理器处理确定性失败。三者覆盖了生产环境绝大部分异常场景。

### 配置层级

容错策略可以在两个层级配置：

| 层级 | 配置方式 | 优先级 |
|------|---------|--------|
| **图级默认** | `graph.compile(retry_policy=..., timeout_policy=...)` | 低（被节点级覆盖） |
| **节点级** | `node.set_retry_policy(...)` / `node.set_timeout_policy(...)` | 高 |

```python
# 图级默认：所有节点共享
graph = builder.compile(
    retry_policy=RetryPolicy(max_attempts=3),
)

# 节点级覆盖：特定节点独立配置
builder.add_node("llm_call", llm_node).set_retry_policy(
    RetryPolicy(max_attempts=5, retry_on=TimeoutError)
)
```

> ⚠️ **注意**：节点级配置**完全覆盖**图级配置，不会合并。所以如果图级配置了全局重试策略，某个节点又设置了自己的 `RetryPolicy`，则该节点只使用自己的策略。

---

## 2、RetryPolicy 深度解析

`RetryPolicy` 是 LangGraph 内置的重试策略类，提供了丰富的参数来控制重试行为。

### 2.1 完整参数表

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `max_attempts` | `int` | `3` | 最大尝试次数（含首次执行） |
| `initial_interval` | `float` | `0.5` | 首次重试前等待秒数 |
| `backoff_factor` | `float` | `2.0` | 退避倍数，每次重试间隔乘以此值 |
| `max_interval` | `float` | `120.0` | 最大等待间隔上限（秒） |
| `jitter` | `bool` | `True` | 是否添加随机抖动防止惊群 |
| `retry_on` | `type / tuple / callable` | `(Exception,)` | 触发重试的异常类型或判断函数 |

### 2.2 指数退避 + Jitter 可视化

以下表格展示了 `initial_interval=0.5, backoff_factor=2.0, max_interval=30.0` 时的等待时间：

| 重试次数 | 基础退避 | 无 Jitter（固定） | 有 Jitter（随机范围） |
|---------|---------|-------------------|---------------------|
| 第 1 次 | 0.5s | 0.5s | 0.25 ~ 0.75s |
| 第 2 次 | 0.5 × 2 = 1.0s | 1.0s | 0.5 ~ 1.5s |
| 第 3 次 | 1.0 × 2 = 2.0s | 2.0s | 1.0 ~ 3.0s |
| 第 4 次 | 2.0 × 2 = 4.0s | 4.0s | 2.0 ~ 6.0s |
| 第 5 次 | 4.0 × 2 = 8.0s | 8.0s | 4.0 ~ 12.0s |
| 第 6 次 | 8.0 × 2 = 16.0s | 16.0s | 8.0 ~ 24.0s |
| 第 7 次 | 16.0 × 2 = 32.0s | 30.0s（封顶） | 15.0 ~ 30.0s（封顶） |
| 第 8 次 | 32.0 × 2 = 64.0s | 30.0s（封顶） | 15.0 ~ 30.0s（封顶） |

**Jitter 的作用**：当多个并发图实例同时失败并一起重试时，如果没有 Jitter，它们会在完全相同的时间点再次冲击下游服务——这称为"惊群效应"。Jitter 通过随机化等待时间，将请求峰均摊到一个时间窗口内。

> 💡 **最佳实践**：始终保持 `jitter=True`。Jitter 带来的收益（避免惊群）远大于额外几毫秒的延迟成本。

### 2.3 条件重试

默认情况下，`RetryPolicy` 会重试所有 `Exception`。但有些异常不需要重试（如输入校验错误 `ValueError`），有些则需要特别关注。

**按异常类型过滤**：

```python
from langgraph.pregel.retry import RetryPolicy
from openai import RateLimitError, APITimeoutError

# 只重试限频和超时错误
policy = RetryPolicy(
    max_attempts=5,
    retry_on=(RateLimitError, APITimeoutError),
)
```

**用谓词函数精确控制**：

```python
# 更细粒度的控制：使用 lambda 判断
policy = RetryPolicy(
    max_attempts=3,
    retry_on=lambda e: isinstance(e, (TimeoutError, ConnectionError, RateLimitError))
                        and "429" not in str(e),  # 状态码 429 不重试
)
```

**完整示例：为 LLM 节点配置智能重试**：

```python
from langgraph.pregel.retry import RetryPolicy

def smart_retry_rule(e: Exception) -> bool:
    """智能判断是否需要重试"""
    # 超时错误 → 重试
    if isinstance(e, TimeoutError):
        return True
    # 限频错误 → 重试（等待更长时间）
    if "rate_limit" in str(e).lower() or "429" in str(e):
        return True
    # 服务不可用 → 重试
    if "503" in str(e) or "service_unavailable" in str(e).lower():
        return True
    # 输入校验错误 → 不重试，改也没用
    if isinstance(e, ValueError):
        return False
    # 鉴权错误 → 坚决不重试
    if "auth" in str(e).lower() or "401" in str(e):
        return False
    # 默认重试
    return True

policy = RetryPolicy(
    max_attempts=5,
    initial_interval=1.0,
    backoff_factor=2.0,
    max_interval=60.0,
    jitter=True,
    retry_on=smart_retry_rule,
)

# 应用到节点
builder.add_node("llm_call", llm_node).set_retry_policy(policy)
```

### ▶ 执行代码

```powershell
cd code/10-生产化部署
python 01_retry_policy_demo.py
```

---

## 3、TimeoutPolicy

LangGraph 的 `TimeoutPolicy` 提供两种超时模式：

| 模式 | 参数名 | 语义 | 适用场景 |
|------|--------|------|---------|
| **运行超时** | `run_timeout` | 从节点开始执行的**总墙钟时间** | LLM 调用、API 请求等有明确最大等待时间的操作 |
| **空闲超时** | `idle_timeout` | 节点**没有产生任何输出**的最大时间 | 流式响应、长时间运行但应持续产生中间结果的节点 |

### 3.1 run_timeout（墙钟超时）

```python
from langgraph.pregel.timeout import TimeoutPolicy

# 节点最多执行 30 秒
builder.add_node("llm_call", llm_node).set_timeout_policy(
    TimeoutPolicy(run_timeout=30.0)
)
```

超时后，LangGraph 抛出 `NodeTimeoutError`。如果同时配置了 `RetryPolicy`，此错误会被 RetryPolicy 捕获并触发重试：

```python
# 超时 + 重试组合：总共最多尝试 3 次，每次最多 30 秒
builder.add_node("llm_call", llm_node).set_timeout_policy(
    TimeoutPolicy(run_timeout=30.0)
).set_retry_policy(
    RetryPolicy(max_attempts=3)
)
```

### 3.2 idle_timeout（空闲超时）

`idle_timeout` 解决的是更隐蔽的问题——节点"卡住"但不崩溃。比如一个流式 LLM 调用，前几秒正常产出 token，然后突然停止但进程还在跑。`run_timeout` 无法检测这种情况（因为总时间没超），而 `idle_timeout` 可以：

```python
# 节点如果 10 秒内没有新输出，判定为超时
builder.add_node("streaming_llm", stream_node).set_timeout_policy(
    TimeoutPolicy(idle_timeout=10.0)
)
```

### 3.3 refresh_on 机制

`refresh_on` 控制超时计时器何时重置：

| 取值 | 行为 | 说明 |
|------|------|------|
| `"auto"`（默认） | State 有任何更新时自动重置 | 最安全，适用于大多数场景 |
| `"heartbeat"` | 需要手动调用 `heartbeat()` | 精确控制，适合自定义逻辑的节点 |

```python
from langgraph.pregel.timeout import TimeoutPolicy, heartbeat

def long_running_node(state: dict) -> dict:
    """手动心跳的长时间运行节点"""
    for i in range(100):
        # 做一部分工作...
        process_chunk(i)
        # 告诉 LangGraph："我还活着"
        heartbeat()
    return {"result": "done"}

builder.add_node("long_task", long_running_node).set_timeout_policy(
    TimeoutPolicy(idle_timeout=30.0, refresh_on="heartbeat")
)
```

### ▶ 执行代码

```powershell
cd code/10-生产化部署
python 02_timeout_policy_demo.py
```

---

## 4、ErrorHandler 与 Saga 模式

当 RetryPolicy 重试耗尽后，ErrorHandler 是最后的兜底方案。

### 4.1 ErrorHandler 函数签名

```python
def error_handler(state: dict, error: Exception) -> Union[Command, dict]:
    """错误处理器的标准签名
    Args:
        state: 当前 State（包含错误发生时的全部上下文）
        error: 最终抛出的异常（重试耗尽后的实例）
    Returns:
        Union[Command, dict]: 可以返回 Command 来改变控制流，或返回 dict 更新 State
    """
```

**关键能力**：ErrorHandler 可以返回 `Command` 对象来**重定向执行流**，而不仅仅是更新状态。

### 4.2 基本用法

```python
from langgraph.pregel.error import ErrorHandler

def handle_api_failure(state: dict, error: Exception) -> dict:
    """API 调用失败后的兜底处理"""
    return {
        "error": str(error),
        "status": "failed",
        "fallback_response": "服务暂时不可用，请稍后重试",
    }

builder.add_node("api_call", api_node).set_error_handler(
    ErrorHandler(handle_api_failure)
)
```

### 4.3 Saga 模式：补偿事务

Saga 模式是分布式系统中的经典模式——当一系列操作中的某一步失败时，需要执行"补偿操作"来撤销之前已完成的步骤。LangGraph 的 ErrorHandler 天然支持这种模式。

```mermaid
graph LR
    subgraph Saga["Saga 模式：支付流程"]
        A["扣减库存"] --> B["扣减余额"]
        B --> C["生成订单"]
        C --> D["通知发货"]
    end
    subgraph Compensation["补偿流程"]
        B2["扣减余额 失败 ❌"] --> C2["回滚：恢复库存 🔄"]
        C2 --> D2["通知：订单取消"]
    end
    A -.-> B2
```

**完整代码示例**：

```python
from langgraph.graph import StateGraph, START, END, Command
from typing_extensions import TypedDict
from langgraph.pregel.retry import RetryPolicy
from langgraph.pregel.error import ErrorHandler

class OrderState(TypedDict):
    order_id: str
    product_id: str
    quantity: int
    user_id: str
    amount: float
    inventory_reserved: bool
    balance_deducted: bool
    order_created: bool
    error: str
    compensated: bool

# 步骤 1：扣减库存
def reserve_inventory(state: OrderState) -> dict:
    print(f"[库存] 预扣商品 {state['product_id']} x {state['quantity']}")
    # 实际业务中调用库存服务 API
    return {"inventory_reserved": True}

# 步骤 2：扣减余额
def deduct_balance(state: OrderState) -> dict:
    print(f"[余额] 扣减用户 {state['user_id']} 金额 {state['amount']}")
    # 模拟失败场景
    raise ConnectionError("支付服务暂时不可用")
    # return {"balance_deducted": True}

# 步骤 3：生成订单
def create_order(state: OrderState) -> dict:
    print("[订单] 生成订单记录")
    return {"order_created": True}

# 步骤 4：通知发货
def notify_shipping(state: OrderState) -> dict:
    print("[发货] 通知仓库发货")
    return {"notified": True}

# --- 补偿函数 ---

def compensate_inventory(state: dict, error: Exception) -> dict:
    """扣减余额失败时，补偿：恢复库存"""
    print(f"[补偿] 恢复库存：商品 {state.get('product_id')}")
    print(f"[补偿] 错误原因：{error}")
    return {
        "inventory_reserved": False,
        "compensated": True,
        "error": str(error),
    }

def compensate_notify(state: dict, error: Exception) -> Command:
    """补偿后通知用户"""
    print(f"[通知] 订单失败已取消，通知用户 {state.get('user_id')}")
    return Command(
        goto=END,
        update={"compensated": True, "error": str(error)}
    )

# 构建带 Saga 补偿的图
builder = StateGraph(OrderState)

# 正常流程节点
builder.add_node("reserve_inventory", reserve_inventory)
builder.add_node("deduct_balance", deduct_balance)
builder.add_node("create_order", create_order)
builder.add_node("notify_shipping", notify_shipping)

# 为关键节点配置重试 + 错误处理器（Saga 补偿）
builder.add_node("deduct_balance", deduct_balance).set_retry_policy(
    RetryPolicy(max_attempts=2, initial_interval=1.0, retry_on=ConnectionError)
).set_error_handler(
    ErrorHandler(compensate_inventory)
)

# 添加边
builder.add_edge(START, "reserve_inventory")
builder.add_edge("reserve_inventory", "deduct_balance")
builder.add_edge("deduct_balance", "create_order")
builder.add_edge("create_order", "notify_shipping")
builder.add_edge("notify_shipping", END)

graph = builder.compile()

# 执行测试
result = graph.invoke({
    "order_id": "ORD-001",
    "product_id": "PROD-A",
    "quantity": 2,
    "user_id": "USER-123",
    "amount": 99.99,
    "inventory_reserved": False,
    "balance_deducted": False,
    "order_created": False,
    "error": "",
    "compensated": False,
})

print(f"\n最终状态：{result}")
```

**执行结果**（预期输出）：

```
[库存] 预扣商品 PROD-A x 2
[余额] 扣减用户 USER-123 金额 99.99
[余额] 扣减用户 USER-123 金额 99.99  (重试第 1 次)
[补偿] 恢复库存：商品 PROD-A
[补偿] 错误原因：支付服务暂时不可用
最终状态：{'order_id': 'ORD-001', ..., 'inventory_reserved': False,
           'balance_deducted': False, 'order_created': False,
           'compensated': True, 'error': '支付服务暂时不可用'}
```

> 💡 **Saga 模式要点**：ErrorHandler 的返回值是关键——它返回 `dict` 更新状态，或者返回 `Command(goto=END, update=...)` 直接结束图并输出包含补偿结果的状态。

### ▶ 执行代码

```powershell
cd code/10-生产化部署
python 03_saga_pattern.py
```

---

## 第二部分：调试与工具链

## 5、时间旅行调试（Time Travel Debugging）

时间旅行是 LangGraph 最强大的调试功能之一。它利用 Checkpoint 机制，让你可以**回溯到任意历史状态**，查看、修改、甚至**重放**或**分叉**执行。

### 5.1 前置条件：Checkpointer

时间旅行的基础是 Checkpointer。没有 Checkpointer，图执行完状态就消失了：

```python
from langgraph.checkpoint.memory import MemorySaver

# 启用检查点（开发调试用）
checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)
```

> ⚠️ **生产环境**：使用 `MemorySaver` 仅适合开发调试。生产环境应使用 `PostgresSaver` 或 `SqliteSaver` 确保持久化。

### 5.2 核心 API

| API | 功能 | 返回值 |
|-----|------|--------|
| `graph.get_state_history(config)` | 获取指定 thread 的所有检查点历史 | 迭代器，按时间倒序 |
| `graph.get_state(config)` | 获取指定检查点的状态快照 | `StateSnapshot` 对象 |
| `graph.invoke(None, config)` | 从指定检查点**重放**执行（传入 `None` 表示无新输入） | 最终状态 |
| `graph.update_state(config, values)` | 在指定检查点**修改状态**（分叉） | 新的检查点配置 |

### 5.3 Replay（重放）

重放是指从某个历史检查点**重新执行**后续所有节点，不修改任何历史状态。这用于复现问题和验证修复。

```python
# 1. 先执行一次图（假设中途出错）
config = {"configurable": {"thread_id": "thread-001"}}
try:
    graph.invoke({"input": "Hello"}, config)
except Exception as e:
    print(f"执行失败：{e}")

# 2. 查看所有历史检查点
history = list(graph.get_state_history(config))
for i, snapshot in enumerate(history):
    print(f"[{i}] step={snapshot.metadata.get('step')} "
          f"next_node={snapshot.next} "
          f"state={snapshot.values}")

# 3. 选择倒数第二个检查点（出错前一刻）重放
last_valid = history[1]  # history[0] 是最终状态
replay_config = last_valid.config

# 传入 None 表示没有新输入，沿用历史的输入
final = graph.invoke(None, replay_config)
print(f"重放结果：{final}")
```

### 5.4 Fork（分叉）

分叉比重放更强大——你可以在某个检查点**修改 State**，然后从修改后的状态继续执行。这相当于"如果当时状态不同，结果会怎样"：

```python
# 1. 在图执行到中间时（比如 LLM 返回了错误格式），查看当前状态
history = list(graph.get_state_history(config))
midpoint = history[2]  # 假设这是 LLM 刚返回结果的检查点

print(f"当前消息：{midpoint.values['messages']}")

# 2. 修改状态：修正 LLM 的输出格式
corrected_state = graph.update_state(
    midpoint.config,
    {"messages": [{"role": "assistant", "content": "修正后的正确输出"}]}
)

# 3. 从修正后的状态继续执行
final = graph.invoke(None, corrected_state)
print(f"分叉执行结果：{final}")
```

### 5.5 Replay vs Fork 对比

```mermaid
graph LR
    subgraph Normal["正常执行"]
        A["检查点 1<br/>step=0"] --> B["检查点 2<br/>step=1"]
        B --> C["检查点 3<br/>step=2 ❌ 出错"]
    end
    subgraph Replay["Replay 重放"]
        D["检查点 1"] --> E["检查点 2"]
        E --> F["检查点 3'<br/>重新执行（相同输入）"]
        F --> G["检查点 4'<br/>继续执行"]
    end
    subgraph Fork["Fork 分叉"]
        H["检查点 1"] --> I["检查点 2"]
        I --> J["✏️ 修改状态"]
        J --> K["新检查点 3'<br/>（新分支）"]
        K --> L["新检查点 4'<br/>（新分支）"]
    end
    C -.->|Replay| D
    C -.->|Fork| H
```

| 特性 | Replay | Fork |
|------|--------|------|
| 状态是否修改 | 否（原样重放） | 是（可修改任意字段） |
| 执行路径 | 与原始路径相同 | 可能产生新路径 |
| 使用场景 | 复现 bug、验证修复 | 假设分析、手动纠正错误 |
| 对应传统调试 | "重新运行并断点到某行" | "修改变量值后继续" |

### ▶ 执行代码

```powershell
cd code/10-生产化部署
python 04_time_travel.py
```

---

## 6、LangGraph Studio v2

LangGraph Studio v2 是基于浏览器的可视化调试工具，取代了早期的桌面应用版本。它是开发 LangGraph 应用的最佳伴侣。

### 6.1 启动方式

```powershell
# 在项目目录中运行
langgraph dev
```

启动后访问 `http://localhost:8123` 即可打开 Studio。

### 6.2 核心功能

| 功能 | 说明 |
|------|------|
| **图可视化** | 图形化展示 graph 结构，节点、边、条件分支一目了然 |
| **逐步执行** | 按节点步进执行，每一步都可以查看 State 变更 |
| **状态检查器** | 在任意执行点查看完整的 State 内容（包括嵌套字段） |
| **时间旅行** | 直接在 UI 中点击历史检查点，拖拽滑块回溯状态 |
| **生产回放** | 导入生产环境的 trace，在本地 Studio 中回放调试 |
| **断点模式** | 在特定节点前暂停执行，进入交互式调试 |

### 6.3 UI 界面说明

Studio v2 的界面布局大致如下：

```
┌────────────────────────────────────────────────────────────┐
│  LangGraph Studio  │  Thread: thread-001  │  ⚙️  Settings   │
├────────────────┬───────────────────────────────────────────┤
│                │                                           │
│   图面板        │          State 面板                       │
│                │                                           │
│  ┌──────────┐  │  ┌─────────────────────────────────────┐  │
│  │  START   │  │  │ messages: [                         │  │
│  └────┬─────┘  │  │   {"role": "user", "content": ...}, │  │
│       │        │  │   {"role": "ai", "content": ...},   │  │
│  ┌────▼─────┐  │  │ ]                                   │  │
│  │  classify │  │  │ input: "Hello"                     │  │
│  └────┬─────┘  │  │ next_node: "classify"               │  │
│  ┌────┴────┐   │  └─────────────────────────────────────┘  │
│  │  greet  │   │                                           │
│  └────┬─────┘  │    操作按钮                               │
│  ┌────▼─────┐  │  ┌─────┐ ┌──────┐ ┌───────┐             │
│  │   END    │  │  │ ▶ 运行 │ │ ⏸ 暂停 │ │ ⏪ 回溯 │             │
│  └──────────┘  │  └─────┘ └──────┘ └───────┘             │
│                │                                           │
├────────────────┴───────────────────────────────────────────┤
│  Console / Logs 面板  │  Trace ID: abc-123                │
└────────────────────────────────────────────────────────────┘
```

> 💡 **提示**：左键点击图面板中的节点可以查看该节点的输入/输出；右键点击可以设置断点。

---

## 7、LangGraph CLI

LangGraph CLI 是整个开发部署流程的核心工具。

### 7.1 命令一览

| 命令 | 用途 | 等效传统工具 |
|------|------|-------------|
| `langgraph new` | 从模板初始化新项目 | `create-react-app` |
| `langgraph dev` | 本地开发模式 + Studio | `npm run dev` |
| `langgraph up` | Docker Compose 生产部署 | `docker-compose up` |
| `langgraph deploy` | 部署到 LangGraph Cloud | `serverless deploy` |

### 7.2 初始化项目

```powershell
# 创建新项目
langgraph new my-agent-app
cd my-agent-app
```

生成的目录结构：

```
my-agent-app/
├── src/
│   ├── agent.py          # LangGraph 图定义
│   └── utils.py          # 辅助函数
├── langgraph.json        # LangGraph 配置文件
├── requirements.txt      # Python 依赖
├── .env                  # 环境变量（本地开发）
└── Dockerfile            # Docker 部署文件
```

### 7.3 langgraph.json 配置

此文件是 LangGraph 项目的核心配置文件：

```json
{
  "python_version": "3.12",
  "dependencies": [
    ".",
    "langgraph",
    "langchain-openai"
  ],
  "graphs": {
    "my_agent": "./src/agent.py:graph"
  },
  "env": ".env",
  "dockerfile": "./Dockerfile"
}
```

关键字段说明：

| 字段 | 说明 |
|------|------|
| `graphs` | 定义可部署的图，格式为 `"名称": "模块路径:变量名"` |
| `dependencies` | Python 包依赖列表，`.` 表示本地项目 |
| `env` | 环境变量文件 |
| `dockerfile` | 自定义 Dockerfile（可选） |

### 7.4 本地开发

```powershell
# 启动开发服务器（自动检测文件变更，热重载）
langgraph dev

# 指定端口
langgraph dev --port 2024
```

启动后：
- API 服务运行在 `localhost:2024`
- Studio UI 运行在 `localhost:8123`
- 修改 Python 文件后，服务自动重载

### 7.5 生产部署准备

```powershell
# 使用 Docker Compose 启动生产环境
langgraph up

# 带自定义配置
langgraph up --config my-config.yaml
```

### ▶ 执行代码

```powershell
# 查看 CLI 帮助
langgraph --help
```

---

## 第三部分：生产部署与监控

## 8、部署选项对比

LangGraph 应用可以通过四种方式部署，从零成本的本地运行到自动扩展的云服务：

| 选项 | 设置复杂度 | 扩展性 | 成本 | 适用场景 |
|------|-----------|--------|------|---------|
| `langgraph dev` | 无 | 单用户 | 免费 | 本地开发、调试 |
| `langgraph up` + Docker | 低 | 单机多副本 | 仅基础设施 | 内部工具、小规模生产 |
| 自托管（Postgres + API Server） | 中 | 多副本 + 读写分离 | 基础设施 + 运维 | 对数据主权有要求的企业 |
| LangGraph Platform Cloud | 低 | 自动扩展 | 按量计费 | 面向用户的生产服务 |

### 8.1 自托管方案要点

自托管需要自己搭建以下组件：

```mermaid
graph TD
    subgraph SelfHosted["自托管架构"]
        LB["负载均衡器"] --> API1["API Server 副本 1"]
        LB --> API2["API Server 副本 2"]
        LB --> API3["API Server 副本 3"]
        API1 --> PG[("Postgres <br/>（检查点 + 状态）")]
        API2 --> PG
        API3 --> PG
        API1 --> Q[("消息队列 <br/>（异步任务）")]
        API2 --> Q
        API3 --> Q
    end
```

关键依赖：

```python
# 安装生产环境所需的额外包
# pip install langgraph-checkpoint-postgres psycopg2-binary

from langgraph.checkpoint.postgres import PostgresSaver

# 使用 Postgres 作为持久化检查点存储
checkpointer = PostgresSaver.from_conn_string(
    "postgresql://user:password@host:5432/langgraph"
)

graph = builder.compile(checkpointer=checkpointer)
```

> ⚠️ **重要**：`MemorySaver` 在进程重启后数据全部丢失。**生产环境必须使用 `PostgresSaver`**，否则你的图没有持久化能力，时间旅行、断点恢复等功能全部失效。

---

## 9、LangSmith 集成

LangSmith 是 LangChain/LangGraph 的可观测性平台，提供追踪、调试、评估、监控一站式服务。

### 9.1 启用追踪

```python
import os
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = "your-api-key"
os.environ["LANGSMITH_PROJECT"] = "my-agent-project"
```

或者通过 LangGraph CLI 的配置文件：

```json
// langgraph.json
{
  "env": ".env",
  "langsmith": {
    "tracing": true,
    "project_name": "my-agent-production"
  }
}
```

### 9.2 在 LangSmith 中能看到的

```
┌──────────────────────────────────────────────────────────────────┐
│  LangSmith Dashboard  │  Project: my-agent-production           │
├──────────────────────────────────────────────────────────────────┤
│  Runs 列表                                                        │
│  ┌──────┬──────────┬────────┬──────────┬──────────┬──────────┐  │
│  │ 时间 │ 图名称    │ Thread │ 耗时     │ Token数  │ 状态     │  │
│  ├──────┼──────────┼────────┼──────────┼──────────┼──────────┤  │
│  │ 10:32 │ my_agent │ t-001  │ 12.3s   │ 1,234   │ ✅ 成功   │  │
│  │ 10:31 │ my_agent │ t-002  │ 45.7s   │ 5,678   │ ❌ 失败   │  │
│  │ 10:30 │ my_agent │ t-003  │ 8.1s    │ 890     │ ✅ 成功   │  │
│  └──────┴──────────┴────────┴──────────┴──────────┴──────────┘  │
│                                                                  │
│  点击某一行展开详情：                                              │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ Run Detail: my_agent / t-002                                │  │
│  │                                                             │  │
│  │  Timeline:                                                  │  │
│  │  START [0.0s] → classify [0.5s] → llm_call [3.2s]          │  │
│  │       → search_api [15.1s] ❌ → RETRY [18.3s]               │  │
│  │       → search_api [20.4s] → llm_call [25.7s] → END        │  │
│  │                                                             │  │
│  │  Token Usage:                                               │  │
│  │  - 总 Prompt tokens: 3,456                                   │  │
│  │  - 总 Completion tokens: 2,222                               │  │
│  │  - 总费用: $0.123                                            │  │
│  └─────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

### 9.3 LangSmith 核心用途

| 场景 | 操作 | 价值 |
|------|------|------|
| 调试失败 | 筛选 `status=error` 的 runs，查看具体节点错误 | 快速定位问题节点 |
| 性能分析 | 查看每个节点的执行耗时，找到瓶颈 | 优化慢节点 |
| 成本控制 | 监控每个 thread 的 token 消耗 | 预估和优化 API 费用 |
| 回归测试 | 使用 LangSmith 数据集批量测试图 | 防止变更引入 bug |
| 生产回放 | 将生产 trace 导入 Studio 进行本地调试 | 安全复现线上问题 |

---

## 10、生产部署清单

将 LangGraph 应用推向生产环境前，逐项检查以下清单：

### 10.1 检查点存储

```python
# ❌ 错误：使用 MemorySaver
from langgraph.checkpoint.memory import MemorySaver
graph = builder.compile(checkpointer=MemorySaver())  # 进程重启后数据丢失

# ✅ 正确：使用 PostgresSaver
from langgraph.checkpoint.postgres import PostgresSaver
checkpointer = PostgresSaver.from_conn_string(
    os.environ["DATABASE_URL"]
)
graph = builder.compile(checkpointer=checkpointer)
```

### 10.2 超时配置

为所有**调用外部服务**的节点配置超时：

```python
# 为 LLM 调用节点设置 60 秒超时
builder.add_node("llm_call", llm_node).set_timeout_policy(
    TimeoutPolicy(run_timeout=60.0)
)

# 为外部 API 节点设置 30 秒超时 + 空闲超时
builder.add_node("search_api", search_node).set_timeout_policy(
    TimeoutPolicy(run_timeout=30.0, idle_timeout=10.0)
)
```

### 10.3 重试配置

| 节点类型 | 建议策略 |
|---------|---------|
| LLM 调用 | 3-5 次，退避 1s→2s→4s，只重试 RateLimitError / TimeoutError |
| HTTP API | 3 次，退避 0.5s→1s→2s，重试所有 5xx 错误 |
| 数据库操作 | 2 次，退避 0.1s→0.2s，重试连接异常 |
| 本地计算 | 不重试 |

### 10.4 递归限制

```python
# 防止无限循环：最大 100 个超步
graph = builder.compile(
    checkpointer=checkpointer,
    recursion_limit=100,
)
```

### 10.5 流式与持久性

```python
# 根据业务需求选择 durability 级别
graph = builder.compile(
    checkpointer=checkpointer,
    # "complete": 每个超步结束保存检查点
    # "major": 仅在图终止时保存
    # "minor": 在特定节点后保存（需显式标记）
)

# 生产环境建议使用 stream_mode="updates" + 异步流
async for chunk in graph.astream(input, config, stream_mode="updates"):
    for node_name, update in chunk.items():
        print(f"[{node_name}] {update}")
```

### 10.6 监控与日志

```python
import logging
import os

# 1. 启用 LangSmith 追踪
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = "production"

# 2. 配置 Python 日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("langgraph")

# 3. 在节点中记录关键信息
def process_node(state: dict) -> dict:
    logger.info(f"Processing order {state.get('order_id')}")
    try:
        result = do_work(state)
        logger.info(f"Order {state.get('order_id')} completed")
        return result
    except Exception as e:
        logger.error(f"Order {state.get('order_id')} failed: {e}")
        raise
```

### 10.7 密钥管理

```python
# ❌ 错误：密钥硬编码
llm = ChatOpenAI(api_key="sk-xxxxx")

# ✅ 正确：从环境变量读取
from dotenv import load_dotenv
load_dotenv()
llm = ChatOpenAI(api_key=os.environ["OPENAI_API_KEY"])

# ✅ 生产环境最佳实践：使用密钥管理服务
# 例如 AWS Secrets Manager、Azure Key Vault、Vault
```

### 10.8 节点级单元测试

```python
# 每个节点应该是可独立测试的纯函数
def test_classify_node():
    state = {"messages": [{"role": "user", "content": "Hello"}]}
    result = classify_node(state)
    assert "intent" in result
    assert result["intent"] in ("greeting", "question", "goodbye")

def test_retry_policy():
    """验证重试策略只捕获预期异常"""
    from langgraph.pregel.retry import RetryPolicy
    
    policy = RetryPolicy(max_attempts=3, retry_on=TimeoutError)
    
    # 应触发重试
    assert policy.should_retry(TimeoutError("timeout")) is True
    # 不应触发重试
    assert policy.should_retry(ValueError("bad input")) is False
```

### 生产检查清单总表

| 编号 | 检查项 | 必须/推荐 | 验证方式 |
|------|--------|-----------|---------|
| 1 | 使用 PostgresSaver 而非 MemorySaver | **必须** | 代码审查 |
| 2 | 所有外部调用节点配置超时 | **必须** | 代码审查 |
| 3 | 不可靠服务配置重试策略 | **推荐** | 代码审查 |
| 4 | 关键节点配置 ErrorHandler 或 Saga 补偿 | **推荐** | 集成测试 |
| 5 | 设置合理的 recursion_limit | **必须** | 代码审查 |
| 6 | LangSmith 追踪已启用 | **推荐** | 验证 trace 数据 |
| 7 | API 密钥通过环境变量注入 | **必须** | 代码审查 + 扫描 |
| 8 | 每个节点有独立单元测试 | **推荐** | CI 覆盖率报告 |
| 9 | 所有外部依赖有熔断兜底 | **推荐** | 混沌工程测试 |

> 💡 **一步到位**：如果你的项目刚起步，至少保证前三项（PostgresSaver + 超时 + 重试）。这三项覆盖了 90% 的生产故障场景。

---

## 11、生产部署完整示例

将前面所有知识整合到一个完整示例中：

```python
import os
import logging
from typing_extensions import TypedDict
from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.pregel.retry import RetryPolicy
from langgraph.pregel.timeout import TimeoutPolicy
from langgraph.pregel.error import ErrorHandler

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("production_agent")

# --- 状态定义 ---
class AgentState(TypedDict):
    input: str
    output: str
    error: str
    retry_count: int

# --- 节点定义 ---
def llm_node(state: AgentState) -> dict:
    logger.info(f"LLM 调用开始，输入: {state['input'][:50]}...")
    # 实际调用 LLM
    return {"output": "处理结果"}

def fallback_handler(state: AgentState, error: Exception) -> dict:
    logger.error(f"所有重试耗尽: {error}")
    return {
        "error": str(error),
        "output": "服务暂时不可用，请稍后重试",
    }

# --- 构建生产级图 ---
builder = StateGraph(AgentState)

builder.add_node("llm_call", llm_node).set_timeout_policy(
    TimeoutPolicy(run_timeout=30.0)
).set_retry_policy(
    RetryPolicy(
        max_attempts=3,
        initial_interval=1.0,
        backoff_factor=2.0,
        jitter=True,
    )
).set_error_handler(
    ErrorHandler(fallback_handler)
)

builder.add_edge(START, "llm_call")
builder.add_edge("llm_call", END)

# --- 编译（带上 Postgres 检查点） ---
checkpointer = PostgresSaver.from_conn_string(
    os.environ["DATABASE_URL"]
)

graph = builder.compile(
    checkpointer=checkpointer,
    recursion_limit=50,
)

# 生产环境调用方式
config = {"configurable": {"thread_id": "prod-thread-001"}}
result = graph.invoke(
    {"input": "用户问题"},
    config,
)
```

---

## 12、课程总结

恭喜你完成了整门 LangGraph 课程的学习！让我们回顾一下走过的路。

### 12.1 十章知识全景

```mermaid
graph TD
    subgraph Foundation["基础篇"]
        C1["第1章 快速上手<br/>从链到图"] --> C2["第2章 StateGraph 核心<br/>状态与归约器"]
    end
    subgraph Core["进阶篇"]
        C2 --> C3["第3章 图结构<br/>并行与子图"]
        C3 --> C4["第4章 控制流<br/>Box/Node/命令"]
        C4 --> C5["第5章 检查点<br/>断点与持久化"]
    end
    subgraph Application["应用篇"]
        C5 --> C6["第6章 ToolNode<br/>工具调用"]
        C6 --> C7["第7章 Agent<br/>React Agent"]
        C7 --> C8["第8章 多 Agent<br/>协作系统"]
    end
    subgraph Production["生产篇"]
        C8 --> C9["第9章 API 服务<br/>FastAPI 集成"]
        C9 --> C10["第10章 生产部署<br/>容错/调试/Platform"]
    end
```

| 篇章 | 章节 | 核心能力 |
|------|------|---------|
| **基础篇** | 1-2 | StateGraph 基本构建、State 模式、Reducer、节点通信 |
| **进阶篇** | 3-5 | 并行执行、高级控制流、Checkpoint 持久化、断点 |
| **应用篇** | 6-8 | ToolNode 工具调用、ReAct Agent、多 Agent 协作 |
| **生产篇** | 9-10 | API 服务集成、容错机制、调试工具、生产部署 |

### 12.2 关键思维转变

学习 LangGraph 最重要的收获，是**思维模式的转变**：

| 旧的思维方式 | 新的思维方式 |
|-------------|-------------|
| 线性管道：A → B → C | 有向图：节点 + 边 + 条件分支 |
| 隐式状态传递 | 显式 State 模式定义 |
| 顺序执行 | 超步 + 并行 |
| 一次运行 | 持久化 + 断点 + 时间旅行 |
| 固定流程 | 动态路由 + Agent 决策 |
| 不可恢复的错误 | 容错 + 重试 + Saga 补偿 |

### 12.3 学习路径图

```
初学者
  │
  ▼
Chain（线性链）────── 简单任务，一行代码搞定
  │
  ▼
Graph（有状态图）──── 需要分支和循环
  │
  ▼
Agent（单智能体）──── LLM 自己做路由决策
  │
  ▼
Multi-Agent（多智能体）── 分工协作，各司其职
  │
  ▼
Production（生产化）── 容错、监控、扩展
```

### 12.4 下一步学习方向

完成本课程后，你可以继续探索：

1. **LangGraph 官方文档**：深入阅读 API 参考和最佳实践（`docs.langchain.com/langgraph`）
2. **LangChain v1 集成**：了解 LangGraph 如何与 LangChain 的工具链、Memory、Callbacks 深度集成
3. **社区生态**：探索 LangGraph Hub（共享图模板）、LangGraph Examples 仓库
4. **高级主题**：自定义 Checkpointer 实现、分布式图执行、图编译优化
5. **实战项目**：用 LangGraph 构建完整的客服机器人、代码审查 Agent、数据分析 Copilot

> 💡 **最后一句话**：LangGraph 不仅仅是另一个框架——它是 AI 应用从"脚本"进化到"系统"的运行时基础设施。掌握了它，你就拥有了构建复杂、可靠、可扩展 AI 系统的核心能力。

---

## 常见踩坑

1. **MemorySaver 用于生产**：开发时使用 MemorySaver 很方便，但部署到生产环境后，每次重启所有用户的对话状态都会丢失。务必换成 PostgresSaver，并在部署前验证连接字符串的正确性。

2. **ErrorHandler 不执行**：如果 ErrorHandler 本身抛出异常（比如访问了 State 中不存在的 key），则整个图会直接崩溃，ErrorHandler 的补偿逻辑不会执行。确保 ErrorHandler 内部是防御性编程——对所有可能缺失的 key 使用 `.get()` 并提供默认值。

3. **RetryPolicy + TimeoutPolicy 组合陷阱**：TimeoutPolicy 的超时时间不会随重试重置。一个节点如果设置了 `run_timeout=30s` 和 `max_attempts=3`，三次重试的**总时间**只有 30 秒，而不是每次 30 秒。如果需要每次重试都有独立的超时，需要在 ErrorHandler 中手动实现。

4. **`langgraph dev` 端口冲突**：如果 8123 端口被占用，Studio 会启动失败。使用 `langgraph dev --port 8124` 指定其他端口。同时注意，`langgraph dev` 和 `langgraph up` 不能同时运行，因为它们都会占用 API 端口。

5. **时间旅行时 thread_id 不匹配**：`get_state_history(config)` 需要传入正确的 `configurable.thread_id`。不同 thread 的历史是隔离的——如果 A 线程中执行的图，用 B 线程的 config 去查询历史，结果为空。务必通过统一的方式生成和管理 thread_id（如用 session_id 或 user_id）。

---

## 课后练习

1. **配置生产级重试策略**：为以下三个节点分别设计 RetryPolicy：(a) OpenAI LLM 调用 (b) 外部汇率查询 API (c) 本地文件读取。考虑每种场景下，哪些异常值得重试，哪些不值得。

2. **实现 Saga 模式**：构建一个"用户注册"图，包含三个步骤：创建用户 → 发送欢迎邮件 → 赠送新人优惠券。如果发送邮件失败，需要回滚用户创建和优惠券赠送。用 ErrorHandler 实现完整的补偿逻辑。

3. **时间旅行调试实战**：创建一个可能出错的图（比如随机模拟 API 失败），用 `get_state_history` 找到失败的检查点，然后分别用 Replay 和 Fork 两种方式恢复执行。对比两种方式的结果差异并总结适用场景。

4. **完整生产部署**：用 `langgraph new` 创建一个新项目，在其中定义一个多 Agent 图，配置好 RetryPolicy、TimeoutPolicy、PostgresSaver，然后用 `langgraph up` 启动并测试。完成后用 LangSmith 查看完整的 trace 数据。

---

## 本节小结

- ✅ 理解了 LangGraph 三层容错防护模型：TimeoutPolicy → RetryPolicy → ErrorHandler
- ✅ 掌握了 RetryPolicy 的完整参数配置，包括指数退避、Jitter、条件重试
- ✅ 学会了用 TimeoutPolicy 设置运行超时和空闲超时，避免节点永久阻塞
- ✅ 实现了 ErrorHandler 和 Saga 补偿模式，处理重试耗尽后的兜底逻辑
- ✅ 掌握了时间旅行调试：Replay（重放）和 Fork（分叉）两种模式
- ✅ 学会了使用 LangGraph Studio v2 进行可视化调试
- ✅ 理解了 LangGraph CLI 命令链：`new` → `dev` → `up` → `deploy`
- ✅ 对比了四种部署选项，理解了自托管架构的关键组件
- ✅ 集成了 LangSmith 进行生产环境追踪和成本监控
- ✅ 掌握了生产部署清单，确保 LangGraph 应用可靠运行

---

> **课程完成**：恭喜你完成了全部 10 章的学习！从最基础的 StateGraph 构建，到 Agent 系统设计，再到生产化部署——你已经具备了用 LangGraph 构建专业级 AI 应用的完整知识体系。
