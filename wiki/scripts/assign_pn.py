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

import json, os, re, subprocess, sys
from pathlib import Path

WIKI_ROOT = Path(__file__).resolve().parent.parent.parent
MEMEX_ROOT = Path(os.environ.get('MEMEX_ROOT', os.path.expanduser('~/memex')))
PAGES_DIR = WIKI_ROOT / 'docs/wiki/pages'
CHAPTER_ORDER = WIKI_ROOT / 'ref/chapter-order.md'
PAGES_JSON = WIKI_ROOT / 'docs/wiki/pages.json'

# ── 加载 NNN 映射 ──────────────────────────────────────────────────────────
CHAPTER_MAP: dict[str, str] = {}  # page_id → nnn
NNN_MAP: dict[str, str] = {}      # nnn → page_id
PAGE_PATHS: dict[str, Path] = {}  # page_id → 实际文件路径（从 pages.json 加载）

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


def load_page_paths():
    if not PAGES_JSON.exists():
        return
    data = json.load(PAGES_JSON.open(encoding='utf-8'))
    for pid, info in data.get('pages', {}).items():
        rel = info.get('path', '')
        if rel:
            PAGE_PATHS[pid] = PAGES_DIR / rel

load_page_paths()


def find_page_file(page_id: str) -> Path | None:
    """按 pages.json 路径查找页面文件（CONSTITUTION §十九）。"""
    if page_id in PAGE_PATHS:
        p = PAGE_PATHS[page_id]
        return p if p.exists() else None
    return None


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
    in_sem_block = False  # 是否在 :::TYPE ... ::: 语义块内部
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

        # ::: 闭合标签 → 跳过，不赋 PN，退出语义块状态
        if block == ':::':
            in_sem_block = False
            result_parts.append(blocks[i])
            i += 1
            continue

        # ::: 语义块开启行（::: image / ::: table / ::: note 等）→ pn= 属性，进入块内状态
        if block.startswith(':::'):
            lines = block.split('\n')
            # 若块末行为 ::: 则自包含，无需进入跨段状态
            is_self_contained = lines[-1].strip() == ':::'
            in_sem_block = not is_self_contained
            pn_str = f'{nnn_str}-{pn_counter:03d}'
            pn_counter += 1
            first_line = lines[0]
            rest = '\n'.join(lines[1:])
            # 规范化：:::TYPE（无空格）→ ::: TYPE（有空格）
            first_line = re.sub(r'^:::([a-zA-Z])', r'::: \1', first_line)
            if 'pn=' not in first_line:
                new_first = first_line + f' pn={pn_str}'
                result_parts.append((new_first + '\n' + rest) if rest else new_first)
            else:
                result_parts.append(block)
            i += 1
            continue

        # 语义块内部内容（说明文字、图片 markdown 等）→ 跳过，不赋内联 PN
        if in_sem_block:
            # 移除误赋的内联 PN（幂等安全）
            cleaned = re.sub(r'^\[(?:\d{3}|P\d{2})-\d{3}\]', '', blocks[i], flags=re.MULTILINE)
            result_parts.append(cleaned)
            i += 1
            continue

        # 普通段落
        pn_str = f'{nnn_str}-{pn_counter:03d}'
        pn_counter += 1
        # 检查是否已有 PN（幂等，兼容数字 NNN 和 P 前缀 NNN）
        if re.match(r'^\[(?:\d{3}|P\d{2})-\d{3}\]', block):
            result_parts.append(blocks[i])
            i += 1
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

    fpath = find_page_file(page_id)
    if not fpath:
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
    # 记录修订（CONSTITUTION §4.6）
    record_script = MEMEX_ROOT / 'wiki/scripts/record_revision.py'
    if record_script.exists():
        subprocess.run([
            sys.executable, str(record_script),
            page_id,
            '--summary', f'assign_pn: {nnn} 标注 {total_pns} 段',
            '--author', 'baojie',
            '--public', str(WIKI_ROOT / 'docs/wiki'),
        ], check=False)
    else:
        print(f"  ! record_revision.py 不存在，跳过修订记录")
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
        # 所有赋 PN 的章节页，按 chapter-order.md 顺序（P 前缀在前，数字章节在后）
        p_pages = [(nnn, NNN_MAP[nnn]) for nnn in sorted(NNN_MAP.keys()) if re.match(r'^P\d{2}$', nnn)]
        n_pages = [(nnn, NNN_MAP[nnn]) for nnn in sorted(NNN_MAP.keys()) if re.match(r'^\d{3}$', nnn)]
        for _, pid in p_pages + n_pages:
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
