#!/usr/bin/env python3
"""
PreToolUse hook: 拒绝 Edit / Write / NotebookEdit 操作项目目录之外的文件，
以及 Bash 命令中对项目目录之外路径的写操作。

由 init_security.py 生成到 <wiki_root>/.claude/hooks/restrict_to_project.py。

退出码:
  0  = 放行（路径在项目内或无写操作）
  2  = 拒绝（路径超出项目目录或检测到外部写操作）

Claude Code 规范: exit code 2 阻止工具执行，错误信息写入 stderr。
"""
from __future__ import annotations

import json
import os
import re
import sys

PROJECT_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Bash 写操作静态检测模式：(正则, 捕获组索引, 说明)
# 每条模式从命令中提取目标路径，若路径在 PROJECT_ROOT 外则拒绝。
_WRITE_PATTERNS: list[tuple[re.Pattern, int, str]] = [
    # Python open() 写/追加模式: open('/path', 'w')  open("/path", 'a')  open('/path', 'wb')
    (re.compile(r"""open\s*\(\s*["']([^"']+)["']\s*,\s*["'][wa]"""), 1, "Python open() write/append"),
    # Shell 重定向写入: ... > /abs/path  或  ... >> /abs/path
    (re.compile(r""">>?\s+(/[^\s;|&'"\n>]+)"""), 1, "shell redirect"),
    # cp/mv 带绝对目标路径
    (re.compile(r"""\b(?:cp|mv)\s+(?:-[a-zA-Z]+\s+)*\S+\s+(/[^\s;|&]+)"""), 1, "cp/mv to external"),
    # tee 带绝对路径
    (re.compile(r"""\btee\s+(?:-[a-zA-Z]+\s+)*(/[^\s;|&]+)"""), 1, "tee to external"),
    # dd of=绝对路径
    (re.compile(r"""\bdd\b[^\n;|&]*\bof=(/[^\s;|&\n]+)"""), 1, "dd of= external"),
    # install 到绝对路径（最后一个绝对路径参数）
    (re.compile(r"""\binstall\s+(?:-[a-zA-Z0-9]+\s+)*\S+\s+(/[^\s;|&]+)\s*(?:[;&|]|$)"""), 1, "install to external"),
    # sed -i 操作文件（取最后一个绝对路径参数）
    (re.compile(r"""\bsed\s+(?:-[a-zA-Z]*i[a-zA-Z]*\s+|--in-place(?:=\S+)?\s+)(?:\S+\s+)+(/[^\s;|&]+)"""), 1, "sed -i external"),
]


def _is_external(path: str) -> bool:
    """如果 path 解析后在 PROJECT_ROOT 之外则返回 True。"""
    if not path:
        return False
    path = os.path.expanduser(path)
    if not os.path.isabs(path):
        return False  # 相对路径假定在项目内
    real = os.path.realpath(path)
    return not (real.startswith(PROJECT_ROOT + os.sep) or real == PROJECT_ROOT)


def _scan_bash_writes(command: str) -> list[str]:
    """扫描 Bash 命令中对外部路径的写操作，返回违规描述列表。"""
    violations: list[str] = []
    for pattern, group, label in _WRITE_PATTERNS:
        for m in pattern.finditer(command):
            path = m.group(group)
            if _is_external(path):
                violations.append(f"{label}: {path}")
    return violations


def main() -> int:
    data = json.load(sys.stdin)
    tool_input = data.get("tool_input", {})
    tool_name = data.get("tool_name", "")

    if tool_name == "Bash":
        command = tool_input.get("command", "")
        violations = _scan_bash_writes(command)
        if violations:
            print(
                "[restrict_to_project] 已拒绝 Bash 命令：检测到对项目外路径的写操作\n"
                + "\n".join(f"  {v}" for v in violations)
                + f"\n  项目目录: {PROJECT_ROOT}",
                file=sys.stderr,
            )
            return 2
        return 0

    # Edit / Write / NotebookEdit：检查文件路径
    path = tool_input.get("file_path") or tool_input.get("notebook_path", "")
    if not path:
        return 0

    real_path = os.path.realpath(path)
    if not real_path.startswith(PROJECT_ROOT + os.sep) and real_path != PROJECT_ROOT:
        print(
            f"[restrict_to_project] 已拒绝 {tool_name}：\n"
            f"  路径: {real_path}\n"
            f"  超出项目目录: {PROJECT_ROOT}",
            file=sys.stderr,
        )
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
