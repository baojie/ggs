# RFC-ggs-0032: pn_verify.py 使用未定义变量 ROOT 导致 --fix 模式崩溃

- **Status**: proposed
- **Date**: 2026-05-26
- **Issue**: https://github.com/baojie/memex/issues/186
- **Source wiki**: ggs
- **Target**: `wiki/scripts/butler/pn_verify.py`

---

## Problem

`pn_verify.py` 第 265 行调用 `subprocess.run(..., cwd=ROOT)`，但 `ROOT` 在该文件中从未定义（正确的变量名是 `WIKI_ROOT`，已在第 33 行定义）。这导致脚本的 `--fix` 模式在尝试执行任何修复操作时都会抛出 `NameError: name 'ROOT' is not defined`，使得 PN 偏移自动修复功能完全不可用。

## Root cause

文件全局变量区域只定义了 `WIKI_ROOT`、`_SCRIPTS_DIR`、`PAGES_DIR`、`EDIT_PAGE`、`RECORD_REV`，没有定义 `ROOT`。第 265 行误用了不存在的变量名。

## Proposed change

将第 265 行的 `cwd=ROOT` 改为 `cwd=WIKI_ROOT`。

```diff
-            cwd=ROOT,
+            cwd=WIKI_ROOT,
```

这是一个单行机械性修复，不涉及逻辑变更。

## 连带发现

同次审计中还发现 `record_revision.py`（第 215、226 行）和 `backfill_recent.py`（第 240 行）存在类似的 KeyError `'dl'` bug——v0 格式的历史条目没有 `"dl"` 键，而代码直接使用 `entries[j]["dl"]`。这两项已在 ggs wiki 本地修复（改用 `.get("dl", [])`），建议合并入 memex 主库以避免下游 revivor 工具受影响。
