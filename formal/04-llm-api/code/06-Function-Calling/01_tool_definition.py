"""
01_tool_definition.py
工具定义示例

演示如何使用 JSON Schema 定义各种类型的工具
"""

# 示例1：简单工具
weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "获取指定城市的当前天气信息。当用户询问天气相关问题时使用此工具。",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称，如：北京、上海、广州"
                }
            },
            "required": ["city"]
        }
    }
}

# 示例2：带枚举的工具
search_tool = {
    "type": "function",
    "function": {
        "name": "search_web",
        "description": "搜索互联网获取实时信息。当用户询问新闻、时事或需要最新数据时使用。",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "搜索关键词"
                },
                "search_type": {
                    "type": "string",
                    "enum": ["web", "news", "images"],
                    "description": "搜索类型：web-网页，news-新闻，images-图片"
                },
                "max_results": {
                    "type": "integer",
                    "description": "返回结果数量，默认5，最大20",
                    "minimum": 1,
                    "maximum": 20,
                    "default": 5
                }
            },
            "required": ["query"]
        }
    }
}

# 示例3：复杂嵌套参数
create_event_tool = {
    "type": "function",
    "function": {
        "name": "create_calendar_event",
        "description": "创建日历事件。当用户需要安排会议、约会或提醒时使用。",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "事件标题"
                },
                "start_time": {
                    "type": "string",
                    "description": "开始时间，ISO 8601格式，如：2024-03-15T09:00:00"
                },
                "end_time": {
                    "type": "string",
                    "description": "结束时间，ISO 8601格式"
                },
                "attendees": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "参与者邮箱列表"
                },
                "location": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "地点名称"},
                        "address": {"type": "string", "description": "详细地址"}
                    },
                    "description": "会议地点信息"
                },
                "reminder_minutes": {
                    "type": "integer",
                    "description": "提前提醒的分钟数",
                    "enum": [5, 10, 15, 30, 60],
                    "default": 15
                }
            },
            "required": ["title", "start_time"]
        }
    }
}

# 示例4：带条件依赖的工具
order_tool = {
    "type": "function",
    "function": {
        "name": "create_order",
        "description": "创建订单。支持多种支付方式和配送方式。",
        "parameters": {
            "type": "object",
            "properties": {
                "product_id": {
                    "type": "string",
                    "description": "商品ID"
                },
                "quantity": {
                    "type": "integer",
                    "description": "购买数量",
                    "minimum": 1
                },
                "payment_method": {
                    "type": "string",
                    "enum": ["alipay", "wechat", "credit_card", "bank_transfer"],
                    "description": "支付方式"
                },
                "delivery": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "string",
                            "enum": ["standard", "express", "pickup"],
                            "description": "配送方式"
                        },
                        "address": {
                            "type": "string",
                            "description": "配送地址（pickup 时可选）"
                        },
                        "phone": {
                            "type": "string",
                            "description": "联系电话"
                        }
                    },
                    "required": ["type", "phone"]
                }
            },
            "required": ["product_id", "quantity", "payment_method", "delivery"]
        }
    }
}

# 示例5：带详细说明的工具（推荐格式）
knowledge_search_tool = {
    "type": "function",
    "function": {
        "name": "search_knowledge_base",
        "description": """搜索企业知识库获取内部信息。

使用场景：
- 用户询问公司政策、规章制度
- 用户需要查找产品文档、技术文档
- 用户询问常见问题解答

不适用：
- 用户询问实时信息（使用 search_web）
- 用户询问个人订单（使用 get_order_status）
- 用户需要人工服务（使用 transfer_to_agent）""",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "搜索关键词，如：'年假政策'、'报销流程'、'产品使用说明'"
                },
                "category": {
                    "type": "string",
                    "enum": ["policy", "product", "tech", "faq"],
                    "description": "知识库分类：policy-政策制度，product-产品文档，tech-技术文档，faq-常见问题"
                },
                "top_k": {
                    "type": "integer",
                    "description": "返回结果数量",
                    "default": 3,
                    "minimum": 1,
                    "maximum": 10
                }
            },
            "required": ["query"]
        }
    }
}


def print_tool_schema(tool: dict):
    """打印工具定义"""
    import json
    func = tool["function"]
    print(f"\n工具名: {func['name']}")
    print(f"描述: {func['description'][:50]}...")
    print(f"参数 Schema:")
    print(json.dumps(func["parameters"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    print("=" * 60)
    print("【工具定义示例】")
    print("=" * 60)

    tools = [
        ("简单工具", weather_tool),
        ("带枚举的工具", search_tool),
        ("复杂嵌套参数", create_event_tool),
        ("带详细说明（推荐）", knowledge_search_tool),
    ]

    for name, tool in tools:
        print(f"\n{'='*40}")
        print(f"【{name}】")
        print_tool_schema(tool)
