# -*- coding: utf-8 -*-
"""W1 周四 · 练习：写 3 个函数（第 4 题是加餐）

怎么用：
  1. 第 4 题还有一处 TODO
  2. 保存 → py week1\\d3_exercise.py → 看判分
  3. 目标：3/3 已达标，有余力再做第 4 题（4/4）

第 1、2、3 题的正确逻辑已经按你写的填好了，缩进改成了统一的空格。
"""

# 样本：6 条评测记录，其中 4 条判对、2 条判错
records = [
    {"id": 1, "score": 1, "latency": 1.83},
    {"id": 2, "score": 1, "latency": 2.10},
    {"id": 3, "score": 0, "latency": 1.62},
    {"id": 4, "score": 1, "latency": 2.40},
    {"id": 5, "score": 0, "latency": 1.95},
    {"id": 6, "score": 1, "latency": 1.70},
]

# ==================== 你的部分 ====================


def pass_rate(items):
    """题 1（已完成）：返回准确率，百分比，保留 1 位小数。"""
    total = 0
    for it in items:
        total = total + it["score"]
    return round(total / len(items) * 100, 1)


def bad_count(items):
    """题 2（已完成）：返回 score == 0 的条数。"""
    n = 0
    for it in items:
        if it["score"] == 0:
            n = n + 1
    return n


def grade(rate):
    """题 3（已完成）：按准确率返回评级。>=90 优，>=75 良，其余待改进。"""
    if rate >= 90:
        return "优"
    elif rate >= 75:
        return "良"
    else:
        return "待改进"


def report_line(items):
    """题 4（加餐）：返回一行报告，格式必须**一字不差**：

    样本 6 条 | 准确率 66.7% | 评级 待改进 | 错误 2 条

    提示：用 f-string，把 len(items)、pass_rate(items)、grade(...)、bad_count(items) 塞进去。
    只写 4 个空格的缩进，不要粘 def 那一行。
    """
    return f"样本 {len(items)} 条 | 准确率 {pass_rate(items)}% | 评级 {grade(pass_rate(items))} | 错误 {bad_count(items)} 条"

# ==================== 判分，别改 ====================

score = 0


def report(ok, no, title, hint=""):
    global score
    if ok:
        score += 1
        print("[OK] 第 %d 题：%s" % (no, title))
    else:
        print("[X ] 第 %d 题：%s" % (no, title))
        if hint:
            print("     提示：%s" % hint)


def call(fn, *args):
    """调用函数，把报错接住，不让脚本整个崩掉。"""
    try:
        return fn(*args), None
    except Exception as e:
        return None, repr(e)


def judge(no, title, fn, args, expect, hint):
    val, err = call(fn, *args)
    if err:
        report(False, no, title, "函数报错了：%s" % err)
        return
    if val is None:
        report(False, no, title, "返回了 None —— 大概率是忘了写 return")
        return
    if isinstance(expect, (int, float)) and isinstance(val, (int, float)):
        ok = abs(val - expect) < 1e-6
    else:
        ok = val == expect
    report(ok, no, title, "" if ok else "返回值是 %r，期望 %r。%s" % (val, expect, hint))


judge(1, "pass_rate 返回 66.7", pass_rate, (records,), 66.7,
      "写法：round(总分 / 条数 * 100, 1)")

judge(2, "bad_count 返回 2", bad_count, (records,), 2,
      "n 从 0 开始，遇到 score == 0 就 +1，最后 return n")

# 第 3 题查三个档位，全对才算过
v1, e1 = call(grade, 95)
v2, e2 = call(grade, 80)
v3, e3 = call(grade, 66.7)
if e1 or e2 or e3:
    report(False, 3, "grade 分档正确", "函数报错了：%s" % (e1 or e2 or e3))
elif (v1, v2, v3) == ("优", "良", "待改进"):
    report(True, 3, "grade 分档正确（95→优，80→良，66.7→待改进）")
else:
    report(False, 3, "grade 分档正确",
           "95 应返回 '优'，80 应返回 '良'，66.7 应返回 '待改进'；你给的是 %r / %r / %r" % (v1, v2, v3))

expect_line = "样本 6 条 | 准确率 66.7% | 评级 待改进 | 错误 2 条"
val, err = call(report_line, records)
if err:
    report(False, 4, "report_line 格式一致（加餐）", "函数报错了：%s" % err)
elif val is None:
    report(False, 4, "report_line 格式一致（加餐）", "还没写，或忘了 return")
elif val == expect_line:
    report(True, 4, "report_line 格式一致（加餐）")
else:
    report(False, 4, "report_line 格式一致（加餐）",
           "竖线是英文 |，前后各一个空格；期望：%s" % expect_line)

print("-" * 46)
print("得分：%d/4（前 3 题必做，第 4 题加餐）" % score)
if score >= 3:
    print("达标。截图存进 notes\\W1D4.png，然后去打卡表第 7 行。")
else:
    print("按提示改，改一处跑一次。卡住就把这一屏发我。")
