# -*- coding: utf-8 -*-
"""Day 1 · 环境体检（零依赖）

用法：
    py check_env.py

它会逐项告诉你：装好了什么、还缺什么、下一步点哪个链接。
不装任何东西，只读状态，可以随时重复运行。
"""

import os
import shutil
import socket
import subprocess
import sys

LINE = "-" * 64
OK, WARN, BAD = "[OK]  ", "[待办]", "[注意]"


def run(cmd, timeout=15):
    """安全地跑一条命令，返回 (成功?, 输出文本)。

    Windows 上 git 可能是 git.cmd 这种批处理壳，必须用 cmd /c 调起；
    直接 subprocess 跑 .cmd 会 FileNotFoundError。
    """
    argv = list(cmd)
    resolved = shutil.which(argv[0]) or ""
    if resolved:
        argv[0] = resolved
    if argv[0].lower().endswith((".cmd", ".bat")):
        argv = ["cmd", "/c"] + argv
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout,
                           encoding="utf-8", errors="replace")
        out = (p.stdout or "").strip() or (p.stderr or "").strip()
        return p.returncode == 0, out.replace("\n", " ")[:160]
    except FileNotFoundError:
        return False, "命令不存在"
    except Exception as e:
        return False, repr(e)


def exists(*paths):
    for p in paths:
        if p and os.path.exists(p):
            return p
    return ""


def check_python():
    ver = "%d.%d.%d" % sys.version_info[:3]
    exe = sys.executable
    if "WindowsApps" in exe:
        return WARN, "Python " + ver + "（这是微软商店的占位程序，不是真正的 Python）", \
            "用 py check_env.py 重跑；或装 Python 时别用商店版"
    if sys.version_info < (3, 10):
        return BAD, "Python " + ver + "（太低）", "装 Python 3.11 或 3.12：https://www.python.org/downloads/"
    return OK, "Python " + ver + "  " + exe, ""


def check_pip():
    ok, out = run([sys.executable, "-m", "pip", "--version"])
    if ok and "pip" in out:
        return OK, out, ""
    return WARN, "pip 不可用", "运行：py -m ensurepip --upgrade"


def check_git():
    ok, out = run(["git", "--version"])
    if not ok:
        return BAD, "没装 Git", "装 Git：https://git-scm.com/download/win"
    name_ok, name = run(["git", "config", "--global", "user.name"])
    mail_ok, mail = run(["git", "config", "--global", "user.email"])
    if not (name_ok and name) or not (mail_ok and mail):
        return WARN, out + "（但还没配名字/邮箱，明天提交会失败）", \
            '执行：git config --global user.name "你的名字"  和  git config --global user.email "你的邮箱"'
    return OK, out + "  user=" + name + " <" + mail + ">", ""


def check_vscode():
    p = exists(
        os.path.join(os.environ.get("LOCALAPPDATA", ""), r"Programs\Microsoft VS Code\Code.exe"),
        os.path.join(os.environ.get("ProgramFiles", ""), r"Microsoft VS Code\Code.exe"),
        shutil.which("code"),
    )
    if p:
        return OK, p, ""
    return WARN, "没装 VS Code", "在终端执行：winget install -e --id Microsoft.VisualStudioCode --accept-package-agreements --accept-source-agreements"


def check_ollama():
    p = exists(os.path.join(os.environ.get("LOCALAPPDATA", ""), r"Programs\Ollama\ollama.exe"),
               shutil.which("ollama"))
    if p:
        ok, out = run([p, "--version"])
        return OK, "已装：" + out, ""
    return WARN, "没装 Ollama（Day 1 不需要，周三再装）", "https://ollama.com/download/windows"


def check_key():
    key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if not key:
        return WARN, "环境变量 DEEPSEEK_API_KEY 未设置", \
            '新终端执行：setx DEEPSEEK_API_KEY "sk-你的key"，然后重开终端'
    if not key.startswith("sk-"):
        return WARN, "已设置，但不像 sk- 开头（长度 %d）" % len(key), "确认复制的是 API Key，不是别的编号"
    return OK, "已设置：sk-" + "*" * 8 + "（长度 %d）" % len(key), ""


def check_network():
    reachable = []
    for host in ("api.deepseek.com", "github.com"):
        try:
            s = socket.create_connection((host, 443), timeout=8)
            s.close()
            reachable.append(host)
        except Exception:
            pass
    if len(reachable) == 2:
        return OK, "443 端口可达：api.deepseek.com / github.com", ""
    if reachable:
        return WARN, "只有 %s 可达，另一个不通" % reachable[0], "换网络（手机热点）再试，或检查代理设置"
    return BAD, "两个都连不上", "换个网络（手机热点）；校园网/公司网常见限制"


def check_write():
    target = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
    try:
        os.makedirs(target, exist_ok=True)
        f = os.path.join(target, ".write_test")
        with open(f, "w", encoding="utf-8") as fh:
            fh.write("ok")
        os.remove(f)
        return OK, "可以写入：" + target, ""
    except Exception as e:
        return BAD, "写不进去：" + repr(e), "把整个文件夹换个位置（比如 D 盘），别放 OneDrive 同步盘"


CHECKS = [
    ("Python 解释器", check_python),
    ("pip 包管理器", check_pip),
    ("Git", check_git),
    ("VS Code", check_vscode),
    ("Ollama（周三才需要）", check_ollama),
    ("DeepSeek 密钥", check_key),
    ("网络连通", check_network),
    ("文件夹写入", check_write),
]


def main():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    print(LINE)
    print("Day 1 环境体检  " + os.path.dirname(os.path.abspath(__file__)))
    print(LINE)

    todo = []
    for name, fn in CHECKS:
        try:
            status, detail, action = fn()
        except Exception as e:
            status, detail, action = BAD, "检查本身出错了：" + repr(e), "把这段发给我"
        print(status + "  " + name)
        print("        " + detail)
        if action:
            print("        -> " + action)
            todo.append(name)
    print(LINE)

    if not todo:
        print("全部通过。下一步：py hello_api.py")
    else:
        print("还有 %d 项待办：%s" % (len(todo), "、".join(todo)))
        print("按上面 -> 后面的命令做，做完再跑一次 py check_env.py")
    print(LINE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
