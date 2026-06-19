"""
时间和日期 — Time and Datetime
演示 time 模块与 datetime 模块的核心用法。
"""

import time
from datetime import datetime, date, time as dtime, timedelta

print("=" * 60)
print("1. time 模块 — 底层时间函数")
print("=" * 60)

# time.time() — 时间戳（秒）
ts = time.time()
print(f"  当前时间戳: {ts:.3f}")

# time.localtime — 结构化时间
lt = time.localtime()
print(f"  本地时间:    {lt.tm_year}-{lt.tm_mon:02d}-{lt.tm_mday:02d} "
      f"{lt.tm_hour:02d}:{lt.tm_min:02d}:{lt.tm_sec:02d}")

# time.sleep — 暂停执行
print("  time.sleep(0.5)...")
time.sleep(0.5)
print("  继续执行")

# time.strftime — 格式化
formatted = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print(f"  strftime:   {formatted}")

# time.strptime — 解析字符串
parsed = time.strptime("2024-01-15 10:30:00", "%Y-%m-%d %H:%M:%S")
print(f"  strptime:   {parsed.tm_year}-{parsed.tm_mon}-{parsed.tm_mday}")


print("\n" + "=" * 60)
print("2. datetime 模块 — 高级日期时间")
print("=" * 60)

# datetime.now
now = datetime.now()
print(f"  datetime.now():   {now}")

# 创建特定日期时间
dt = datetime(2024, 12, 25, 10, 30, 0)
print(f"  特定时间:        {dt}")

# date 对象
d = date.today()
print(f"  date.today():     {d}")
print(f"  年={d.year}, 月={d.month}, 日={d.day}")

# time 对象
t = dtime(14, 30, 0)
print(f"  time:             {t}")
print(f"  时={t.hour}, 分={t.minute}, 秒={t.second}")


print("\n" + "=" * 60)
print("3. datetime.strptime / strftime")
print("=" * 60)

date_str = "2024/08/15 09:15:30"
parsed_dt = datetime.strptime(date_str, "%Y/%m/%d %H:%M:%S")
print(f"  strptime:  '{date_str}' -> {parsed_dt}")

back_to_str = parsed_dt.strftime("%A, %B %d, %Y (%I:%M %p)")
print(f"  strftime:  {back_to_str}")

# 常见格式码
fmt = "%Y-%m-%d %H:%M:%S"
print(f"  ISO 格式:  {now.strftime(fmt)}")


print("\n" + "=" * 60)
print("4. timedelta — 时间算术")
print("=" * 60)

today = date.today()
one_day = timedelta(days=1)
one_week = timedelta(weeks=1)

print(f"  今天:           {today}")
print(f"  明天:           {today + one_day}")
print(f"  昨天:           {today - one_day}")
print(f"  一周后:         {today + one_week}")
print(f"  一周前:         {today - one_week}")

# datetime 相减得到 timedelta
start = datetime(2024, 1, 1, 0, 0, 0)
end = datetime(2024, 12, 31, 23, 59, 59)
diff = end - start
print(f"  2024 年剩余:    {diff.days} 天, {diff.total_seconds():.0f} 秒")

# timedelta 与 datetime 运算
future = now + timedelta(hours=48, minutes=30)
print(f"  48.5 小时后:    {future}")


print("\n" + "=" * 60)
print("5. 实用日期操作")
print("=" * 60)

# 当月第一天
first_day = today.replace(day=1)
print(f"  本月第一天:     {first_day}")

# 星期几 (0=周一, 6=周日)
print(f"  今天是星期{now.weekday() + 1}")


print("\n" + "=" * 60)
print("6. time 与 datetime 的对比")
print("=" * 60)

print("  time 模块:")
print("    - 偏向系统级: sleep, 计时, 时间戳")
print("  datetime 模块:")
print("    - 偏向业务级: 日期运算, 格式化, 时区")
