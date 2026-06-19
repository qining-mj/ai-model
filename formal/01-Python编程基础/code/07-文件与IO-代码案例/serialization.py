"""
序列化 — pickle 与 JSON
演示 pickle.dump/load、json.dumps/loads、以及文件读写。
"""

import pickle
import json
import os

data_file = os.path.join(os.path.dirname(__file__), "_demo_data.pkl")
json_file = os.path.join(os.path.dirname(__file__), "_demo_data.json")

print("=" * 60)
print("1. pickle — Python 对象序列化（二进制格式）")
print("=" * 60)

data = {
    "name": "Alice",
    "scores": [95, 87, 92],
    "grades": {"数学": "A", "英语": "B+"},
    "active": True,
    "pi": 3.14159,
}

# 序列化到文件
with open(data_file, "wb") as f:
    pickle.dump(data, f)
print(f"  已 pickle 写入: {os.path.getsize(data_file)} 字节")

# 反序列化
with open(data_file, "rb") as f:
    loaded = pickle.load(f)
print(f"  pickle 加载结果: {loaded}")
print(f"  类型一致: {type(data) == type(loaded)}")


print("\n" + "=" * 60)
print("2. json.dumps() — Python 对象 -> JSON 字符串")
print("=" * 60)

py_obj = {
    "name": "Python",
    "version": 3.12,
    "features": ["动态", "强类型", "优雅"],
    "count": 42,
    "enabled": True,
    "data": None,
}

json_str = json.dumps(py_obj)
print(f"  JSON: {json_str}")

# 格式化输出
json_pretty = json.dumps(py_obj, ensure_ascii=False, indent=2)
print(f"  格式化 JSON:")
print(f"{json_pretty}")

# ensure_ascii=False 保留非 ASCII
cn = {"消息": "你好，世界！"}
print(f"  ensure_ascii=True:  {json.dumps(cn)}")
print(f"  ensure_ascii=False: {json.dumps(cn, ensure_ascii=False)}")


print("\n" + "=" * 60)
print("3. json.loads() — JSON 字符串 -> Python 对象")
print("=" * 60)

raw = '{"name": "Bob", "age": 30, "skills": ["Python", "Java"]}'
parsed = json.loads(raw)
print(f"  解析结果: {parsed}")
print(f"  name = {parsed['name']}, age = {parsed['age']}")


print("\n" + "=" * 60)
print("4. json.dump() / json.load() — 文件读写")
print("=" * 60)

config = {
    "host": "localhost",
    "port": 8080,
    "debug": True,
    "allowed_origins": ["*"],
}

with open(json_file, "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2)

print(f"  JSON 文件大小: {os.path.getsize(json_file)} 字节")

with open(json_file, "r", encoding="utf-8") as f:
    loaded_config = json.load(f)

print(f"  从文件加载: {loaded_config}")


print("\n" + "=" * 60)
print("5. Python — JSON 类型映射")
print("=" * 60)

mapping = [
    ("dict", "object"),
    ("list / tuple", "array"),
    ("str", "string"),
    ("int / float", "number"),
    ("True / False", "boolean"),
    ("None", "null"),
]

print(f"  {'Python 类型':<15} -> {'JSON 类型':<10}")
print(f"  {'-'*15}    {'-'*10}")
for py_t, js_t in mapping:
    print(f"  {py_t:<15} -> {js_t:<10}")


print("\n" + "=" * 60)
print("6. pickle vs JSON 对比")
print("=" * 60)

print("  pickle:")
print("    + 支持任意 Python 对象（类实例等）")
print("    + 仅 Python 可用")
print("    - 不安全（不要加载不可信数据）")
print("    - 二进制格式，不可读")
print("  JSON:")
print("    + 跨语言、人类可读")
print("    + 安全")
print("    - 仅支持基本类型")


# 清理
os.remove(data_file)
os.remove(json_file)
