#!/usr/bin/env python3
"""Phase 5-C: 为章节页分配 PN 段落编号。

依赖:
  - ref/chapter-order.md（NNN 映射）
  - docs/wiki/data/chapter_map.json（NNN → page_id）
  - 各章节页 frontmatter 已有 pn_prefix（Phase 5-B 写入）

用法:
  python3 wiki/scripts/assign_pn.py ch08        # 指定章节
  python3 wiki/scripts/assign_pn.py --pilot     # 试验章 (ch08)
  python3 wiki/scripts/assign_pn.py --all       # 全量赋号
  python3 wiki/scripts/assign_pn.py ch08 --dry-run  # 预览不改文件

PN 规则（参考 data-pn.md + PRE7）:
  - 普通段落: 段首 [NNN-PPP] 紧靠正文
  - ::: image 块: 行首 ::: image → ::: image pn=NNN-PPP
  - 标题行 (##): 跳过
  - frontmatter (---): 跳过
  - 空行: 跳过
  - blockquote (>): 跳过
"""

import json, re, sys
from pathlib import Path

WIKI_ROOT = Path(__file__).resolve().parent.parent.parent
PAGES_DIR = WIKI_ROOT / 'docs/wiki/pages'
CHAPTER_ORDER = WIKI_ROOT / 'ref/chapter-order.md'

# ── 加载 NNN 映射 ──────────────────────────────────────────────────────────
CHAPTER_MAP: dict[str, str] = {}  # page_id → nnn
NNN_MAP: dict[str, str] = {}      # nnn → page_id

def load_nnn_map():
    text = CHAPTER_ORDER.read_text(encoding='utf-8')
    for line in text.splitlines():
        line = line.strip()
        if not line or not line.startswith('|') or line.startswith('|---'):
            continue
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 3:
            nnn = parts[1]
            pid = parts[2]
            if nnn and pid and re.match(r'^(P\d{2}|\d{3})$', nnn):
                CHAPTER_MAP[pid] = nnn
                NNN_MAP[nnn] = pid

load_nnn_map()

# ── 赋号核心 ────────────────────────────────────────────────────────────────

def assign_pn_to_chapter(text: str, nnn: str, start_pn: int = 1) -> tuple[str, int]:
    """为章节内容分配 PN，返回 (标注后内容, 末号)."""
    has_frontmatter = text.startswith('---')
    if has_frontmatter:
        m = re.match(r'^---.*?\n---', text, re.DOTALL)
        if m:
            frontmatter = m.group(0)
            body = text[m.end():].strip()
        else:
            frontmatter = ''
            body = text
    else:
        frontmatter = ''
        body = text

    blocks = re.split(r'(\n\n)', body)
    result_parts = []
    pn_counter = start_pn
    nnn_str = nnn

    # 用累积器处理段落
    i = 0
    while i < len(blocks):
        block = blocks[i]
        # 保留空行分隔符
        if block == '\n\n':
            result_parts.append(block)
            i += 1
            continue

        block = block.strip()
        if not block:
            result_parts.append(blocks[i])
            i += 1
            continue

        # 标题行 → 跳过
        if re.match(r'^#{1,6} ', block):
            result_parts.append(blocks[i])
            i += 1
            continue

        # blockquote → 跳过
        if block.startswith('>'):
            result_parts.append(blocks[i])
            i += 1
            continue

        # 脚注定义（[^N]: text）→ 跳过（ggs 所有脚注为译者注，豁免 PN）
        if re.match(r'^\[\^', block):
            result_parts.append(blocks[i])
            i += 1
            continue

        # ::: image 块
        if block.startswith('::: image') or block.startswith(':::'):
            pn_str = f'{nnn_str}-{pn_counter:03d}'
            pn_counter += 1
            # 已含 ::: image 的加 pn 属性
            if block.startswith('::: image'):
                # 检查是否已有 pn=
                if 'pn=' not in block.split('\n')[0]:
                    first_line = block.split('\n')[0]
                    rest = '\n'.join(block.split('\n')[1:])
                    new_block = first_line + f' pn={pn_str}\n' + rest
                    result_parts.append(new_block)
                else:
                    result_parts.append(block)
                continue
        # 普通段落
        pn_str = f'{nnn_str}-{pn_counter:03d}'
        pn_counter += 1
        # 检查是否已有 PN（幂等）
        if re.match(r'^\[\d{3}-\d{3}\]', block):
            result_parts.append(blocks[i])
            continue
        result_parts.append(f'[{pn_str}]{block}')
        i += 1

    result_body = ''.join(result_parts).strip()
    if frontmatter:
        return frontmatter + '\n\n' + result_body + '\n', pn_counter - 1
    return result_body + '\n', pn_counter - 1


def verify_pn_sequence(text: str, nnn: str) -> list[str]:
    """验证 PN 连续性."""
    pns = re.findall(rf'\[{nnn}-(\d{{3}})\]', text)
    pns += re.findall(rf'pn={nnn}-(\d{{3}})', text)
    nums = sorted(set(int(p) for p in pns))
    errors = []
    for i, n in enumerate(nums):
        if i == 0 and n != 1:
            errors.append(f'起始 PN 不是 001，而是 {n:03d}')
        elif i > 0 and n != nums[i-1] + 1:
            errors.append(f'跳号: {nums[i-1]:03d} → {n:03d}')
    return errors


def process_chapter(page_id: str, dry_run: bool = False) -> bool:
    """处理单个章节。返回 True 表示成功。"""
    nnn = CHAPTER_MAP.get(page_id)
    if not nnn:
        print(f"  ✗ {page_id}: 未找到 NNN 映射")
        return False

    prefix = page_id[:2].lower()
    fpath = PAGES_DIR / prefix / f'{page_id}.md'
    if not fpath.exists():
        print(f"  ✗ {page_id}: 文件不存在")
        return False

    text = fpath.read_text(encoding='utf-8')
    new_text, last_pn = assign_pn_to_chapter(text, nnn)

    errors = verify_pn_sequence(new_text, nnn)
    if errors:
        print(f"  ✗ {page_id} ({nnn}): PN 验证失败:")
        for e in errors:
            print(f"    {e}")
        return False

    total_pns = len(re.findall(rf'\[{nnn}-\d{{3}}\]', new_text)) + \
                len(re.findall(rf'pn={nnn}-\d{{3}}', new_text))

    if dry_run:
        print(f"  ~ {page_id} ({nnn}): {total_pns} PN, 末号 {last_pn:03d}")
        return True

    fpath.write_text(new_text, encoding='utf-8')
    print(f"  ✓ {page_id} ({nnn}): {total_pns} PN, 末号 {last_pn:03d}")
    return True


def main():
    dry_run = '--dry-run' in sys.argv
    do_all = '--all' in sys.argv
    do_pilot = '--pilot' in sys.argv
    specific = [a for a in sys.argv[1:] if not a.startswith('--') and a != '--dry-run']

    pages = []

    if do_pilot:
        pages = ['ch08-apples-or-indians']
    elif do_all:
        # 所有章节页（按 chapter-order.md 中 NNN 为数字的）
        for nnn in sorted(NNN_MAP.keys()):
            pid = NNN_MAP[nnn]
            if re.match(r'^\d{3}$', nnn):  # 仅正文章节 001-020
                pages.append(pid)
    elif specific:
        for s in specific:
            # 支持简写 ch08 → ch08-apples-or-indians
            if re.match(r'^ch\d{2}$', s):
                for pid in CHAPTER_MAP:
                    if pid.startswith(s):
                        pages.append(pid)
                        break
                else:
                    print(f"  ✗ 未找到匹配: {s}")
            else:
                pages.append(s)
    else:
        print("用法: python3 wiki/scripts/assign_pn.py <page_id|chNN|--pilot|--all> [--dry-run]")
        return 1

    if not pages:
        print("未指定章节")
        return 1

    print(f"{'预览' if dry_run else '标注'} {len(pages)} 个章节:")
    success = 0
    for pid in pages:
        if process_chapter(pid, dry_run):
            success += 1

    print(f"\n结果: {success}/{len(pages)} 成功")
    return 0 if success == len(pages) else 1


if __name__ == '__main__':
    sys.exit(main())
