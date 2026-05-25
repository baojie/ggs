#!/usr/bin/env python3
"""
LNT17 alias-conflict-lint — 检测并修复 wiki 页面间的 alias 冲突。

修复规则：
  Auto-fix: 若 alias A 与另一页面的 slug 相同，则从"非拥有者"页面的 aliases 中移除 A。
  Report:   若冲突双方均非 A 的拥有者，输出警告，需人工决策。

用法:
    python3 wiki/scripts/lint_alias_conflict.py [--public docs/wiki] [--fix] [--dry-run]
"""
from __future__ import annotations
import argparse, re, sys
from pathlib import Path


def get_wiki_root() -> Path:
    p = Path.cwd()
    while p != p.parent:
        if (p / "BIRTH.md").exists():
            return p
        p = p.parent
    return Path.cwd()


def parse_frontmatter(text: str) -> dict:
    fm: dict = {"aliases": []}
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return fm
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if line.startswith("aliases:"):
            m = re.search(r'\[(.+)\]', line)
            if m:
                fm["aliases"] = [a.strip().strip('"\'') for a in m.group(1).split(",") if a.strip()]
        elif ": " in line:
            k, v = line.split(": ", 1)
            fm[k.strip()] = v.strip()
    return fm


def set_aliases(text: str, new_aliases: list[str]) -> str:
    if new_aliases:
        new_line = f'aliases: [{", ".join(new_aliases)}]'
    else:
        new_line = "aliases: []"
    return re.sub(r"^aliases:.*$", new_line, text, flags=re.MULTILINE)


def main() -> int:
    ap = argparse.ArgumentParser(description="LNT17: alias conflict lint & fix")
    ap.add_argument("--public", default=None, help="public 目录，默认 docs/wiki")
    ap.add_argument("--fix", action="store_true", help="执行自动修复")
    ap.add_argument("--dry-run", action="store_true", help="仅打印修复计划，不写文件")
    args = ap.parse_args()

    wiki_root = get_wiki_root()
    pages_dir = (wiki_root / args.public / "pages") if args.public else (wiki_root / "docs" / "wiki" / "pages")

    # Load all pages
    pages: dict[str, dict] = {}
    for f in sorted(pages_dir.rglob("*.md")):
        slug = f.stem
        text = f.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        pages[slug] = {"fm": fm, "path": f, "text": text}

    # Build alias → claimants map
    alias_claimants: dict[str, list[str]] = {}

    for slug, info in pages.items():
        fm = info["fm"]
        alias_claimants.setdefault(slug, []).append(slug)
        label = fm.get("label", "")
        if label:
            alias_claimants.setdefault(label, []).append(slug)
        fid = fm.get("id", "")
        if fid and fid != slug:
            alias_claimants.setdefault(fid, []).append(slug)
        for a in fm.get("aliases", []):
            if a:
                alias_claimants.setdefault(a, []).append(slug)

    # Find conflicts
    conflicts = {a: list(dict.fromkeys(slugs))
                 for a, slugs in alias_claimants.items()
                 if len(set(slugs)) > 1}

    auto_fixes: dict[str, list[str]] = {}
    manual_needed: list[tuple] = []

    for alias, claimants in sorted(conflicts.items()):
        # Owner = the page whose slug == alias
        owners = [s for s in claimants if s == alias]
        if not owners:
            for s in claimants:
                fm = pages[s]["fm"]
                if fm.get("id") == alias or fm.get("label") == alias:
                    owners.append(s)
        if owners:
            for s in claimants:
                if s not in owners and alias in pages[s]["fm"].get("aliases", []):
                    auto_fixes.setdefault(s, []).append(alias)
        else:
            manual_needed.append((alias, claimants))

    # Report
    total_auto = sum(len(v) for v in auto_fixes.values())
    print(f"冲突 alias 总数：{len(conflicts)}")
    print(f"可自动修复：{total_auto} 处，涉及 {len(auto_fixes)} 个页面")
    print(f"需人工决策：{len(manual_needed)} 项")

    if manual_needed:
        print("\n[需人工决策]")
        for alias, claimants in manual_needed:
            print(f"  '{alias}' → {claimants}")

    if auto_fixes:
        print("\n[自动修复计划]")
        for slug, aliases in sorted(auto_fixes.items()):
            print(f"  {slug}: 移除 aliases {aliases}")

    if not args.fix and not args.dry_run:
        print("\n使用 --fix 执行修复，--dry-run 查看计划。")
        return 0

    # Apply fixes
    fixed = 0
    for slug, to_remove in sorted(auto_fixes.items()):
        info = pages[slug]
        fm = info["fm"]
        new_aliases = [a for a in fm.get("aliases", []) if a not in to_remove]
        if args.dry_run:
            print(f"  [dry-run] {slug}: {fm['aliases']} → {new_aliases}")
        else:
            new_text = set_aliases(info["text"], new_aliases)
            with open(info["path"], "w", encoding="utf-8") as fh:
                fh.write(new_text)
            print(f"  ✓ {slug}: 移除 {to_remove}")
            fixed += 1

    if not args.dry_run:
        print(f"\n✓ 已修复 {fixed} 个页面。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
