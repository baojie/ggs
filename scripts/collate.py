#!/usr/bin/env python3
"""
三版《枪炮、病菌与钢铁》校勘脚本
底本：谢延光译本 epub
校本1：修订版PDF
校本2：v2 epub
产出：corpus/raw/枪炮病菌与钢铁_校勘底稿.md

策略：章级全文字符对齐，过滤纯排印差异，只记录实质性文字异同。
"""

import re
import difflib
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional

BASE = "corpus/枪炮病菌与钢铁_谢延光译.md"
REV  = "corpus/枪炮病菌与钢铁_修订版PDF.md"
V2   = "corpus/枪炮病菌与钢铁_v2.md"
OUT  = "corpus/raw/枪炮病菌与钢铁_校勘底稿.md"

# ── 1. 预处理 ─────────────────────────────────────────────────────

def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()

PDF_HEADING = re.compile(
    r'^(前言[\s　]\S.{0,25}|后记[\s　]\S.{0,25}'
    r'|附录[\s　]?\S.{0,30}'
    r'|第[一二三四五六七八九十百]+[部章][\s　].{0,30}'
    r'|第\s*\d+\s*[部章][\s　].{0,30})$'
)

def prepare_pdf(text: str) -> str:
    """合并 PDF 短行为段落，章节标题加 ## 前缀"""
    lines = text.split('\n')
    out, buf = [], []

    def flush():
        if buf:
            out.append(''.join(buf))
            out.append('')
            buf.clear()

    for raw in lines:
        s = raw.strip()
        if not s:
            flush(); continue
        if s.startswith('#'):
            flush(); out.append(s); out.append(''); continue
        if PDF_HEADING.match(s):
            flush(); out.append(f'## {s}'); out.append(''); continue
        buf.append(s)
    flush()
    return '\n'.join(out)

def prepare_v2(text: str) -> str:
    """清理 v2 EPUB HTML 残留，保留 ## 标题"""
    lines = []
    for line in text.split('\n'):
        if re.match(r'^#{1,6}\s', line):
            line = re.sub(r'\s*\{[^}]{0,120}\}\s*$', '', line)
        else:
            line = re.sub(r'\{[^}]{0,120}\}', '', line)
            line = re.sub(r'\[\]\{[^}]*\}', '', line)
            line = re.sub(r'<[^>]+>', '', line)
        lines.append(line)
    text = '\n'.join(lines)
    text = re.sub(r'^:::.*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\\\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*!\[.*?\]\([^)]+\)\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text

# ── 2. 切分章节 ───────────────────────────────────────────────────

@dataclass
class Chapter:
    key: str
    raw_title: str
    level: int
    paragraphs: List[str] = field(default_factory=list)

_CN2INT = {k: v for v, k in enumerate(
    ['零','一','二','三','四','五','六','七','八','九','十',
     '十一','十二','十三','十四','十五','十六','十七','十八','十九','二十'], 0)}

def chapter_key(title: str) -> str:
    t = re.sub(r'\s+', '', title)
    m = re.search(r'第([一二三四五六七八九十\d]+)([部章])', t)
    if m:
        raw, kind = m.group(1), m.group(2)
        n = _CN2INT.get(raw) or (int(raw) if raw.isdigit() else 0)
        return f'{"部" if kind == "部" else "章"}{n:02d}'
    if '前言' in t: return '前言'
    if '后记' in t or '附录' in t: return '后记'
    return t[:8]

HEADING_RE = re.compile(r'^(#{1,6})\s+(.*\S)')

def split_chapters(text: str) -> List[Chapter]:
    chapters, cur = [], None
    for line in text.split('\n'):
        m = HEADING_RE.match(line.rstrip())
        if m:
            lvl = len(m.group(1))
            title = m.group(2).strip()
            key = chapter_key(title)
            if lvl <= 2:
                if cur: chapters.append(cur)
                cur = Chapter(key=key, raw_title=title, level=lvl)
                continue
        if cur is not None:
            s = line.strip()
            if s and not s.startswith('#'):
                cur.paragraphs.append(s)
    if cur: chapters.append(cur)
    return chapters

# ── 3. 文字提取与规范化 ────────────────────────────────────────────

INLINE_MD = re.compile(r'\*{1,3}([^*\n]+)\*{1,3}|`[^`]+`|\[[^\]]*\]\([^)]*\)')
ATTR_BLOCK = re.compile(r'\{[^}]{0,120}\}')
FOOTNOTE_EPUB = re.compile(r'\^\[.*?\]')          # epub 格式：^[text](#url)
FOOTNOTE_PDF  = re.compile(r'\[\d{1,3}\]')        # PDF 格式：[1]

def plain_text(paras: List[str]) -> str:
    """把段落列表转为纯文字（去 markdown 和脚注，拼成一串）"""
    parts = []
    for p in paras:
        p = FOOTNOTE_EPUB.sub('', p)
        p = FOOTNOTE_PDF.sub('', p)
        p = INLINE_MD.sub(r'\1', p)
        p = ATTR_BLOCK.sub('', p)
        p = re.sub(r'<[^>]+>', '', p)
        parts.append(p)
    return ''.join(parts)

# 排印规范化：只保留汉字、字母、数字；抹去所有标点/空格/括号差异
# 用于判断两段是否"实质相同"
def typeset_norm(text: str) -> str:
    """去除所有标点、空白，只保留汉字/字母/数字，用于判断实质差异。"""
    import unicodedata
    out = []
    for ch in text:
        cat = unicodedata.category(ch)
        # 保留字母(L*)、数字(N*)
        if cat.startswith('L') or cat.startswith('N'):
            out.append(ch)
        # 跳过标点(P*)、符号(S*)、空白(Z*)、控制字符(C*)
    return ''.join(out)

def has_real_diff(base: str, other: str) -> bool:
    """判断两段文字是否有实质内容差异（排印差异不算）"""
    return typeset_norm(base) != typeset_norm(other)

# ── 4. 章级 diff ─────────────────────────────────────────────────

def build_norm_map(text: str) -> Tuple[str, List[int]]:
    """
    返回 (norm_text, orig_positions)。
    orig_positions[i] = norm_text[i] 对应 text 中的原始字符索引。
    """
    norm_chars = []
    orig_pos = []
    for i, ch in enumerate(text):
        n = typeset_norm(ch)
        if n:  # 只保留非空规范化字符
            norm_chars.append(n)
            orig_pos.append(i)
    return ''.join(norm_chars), orig_pos

def find_diffs(base_text: str, other_text: str, label: str, ctx: int = 40) -> List[dict]:
    """
    在两个纯文字串上做字符级 diff，只返回实质性差异片段。
    先在规范化串上对齐，再把位置映射回原始文本展示上下文。
    """
    if not has_real_diff(base_text, other_text):
        return []

    bnorm, bpos = build_norm_map(base_text)
    onorm, opos = build_norm_map(other_text)

    sm = difflib.SequenceMatcher(None, bnorm, onorm, autojunk=False)

    diffs = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            continue
        # 至少有3个规范化字符的差异才记录（排除单字标点残余）
        if (i2 - i1) + (j2 - j1) < 3:
            continue

        # 把规范化位置映射回原文，加上上下文
        if bpos and i1 < len(bpos):
            b_start = max(0, bpos[i1] - ctx)
            b_end   = (bpos[i2-1] + ctx + 1) if i2 > 0 and i2-1 < len(bpos) else len(base_text)
            b_end   = min(b_end, len(base_text))
            base_snippet = base_text[b_start:b_end].strip()
        else:
            base_snippet = ''

        if opos and j1 < len(opos):
            o_start = max(0, opos[j1] - ctx)
            o_end   = (opos[j2-1] + ctx + 1) if j2 > 0 and j2-1 < len(opos) else len(other_text)
            o_end   = min(o_end, len(other_text))
            other_snippet = other_text[o_start:o_end].strip()
        else:
            other_snippet = ''

        # 再次检查展示片段是否真有实质差异
        if not has_real_diff(base_snippet, other_snippet):
            continue

        diffs.append({
            'label': label,
            'base':  base_snippet[:150],
            'other': other_snippet[:150],
        })

    # 合并相邻差异（位置相近则合并）
    merged = []
    for d in diffs:
        if merged and merged[-1]['base'][-20:] in d['base']:
            continue  # 重叠片段，跳过
        merged.append(d)

    return merged

# ── 5. 底稿生成 ───────────────────────────────────────────────────

def render_notes(diffs: List[dict], max_items: int = 12) -> List[str]:
    if not diffs: return []
    label = diffs[0]['label']
    lines = [f'\n> **【校勘·{label}】**（{len(diffs)} 处）']
    for d in diffs[:max_items]:
        b, o = d['base'], d['other']
        if b and o:
            lines.append(f'> - 底本：…{b}…')
            lines.append(f'>   {label}：…{o}…')
        elif o:
            lines.append(f'>   {label} 新增：…{o}…')
        elif b:
            lines.append(f'>   底本独有：…{b}…')
    if len(diffs) > max_items:
        lines.append(f'>   …（另 {len(diffs)-max_items} 处略）')
    lines.append('')
    return lines

def build_output(base_chs: List[Chapter],
                 rev_map: Dict[str, Chapter],
                 v2_map:  Dict[str, Chapter]) -> Tuple[str, dict]:
    lines = []
    stats = {'rev': 0, 'v2': 0, 'missing_rev': [], 'missing_v2': []}

    for bc in base_chs:
        hashes = '#' * bc.level
        lines.append(f'\n{hashes} {bc.raw_title}\n')
        lines.extend(bc.paragraphs)
        lines.append('')

        base_plain = plain_text(bc.paragraphs)
        rc = rev_map.get(bc.key)
        vc = v2_map.get(bc.key)

        if rc is None:
            stats['missing_rev'].append(bc.raw_title)
        if vc is None:
            stats['missing_v2'].append(bc.raw_title)

        if rc:
            diffs = find_diffs(base_plain, plain_text(rc.paragraphs), '修订版')
            stats['rev'] += len(diffs)
            lines.extend(render_notes(diffs))

        if vc:
            diffs = find_diffs(base_plain, plain_text(vc.paragraphs), 'v2')
            stats['v2'] += len(diffs)
            if diffs:
                lines.extend(render_notes(diffs, max_items=6))

    return '\n'.join(lines), stats

# ── 6. main ───────────────────────────────────────────────────────

def main():
    import os
    os.makedirs('corpus/raw', exist_ok=True)

    print("读取...")
    base_raw = read(BASE)
    rev_raw  = read(REV)
    v2_raw   = read(V2)

    print("预处理...")
    rev_prep = prepare_pdf(rev_raw)
    v2_prep  = prepare_v2(v2_raw)

    print("切分章节...")
    base_chs = split_chapters(base_raw)
    rev_chs  = split_chapters(rev_prep)
    v2_chs   = split_chapters(v2_prep)

    print(f"  底本 {len(base_chs)} 章  修订版 {len(rev_chs)} 章  v2 {len(v2_chs)} 章")

    # 修订版有 TOC 导致重复 key，只取最后出现的（正文）
    rev_map: Dict[str, Chapter] = {}
    for c in rev_chs:
        rev_map[c.key] = c

    v2_map: Dict[str, Chapter] = {}
    for c in v2_chs:
        v2_map[c.key] = c  # v2 key 应唯一

    print("校勘中...")
    body, stats = build_output(base_chs, rev_map, v2_map)

    header = """\
# 枪炮、病菌与钢铁：人类社会的命运

**底本**：谢延光译本（epub）
**校本**：修订版PDF、v2 epub
**校勘规则**：以底本为全文，章内差异以 `> 【校勘·XX】` 注记跟附于各章末。
仅记录汉字/数字层面的实质性差异；标点、括号、破折号等排印差异不计入。

---
"""
    result = header + body
    result = re.sub(r'\n{4,}', '\n\n\n', result)

    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(result)

    print(f"\n→ {OUT}")
    print(f"总字数：{len(result):,}")
    print(f"修订版实质差异：{stats['rev']} 处")
    print(f"v2 实质差异：{stats['v2']} 处")
    if stats['missing_rev']:
        print(f"修订版无对应章：{stats['missing_rev']}")
    if stats['missing_v2']:
        print(f"v2 无对应章：{stats['missing_v2']}")

if __name__ == '__main__':
    main()
