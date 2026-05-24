#!/usr/bin/env python3
"""LNT15 block-format-lint — ::: 区块格式统一检查与修复。

用法:
  python3 wiki/scripts/lint_block_format.py --dir docs/wiki/pages/
  python3 wiki/scripts/lint_block_format.py --dir docs/wiki/pages/ --fix
"""

import re
import sys
from pathlib import Path


def check_and_fix(text: str, fix: bool) -> tuple[str, list[str]]:
    """检查并（可选）修复 ::: 区块格式问题。返回 (处理后文本, 问题列表)。"""
    issues = []

    # 跳过 frontmatter
    if text.startswith('---'):
        m = re.match(r'^---.*?\n---\n', text, re.DOTALL)
        fm_end = m.end() if m else 0
    else:
        fm_end = 0

    lines = text.splitlines(keepends=True)

    # 标记代码块范围（不检查其中的 :::）
    in_code = False
    code_blocks: list[tuple[int, int]] = []
    code_start = -1
    for i, line in enumerate(lines):
        if line.strip().startswith('```'):
            if not in_code:
                in_code = True
                code_start = i
            else:
                in_code = False
                code_blocks.append((code_start, i))
    if in_code:
        code_blocks.append((code_start, len(lines) - 1))

    def in_code_block(idx: int) -> bool:
        return any(s <= idx <= e for s, e in code_blocks)

    def line_char_pos(idx: int) -> int:
        return sum(len(lines[j]) for j in range(idx))

    # 检查项 3 & 4 & 5: ::: 空格规范（逐行）
    new_lines = list(lines)
    for i, line in enumerate(lines):
        if in_code_block(i):
            continue
        stripped = line.rstrip('\n')
        # 检查项 3: :::TYPE 后缺空格
        if re.match(r'^:::[a-zA-Z]', stripped):
            issues.append(f'[3] ::: 后缺空格: line {i+1}: {stripped[:60]!r}')
            if fix:
                new_lines[i] = re.sub(r'^:::([a-zA-Z])', r'::: \1', line)
        # 检查项 4: ::: 后多余空格（两个以上）
        elif re.match(r'^:::  ', stripped):
            issues.append(f'[4] ::: 后多余空格: line {i+1}: {stripped[:60]!r}')
            if fix:
                new_lines[i] = re.sub(r'^:::  +', '::: ', line)
        # 检查项 5: TYPE 后多余空格（::: TYPE  attr 中 TYPE 后多个空格）
        if re.match(r'^::: [a-zA-Z]+  ', stripped):
            issues.append(f'[5] TYPE 后多余空格: line {i+1}: {stripped[:60]!r}')
            if fix:
                new_lines[i] = re.sub(r'^(::: [a-zA-Z]+) {2,}', r'\1 ', new_lines[i])

    # 检查项 6: 行末尾随空格（跳过表格行和空行）
    for i, line in enumerate(new_lines):
        if in_code_block(i):
            continue
        stripped_content = line.rstrip('\n')
        if stripped_content and not stripped_content.startswith('|'):
            if stripped_content != stripped_content.rstrip():
                issues.append(f'[6] 行末尾随空格: line {i+1}')
                if fix:
                    new_lines[i] = stripped_content.rstrip() + '\n' if line.endswith('\n') else stripped_content.rstrip()

    # 重新拼接文本以检查空行
    working_text = ''.join(new_lines)

    # 检查项 1: 开启行前缺空行
    # ::: 开启行 = 以 ::: 开头且后面有非空字符（非纯 ::: 闭合）
    def fix_missing_blank_before(text: str) -> tuple[str, list[str]]:
        result_issues = []
        lines = text.splitlines(keepends=True)
        out = []
        for i, line in enumerate(lines):
            if in_code_block(i):
                out.append(line)
                continue
            stripped = line.rstrip('\n').rstrip()
            is_opener = re.match(r'^::: [a-zA-Z]', stripped)
            if is_opener and i > 0:
                prev = lines[i-1].rstrip('\n').rstrip()
                # 前一行不是空行、不是 ::: 闭合、不是 frontmatter 边界
                if prev and prev != '---' and not prev.startswith(':::'):
                    result_issues.append(f'[1] 开启行前缺空行: line {i+1}: {stripped[:50]!r}')
                    if fix:
                        out.append('\n')
            out.append(line)
        return ''.join(out), result_issues

    # 检查项 2: 闭合行后缺空行
    def fix_missing_blank_after(text: str) -> tuple[str, list[str]]:
        result_issues = []
        lines = text.splitlines(keepends=True)
        out = []
        for i, line in enumerate(lines):
            out.append(line)
            if in_code_block(i):
                continue
            stripped = line.rstrip('\n').rstrip()
            is_closer = stripped == ':::'
            if is_closer and i < len(lines) - 1:
                nxt = lines[i+1].rstrip('\n').rstrip()
                # 后一行不是空行且不是另一个 ::: 块
                if nxt and not nxt.startswith(':::'):
                    result_issues.append(f'[2] 闭合行后缺空行: line {i+1}')
                    if fix:
                        out.append('\n')
        return ''.join(out), result_issues

    working_text, issues1 = fix_missing_blank_before(working_text)
    working_text, issues2 = fix_missing_blank_after(working_text)
    issues = issues1 + issues2 + [x for x in issues if not x.startswith('[1]') and not x.startswith('[2]')]

    return working_text, issues


def process_file(path: Path, fix: bool) -> list[str]:
    text = path.read_text(encoding='utf-8')
    new_text, issues = check_and_fix(text, fix)
    if fix and new_text != text:
        path.write_text(new_text, encoding='utf-8')
    return [f'  {path.name}:{iss}' for iss in issues]


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', required=True)
    parser.add_argument('--fix', action='store_true')
    args = parser.parse_args()

    root = Path(args.dir)
    files = sorted(root.rglob('*.md'))
    all_issues = []
    for f in files:
        issues = process_file(f, args.fix)
        all_issues.extend(issues)

    cats = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
    for iss in all_issues:
        for k in cats:
            if f'[{k}]' in iss:
                cats[k].append(iss)
                break

    print(f"=== LNT15 报告（{'自动修复' if args.fix else '仅检查'}）===")
    print(f"扫描文件: {len(files)}\n")
    labels = {
        1: '开启行前缺空行',
        2: '闭合行后缺空行',
        3: '::: 后缺空格',
        4: '::: 后多余空格',
        5: 'TYPE 后多余空格',
        6: '行末尾随空格',
    }
    total = 0
    for k, label in labels.items():
        items = cats[k]
        total += len(items)
        print(f'[{k}] {label}: {len(items)} 处')
        for iss in items[:10]:
            print(iss)
        if len(items) > 10:
            print(f'  ... 还有 {len(items)-10} 处')

    print(f'\n总计: {total} 处问题')
    return 0 if total == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
