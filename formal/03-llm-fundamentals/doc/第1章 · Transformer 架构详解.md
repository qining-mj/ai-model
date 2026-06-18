# 第1章 · Transformer 架构详解

> **时长**：约 3 小时 ｜ **难度**：⭐⭐⭐ ｜ **类型**：原理理解
>
> **目标**：深入理解 Self-Attention 和 Transformer 架构

---

## 1.1 为什么需要 Transformer

### RNN 的困境

```
RNN 的顺序处理

词1 → 词2 → 词3 → ... → 词100
 ↓     ↓     ↓            ↓
h1  → h2  → h3  → ... → h100

问题1：长距离依赖
  词100 想"记住"词1的信息，需要经过99次传递
  信息在传递中逐渐丢失（梯度消失）

问题2：无法并行
  必须等词1处理完才能处理词2
  训练速度慢
```

### Attention 的引入

> **核心思想：直接关注重要的部分，而不是顺序传递**

```
传统 RNN                      Attention 机制
─────────────────────────────────────────────
词1 → 词2 → 词3              词1 ←──→ 词2 ←──→ 词3
顺序传递信息                    ↖     ↗↖     ↗
                               任意位置直接交互
```

### Transformer 的革命

**2017年 Google 提出：完全基于 Attention，抛弃 RNN**

```
┌─────────────────────────────────────────────┐
│  Transformer = Self-Attention + 前馈网络    │
│                                             │
│  ✓ 并行计算 — 所有位置同时处理              │
│  ✓ 长距离依赖 — 任意位置直接交互            │
│  ✓ 可扩展 — 参数越多效果越好                │
└─────────────────────────────────────────────┘
```

---

## 1.2 Self-Attention 机制深度解析

### 直觉理解

**场景：理解句子 "小明把书还给了图书馆"**

```
"小明把书还给了图书馆"
   ↓
处理 "还" 这个词时，需要关注：
  - "小明" — 谁在还？
  - "书" — 还什么？
  - "图书馆" — 还给谁？

Self-Attention 让每个词都能"看到"其他所有词
并自动学习该关注哪些词
```

### Query、Key、Value

```
类比：图书馆找书

Query (Q): 我要找什么书？    ← "我想找一本关于AI的书"
Key (K):   书的标签是什么？  ← 每本书都有标签
Value (V): 书的实际内容     ← 书的具体内容

流程：
1. 用 Query 和所有 Key 计算相似度
2. 相似度高的 Key 对应的 Value 权重大
3. 加权求和得到结果
```

### 计算流程

```
输入: X (序列中每个词的向量)

Step 1: 生成 Q, K, V
  Q = X × W_Q    (查询)
  K = X × W_K    (键)
  V = X × W_V    (值)

Step 2: 计算注意力分数
  Score = Q × K^T    (点积衡量相似度)
  
Step 3: 缩放
  Score = Score / √d_k    (d_k 是维度，防止数值过大)

Step 4: Softmax 归一化
  Attention = softmax(Score)    (转换为概率分布)

Step 5: 加权求和
  Output = Attention × V    (用注意力权重加权 Value)
```

### 可视化

```
输入: "我 爱 北京"

注意力权重矩阵：
        我    爱    北京
      ┌────┬────┬────┐
  我  │0.5 │0.2 │0.3 │  ← "我"关注各个词的程度
      ├────┼────┼────┤
  爱  │0.3 │0.3 │0.4 │  ← "爱"关注各个词的程度
      ├────┼────┼────┤
 北京 │0.2 │0.3 │0.5 │  ← "北京"关注各个词的程度
      └────┴────┴────┘
```

### 为什么要除以 √d_k

```
问题：点积的值会随维度增大而增大

d_k = 64 时，点积均值 ≈ 64
d_k = 512 时，点积均值 ≈ 512

大值 → softmax 饱和 → 梯度消失

解决：除以 √d_k 让分布稳定
```

---

## 1.3 Multi-Head Attention

### 为什么需要多头

```
单头 Attention：只能学习一种关注模式

多头 Attention：同时学习多种关注模式
  - 头1：关注语法关系
  - 头2：关注语义关系
  - 头3：关注指代关系
  - ...
```

### 计算方式

```
Multi-Head Attention

输入 X
   │
   ├─→ Head1: Attention(Q1, K1, V1) ─┐
   │                                  │
   ├─→ Head2: Attention(Q2, K2, V2) ─┼─→ Concat ─→ Linear ─→ 输出
   │                                  │
   └─→ Head3: Attention(Q3, K3, V3) ─┘

每个头有独立的 W_Q, W_K, W_V
最后拼接所有头的输出，再做线性变换
```

### 代码示意

```python
class MultiHeadAttention:
    def __init__(self, d_model, num_heads):
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        # 每个头的投影矩阵
        self.W_Q = Linear(d_model, d_model)
        self.W_K = Linear(d_model, d_model)
        self.W_V = Linear(d_model, d_model)
        self.W_O = Linear(d_model, d_model)
    
    def forward(self, Q, K, V):
        # 1. 线性投影
        Q = self.W_Q(Q)  # [batch, seq, d_model]
        K = self.W_K(K)
        V = self.W_V(V)
        
        # 2. 分割成多头
        Q = split_heads(Q, self.num_heads)  # [batch, heads, seq, d_k]
        K = split_heads(K, self.num_heads)
        V = split_heads(V, self.num_heads)
        
        # 3. 计算注意力
        attn = scaled_dot_product_attention(Q, K, V)
        
        # 4. 拼接并输出
        output = concat_heads(attn)
        return self.W_O(output)
```

---

## 1.4 位置编码

### 为什么需要位置信息

```
Self-Attention 的问题：对顺序不敏感

"我 爱 你" 和 "你 爱 我" 
在纯 Attention 看来，每个词关注到的信息相同（只是顺序不同）
但这两句话含义完全不同！

→ 需要额外注入位置信息
```

### 正弦余弦位置编码（原始方案）

```python
PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))

pos: 位置索引 (0, 1, 2, ...)
i:   维度索引
d_model: 模型维度

特点：
- 不同位置有唯一的编码
- 可以泛化到更长的序列
- 相对位置信息可以通过线性变换获得
```

### RoPE（旋转位置编码）

**现代大模型的主流方案**

```
核心思想：通过旋转向量来编码位置

优势：
- 更好的长序列泛化能力
- 相对位置信息更自然
- 被 LLaMA、Qwen 等广泛采用
```

---

## 1.5 Transformer 完整架构

### 编码器-解码器结构

```
         Transformer 架构
         
┌─────────────────┬─────────────────┐
│     编码器       │     解码器       │
│   (Encoder)     │   (Decoder)     │
├─────────────────┼─────────────────┤
│                 │   Masked       │
│ Self-Attention  │ Self-Attention │
│       ↓         │       ↓        │
│  Add & Norm     │  Add & Norm    │
│       ↓         │       ↓        │
│                 │ Cross-Attention│← 从编码器获取信息
│                 │       ↓        │
│                 │  Add & Norm    │
│       ↓         │       ↓        │
│    FFN          │     FFN        │
│       ↓         │       ↓        │
│  Add & Norm     │  Add & Norm    │
├─────────────────┼─────────────────┤
│   × N 层        │    × N 层       │
└─────────────────┴─────────────────┘
         ↓                 ↓
   编码表示            生成输出
```

### 关键组件

| 组件 | 作用 |
|------|------|
| **Self-Attention** | 捕获序列内部关系 |
| **Masked Self-Attention** | 解码器只能看到之前的词 |
| **Cross-Attention** | 解码器关注编码器输出 |
| **FFN** | 非线性变换，增加表达能力 |
| **Add & Norm** | 残差连接 + 层归一化，稳定训练 |

### 前馈网络（FFN）

```python
FFN(x) = ReLU(x × W1 + b1) × W2 + b2

# 通常 W1 将维度放大 4 倍，W2 再缩回来
# d_model=512 → d_ff=2048 → d_model=512
```

### 残差连接与层归一化

```
残差连接：Output = LayerNorm(x + SubLayer(x))

作用：
- 残差：让梯度直接传递，避免梯度消失
- 层归一化：稳定训练，加速收敛
```

---

## 本章小结

- ✅ Self-Attention 通过 Q、K、V 让每个位置关注所有位置
- ✅ Multi-Head 同时学习多种关注模式
- ✅ 位置编码为 Attention 注入顺序信息
- ✅ Transformer = Self-Attention + FFN + 残差 + 层归一化

---

> **下一章**：第2章 · GPT 系列模型演进
