# -*- coding: utf-8 -*-
"""W1 周一 · 练习：把 5 个 ___ 换掉，让脚本自己告诉你好不好。

怎么用：
  1. 只改「你的部分」那 5 行，别动下面判分
  2. 保存，运行：py week1\\d1_exercise.py
  3. 看最后的得分：5/5 就是今天的交付物

卡住了就把整个屏幕的输出发我。
"""

___ = None  # 占位符，别改这一行

# ==================== 你的部分 ====================

# 题 1：把 model 改成你的模型名（字符串，要引号）
model = "deepseek-chat"

# 题 2：temperature 改成数字 0.3（数字不加引号）
temperature = 0.3

# 题 3：accuracy 改成数字 92.5（不要百分号）
accuracy = 92.5

# 题 4：用 f-string 拼出这一句，不要用 + 号：
#       模型 <模型名> 温度 <温度> 准确率 <准确率>%
line = f"模型 {model} 温度 {temperature} 准确率 {accuracy}%"

# 题 5：把上面三个值拼成一行 CSV（逗号分隔），也用 f-string
csv_line = f"{model},{temperature},{accuracy}"

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


m = model
report(isinstance(m, str) and m.strip() not in ("", "___") and not m.startswith("___"),
       1, "model 是字符串，且真的填了",
       '把 ___ 换成模型名，比如 "deepseek-chat"')

t = temperature
report(isinstance(t, (int, float)) and not isinstance(t, bool) and abs(t - 0.3) < 1e-9,
       2, "temperature 是数字 0.3",
       "数字不要加引号：写 0.3，不是 \"0.3\"")

a = accuracy
report(isinstance(a, (int, float)) and not isinstance(a, bool) and abs(a - 92.5) < 1e-9,
       3, "accuracy 是数字 92.5",
       "写 92.5，不带百分号")

expect_line = f"模型 {m} 温度 {t} 准确率 {a}%"
report(line == expect_line, 4, "line 用 f-string 拼对了",
       "期望这一行：%s  ｜ 写法：f\"模型 {model} 温度 {temperature} 准确率 {accuracy}%%\"" % expect_line)

expect_csv = f"{m},{t},{a}"
report(csv_line == expect_csv, 5, "csv_line 拼对了",
       "期望：%s  ｜ 写法：f\"{model},{temperature},{accuracy}\"" % expect_csv)

print("-" * 44)
print("得分：%d/5" % score)
if score == 5:
    print("全过。截图存进 notes\\W1D1.png，这就是今天的交付物。")
else:
    print("按提示改那几行，再跑一次。改一行、跑一次，别一次改五处。")
