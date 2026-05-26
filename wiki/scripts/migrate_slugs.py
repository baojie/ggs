#!/usr/bin/env python3
"""
migrate_slugs.py — 将所有拼音/英文 slug 批量迁移为中文 slug

用法:
  python3 wiki/scripts/migrate_slugs.py --dry-run
  python3 wiki/scripts/migrate_slugs.py --execute
"""
import json, re, os, sys, shutil, argparse
from pathlib import Path

sys.path.insert(0, str(Path.home() / 'memex/wiki/scripts'))
from page_bucket import page_bucket

WIKI_ROOT = Path('docs/wiki')
PAGES_DIR = WIKI_ROOT / 'pages'
HISTORY_DIR = WIKI_ROOT / 'history'
PAGES_JSON = WIKI_ROOT / 'pages.json'
PAGES_LITE = WIKI_ROOT / 'pages.lite.json'

SYSTEM_SLUGS = {'About', 'Epilogue', 'Frontispiece', 'Preface'}
CHAPTER_PAT = re.compile(r'^ch\d+')

MANUAL_FIX = {
    'huo-pu-wei-er-wen-hua': '霍普韦尔文化',
    'ku-chao-cai': '苦巢菜',
    'zou-chu-fei-zhou': '走出非洲',
}


def is_latin(slug):
    return all(ord(c) < 128 for c in slug) and slug not in SYSTEM_SLUGS and not CHAPTER_PAT.match(slug)


def label_to_slug(label):
    clean = re.sub(r'[（(][^）)]{0,10}[）)]$', '', label).strip()
    return clean if clean else label


def find_page_file(slug):
    bucket = page_bucket(slug)
    candidate = PAGES_DIR / bucket / f"{slug}.md"
    if candidate.exists():
        return candidate
    for f in PAGES_DIR.rglob(f"{slug}.md"):
        return f
    return None


def find_history_file(slug):
    bucket = page_bucket(slug)
    candidate = HISTORY_DIR / bucket / f"{slug}.jsonl"
    if candidate.exists():
        return candidate
    for f in HISTORY_DIR.rglob(f"{slug}.jsonl"):
        return f
    return None


def update_frontmatter_id(content, old_id, new_id):
    return re.sub(
        rf'^(id:\s*){re.escape(old_id)}(\s*)$',
        rf'\g<1>{new_id}\2',
        content, count=1, flags=re.MULTILINE
    )


def update_wikilinks(content, old_slug, new_slug):
    return re.sub(
        rf'\[\[{re.escape(old_slug)}(\|[^\]]+)?\]\]',
        lambda m: f'[[{new_slug}{m.group(1) or ""}]]',
        content
    )


def write_text(path, content):
    with open(str(path), 'w', encoding='utf-8') as f:
        f.write(content)


def read_text(path):
    with open(str(path), encoding='utf-8') as f:
        return f.read()


def build_mapping(pages):
    mapping = {}
    skipped = []

    for slug, info in pages.items():
        if not is_latin(slug):
            continue

        if slug in MANUAL_FIX:
            new_slug = MANUAL_FIX[slug]
        else:
            label = info.get('label', slug)
            new_slug = label_to_slug(label)
            if all(ord(c) < 128 for c in new_slug):
                skipped.append((slug, label, 'label is ASCII'))
                continue

        if slug != 'xinyuewodi' and new_slug in pages and new_slug not in {v for k, v in MANUAL_FIX.items()}:
            # Only skip if there's already a Chinese page with this slug AND it's not in our mapping
            pass

        if slug == 'xinyuewodi' and new_slug in pages:
            skipped.append((slug, new_slug, 'conflicts with existing Chinese slug — handle separately'))
            continue

        mapping[slug] = new_slug

    return mapping, skipped


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()

    if not args.dry_run and not args.execute:
        print("须指定 --dry-run 或 --execute")
        sys.exit(1)

    dry = args.dry_run

    data = json.load(open(str(PAGES_JSON)))
    pages = data['pages']

    mapping, skipped = build_mapping(pages)
    print(f"待迁移: {len(mapping)} 个")
    print(f"跳过: {len(skipped)} 个")
    for s in skipped:
        print(f"  SKIP {s[0]!r} → {s[1]!r} ({s[2]})")
    print()

    if dry:
        print("=== DRY-RUN 映射预览（前 30 个）===")
        for old, new in sorted(mapping.items())[:30]:
            old_q = pages[old].get('quality', '?')
            old_file = find_page_file(old)
            new_bucket = page_bucket(new)
            missing = ' FILE_MISSING' if not old_file else ''
            print(f"  {old!r:42} → {new!r:25} [bucket:{new_bucket}]{missing}")

        new_slugs = list(mapping.values())
        seen, dups = set(), []
        for n in new_slugs:
            if n in seen:
                dups.append(n)
            seen.add(n)
        if dups:
            print(f"\n⚠ 目标中文 slug 重复 ({len(dups)}):")
            for d in dups:
                print(f"  {d}")
        else:
            print(f"\n✓ 无目标 slug 重复")

        all_pages = list(PAGES_DIR.rglob('*.md'))
        old_slugs_set = set(mapping.keys())
        wl_files = sum(
            1 for f in all_pages
            if any(f'[[{o}' in read_text(f) for o in old_slugs_set)
        )
        print(f"\n将扫描 {len(all_pages)} 个页面文件")
        print(f"含待更新 wikilink 的文件: {wl_files} 个")
        return

    # === EXECUTE MODE ===
    print("=== 开始迁移 ===")

    data_lite_raw = read_text(PAGES_LITE)
    data_lite = json.loads(data_lite_raw)
    if isinstance(data_lite, dict) and 'pages' in data_lite:
        pages_lite = data_lite['pages']
        lite_wrapped = True
    else:
        pages_lite = data_lite
        lite_wrapped = False

    for i, (old_slug, new_slug) in enumerate(sorted(mapping.items()), 1):
        info = pages[old_slug].copy()

        # Rename page file
        old_file = find_page_file(old_slug)
        new_bucket = page_bucket(new_slug)
        new_dir = PAGES_DIR / new_bucket
        new_file = new_dir / f"{new_slug}.md"

        if old_file and old_file.exists():
            content = read_text(old_file)
            content = update_frontmatter_id(content, old_slug, new_slug)
            new_dir.mkdir(parents=True, exist_ok=True)
            write_text(new_file, content)
            if new_file != old_file:
                old_file.unlink()
                try:
                    old_file.parent.rmdir()
                except OSError:
                    pass
        else:
            print(f"  ⚠ FILE NOT FOUND: {old_slug}")

        # Rename history file
        old_hist = find_history_file(old_slug)
        new_hist_dir = HISTORY_DIR / new_bucket
        new_hist = new_hist_dir / f"{new_slug}.jsonl"

        if old_hist and old_hist.exists():
            new_hist_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(old_hist), str(new_hist))
            try:
                old_hist.parent.rmdir()
            except OSError:
                pass

        # Update pages dict
        info['id'] = new_slug
        pages[new_slug] = info
        del pages[old_slug]

        if old_slug in pages_lite:
            lite_info = pages_lite[old_slug].copy()
            lite_info['id'] = new_slug
            pages_lite[new_slug] = lite_info
            del pages_lite[old_slug]

        if i % 50 == 0:
            print(f"  ... {i}/{len(mapping)}")

    # Write pages.json
    data['pages'] = pages
    write_text(PAGES_JSON, json.dumps(data, ensure_ascii=False, indent=2))

    if lite_wrapped:
        data_lite['pages'] = pages_lite
        write_text(PAGES_LITE, json.dumps(data_lite, ensure_ascii=False, indent=2))
    else:
        write_text(PAGES_LITE, json.dumps(pages_lite, ensure_ascii=False, indent=2))

    print(f"✓ pages.json / pages.lite.json 更新完毕")

    # Update wikilinks across all page files
    all_page_files = list(PAGES_DIR.rglob('*.md'))
    wikilink_files_updated = 0

    for f in all_page_files:
        content = read_text(f)
        new_content = content
        for old_slug, new_slug in mapping.items():
            if f'[[{old_slug}' in new_content:
                new_content = update_wikilinks(new_content, old_slug, new_slug)
        if new_content != content:
            write_text(f, new_content)
            wikilink_files_updated += 1

    print(f"✓ wikilink 更新: {wikilink_files_updated} 个文件")
    print(f"✓ 迁移完成: {len(mapping)} 个 slug")
    print()
    print("跳过（需手动处理）:")
    for s in skipped:
        print(f"  {s[0]!r}: {s[2]}")


if __name__ == '__main__':
    main()
