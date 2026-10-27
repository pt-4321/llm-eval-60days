# -*- coding: utf-8 -*-
"""W1 周二 · 列表 + 字典：把 3 条评测记录存成「评测集」的形状"""

records = [
    {
        "id": 1,
        "question": "GB 50300-2013 中，单位工程验收由谁组织？",
        "answer": "由总监理工程师组织。",
        "reference": "应由建设单位项目负责人组织。",
        "score": 0,
        "latency": 1.83,
    },
    {
        "id": 2,
        "question": "工程量清单计价中，综合单价包含税金吗？",
        "answer": "包含。",
        "reference": "不包含，税金单列。",
        "score": 0,
        "latency": 2.10,
    },
    {
        "id": 3,
        "question": "建设工程施工合同（示范文本）现行版本是哪一年？",
        "answer": "2017 年版。",
        "reference": "2017 年版。",
        "score": 1,
        "latency": 1.62,
    },
    {
        "id": 4,
        "question": "这里换成你自己工作里的一个真实问题",
        "answer": "模型会怎么答，随便写",
        "reference": "标准答案，按你的判断写",
        "score": 0,
        "latency": 2.40,
    },
]

print("=" * 60)
print(f"共 {len(records)} 条样本")
print("=" * 60)

scores = []
latencies=[]
for r in records:
   print(f"[{r['id']}]问:{r['question']}|答:{r['answer']}|判:{r['score']}")
   scores.append(r["score"])
   latencies.append(r["latency"])

avg = sum(scores) / len(scores)
print("-" * 60)
print(f"平均得分：{round(avg, 2)}（{sum(scores)}/{len(scores)}）")
avg_lat=sum(latencies)/len(latencies)
print(f"平均延迟:{round(avg_lat,2)}秒")