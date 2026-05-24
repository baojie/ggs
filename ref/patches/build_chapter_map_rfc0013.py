#!/usr/bin/env python3
"""
build_chapter_map.py — 从 wiki 语料自动生成 local/butler/chapter-map.md。

通过 local/config/butler.json 读取：
  corpus_file           语料文件路径（相对 WIKI_ROOT）
  chapter_pattern       章节标题正则（边界检测用，Plan A 模式无需捕获组）
  chapter_title_offset  标题行偏移，默认 1（AIMA 中标题在 CHAPTER 行之后 1 行）
  preface_pattern       前言标题正则（旧模式兼容）
  preface_nnn           前言 NNN 值（旧模式兼容）
  appendix_pattern      附录标题正则（旧模式兼容）

  ── Plan A 模式（chapter_order_file 存在时启用）──
  chapter_order_file    章节次序表路径（相对 WIKI_ROOT，如 "ref/chapter-order.md"）
  chapter_order_skip    跳过的 NNN 列表（如 ["P01","P02"]，对应非语料页）

  Plan A 模式下 chapter_pattern 无需捕获组，NNN 直接来自 chapter_order_file。

来源: RFC-aima-0046, RFC-ggs-0013

用法：
    python3 build_chapter_map.py            # 生成 local/butler/chapter-map.md
    python3 build_chapter_map.py --dry-run  # 预览不写文件
    python3 build_chapter_map.py --wiki-root /path/to/wiki

安装（在 memex 目录执行）：
    cp <ggs_root>/ref/patches/build_chapter_map_rfc0013.py \
       ~/memex/wiki/scripts/butler/build_chapter_map.py
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from page_utils import get_wiki_root, get_local_config


def _strip_title_markup(line: str) -> str:
    """去除 markdown 标题前缀和加粗标记，返回纯文本标题。"""
    title = line.strip()
    title = re.sub(r'^#+\s*', '', title)
    title = re.sub(r'^\*{1,2}(.*?)\*{1,2}$', r'\1', title)
    return title.strip()


def _parse_chapter_order(order_path: Path, skip: list[str]) -> list[tuple[str, str]]:
    """
    解析 chapter-order.md 的 markdown 表格，返回过滤后的 [(NNN, page_id)] 有序列表。
    跳过 NNN 在 skip 列表中的条目。
    """
    skip_set = set(skip)
    entries: list[tuple[str, str]] = []
    for line in order_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith('|') or line.startswith('|---'):
            continue
        cols = [c.strip() for c in line.strip('|').split('|')]
        if len(cols) < 2:
            continue
        nnn = cols[0].strip('` ')
        page_id = cols[1].strip()
        if nnn.lower() in ('nnn', 'pn', 'prefix') or not nnn:
            continue
        if nnn in skip_set:
            continue
        entries.append((nnn, page_id))
    return entries


def extract_sections(
    lines: list[str],
    config: dict,
    chapter_order: list[tuple[str, str]] | None = None,
) -> list[tuple[str, str, str]]:
    """
    扫描语料，返回 [(nnn, part_label, title)] 列表。
    nnn: PN 前缀（如 "P01"、"001"、"A01"）
    part_label: 人类可读部分名（如 "Preface"、"Chapter 1"、"Appendix A"）
    title: 语料章节标题文本

    chapter_order 非 None 时启用 Plan A：正则仅做边界检测，NNN 按位置来自 chapter_order。
    """
    re_chapter = re.compile(config.get("chapter_pattern", r'^##\s+第\s*(\d+)\s*章'))
    title_offset = int(config.get("chapter_title_offset", 1))

    # ── Plan A 模式 ──────────────────────────────────────────────────────────
    if chapter_order is not None:
        sections: list[tuple[str, str, str]] = []
        order_idx = 0
        for i, line in enumerate(lines):
            stripped = line.rstrip()
            if not re_chapter.match(stripped):
                continue
            if order_idx >= len(chapter_order):
                print(
                    f"警告：语料中检测到的章节数（{order_idx + 1}）超过 chapter_order 条目数"
                    f"（{len(chapter_order)}）。",
                    file=sys.stderr,
                )
                break
            nnn, page_id = chapter_order[order_idx]
            if title_offset > 0 and i + title_offset < len(lines):
                title = _strip_title_markup(lines[i + title_offset])
            else:
                title = _strip_title_markup(stripped)
            sections.append((nnn, page_id, title))
            order_idx += 1
        if order_idx < len(chapter_order):
            print(
                f"警告：chapter_order 有 {len(chapter_order)} 条，但语料只检测到 {order_idx} 个章节标题。",
                file=sys.stderr,
            )
        return sections

    # ── 旧模式（AIMA 兼容） ───────────────────────────────────────────────────
    re_preface = re.compile(config.get("preface_pattern", r'^##\s+前言')) if config.get("preface_pattern") else None
    re_appendix = re.compile(config.get("appendix_pattern", r'^# APPENDIX ([A-Z])$'))
    preface_nnn = config.get("preface_nnn", "P01")

    sections = []

    for i, line in enumerate(lines):
        stripped = line.rstrip()

        if re_preface and re_preface.match(stripped):
            title = _strip_title_markup(stripped)
            sections.append((preface_nnn, "Preface", title))
            continue

        m = re_chapter.match(stripped)
        if m:
            chapter_num = int(m.group(1))
            nnn = f"{chapter_num:03d}"
            if title_offset > 0 and i + title_offset < len(lines):
                title = _strip_title_markup(lines[i + title_offset])
            else:
                title = _strip_title_markup(stripped)
            sections.append((nnn, f"Chapter {chapter_num}", title))
            continue

        if re_appendix is not None:
            am = re_appendix.match(stripped)
            if am:
                letter = am.group(1)
                appendix_num = ord(letter) - ord('A') + 1
                nnn = f"A{appendix_num:02d}"
                if title_offset > 0 and i + title_offset < len(lines):
                    title = _strip_title_markup(lines[i + title_offset])
                else:
                    title = _strip_title_markup(stripped)
                sections.append((nnn, f"Appendix {letter}", title))

    return sections


def build_chapter_map(wiki_root: Path, dry_run: bool = False) -> None:
    config_path = get_local_config(wiki_root) / "butler.json"
    config: dict = json.loads(config_path.read_text()) if config_path.exists() else {}

    corpus_rel = config.get("corpus_file", "corpus/语料.md")
    corpus_path = wiki_root / corpus_rel
    if not corpus_path.exists():
        print(f"错误：语料文件不存在：{corpus_path}", file=sys.stderr)
        sys.exit(1)

    # Plan A：从 chapter_order_file 读取 NNN 序列
    chapter_order: list[tuple[str, str]] | None = None
    order_rel = config.get("chapter_order_file")
    if order_rel:
        order_path = wiki_root / order_rel
        if not order_path.exists():
            print(f"错误：chapter_order_file 不存在：{order_path}", file=sys.stderr)
            sys.exit(1)
        skip = config.get("chapter_order_skip", [])
        chapter_order = _parse_chapter_order(order_path, skip)

    lines = corpus_path.read_text(encoding="utf-8").splitlines()
    sections = extract_sections(lines, config, chapter_order)

    if not sections:
        print("警告：未在语料中找到任何章节，请检查 butler.json 中的正则配置。", file=sys.stderr)
        sys.exit(1)

    max_nnn = max(len(s[0]) for s in sections)
    max_part = max(len(s[1]) for s in sections)

    rows = []
    for nnn, part, title in sections:
        rows.append(f"| `{nnn}`{' ' * (max_nnn - len(nnn))}   | {part}{' ' * (max_part - len(part))} | {title} |")

    mode_note = f"章节次序来源：`{order_rel}`" if order_rel else "章节号来源：语料标题正则"
    header = f"""\
# PN 章节映射表

PN 格式：`NNN-PPP`（章节编号三位零填充 + 段号三位零填充）

语料来源：`{corpus_rel}`

{mode_note}

## 章节编号映射

| PN 前缀 | 对应部分 | 语料章节标题 |
|---------|----------|-------------|
{chr(10).join(rows)}
"""

    out_path = wiki_root / "local" / "butler" / "chapter-map.md"

    if dry_run:
        print("--- 预览（dry-run，不写文件）---")
        print(header)
        print(f"--- 目标路径：{out_path} ---")
        return

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(header, encoding="utf-8")
    print(f"已写入 {out_path}（{len(sections)} 章节）")


def main() -> None:
    parser = argparse.ArgumentParser(description="从 wiki 语料生成 local/butler/chapter-map.md")
    parser.add_argument("--wiki-root", type=Path, default=None, help="wiki 根目录（默认 $WIKI_ROOT 或 cwd）")
    parser.add_argument("--dry-run", action="store_true", help="预览输出，不写文件")
    args = parser.parse_args()

    wiki_root = args.wiki_root or get_wiki_root()
    build_chapter_map(wiki_root, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
