# RFC-ggs-0025: GROW.spec.md Phase 0-E backlinks 路径过时

- **Status**: proposed
- **Date**: 2026-05-25
- **Issue**: https://github.com/baojie/memex/issues/161
- **Source wiki**: ggs
- **Target**: $MEMEX_ROOT/GROW.spec.md

---

## Problem

`GROW.spec.md` Phase 0-E（链接网络密度评估）的示例代码块中，`backlinks.json` 路径使用了已弃用的旧路径：

```python
d = json.load(open('wiki/public/backlinks.json'))
```

实际项目中 `backlinks.json` 已迁移至 `docs/wiki/backlinks.json`（由 RFC-ggs-0008 系列路径迁移确立）。使用旧路径会导致 `FileNotFoundError`，掩盖真实的文件存在情况。

在 ggs wiki `/grow init 0` 实例化时，该代码块被逐字复制进 `GROW.md`，通过 `/comply` 检查后发现并在本地修正，但 spec 上游未同步。

## Root cause

`GROW.spec.md` 中的代码示例编写时使用了 `wiki/public/` 前缀，该前缀在路径迁移后未在 spec 中同步更新。

## Proposed change

将 `GROW.spec.md` Phase 0-E 中的代码块路径修改为：

```python
d = json.load(open('docs/wiki/backlinks.json'))
```

同时建议排查 `GROW.spec.md` 其他节中是否还有 `wiki/public/` 路径残留，一并修正。
