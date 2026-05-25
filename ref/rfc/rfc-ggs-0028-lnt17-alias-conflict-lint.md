# RFC-ggs-0028: 新增 LNT17 alias-conflict-lint 基因及配套脚本

- **Status**: proposed
- **Date**: 2026-05-26
- **Issue**: https://github.com/baojie/memex/issues/173
- **Source wiki**: ggs
- **Target**: skills/gene/LNT17-alias-conflict-lint.md, wiki/scripts/lint_alias_conflict.py

---

## Problem

当多个 wiki 页面声明了相同的 alias 时（例如 `病原体` 的 aliases 包含 `病菌`，而 `病菌` 本身也是独立页面），wikilink 解析器遇到 `[[病菌]]` 时会产生歧义，渲染结果不可预期。

随着 wiki 词条数量增长（ggs 已超过 200 页），alias 冲突数量快速增加，手工维护困难。在 ggs 的 GROW Phase 2 过程中，共检测到 51 处冲突。

## Root cause

缺乏系统性的 alias 冲突检测机制。页面创建时（NEW1 基因）和批量修改时没有检查 alias 唯一性，导致冲突在多轮新建后积累。

## Proposed change

### Gene: `skills/gene/LNT17-alias-conflict-lint.md`

```markdown
---
id: LNT17-alias-conflict-lint
group: LNT
wu: 5
diff_limit: 只读（--fix 模式：每次修复一批页面）
sources: []
applicable: true
scope: general
tags: [lint, fix, alias, frontmatter]
born: 2026-05-26
---

# LNT17 alias-conflict-lint — alias 冲突检测与修复

**定义**：扫描所有 wiki 页面的 frontmatter，检测跨页面的 alias 冲突。

**冲突定义**：alias A 被多个页面同时声明（含 slug、label、id、aliases 四个来源）。

**修复规则**：
- Auto-fix：若 alias A 等于某页面的 slug，则该页面"拥有"A；其他页面的 aliases 列表中移除 A。
- Report：若无页面 slug 等于 A，输出警告，需人工决策后手动修复。

对应脚本：`wiki/scripts/lint_alias_conflict.py`

## 触发时机

| 时机 | 条件 |
|------|------|
| GROW Phase 2 每 10 轮 | 与 EVV5 同批触发 |
| NEW1 执行后 | 新建页面数 ≥ 5 时触发 |
| 手动 | `python3 wiki/scripts/lint_alias_conflict.py [--fix]` |

## 执行命令

```bash
# 检查（只读）
python3 wiki/scripts/lint_alias_conflict.py

# 自动修复
python3 wiki/scripts/lint_alias_conflict.py --fix
```

## 输出格式

```
冲突 alias 总数：N
可自动修复：M 处，涉及 K 个页面
需人工决策：P 项

[需人工决策]
  'alias' → [slug_a, slug_b]

[自动修复计划]
  slug: 移除 aliases ['alias']

✓ 已修复 K 个页面。
```
```

### Script: `wiki/scripts/lint_alias_conflict.py`

脚本已在 ggs 本地创建并验证（修复了 51 处冲突至 0）。内容见 ggs/wiki/scripts/lint_alias_conflict.py。
```
