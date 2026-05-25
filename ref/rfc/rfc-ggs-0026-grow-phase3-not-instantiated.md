# RFC-ggs-0026: `/grow` 执行未实例化 Phase 节到 GROW.md

- **Status**: proposed
- **Date**: 2026-05-25
- **Source wiki**: ggs

---

## Problem

GROW.md 遵循"做一步写一步"原则（3 行）：未执行的 Phase 待启动时从 `GROW.spec.md` 复制模板，填写实际参数后写入 GROW.md。

Phase 3（R89–R93，共 5 轮 enrich 26 页）已完整执行并 commit，但 Phase 3 节从未从 `GROW.spec.md` 实例化到 GROW.md 中。当前 GROW.md 以 Phase 2 的结尾 `---` 行截断，Phase 3 内容完全缺失。

用户通过 `/open grow` 查看 GROW.md 时，看不到任何 Phase 3 执行记录，造成"连 Phase 3 都没有"的观感。

## Root cause

`/grow` skill 的 Phase 3 执行流程直接从 `$MEMEX_ROOT/GROW.spec.md` 读取步骤内容执行，跳过了「将 Phase N 节写入 GROW.md」的步骤。具体来说，标准 init/执行流程（`init phaseN`）包含 Step 2 实例化，但"自动继续"模式下的 Phase 3 执行未走 init 初始化流程，直接进入了执行循环。

Phase 2 之所以有记录，是因为 `init phase2` 在 Phase 2 开始时执行过一次实例化。Phase 3 由 `grow phase 3` 参数直接启动，未走 `init phase3`，因此没有触发实例化。

## Proposed change

### A. 修复存量（立即执行）

将 `GROW.spec.md §Phase 3`（1468–2445）的内容实例化到 GROW.md，填入实际执行数据（R89–R93、26 页、featured+ 67.0%），标记所有检查项 [x]，写入 `local/memory/grow_phase3_summary.md` 作为总结文件。

### B. 修复流程（防止复发）

在 `/grow` skill 的 Phase 执行逻辑中，加入以下步骤：

1. **Phase 启动前核验**：检查 GROW.md 中是否已包含目标 Phase 的对应节（以 `^## Phase N：` 标题为准）
2. **缺失则实例化**：从 `GROW.spec.md` 复制对应 Phase 内容，填写当前已知参数，写入 GROW.md，commit 后再进入执行循环
3. **强制校验**：若 GROW.md 中不存在当前 Phase 节，pre-flight 检查报错阻止执行，提示用户先执行 `/grow init phaseN`

### C. 适用性检查

此规则同样适用于 Phase 4 及后续阶段——任何 Phase 首次启动前必须确认 GROW.md 中已有实例化内容。

## Implementation

**Review**: faithful
**Date**: 2026-05-25

**检查清单**：

- [ ] 将上述修复写入 `/grow` skill 的 Phase 启动逻辑
- [ ] 在 `pre-flight check` 中加入 GROW.md 节存在性检查
- [ ] 文档化：在 GROW.spec.md 的 Phase 3/4 入口处加入`⚠️ 启动前确认 GROW.md 中已实例化本节`
