"""
Python 列表操作综合演示
运行: python lists.py
"""

# ============================================================
# 1. 创建列表
# ============================================================
print("=== 创建列表 ===")
empty = []
nums = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]
rng = list(range(5))
print(f"empty: {empty}")
print(f"nums:  {nums}")
print(f"mixed: {mixed}")
print(f"range: {rng}")

# ============================================================
# 2. 索引 (正/负)
# ============================================================
print("\n=== 索引 ===")
print(f"nums[0]   = {nums[0]}")     # 1
print(f"nums[-1]  = {nums[-1]}")    # 5 (倒数第一个)
print(f"nums[-2]  = {nums[-2]}")    # 4

# ============================================================
# 3. 切片 [start:end:step]
# ============================================================
print("\n=== 切片 ===")
print(f"nums[1:4]    = {nums[1:4]}")    # [2, 3, 4]
print(f"nums[:3]     = {nums[:3]}")     # [1, 2, 3]
print(f"nums[::2]    = {nums[::2]}")    # [1, 3, 5]
print(f"nums[::-1]   = {nums[::-1]}")   # 反转

# ============================================================
# 4. 修改列表
# ============================================================
print("\n=== 修改列表 ===")
lst = [1, 2, 3]
lst[0] = 10           # 修改元素
print(f"lst[0] = 10 → {lst}")

lst.append(4)          # 追加
print(f"append(4)   → {lst}")

lst.extend([5, 6])     # 扩展
print(f"extend([5,6])→ {lst}")

lst.insert(0, 0)       # 插入
print(f"insert(0,0) → {lst}")

# ============================================================
# 5. 删除元素
# ============================================================
print("\n=== 删除元素 ===")
lst = [1, 2, 3, 4, 5, 3]
del lst[0]             # del 按索引删除
print(f"del lst[0]  → {lst}")

popped = lst.pop()     # pop 弹出最后一个
print(f"pop()      → {lst}, 弹出: {popped}")

popped = lst.pop(1)    # pop 按索引弹出
print(f"pop(1)     → {lst}, 弹出: {popped}")

lst.remove(3)          # remove 按值删除 (第一个匹配)
print(f"remove(3)  → {lst}")

lst.clear()            # 清空
print(f"clear()    → {lst}")

# ============================================================
# 6. 排序
# ============================================================
print("\n=== 排序 ===")
nums = [3, 1, 4, 1, 5, 9, 2, 6]
print(f"原始:     {nums}")
print(f"sorted(): {sorted(nums)}")        # 返回新列表
print(f"原列表:   {nums}")

nums.sort()                                 # 原地排序
print(f"sort():   {nums}")

nums.sort(reverse=True)
print(f"sort(reverse): {nums}")

# 按自定义 key 排序
words = ["banana", "apple", "cherry", "date"]
words.sort(key=len)                         # 按长度排序
print(f"sort(key=len): {words}")

# ============================================================
# 7. 反转
# ============================================================
print("\n=== 反转 ===")
nums = [1, 2, 3, 4]
nums.reverse()
print(f"reverse(): {nums}")

# ============================================================
# 8. 复制 vs 深拷贝
# ============================================================
print("\n=== copy vs deepcopy ===")
import copy
original = [[1, 2], [3, 4]]
shallow = original.copy()      # 浅拷贝
deep = copy.deepcopy(original)  # 深拷贝

original[0][0] = 99
print(f"original: {original}")
print(f"shallow:  {shallow}")  # 内部也变了! 浅拷贝共享内部对象
print(f"deep:     {deep}")     # 没变

print("\n列表演示完毕！")
