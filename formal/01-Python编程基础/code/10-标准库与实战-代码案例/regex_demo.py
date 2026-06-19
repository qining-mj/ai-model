"""
正则表达式 — Regular Expressions with re
演示 re.match / search / findall / sub / split，元字符与贪婪匹配。
"""

import re

print("=" * 60)
print("1. 基本元字符")
print("=" * 60)

text = "Hello! My email is alice@example.com and phone is 138-1234-5678."

# .  匹配任意字符（除换行）
# ^  字符串开头
# $  字符串结尾
# *  0次或多次
# +  1次或多次
# ?  0次或1次

# 示例: 匹配邮箱
pattern = r"\w+@\w+\.\w+"
match = re.search(pattern, text)
if match:
    print(f"  查找邮箱:    {match.group()}")

# \d 数字 \w 字母数字 \s 空白
phone_pat = r"\d{3}-\d{4}-\d{4}"
phone = re.search(phone_pat, text)
if phone:
    print(f"  查找电话:    {phone.group()}")


print("\n" + "=" * 60)
print("2. re.match — 从字符串开头匹配")
print("=" * 60)

s1 = "Python is great"
s2 = "I love Python"

m1 = re.match(r"Python", s1)
m2 = re.match(r"Python", s2)

print(f"  match('Python', '{s1}'): {'找到: ' + m1.group() if m1 else 'None'}")
print(f"  match('Python', '{s2}'): {'找到: ' + m2.group() if m2 else 'None'}")


print("\n" + "=" * 60)
print("3. re.search — 在整个字符串中搜索")
print("=" * 60)

s = "我的电话是 010-12345678，备用是 021-87654321"
m = re.search(r"\d{3,4}-\d{7,8}", s)
if m:
    print(f"  search 找到: {m.group()}")                  # 只返回第一个匹配


print("\n" + "=" * 60)
print("4. re.findall — 查找所有匹配")
print("=" * 60)

phones = re.findall(r"\d{3,4}-\d{7,8}", s)
print(f"  findall 找到所有电话: {phones}")

# 分组
text2 = "Alice: 90, Bob: 85, Charlie: 95, Diana: 88"
pairs = re.findall(r"(\w+):\s*(\d+)", text2)
print(f"  分组提取: {pairs}")
for name, score in pairs:
    print(f"    {name}: {score}")


print("\n" + "=" * 60)
print("5. re.sub — 替换")
print("=" * 60)

msg = "联系邮箱: old@example.com, 备用: info@test.org"
new_msg = re.sub(r"\w+@\w+\.\w+", "[隐藏]", msg)
print(f"  替换前: {msg}")
print(f"  替换后: {new_msg}")

# 引用分组
date_str = "2024-01-15"
reformatted = re.sub(r"(\d{4})-(\d{2})-(\d{2})", r"\3/\2/\1", date_str)
print(f"  日期重排: {date_str} -> {reformatted}")


print("\n" + "=" * 60)
print("6. re.split — 分割字符串")
print("=" * 60)

csv = "苹果, 香蕉; 樱桃 | 榴莲  葡萄"
items = re.split(r"[,;|\s]+", csv)
print(f"  分割结果: {items}")


print("\n" + "=" * 60)
print("7. re.compile — 编译正则表达式（提高性能）")
print("=" * 60)

# 编译一次，多次使用
email_pattern = re.compile(r"([\w.]+)@([\w.]+)\.(\w+)")

test_emails = ["user@example.com", "first.last@company.org", "invalid@"]
for email in test_emails:
    m = email_pattern.match(email)
    if m:
        print(f"  {email:30s} -> 用户名={m.group(1)}, 域名={m.group(2)}, 后缀={m.group(3)}")
    else:
        print(f"  {email:30s} -> 无效")


print("\n" + "=" * 60)
print("8. 贪婪 vs 非贪婪")
print("=" * 60)

html = "<div><p>第一段</p><p>第二段</p></div>"

# 贪婪模式 (默认) — 尽可能多匹配
greedy = re.search(r"<p>.*</p>", html)
if greedy:
    print(f"  贪婪:   {greedy.group()}")

# 非贪婪 — 尽可能少匹配
non_greedy = re.search(r"<p>.*?</p>", html)
if non_greedy:
    print(f"  非贪婪: {non_greedy.group()}")


print("\n" + "=" * 60)
print("9. 常用正则速查")
print("=" * 60)

patterns = [
    (r"^\s*$", "空行或空白行"),
    (r"\b\d{3,4}-\d{7,8}\b", "中国电话"),
    (r"1[3-9]\d{9}", "手机号"),
    (r"\w+@\w+\.\w+", "简单邮箱"),
    (r"https?://\S+", "URL"),
    (r"\d{4}-\d{2}-\d{2}", "日期 (YYYY-MM-DD)"),
]
for pat, desc in patterns:
    print(f"  {desc:15s}: {pat}")
