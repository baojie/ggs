# RFC-ggs-0026: `/grow phase N` / `/boot phase N` 跳过了 `/comply N` 前置质检

- **Status**: accepted
- **Date**: 2026-05-25
- **Source wiki**: ggs
- **Issue**: https://github.com/baojie/memex/issues/204

---

## Problem

`/grow phase 3` 直接执行了 Phase 3 内容，跳过了两个前置步骤：

1. **实例化缺失**：`GROW.spec.md` 的 Phase 3 节未被实例化到 `GROW.md`（"做一步写一步"原则要求 Phase 启动前先复制模板、填写参数）
2. **`/comply` 质检缺失**：`/grow phase N` 执行前应先经过 `/comply grow N` 质检（对照 spec 检查实例化内容完整、占位符替换、参数正确），质检合格后方可执行

后果：GROW.md 中 Phase 3 节完全不存在，用户查看时"连 Phase 3 都没有"。

## Root cause

`/grow phase N` 和 `/boot phase N` 的执行入口没有强制前置条件检查：

- 没有检查 Phase N 是否已在本地文件中实例化
- 没有检查 `/comply phase N` 是否已完成且质检合格
- `/comply` 被设计为可选的手动检查步骤，而非嵌入执行流程的强制门控

Phase 2 之所以有实例化记录，是因为显式执行了 `/grow init phase2`（含 Step 2 实例化），但 `/grow init phase3` 从未执行。`/grow phase 3` 直接从 spec 读取步骤执行，绕过了实例化和质检。

## Proposed change

### A. 修复存量（立即执行）

将 `GROW.spec.md §Phase 3` 实例化到 GROW.md，填入实际执行数据，标记所有检查项 [x]。

### B. 修复流程（强制门控）

`/boot phase N` 和 `/grow phase N` 的执行入口必须增加两道门控检查，任一不通过则报错中止：

**门控 1 — 实例化检查**：
```
检查本地 BIRTH.md / GROW.md 中是否存在 `^## Phase N` 节
缺失 → 报错并提示：请先执行 `/boot init phaseN` 或 `/grow init phaseN`
```

**门控 2 — `/comply` 质检检查**：
```
检查是否存在 `/comply boot N` 或 `/comply grow N` 的质检通过记录
（例如在 phase 文件中标记 `comply: pass`，或独立的质检日志文件）
未通过 → 报错并提示：请先执行 `/comply boot N` 或 `/comply grow N`
```

### C. 适用性

此规则适用于所有 Phase（boot 和 grow 两侧），以及所有 N（0/1/2/3/4...）。

## Implementation

**Review**: faithful
**Date**: 2026-05-25

## Implementation

**Review**: faithful
**Date**: 2026-05-27

**调整说明**：
- `init phaseN` 入口不加门控（其职责是创建实例，实例化前无法通过实例化检查，质检在 init 之后执行）
- GROW.spec.md 流程图未更新（spec 文件在 `$MEMEX_ROOT` 只读目录中，不直接修改）

**检查清单**：

- [x] 在 `/grow` skill 的 `phase N` 入口加入门控 1（实例化检查）+ 门控 2（comply 质检检查）
- [x] 在 `/boot` skill 的 `phase N` 入口（`phaseN` 模式）加入同样的双门控
- [x] 定义 comply 质检通过的记录方式：Phase 节中标注 `> **comply**: pass`
- [ ] ~~更新 GROW.spec.md 和 boot spec 的执行流程图~~（$MEMEX_ROOT 只读，跳过）

**Commits**:
- 0481795: feat(gates): GROW/Boot phaseN 入口加入实例化+comply 质检双门控
