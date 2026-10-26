# -*- coding: utf-8 -*-
"""W1 周一 · 变量、字符串、f-string、print

用法：在仓库目录里运行
    py week1\\d1_demo.py

读法：先跑一遍，再逐行看注释。哪一行看不懂，把行号发我。
"""

# 1) 变量：给一个值起名字。等号左边是名字，右边是值。
model = "qwen2.5:3b"        # 字符串：用引号包起来（中文/英文引号都行，建议用英文）
temperature = 0.3              # 数字：不用引号。0.7 是小数，叫 float
accuracy = 92.5                # 又是一个数字

# 2) print：把东西打到屏幕上。逗号分隔的多个东西，会自动用空格连起来
print("模型:", model)
print("温度:", temperature)

# 3) 字符串拼接：用 + 号。两边都必须是字符串，否则报错
report = "模型 " + model + " 跑完了"
print(report)

# 4) f-string（重点）：字符串前面加 f，用 {} 把变量塞进去。
#    这是第 3 周写评测报告时天天用的写法，优先学它，别用 + 号硬拼。
print(f"模型 {model} 在温度 {temperature} 下，准确率 {accuracy}%")

# 5) f-string 的格式控制：冒号后面写格式
print(f"准确率保留 1 位小数: {accuracy:.1f}%")
print(f"准确率保留整数: {accuracy:.0f}%")
print(f"模型名右对齐占 15 格: [{model:>15}]")
print(f"模型名左对齐占 15 格: [{model:<15}]")

# 6) 常用的字符串方法（方法 = 字符串自带的动作）
raw = "  建筑规范问答  "
print("原样: [", raw, "]")
print("去首尾空格: [", raw.strip(), "]")
print("转大写:", model.upper())
print("按逗号切分:", "事实性,逻辑性,安全性".split(","))
print("替换:", raw.strip().replace("规范", "规程"))

# 7) 换行：\n 就是一个换行符
print("第一行\n第二行")

# 8) 真实用法：把评测结果拼成一行 CSV（第 3 周你每天都要写这个）
csv_line = f"{model},{temperature},{accuracy}"
print("CSV 行:", csv_line)

# 9) 看看类型：type() 告诉你这个值是什么类型
print("model 的类型:", type(model))
print("temperature 的类型:", type(temperature))
print("accuracy 的类型:", type(accuracy))
