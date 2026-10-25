# -*- coding: utf-8 -*-
"""Day 1 · 让大模型回你一句话（零依赖，只用 Python 自带库）

用法（在 cmd 或 PowerShell 里，先 cd 到本文件夹）：
    py hello_api.py                          # 默认：DeepSeek 云端，问一句"你好"
    py hello_api.py deepseek "用三句话解释什么是大模型评测"
    py hello_api.py ollama                   # 周三本地模型装好后，同一条命令也能跑
    py hello_api.py siliconflow "你好"        # 备用服务商（无 DeepSeek 账号时）

准备（只需一次）：
    1) 去 https://platform.deepseek.com 注册 → 实名 → 充值 50 元 → API keys → 创建
    2) 新开一个终端，执行：setx DEEPSEEK_API_KEY "sk-你复制的那串"
    3) 关掉终端，重新开一个（setx 只对新终端生效），再运行本脚本

注意：密钥只放环境变量，永远不要写进代码、不要提交到 GitHub。
"""

import json
import os
import sys
import time
import traceback
import urllib.error
import urllib.request
from datetime import datetime

# ---------------------------------------------------------------- 服务商配置
# 想换服务商：改 DEFAULT_PROVIDER，或者命令行第一个参数写服务商名字。
PROVIDERS = {
    "deepseek": {
        "label": "DeepSeek（云端）",
        "base_url": "https://api.deepseek.com/v1/chat/completions",
        "model": "deepseek-chat",
        "key_env": "DEEPSEEK_API_KEY",
        "need_key": True,
        "docs": "https://platform.deepseek.com/api_keys",
    },
    "siliconflow": {
        "label": "硅基流动（云端，备用）",
        "base_url": "https://api.siliconflow.cn/v1/chat/completions",
        "model": "Qwen/Qwen2.5-7B-Instruct",
        "key_env": "SILICONFLOW_API_KEY",
        "need_key": True,
        "docs": "https://cloud.siliconflow.cn/account/ak",
    },
    "zhipu": {
        "label": "智谱 GLM（云端，备用）",
        "base_url": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
        "model": "glm-4-flash",
        "key_env": "ZHIPU_API_KEY",
        "need_key": True,
        "docs": "https://bigmodel.cn/usercenter/apikeys",
    },
    "ollama": {
        "label": "Ollama（本地，周三用）",
        "base_url": "http://localhost:11434/v1/chat/completions",
        "model": "qwen2.5:3b",
        "key_env": "",
        "need_key": False,
        "docs": "https://ollama.com/download",
    },
}

DEFAULT_PROVIDER = "deepseek"
DEFAULT_PROMPT = "你好，请用一句话介绍你自己，并说明你的知识截止时间。"
HERE = os.path.dirname(os.path.abspath(__file__))
ERR_DIR = os.path.join(HERE, "errors")
OUT_DIR = os.path.join(HERE, "out")
LINE = "-" * 64


def setup_console():
    """让 Windows 终端少出乱码；失败也不影响主流程。"""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def post_json(url, payload, api_key, timeout=90):
    """发一个最简单的 POST，返回 (status, body_text)。不依赖 requests。"""
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = "Bearer " + api_key
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


def hint_for(status, body, provider):
    """把服务端错误翻译成一句你能立刻行动的话。"""
    tips = {
        400: "请求格式或模型名不对。多半是 MODEL 写错了，去平台文档核对当前模型名。",
        401: "密钥无效或没带上。检查环境变量是否设置、是否新开了终端、key 有没有复制全。",
        402: "账户余额不足。DeepSeek 需要先充值（50 元就够本计划用很久）。",
        403: "这个 key 没有该模型的权限，或账号未实名。",
        404: "地址或模型不存在。检查 base_url 是否带了 /v1，模型名是否停用。",
        429: "请求太频繁/额度用尽，等 1 分钟再试。",
        500: "服务端错误，不是你的问题，等 5 分钟再试。",
        502: "网关错误，等服务恢复。",
        503: "服务繁忙，等几分钟。",
        504: "网关超时，等几分钟。",
    }
    msg = tips.get(status, "未预期的状态码，先看下面的响应原文。")
    if status in (400, 404) and "model" in (body or "").lower():
        msg += " 响应里提到了 model，优先改 MODEL 这一项。"
    return msg


def save(path_dir, name, text):
    os.makedirs(path_dir, exist_ok=True)
    path = os.path.join(path_dir, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


def main(argv):
    setup_console()

    provider_name = DEFAULT_PROVIDER
    prompt = DEFAULT_PROMPT
    rest = argv[1:]
    if rest and rest[0] in PROVIDERS:
        provider_name = rest.pop(0)
    if rest:
        prompt = " ".join(rest).strip() or DEFAULT_PROMPT

    conf = PROVIDERS[provider_name]
    api_key = os.environ.get(conf["key_env"], "").strip() if conf["key_env"] else ""

    print(LINE)
    print("服务商 : " + conf["label"])
    print("模型   : " + conf["model"])
    print("地址   : " + conf["base_url"])
    print(LINE)

    if conf["need_key"] and not api_key:
        print("[缺少密钥] 环境变量 " + conf["key_env"] + " 没有读到。")
        print("")
        print("做这两步（只需一次）：")
        print('  1. 新开一个终端，执行：setx ' + conf["key_env"] + ' "sk-你的key"')
        print("  2. 关掉所有终端，重新开一个，再运行本脚本")
        print("")
        print("密钥申请地址：" + conf["docs"])
        return 2

    payload = {
        "model": conf["model"],
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "stream": False,
    }

    print("提问   : " + prompt)
    print(LINE)
    started = time.time()
    try:
        status, body = post_json(conf["base_url"], payload, api_key)
    except Exception as e:  # 网络层错误
        elapsed = time.time() - started
        details = (
            f"时间: {datetime.now():%Y-%m-%d %H:%M:%S}\n"
            f"服务商: {provider_name}\n"
            f"地址: {conf['base_url']}\n"
            f"耗时: {elapsed:.1f} 秒\n"
            f"异常: {e!r}\n\n"
            "=== 完整堆栈 ===\n" + traceback.format_exc()
        )
        path = save(ERR_DIR, "err_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt", details)
        print("[网络错误] " + str(e))
        print("")
        if "timed out" in str(e).lower() or "timeout" in str(e).lower():
            print("像是超时：检查是否需要开代理/校园网是否限速，然后再试一次。")
        elif "certificate" in str(e).lower() or "SSL" in str(e):
            print("像是证书问题：确认系统时间是今天，关掉系统代理或换个网络再试。")
        elif "refused" in str(e).lower() or "10061" in str(e):
            print("像是本地服务没启动。如果是 ollama，先运行：ollama serve")
        else:
            print("先确认能上外网（浏览器打开 https://platform.deepseek.com 试试）。")
        print("")
        print("报错已存档：" + path)
        print("把这份文件发给我，我直接告诉你下一步。")
        return 3

    elapsed = time.time() - started
    if status != 200:
        details = (
            f"时间: {datetime.now():%Y-%m-%d %H:%M:%S}\n"
            f"服务商: {provider_name}\n"
            f"HTTP 状态码: {status}\n\n"
            f"=== 响应原文 ===\n{body}\n"
        )
        path = save(ERR_DIR, "err_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt", details)
        print("[HTTP %s] " % status + hint_for(status, body, provider_name))
        print("")
        print("响应原文（前 500 字）：")
        print((body or "")[:500])
        print("")
        print("报错已存档：" + path)
        print("把这份文件发给我，我直接告诉你下一步。")
        return 4

    try:
        data = json.loads(body)
        answer = data["choices"][0]["message"]["content"]
        usage = data.get("usage") or {}
        total = usage.get("total_tokens", "?")
        out_tokens = usage.get("completion_tokens", "?")
    except Exception:
        path = save(ERR_DIR, "err_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt",
                    "HTTP 200 但解析失败\n\n" + body)
        print("[解析失败] 返回的不是预期的 JSON 结构。")
        print((body or "")[:500])
        print("报错已存档：" + path)
        return 5

    print("回答：")
    print(answer.strip())
    print(LINE)
    print("耗时 %.1f 秒 | tokens: 输出 %s / 合计 %s" % (elapsed, out_tokens, total))

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    transcript = (
        "# 第一次成功调用\n"
        f"时间: {datetime.now():%Y-%m-%d %H:%M:%S}\n"
        f"服务商: {conf['label']}\n"
        f"模型: {conf['model']}\n"
        f"提示词: {prompt}\n"
        f"耗时: {elapsed:.1f} 秒\n"
        f"tokens: 输出 {out_tokens} / 合计 {total}\n\n"
        "## 回答\n\n" + answer.strip() + "\n"
    )
    path = save(OUT_DIR, "hello_" + stamp + ".md", transcript)
    print("已存档：" + path)
    print("")
    print("[完成] 这就是 Day 1 的验收物：终端里出现了模型回复。")
    print("截图存进 errors/ 或 notes/，然后去打卡表把 R2 打勾。")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
