# RFC-ggs-0009: 新增通用 gene CHKP1 — PN 完整性结构验收

- **Status**: implemented
- **Date**: 2026-05-24
- **Issue**: https://github.com/baojie/memex/issues/137
- **Source wiki**: ggs
- **Target**: `$MEMEX_ROOT/skills/gene/CHKP1-pn-completeness-verify.md`（新增）及配套脚本示例

---

## Problem

当前 memex gene 库中，与 PN 相关的验收工具分散且存在覆盖缺口：

- **PRE7**（chapter-pn-assign）：负责赋号，不负责验收
- **QUO10**（cross-chapter-pn-verify）：检查 PN 引文与原文语义是否一致，依赖 `pn-source.json`，需在 Phase 5-F 完成后才能运行
- **FIX10**（pn-format-repair）：格式修复工具，不是检查报告工具
- **MEA2/MEA3**：覆盖率统计与缺口优先级，不是完整性验收

**缺失的环节**：在 Phase 5-C（全量赋号）完成、Phase 5-F（pn-source 构建）之前，缺少一个专门的"结构层完整性验收"工具，无法系统性地确认：

1. PN 锚点语法是否正确（`[NNN-PPP]` 格式、NNN 与 pn_prefix 一致）
2. 编号是否连续（无跳号、无重号、起始 001）
3. `:::image` / `:::table` 等特殊块是否正确赋号
4. 不该赋号的元素（标题、脚注、blockquote、`:::` 闭合标签）是否被误赋
5. 诗歌/多行引文块是否被逐行赋号（应整块视为一个单元）

ggs 在 Phase 5-E post-PN lint 环节发现上述缺口，在本地临时实现了 `CHKP1`，建议将其提升为 memex 通用 gene。

## Root cause

PRE7 的职责是"赋号"，验收不在其范围内。QUO10 的职责是"语义核验"，时序在 5-F 之后。两者之间恰好存在一个验收空白：**赋号完成但 pn-source 尚未构建时，无法做结构层完整性检查**。

## Proposed change

在 memex gene 库中新增 `CHKP1-pn-completeness-verify.md`，定义以下 16 项结构层检查：

| 编号 | 分类 | 检查内容 | 严重度 |
|------|------|---------|--------|
| A1 | 语法 | `[NNN-PPP]` 锚点格式合规，NNN 与 pn_prefix 一致 | ERROR |
| A2 | 语法 | 所有 `:::TYPE pn=NNN-PPP` 属性格式合规 | ERROR |
| A4 | 语法 | 无半角括号 PN `(NNN-PPP)` | ERROR |
| A5 | 语法 | PN 锚点后无多余空格 | WARN |
| A6 | 语法 | `:::` 与块类型名之间必须有空格（`::: image` ✓，`:::image` ✗）| ERROR |
| B1 | 连续性 | 各章 PPP 从 001 起严格递增，无跳号 | ERROR |
| B2 | 连续性 | 无重号 | ERROR |
| B3 | 连续性 | 每章至少有 1 个 PN | WARN |
| C1 | 特殊块 | 所有 `:::TYPE` 语义块开启行必须有 `pn=NNN-PPP` 属性（统一属性文法） | ERROR |
| D1 | 不当赋号 | 标题行不得有 PN 锚点 | ERROR |
| D3 | 不当赋号 | 脚注定义行不得有 PN 锚点 | ERROR |
| D4 | 不当赋号 | `:::` 闭合行（单独一行）不得有 `[NNN-PPP]` 锚点（与开启行的 `pn=` 属性不同） | ERROR |
| D5 | 不当赋号 | blockquote 行不得有 PN 锚点 | ERROR |
| E1 | 引文完整性 | 连续 blockquote 块（≥4行）前导语段落已赋 PN | WARN |
| F1/F2 | 覆盖 | chapter-order.md 所有章节均存在且 NNN 一致 | ERROR |

**执行时机**：Phase 5-C（全量赋号）完成后、Phase 5-F（pn-source 构建）之前，即 BIRTH.spec.md §5-E post-PN lint 环节。

**参考实现**：ggs 本地 `wiki/scripts/verify_pn_completeness.py`（约 200 行 Python），可作为各 wiki 本地实现的模板，gene 文档中附代码示例。

**BIRTH.spec.md 联动**：建议在 `§5-E post-PN lint Step 1` 中增加对 CHKP1 的引用：
```
python3 wiki/scripts/verify_pn_completeness.py  # CHKP1
```

## Notes

- ggs 本地实现已通过 Phase 5 全量（23 章、1489 PN）验收，结果 ERROR:0 WARN:0
- gene 编号建议使用 `CHKP1`，与现有 CHK 系列（CHK4/CHK5/CHK6/CHK9/CHK13）同组
- E1（诗/引文块完整性）的检测逻辑视各 wiki 的 blockquote 赋号规则而定；ggs 规则为整块跳过，其他 wiki 如有不同规则可在本地 BIRTH.md 覆盖

## Evaluation Note

**决策**: accept-modified

CHKP1 的 16 项检查已被拆分为两个 memex 通用基因：
- **FIX24-pn-structure-verify**（定义格式 + 不当赋号检查）：覆盖 A1-A6、B1-B2、C1、D1-D5、E1
- **FIX26-pn-index-repair**（索引与父子关系完整性）：覆盖 F1/F2，并扩展了父子 PN 关系检查

**变更说明**：
1. 编号从 `CHKP1` → `FIX24`/`FIX26`，因 FIX 前缀更符合"结构层验收"的语义（CHK 用于页面质量检查）
2. 范围从 16 项扩展至 25+ 项（增加了父子关系 A1-A3、映射完整性 B1-B3、pn_prefix 一致性 C1-C3）
3. 执行时机调整为 Step 2（FIX24）和 Step 3（FIX26），而不是原先的 Step 1

**ADM2 实施**：已创建 `FIX24-pn-structure-verify.md`、`FIX26-pn-index-repair.md`，重写 `workflow-post-pn-lint.md`，更新 `BIRTH.spec.md §5-C-2, §5-E`。

## Implementation

**Review**: faithful
**Date**: 2026-05-24
**Commits**:
- baojie/memex@8ec96585fa50edff2ed52eb1cfd3f161d97981ab: implement RFC-ggs-0009 — 拆分 CHKP1 为 FIX24 + FIX26
- baojie/memex@fdff86bb9c55ddd7a21c9e1728ae5194ac5d36e0: feat — Phase 5-E 全量 PN 验收工作流
- baojie/memex@93aa3ef4068a1293a46a6cbe3525fae10432cd2f: docs — PN 赋予阶段错误回顾报告
- baojie/memex@2315fa80a0a1d2f5e3cb5664b95406ac2aa553a6: docs(rfc) — RFC-ggs-0009 处理日志
- baojie/ggs@b337984: docs(rfc) — RFC-ggs-0009 ADM1 评审
