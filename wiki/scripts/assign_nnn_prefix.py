#!/usr/bin/env python3
"""Phase 5-B: 按 chapter-order.md 写入 NNN/pn_prefix + part 到章节 frontmatter.

用法:
  python3 wiki/scripts/assign_nnn_prefix.py          # 执行写入
  python3 wiki/scripts/assign_nnn_prefix.py --dry-run # 预览不改文件
"""

import json, os, re, sys
from pathlib import Path

WIKI_ROOT = Path(os.environ.get('WIKI_ROOT', os.getcwd()))
PAGES_DIR = WIKI_ROOT / 'docs/wiki/pages'
PAGES_JSON = WIKI_ROOT / 'docs/wiki/pages.json'
CHAPTER_ORDER = WIKI_ROOT / 'ref/chapter-order.md'
DATA_DIR = WIKI_ROOT / 'data'

# NNN → page_id 映射
NNN_MAP: dict[str, str] = {}
# page_id → NNN 映射
PAGE_NNN: dict[str, str] = {}

def parse_chapter_order():
    """解析 ref/chapter-order.md 表格."""
    text = CHAPTER_ORDER.read_text(encoding='utf-8')
    for line in text.splitlines():
        line = line.strip()
        if not line or not line.startswith('|') or line.startswith('|---'):
            continue
        parts = [p.strip() for p in line.split('|')]
        # | NNN | page-id | 说明 |
        if len(parts) >= 3:
            nnn = parts[1]
            pid = parts[2]
            if nnn and pid and re.match(r'^(P\d{2}|\d{3})$', nnn):
                NNN_MAP[nnn] = pid
                PAGE_NNN[pid] = nnn

PART_MAP: dict[str, tuple[int, str]] = {}
# page_id → (part_num, part_title)
def build_part_map():
    """part 映射基于 5-B 定义."""
    rules = [
        ('Preface',                                0, '前言'),
        ('ch01-up-to-the-starting-line',           1, '第一部分：从伊甸园到卡哈马卡'),
        ('ch02-natural-experiment-of-history',      1, '第一部分：从伊甸园到卡哈马卡'),
        ('ch03-collision-at-cajamarca',            1, '第一部分：从伊甸园到卡哈马卡'),
        ('ch04-farmer-power',                       2, '第二部分：粮食生产的出现和传播'),
        ('ch05-historys-haves-and-have-nots',      2, '第二部分：粮食生产的出现和传播'),
        ('ch06-to-farm-or-not-to-farm',            2, '第二部分：粮食生产的出现和传播'),
        ('ch07-how-to-make-an-almond',             2, '第二部分：粮食生产的出现和传播'),
        ('ch08-apples-or-indians',                 2, '第二部分：粮食生产的出现和传播'),
        ('ch09-zebras-unhappy-marriages-anna-karenina', 2, '第二部分：粮食生产的出现和传播'),
        ('ch10-spacious-skies-tilted-axis',        2, '第二部分：粮食生产的出现和传播'),
        ('ch11-lethal-gift-of-livestock',           3, '第三部分：从粮食到枪炮、病菌与钢铁'),
        ('ch12-blueprints-borrowed-letters',        3, '第三部分：从粮食到枪炮、病菌与钢铁'),
        ('ch13-necessitys-mother',                  3, '第三部分：从粮食到枪炮、病菌与钢铁'),
        ('ch14-from-egalitarianism-to-kleptocracy', 3, '第三部分：从粮食到枪炮、病菌与钢铁'),
        ('ch15-yalis-people',                       4, '第四部分：在5章中环游世界'),
        ('ch16-how-china-became-chinese',           4, '第四部分：在5章中环游世界'),
        ('ch17-speedboat-to-polynesia',             4, '第四部分：在5章中环游世界'),
        ('ch18-collision-of-two-hemispheres',       4, '第四部分：在5章中环游世界'),
        ('ch19-how-africa-became-black',            4, '第四部分：在5章中环游世界'),
        ('Epilogue',                                5, '后记'),
    ]
    for pid, num, title in rules:
        PART_MAP[pid] = (num, title)


def update_frontmatter(filepath: Path, pid: str, nnn: str) -> bool:
    """更新单个文件的 frontmatter，返回 True 表示有修改."""
    raw = filepath.read_text(encoding='utf-8')
    m = re.match(r'^---\s*\n(.*?)\n---', raw, re.DOTALL)
    if not m:
        print(f"  ✗ {pid}: 无 frontmatter")
        return False

    fm_text = m.group(1)
    lines = fm_text.splitlines()
    new_lines = []
    updated = False

    # 追踪已存在的字段
    fields_seen = set()

    for line in lines:
        key = line.split(':')[0].strip() if ':' in line else ''
        fields_seen.add(key)

        # 更新现有字段
        if key == 'pn_prefix':
            new_lines.append(f'pn_prefix: "{nnn}"')
            updated = updated or (f'pn_prefix: "{nnn}"' != line)
        elif key == 'part_num' and pid in PART_MAP:
            pn = PART_MAP[pid][0]
            new_lines.append(f'part_num: {pn}')
            updated = updated or (f'part_num: {pn}' != line)
        elif key == 'part_title' and pid in PART_MAP:
            pt = PART_MAP[pid][1]
            new_lines.append(f'part_title: "{pt}"')
            updated = updated or (f'part_title: "{pt}"' != line)
        else:
            new_lines.append(line)

    # 追加不存在的字段
    if 'pn_prefix' not in fields_seen:
        new_lines.append(f'pn_prefix: "{nnn}"')
        updated = True
    if pid in PART_MAP and 'part_num' not in fields_seen:
        new_lines.append(f'part_num: {PART_MAP[pid][0]}')
        updated = True
    if pid in PART_MAP and 'part_title' not in fields_seen:
        new_lines.append(f'part_title: "{PART_MAP[pid][1]}"')
        updated = True

    if not updated:
        return False

    new_fm = '\n'.join(new_lines)
    filepath.write_text('---\n' + new_fm + '\n---' + raw[m.end():], encoding='utf-8')

    return True


def build_chapter_map() -> dict:
    """构建 data/chapter_map.json（格式：nnn → page_id，供 pn-citation 插件查询）."""
    return dict(NNN_MAP)  # nnn → page_id


def main():
    dry_run = '--dry-run' in sys.argv
    parse_chapter_order()
    build_part_map()

    if not NNN_MAP:
        print("✗ 未解析到 NNN 映射，检查 ref/chapter-order.md 格式")
        return 1

    pages = json.loads(PAGES_JSON.read_text(encoding='utf-8'))['pages']
    print(f"NNN 映射: {len(NNN_MAP)} 条目")
    total_updated = 0
    for nnn, pid in sorted(NNN_MAP.items(), key=lambda x: x[0]):
        # 用 pages.json 的 path 字段定位文件，支持 CJK 页面 id
        entry = pages.get(pid)
        if not entry:
            print(f"  - {pid}: pages.json 中不存在")
            continue
        fpath_str = entry.get('path', '')
        if not fpath_str:
            print(f"  - {pid}: pages.json 中无 path 字段")
            continue
        fpath = PAGES_DIR / fpath_str
        if not fpath.exists():
            print(f"  - {pid}: 文件不存在，跳过")
            continue
        if dry_run:
            print(f"  ~ {pid}: pn_prefix={nnn!r}" +
                  (f", part_num={PART_MAP[pid][0]}" if pid in PART_MAP else ""))
        else:
            changed = update_frontmatter(fpath, pid, nnn)
            if changed:
                total_updated += 1
                print(f"  ✓ {pid}: pn_prefix={nnn!r}" +
                      (f", part_num={PART_MAP[pid][0]}" if pid in PART_MAP else ""))

    if dry_run:
        print(f"\n预览完成，{len(NNN_MAP)} 文件待更新" +
              (f"（含 {len(PART_MAP)} 个 part 映射）" if PART_MAP else ""))
        return 0

    # chapter_map.json
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    cmap = build_chapter_map()
    cmap_path = DATA_DIR / 'chapter_map.json'
    cmap_path.write_text(
        json.dumps(cmap, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )
    dst = WIKI_ROOT / 'docs/wiki/data/chapter_map.json'
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(cmap_path.read_text(encoding='utf-8'), encoding='utf-8')
    print(f"\nchapter_map.json 已写入 ({len(cmap)} 条目)")

    print(f"\n共更新 {total_updated}/{len(NNN_MAP)} 文件")
    return 0 if total_updated or True else 1


if __name__ == '__main__':
    sys.exit(main())
