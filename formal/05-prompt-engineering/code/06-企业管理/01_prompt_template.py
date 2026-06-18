"""
01_prompt_template.py
Prompt 模板系统
"""
import re
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class PromptTemplate:
    """Prompt 模板"""
    name: str
    template: str
    description: str = ""
    variables: List[str] = field(default_factory=list)
    defaults: Dict[str, str] = field(default_factory=dict)
    examples: List[Dict] = field(default_factory=list)

    def __post_init__(self):
        if not self.variables:
            self.variables = re.findall(r'\{(\w+)\}', self.template)

    def format(self, **kwargs) -> str:
        """填充模板"""
        params = {**self.defaults, **kwargs}
        missing = set(self.variables) - set(params.keys())
        if missing:
            raise ValueError(f"缺少参数: {missing}")
        return self.template.format(**params)

    def with_examples(self, num_examples: int = None) -> str:
        """生成带示例的模板"""
        if not self.examples:
            return self.template

        examples_text = ""
        selected = self.examples[:num_examples] if num_examples else self.examples

        for i, ex in enumerate(selected, 1):
            examples_text += f"\n示例{i}：\n"
            for k, v in ex.items():
                examples_text += f"{k}：{v}\n"

        return self.template.replace("{examples}", examples_text)

    def validate(self, **kwargs) -> bool:
        """验证参数是否完整"""
        params = {**self.defaults, **kwargs}
        missing = set(self.variables) - set(params.keys())
        return len(missing) == 0


class PromptLibrary:
    """Prompt 模板库"""

    def __init__(self):
        self.templates: Dict[str, PromptTemplate] = {}

    def register(self, template: PromptTemplate):
        """注册模板"""
        self.templates[template.name] = template
        print(f"已注册模板: {template.name}")

    def get(self, name: str) -> PromptTemplate:
        """获取模板"""
        if name not in self.templates:
            raise KeyError(f"未找到模板: {name}")
        return self.templates[name]

    def list(self) -> List[str]:
        """列出所有模板"""
        return list(self.templates.keys())

    def search(self, keyword: str) -> List[str]:
        """搜索模板"""
        return [
            name for name, t in self.templates.items()
            if keyword.lower() in name.lower()
            or keyword.lower() in t.description.lower()
        ]


# 创建全局模板库
library = PromptLibrary()

# 注册常用模板
library.register(PromptTemplate(
    name="sentiment_analysis",
    description="情感分析模板",
    template="""你是一个情感分析专家。

请分析以下文本的情感倾向。
{examples}
文本：{text}

请输出：
- 情感：正面/负面/中性
- 置信度：高/中/低
- 理由：简要说明""",
    defaults={"examples": ""},
    examples=[
        {"文本": "这个产品太棒了", "情感": "正面", "置信度": "高"},
        {"文本": "质量一般般", "情感": "中性", "置信度": "中"},
    ]
))

library.register(PromptTemplate(
    name="code_review",
    description="代码审查模板",
    template="""你是一位资深的 {language} 开发工程师。

请审查以下代码：
```{language}
{code}
```

审查要点：
{review_points}

请按以下格式输出：
## 问题列表
| 行号 | 严重程度 | 问题描述 | 修复建议 |
|------|---------|---------|---------|

## 总体评价（1-10分）""",
    defaults={
        "language": "python",
        "review_points": "- 代码规范\n- 潜在bug\n- 性能问题"
    }
))

library.register(PromptTemplate(
    name="summarize",
    description="文本摘要模板",
    template="""请将以下{content_type}总结为{length}的摘要。

要求：
- 保留核心观点
- 使用{style}的语言风格
{extra_requirements}

原文：
{content}

摘要：""",
    defaults={
        "content_type": "文章",
        "length": "100字左右",
        "style": "专业",
        "extra_requirements": ""
    }
))

library.register(PromptTemplate(
    name="translate",
    description="翻译模板",
    template="""请将以下{source_lang}文本翻译成{target_lang}。

要求：
- 保持原文的语气和风格
- 专业术语保持准确
{extra_requirements}

原文：
{text}

译文：""",
    defaults={
        "source_lang": "英文",
        "target_lang": "中文",
        "extra_requirements": ""
    }
))


if __name__ == "__main__":
    print("=" * 60)
    print("【Prompt 模板库演示】")
    print("=" * 60)

    # 列出所有模板
    print("\n可用模板:")
    for name in library.list():
        template = library.get(name)
        print(f"  - {name}: {template.description}")

    # 使用情感分析模板
    print("\n" + "-" * 40)
    print("使用 sentiment_analysis 模板：")
    template = library.get("sentiment_analysis")
    prompt = template.format(text="这家餐厅的服务态度非常好")
    print(prompt)

    # 使用代码审查模板
    print("\n" + "-" * 40)
    print("使用 code_review 模板：")
    template = library.get("code_review")
    prompt = template.format(code="def add(a, b): return a + b")
    print(prompt[:300] + "...")

    # 搜索模板
    print("\n" + "-" * 40)
    print("搜索 '分析' 相关模板:")
    results = library.search("分析")
    print(f"  找到: {results}")
