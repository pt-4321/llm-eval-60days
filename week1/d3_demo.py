# -*- coding: utf-8 -*-
"""W1 周四 · if / for / 函数

用法：py week1\\d3_demo.py

昨天你写的是「一条数据长什么样」，今天写「怎么让程序批量处理一堆数据，
并且把判断标准写成一个可复用的函数」。
"""

# 昨天那份评测记录，今天缩成 5 条，方便看结果
records = [
    {"id": 1, "score": 1, "latency": 1.83},
    {"id": 2, "score": 0, "latency": 2.10},
    {"id": 3, "score": 1, "latency": 1.62},
    {"id": 4, "score": 0, "latency": 2.40},
    {"id": 5, "score": 1, "latency": 1.95},
]

# ============ 1) if / elif / else：把「判断标准」写成代码 ============
print("=" * 50)
print("1) if / elif / else")

rate = 60.0

if rate >= 90:
    level = "优"
elif rate >= 75:
    level = "良"
else:
    level = "待改进"

print(f"准确率 {rate}% → 评级：{level}")

# 注意两个细节：
#   - 冒号和缩进是语法的一部分，缩进错了会报 IndentationError
#   - 条件是从上往下判断，命中第一个就不再往下看
#     所以 >= 90 要写在 >= 75 前面，顺序反了 95 分会被判成「良」

# ============ 2) for：让程序重复干活 ============
print("=" * 50)
print("2) for 循环")

total = 0
for r in records:
    total = total + r["score"]
print(f"总得分：{total}（一共 {len(records)} 条）")

# 想看序号，用 enumerate(列表, 1)：第二个参数是起始编号
for i, r in enumerate(records, 1):
    mark = "对" if r["score"] == 1 else "错"
    print(f"  第 {i} 条：{mark}，延迟 {r['latency']} 秒")

# ============ 3) def：把一段逻辑打包，起个名字 ============
print("=" * 50)
print("3) 函数")


def pass_rate(items):
    """算准确率（百分比，保留 1 位小数）。

    items: 形如 [{"score": 1, ...}, ...] 的列表
    return: 70.0 这样的浮点数
    """
    total_score = 0
    for it in items:
        total_score = total_score + it["score"]
    return round(total_score / len(items) * 100, 1)


def grade(rate):
    """按准确率给评级：>=90 优，>=75 良，其余待改进。"""
    if rate >= 90:
        return "优"
    if rate >= 75:
        return "良"
    return "待改进"


# 函数定义完不会自己执行，要「调用」它：函数名 + 括号 + 参数
r = pass_rate(records)
print(f"pass_rate(records) → {r}")
print(f"grade({r}) → {grade(r)}")

# ============ 4) 组合：函数拼成一份迷你报告 ============
print("=" * 50)
print("4) 组合调用")


def bad_count(items):
    """数出 score == 0 的条数。"""
    n = 0
    for it in items:
        if it["score"] == 0:
            n = n + 1
    return n


print(f"样本 {len(records)} 条 ｜ 准确率 {pass_rate(records)}% ｜ 评级 {grade(pass_rate(records))} ｜ 错误 {bad_count(records)} 条")

# ============ 5) 最容易踩的坑：忘记 return ============
print("=" * 50)
print("5) 坑：没有 return 的函数")


def bad_rate(items):
    total_score = sum(it["score"] for it in items)
    correct = total_score / len(items) * 100
    # 这里忘了写 return


print(f"bad_rate(records) → {bad_rate(records)}   ← 看到 None 就是忘了 return")

# 记住：函数里算出来的值，只有 return 出去，外面才拿得到。
# print 是「给别人看」，return 是「交给下一行代码用」——这是两件完全不同的事。
