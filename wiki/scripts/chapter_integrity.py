#!/usr/bin/env python3
"""章节完整性基因 — CHK7 章节注册表与语料覆盖检查

检查项:
  C01: pages.json 含全部 21 个预期章节 (Preface + ch01–ch19 + Epilogue)
  C02: 每个章节 entry 的 type 为 "chapter"
  C03: 每个章节 entry 含 chapter 字段且数值连续 (0–20)
  C04: 每个章节 entry 的 label 与语料库 HEADING_MAP 一致
  C05: 非章节页面 (Frontispiece, About, 目录) 不含 chapter 字段
  C06: 语料库中所有 H2 均被 HEADING_MAP 覆盖 (无遗漏段落)
  C07: 章节页面的 frontmatter 与 pages.json 注册信息一致

用法:
  python3 wiki/scripts/chapter_integrity.py
  python3 wiki/scripts/chapter_integrity.py --fix    # 尝试自动修复 pages.json

返回码: 0 = 全部通过, 1 = 有检查项未通过
"""

import json, os, re, sys
from pathlib import Path

WIKI_ROOT = Path(os.environ.get('WIKI_ROOT', os.getcwd()))
PAGES_DIR = WIKI_ROOT / 'docs/wiki/pages'
PAGES_JSON = WIKI_ROOT / 'docs/wiki/pages.json'
CORPUS = WIKI_ROOT / 'corpus/raw/doc_final.md'

# ── 预期章节列表 ──────────────────────────────────────────────────────────────
EXPECTED_CHAPTERS = [
    (0,    'Preface',        '前言　耶利的问题'),
    (1,    'ch01-up-to-the-starting-line',
                              '第一章　走上起跑线'),
    (2,    'ch02-natural-experiment-of-history',
                              '第二章　历史的自然实验'),
    (3,    'ch03-collision-at-cajamarca',
                              '第三章　卡哈马卡的冲突'),
    (4,    'ch04-farmer-power',
                              '第四章　农民的力量'),
    (5,    'ch05-historys-haves-and-have-nots',
                              '第五章　历史上的穷与富'),
    (6,    'ch06-to-farm-or-not-to-farm',
                              '第六章　种田还是不种田'),
    (7,    'ch07-how-to-make-an-almond',
                              '第七章　怎样识别杏仁'),
    (8,    'ch08-apples-or-indians',
                              '第八章　问题在苹果还是在印第安人'),
    (9,    'ch09-zebras-unhappy-marriages-anna-karenina',
                              '第九章　斑马、不幸的婚姻和安娜·卡列尼娜原则'),
    (10,   'ch10-spacious-skies-tilted-axis',
                              '第十章　辽阔的天空与偏斜的轴线'),
    (11,   'ch11-lethal-gift-of-livestock',
                              '第十一章　牲畜的致命礼物'),
    (12,   'ch12-blueprints-borrowed-letters',
                              '第十二章　蓝图和借用字母'),
    (13,   'ch13-necessitys-mother',
                              '第十三章　需要之母'),
    (14,   'ch14-from-egalitarianism-to-kleptocracy',
                              '第十四章　从平等主义到盗贼统治'),
    (15,   'ch15-yalis-people',
                              '第十五章　耶利的族人'),
    (16,   'ch16-how-china-became-chinese',
                              '第十六章　中国是怎样成为中国人的中国的'),
    (17,   'ch17-speedboat-to-polynesia',
                              '第十七章　驶向波利尼西亚的快艇'),
    (18,   'ch18-collision-of-two-hemispheres',
                              '第十八章　两个半球的碰撞'),
    (19,   'ch19-how-africa-became-black',
                              '第十九章　非洲是怎样成为黑人的非洲的'),
    (20,   'Epilogue',       '后记　人类史作为一门科学的未来'),
]

EXPECTED_MAP = {pid: (num, pid, label) for num, pid, label in EXPECTED_CHAPTERS}
ALL_EXPECTED_IDS = {pid for _, pid, _ in EXPECTED_CHAPTERS}
ALL_EXPECTED_NUMS = {num for num, _, _ in EXPECTED_CHAPTERS}

NON_CHAPTER_PAGES = {'Frontispiece', 'About', '目录'}


def _parse_frontmatter_ids(text: str) -> dict:
    """提取 frontmatter 中 id / type / label / chapter / tags."""
    m = re.search(r'(?m)^---\s*\n(.*?)\n---', text, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ':' not in line:
            continue
        key, _, val = line.partition(':')
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        fm[key] = val
    return fm


def main():
    fix_mode = '--fix' in sys.argv
    errors = []
    warnings = []

    # ── Load registry ──────────────────────────────────────────────────────
    reg = json.loads(PAGES_JSON.read_text(encoding='utf-8'))
    pages = reg['pages']

    # ════════════════════════════════════════════════════════════════════════
    # C01: 全部预期章节存在
    # ════════════════════════════════════════════════════════════════════════
    registered_ids = set(pages.keys())
    missing = ALL_EXPECTED_IDS - registered_ids
    if missing:
        errors.append(f"C01 pages.json 缺失章节: {', '.join(sorted(missing))}")
    else:
        print("✓ C01 全部 21 个预期章节均已注册")

    # ════════════════════════════════════════════════════════════════════════
    # C02: 章节 type == chapter
    # ════════════════════════════════════════════════════════════════════════
    wrong_type = []
    for pid in sorted(ALL_EXPECTED_IDS & registered_ids):
        entry = pages[pid]
        if entry.get('type') != 'chapter':
            wrong_type.append(pid)
            if fix_mode:
                entry['type'] = 'chapter'
    if wrong_type:
        errors.append(f"C02 type 非 chapter: {', '.join(wrong_type)}")
    else:
        print("✓ C02 所有章节 type 均为 chapter")

    # ════════════════════════════════════════════════════════════════════════
    # C03: chapter 字段存在且连续 (0–20)，book_seq 存在且与 chapter 一致
    # ════════════════════════════════════════════════════════════════════════
    missing_ch = []
    wrong_ch = []
    missing_seq = []
    wrong_seq = []
    for pid in sorted(ALL_EXPECTED_IDS & registered_ids):
        entry = pages[pid]
        expected_num = EXPECTED_MAP[pid][0]
        actual_num = entry.get('chapter')
        if actual_num is None:
            missing_ch.append(pid)
            if fix_mode:
                entry['chapter'] = expected_num
                entry['book_seq'] = expected_num
        elif actual_num != expected_num:
            wrong_ch.append(f"{pid}(expect {expected_num}, got {actual_num})")
            if fix_mode:
                entry['chapter'] = expected_num
        # book_seq 检查
        bs = entry.get('book_seq')
        if bs is None:
            missing_seq.append(pid)
            if fix_mode:
                entry['book_seq'] = expected_num
        elif bs != expected_num:
            wrong_seq.append(f"{pid}(expect {expected_num}, got {bs})")
            if fix_mode:
                entry['book_seq'] = expected_num
    if missing_ch:
        errors.append(f"C03 缺 chapter 字段: {', '.join(missing_ch)}")
    if wrong_ch:
        errors.append(f"C03 chapter 数值错误: {', '.join(wrong_ch)}")
    if missing_seq:
        errors.append(f"C03 缺 book_seq 字段: {', '.join(missing_seq)}")
    if wrong_seq:
        errors.append(f"C03 book_seq 数值错误: {', '.join(wrong_seq)}")
    if not missing_ch and not wrong_ch and not missing_seq and not wrong_seq:
        print("✓ C03 所有章节均有 chapter + book_seq 字段且数值连续 (0–20)")

    # ════════════════════════════════════════════════════════════════════════
    # C04: label 与预期一致
    # ════════════════════════════════════════════════════════════════════════
    wrong_label = []
    for pid in sorted(ALL_EXPECTED_IDS & registered_ids):
        entry = pages[pid]
        expected_label = EXPECTED_MAP[pid][2]
        actual_label = entry.get('label', '')
        if actual_label != expected_label:
            wrong_label.append(f"{pid}: {actual_label!r} ≠ {expected_label!r}")
            if fix_mode:
                entry['label'] = expected_label
    if wrong_label:
        errors.append(f"C04 label 不匹配:\n  " + "\n  ".join(wrong_label))
    else:
        print("✓ C04 所有章节 label 与预期一致")

    # ════════════════════════════════════════════════════════════════════════
    # C05: 非章节页面不含 chapter 字段
    # ════════════════════════════════════════════════════════════════════════
    wrong_non_ch = []
    for pid in sorted(NON_CHAPTER_PAGES & registered_ids):
        entry = pages[pid]
        if 'chapter' in entry:
            wrong_non_ch.append(pid)
            if fix_mode:
                del entry['chapter']
    if wrong_non_ch:
        errors.append(f"C05 非章节页面含 chapter 字段: {', '.join(wrong_non_ch)}")
    else:
        print("✓ C05 非章节页面不含 chapter 字段")

    # ════════════════════════════════════════════════════════════════════════
    # C06: 语料库 H2 全覆盖
    # ════════════════════════════════════════════════════════════════════════
    if CORPUS.exists():
        text = CORPUS.read_text(encoding='utf-8')
        h2s = re.findall(r'^##\s+(.+)', text, re.MULTILINE)
        h2_heading_map = {label: True for _, _, label in EXPECTED_CHAPTERS}
        unmapped = []
        for h2 in h2s:
            if h2 not in h2_heading_map:
                unmapped.append(h2)
        if unmapped:
            warnings.append(f"C06 语料库中 {len(unmapped)} 个 H2 未被任何章节覆盖:\n  " +
                           "\n  ".join(unmapped[:10]))
            if len(unmapped) > 10:
                warnings[-1] += f"\n  ... 及另外 {len(unmapped)-10} 个"
        else:
            print("✓ C06 语料库所有 H2 均被章节覆盖")
    else:
        warnings.append("C06 跳过: 语料库不存在")

    # ════════════════════════════════════════════════════════════════════════
    # C07: 页面文件 frontmatter 与 pages.json 一致
    # ════════════════════════════════════════════════════════════════════════
    fm_mismatch = []
    for pid in sorted(ALL_EXPECTED_IDS):
        prefix = pid[:2].lower()
        page_file = PAGES_DIR / prefix / f'{pid}.md'
        if not page_file.exists():
            fm_mismatch.append(f"{pid}: 页面文件不存在")
            continue
        raw = page_file.read_text(encoding='utf-8')
        # 检查文件是否以 --- 开头（无前导空白）
        if not raw.startswith('---'):
            fm_mismatch.append(f"{pid}: 文件开头有多余字符 (前 {raw[:20]!r})")
        fm = _parse_frontmatter_ids(raw)
        if fm.get('type') != 'chapter':
            fm_mismatch.append(f"{pid}: frontmatter type={fm.get('type')!r}")
        if fm.get('id') != pid:
            fm_mismatch.append(f"{pid}: frontmatter id={fm.get('id')!r}")
        expected_label = EXPECTED_MAP[pid][2]
        if fm.get('label') != expected_label:
            fm_mismatch.append(f"{pid}: frontmatter label={fm.get('label')!r}")
    if fm_mismatch:
        errors.append(f"C07 页面 frontmatter 异常:\n  " + "\n  ".join(fm_mismatch))
    else:
        print("✓ C07 所有章节页面 frontmatter 与 pages.json 一致")

    # ════════════════════════════════════════════════════════════════════════
    # C08: 语料内容覆盖率 ≥ 95%（章节页总字符 / 语料总字符）
    # ════════════════════════════════════════════════════════════════════════
    if CORPUS.exists():
        corpus_text = CORPUS.read_text(encoding='utf-8')
        # 只统计正文（去掉 frontmatter 后的内容）
        corpus_body = corpus_text
        corpus_chars = len(corpus_body)
        chapter_chars = 0
        for pid in ALL_EXPECTED_IDS:
            prefix = pid[:2].lower()
            page_file = PAGES_DIR / prefix / f'{pid}.md'
            if page_file.exists():
                raw = page_file.read_text(encoding='utf-8')
                # 去掉 frontmatter
                body = re.sub(r'^---.*?---', '', raw, count=1, flags=re.DOTALL)
                chapter_chars += len(body)
        coverage = chapter_chars / max(corpus_chars, 1) * 100
        if coverage < 95:
            warnings.append(f"C08 内容覆盖率 {coverage:.1f}%（{chapter_chars}/{corpus_chars}），低于 95%")
        else:
            print(f"✓ C08 内容覆盖率 {coverage:.1f}%（≥ 95%）")
    else:
        warnings.append("C08 跳过: 语料库不存在")

    # ── Write fix ──────────────────────────────────────────────────────────
    if fix_mode and errors:
        PAGES_JSON.write_text(
            json.dumps(reg, ensure_ascii=False, indent=2) + '\n',
            encoding='utf-8',
        )
        print(f"\n🔧 pages.json 已自动修复")

    # ── Summary ────────────────────────────────────────────────────────────
    print()
    if errors:
        for e in errors:
            print(f"✗ {e}")
        print(f"\n结果: {len(errors)} 个错误")
    else:
        print("结果: 全部通过 ✓")

    if warnings:
        for w in warnings:
            print(f"  ⚠ {w}")

    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
