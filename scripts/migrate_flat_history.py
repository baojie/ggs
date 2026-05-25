#!/usr/bin/env python3
"""
一次性迁移：将平铺 history/*.jsonl 合并至分桶 history/<bucket>/*.jsonl。

在修复 backfill_recent.py 的分桶 bug 后，已存在的平铺 history 文件需要合并至
对应的分桶路径。本脚本扫描 docs/wiki/history/ 下的所有 .jsonl 文件：
- 若文件在平铺根目录（如 history/中国.jsonl），尝试找分桶版本
  （如 history/zh/中国.jsonl）
- 若分桶版本存在：合并两文件，按 rev_id 去重，覆写分桶版本，删除平铺版
- 若分桶版本不存在：按 pages/ 分桶结构迁移到对应位置

用法:
    python3 scripts/migrate_flat_history.py          # 执行迁移
    python3 scripts/migrate_flat_history.py --dry-run  # 只预览，不写不删
    python3 scripts/migrate_flat_history.py --backup   # 迁移前先备份平铺文件
"""
from __future__ import annotations
import argparse, json, shutil
from pathlib import Path

WIKI_ROOT = Path(__file__).resolve().parent.parent
PUBLIC = WIKI_ROOT / "docs/wiki"
HIST = PUBLIC / "history"
PAGES = PUBLIC / "pages"


def find_page_file(slug: str, pages_root: Path) -> Path | None:
    flat = pages_root / f"{slug}.md"
    if flat.exists():
        return flat
    matches = list(pages_root.rglob(f"{slug}.md"))
    return matches[0] if matches else None


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return entries


def dedup_by_rev_id(entries: list[dict]) -> list[dict]:
    seen: set[str] = set()
    result = []
    for e in entries:
        rid = e.get("rev_id") or e.get("id")
        if rid and rid not in seen:
            seen.add(rid)
            result.append(e)
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="只预览，不写不删")
    ap.add_argument("--backup", action="store_true", help="迁移前备份平铺文件")
    args = ap.parse_args()

    if not HIST.exists():
        print("history 目录不存在。")
        return 0

    flat_files = sorted(HIST.glob("*.jsonl"))
    if not flat_files:
        print("没有平铺 history 文件需要迁移。")
        return 0

    print(f"发现 {len(flat_files)} 个平铺 history 文件：")
    for f in flat_files:
        slug = f.stem
        src = find_page_file(slug, PAGES)
        if src is None:
            print(f"  ⚠️  {f.name} → 找不到对应页面文件，跳过")
            continue

        rel = src.relative_to(PAGES)
        dest = HIST / rel.with_suffix(".jsonl")

        if dest == f:
            print(f"  ✅ {f.name} 已在正确位置")
            continue

        # 加载平铺文件内容
        flat_entries = load_jsonl(f)
        if not flat_entries:
            print(f"  ➡  {f.name} → {dest}（空文件，直接删除平铺版）")
            if not args.dry_run:
                f.unlink()
            continue

        # 加载已有分桶文件内容
        bucket_entries = load_jsonl(dest)
        merged = dedup_by_rev_id(bucket_entries + flat_entries)

        if args.dry_run:
            print(f"  ➡  {f.name} → {dest}  "
                  f"（{len(flat_entries)} 条 + {len(bucket_entries)} 条已有 "
                  f"= {len(merged)} 条）")
            continue

        # 备份
        if args.backup:
            backup_dir = HIST / ".flat-backup"
            backup_dir.mkdir(exist_ok=True)
            shutil.copy2(f, backup_dir / f.name)
            print(f"  💾 已备份到 {backup_dir / f.name}")

        # 写分桶
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(
            "\n".join(json.dumps(e, ensure_ascii=False) for e in merged) + "\n",
            encoding="utf-8")
        print(f"  ✓ {f.name} → {dest}（{len(merged)} 条记录）")

        # 删除平铺
        f.unlink()
        print(f"  ✗ 已删除平铺文件 {f.name}")

    print("\n迁移完成。")
    return 0


if __name__ == "__main__":
    exit(main())
