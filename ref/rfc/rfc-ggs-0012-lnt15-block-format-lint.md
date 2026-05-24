# RFC-ggs-0012: LNT15-block-format-lint 基因创建

- **Status**: implemented
- **Date**: 2026-05-24
- **Issue**: https://github.com/baojie/memex/issues/144
- **Source wiki**: ggs
- **Target**: `$MEMEX_ROOT/skills/gene/LNT15-block-format-lint.md` + ggs BIRTH.md

---

## Problem

当前 `:::` fenced div 块（`::: table`、`::: image` 等）的格式检查分散在多个基因中，且覆盖不全：

- FIX24 B1 只检查 `:::` 后缺空格，且定位为 PN 上下文
- 没有统一的 lint 检查 `:::` 开启前/闭合后的空行上下文
- 没有检查 TYPE 后多余空格（`::: table  `）
- 没有检查行末尾随空格

最近在 ggs 的 Phase 5 验收中多次手动发现 `::: table` 块后缺空行导致渲染异常，这类问题应由自动化 lint 捕获。

## Proposed change

### 1. 创建共享基因 `LNT15-block-format-lint`

在 `$MEMEX_ROOT/skills/gene/LNT15-block-format-lint.md` 创建基因，定义以下 6 项检查：

| # | 检查 | 正则 | 自动修复 |
|---|------|------|---------|
| 1 | 开启行前缺空行 | `[^\n]\n::: ` 且前一行非 `:::` | ✅ |
| 2 | 闭合行后缺空行 | `:::\n[^\n]` 且后一行非 `:::` | ✅ |
| 3 | `:::` 后缺空格 | `^:::[a-zA-Z]` | ✅ |
| 4 | `:::` 后多余空格 | `^:::  `（两个以上空格） | ✅ |
| 5 | TYPE 后多余空格 | `::: table `（TYPE 后多于一个空格） | ✅ |
| 6 | 行末尾随空格 | `[^\s]\s+$` | ✅ |

### 2. 在 ggs BIRTH.md Phase 5-E 后增加 5-E2 小节

在现有 Phase 5-E（验证与提交）和 5-F（PN 检索源构建）之间插入 **5-E2 LNT15 区块格式检查**，执行 LNT15 全库扫描并修复后方可进入提交。

### 3. 创建配套检测脚本（可选）

可创建 `wiki/scripts/lint_block_format.py` 作为脚本实现。也可先用 grep/sed 实现轻量版本。

## Implementation

- **Commit**: a45ae22 (memex)
- **Date**: 2026-05-24

落地清单：
1. `skills/gene/LNT15-block-format-lint.md` — 基因定义
2. `wiki/scripts/lint_block_format.py` — 扫描/修复脚本
3. ggs BIRTH.md 5-E2 — Phase 5 流程中增加 LNT15 区块格式检查步骤

**ADM3 Review**: faithful — 全部 proposed change 已按预期落地。
