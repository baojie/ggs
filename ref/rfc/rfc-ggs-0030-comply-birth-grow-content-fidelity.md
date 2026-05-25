# RFC-ggs-0030: `/comply` 对 BIRTH/GROW 的 Phase 检查仅比较标题，未验证内容实例化 fidelity

- **Status**: implemented
- **Date**: 2026-05-26
- **Issue**: https://github.com/baojie/memex/issues/178
- **Source wiki**: ggs
- **Target**: `/home/baojie/.claude/skills/comply/SKILL.md`

---

## Problem

Phase 3 的 GROW.md 实例化事故暴露了 `/comply` 对 BIRTH/GROW 这类 spec-instance 文件的检查深度不足。

**事故经过**：`/comply grow 3` 执行时，`init phaseN` Step 3a 的标题树比较通过——Phase 3 的 `3.0`、`3.1-0`、`3.1-B`、`3.1-X`、`3.1-Z` 等各级标题确实存在于 GROW.md 中。但实际内容是**高度简化的摘要**（约 120 行），而非 spec 模板（约 980 行）的完整实例化：
  - 缺少 3.0-E 追踪节标准格式
  - 缺少 3.1-0-A/B/C 的完整配置代码块
  - 缺少 3.1-A 类型扩张顺序表
  - 缺少 3.1-B-pre pre-flight 六步检查
  - 缺少 3.1-C EXIT-GATE 的五门结构（G1–G5 含检测脚本）
  - 缺少 3.1-E/F/G（标注 N/A 并附原因）
  - 3.1-Z 缺少复盘五层分析和验收标准

**标题存在 ≠ 内容完成**。这个问题不仅限于 GROW——BIRTH.md 同样存在 spec→instance 的实例化链条，同样的标题树检查也会漏掉内容缺失。

**具体风险**：

| 场景 | 后果 |
|------|------|
| `/comply birth N` 通过但 BIRTH.md 该 Phase 内容缺失 | 用户以为 Phase 已完成实例化，实际未准备好 |
| `/grow init phaseN` Step 3a 通过但实例化不完整 | 后续 `/grow phase N` 在残缺的 GROW.md 上执行，质量不可控 |
| `init phaseN` 补全 Phase 0..N-1 时只补标题不补内容 | 历史 Phase 失去追踪价值 |

## Root cause

1. **标题树校验（Step 3a）设计范围过窄**：只比较 `^#{2,4}\s+.+$` 的标题文本，不检查标题以下的内容体。这是一种"语法检查"，而非"语义检查"。
2. **`/comply` skill 没有针对 spec-instance 文件的专门检查层**：当前 comply 对非 wiki 文件只做 CHK5（T/L/V 语义检查），没有 Phase Content Fidelity（PCF）检查。BIRTH.md 和 GROW.md 属于 spec-instance 模式（`xxx.spec.md` 是模板，`xxx.md` 是实例），需要专用的 fidelity 检查。
3. **`/comply grow N` 未绑定 spec 对比**：当参数包含 Phase N 时，comply 应该自动找到对应的 spec 文件，做 A/B 对比，而不是只分析目标文件自身。

## Proposed change

### A. 在 comply skill 中新增 PCF（Phase Content Fidelity）检查层

当 `comply` 的目标文件是 `BIRTH.md` 或 `GROW.md` 且参数包含 Phase N 时（如 `/comply GROW.md phase 3`），新增以下检查项目：

#### PCF1 — 代码块完整性

```
从 spec 的 Phase N 节提取所有 ``` 代码块的数量和类型（python/bash/json/...）
从实例的 Phase N 节提取同样的统计

差异报告：
  - spec 有 N 个代码块，实例有 M 个 → M/N 覆盖率
  - 缺失的代码块按节标题列出
```

#### PCF2 — 复选框完整性

```
从 spec 的 Phase N 节提取所有 `[ ]` 位置（含代码块内的）
从实例的 Phase N 节提取所有 `[x]` 和 `[ ]` 位置

差异报告：
  - spec 有 N 个 `[ ]`，实例有 M 个复选框（无论 checked 与否）
  - 若 M 显著小于 N → 实例可能跳过了许多步骤
  - 按节标题列出缺失的复选框所在
```

#### PCF3 — 内容体量偏差检测

```
比较 spec 和实例的 Phase N 节各自的行数（或字符数）
若实例行数 < spec 行数的 50% → 报警：疑似摘要而非实例化

例外机制：
  - Phase 实际情况与 spec 通用模板差异大（如 ggs Phase 3 为纯 enrich vs spec 的 6:4 通用模式）→ 在 GROW.md 节开头注明偏离
  - 已注明偏离的节跳过体量检查
```

#### PCF4 — 占位符残留检测

```
在实例的 Phase N 节中搜索 `{{...}}` 模式
任何残留 → 报错：存在未替换的占位符
```

#### PCF5 — 结构性节缺失检测（超越标题比较）

```
从 spec 提取 Phase N 的完整结构树（含标题层级、列表、表格、引用块、代码块、checklist）
从实例提取同样的结构树
不仅比较标题文本，还比较标题下的"第一级结构元素"是否存在

例：
  spec 3.1-0-A 下有: 表格 + 代码块
  实例 3.1-0-A 下只有: 一句话 → 报警：结构元素缺失
```

### B. 整合到现有流程

1. **`/comply GROW.md phase N`（或 `/comply BIRTH.md phase N`）**：在现有 CHK5 检查之后，附加 PCF1–PCF5 检查层
2. **`init phaseN` Step 3a 标题树校验**：通过标题树检查后，追加 PCF1–PCF3 作为 Step 3c（content fidelity check），标题树通过 + content fidelity 通过才算完整的结构校验
3. **`init phaseN` Step 3b 语义合规检查**：在此基础上增强——在当前"忠实于 spec、占位符替换、与 LAW/CONSTITUTION 一致"之外，追加 PCF4（占位符残留）和 PCF5（结构性节缺失）检查

### C. 输出格式

在 comply 的现有 CHK5 节之后，新增 PCF 节：

```
=== PCF Phase Content Fidelity（BIRTH.spec.md / GROW.spec.md → 实例文件）===
✓/✗ PCF1 代码块完整性  （spec 12 个，实例 12 个 — 100%）
✓/✗ PCF2 复选框完整性  （spec 45 个，实例 42 个 — 缺失 3 个在 3.1-Z-X）
✓/✗ PCF3 内容体量偏差  （spec 980 行 vs 实例 950 行 — 97%，正常）
✓/✗ PCF4 占位符残留   （无）
✓/✗ PCF5 结构性节缺失  （全部结构元素存在）
```

### D. 适用性

- BIRTH 侧：`/comply BIRTH.md phase N`、`/boot init phaseN` Step 标题树校验
- GROW 侧：`/comply GROW.md phase N`、`/grow init phaseN` Step 3a 标题树校验
- 所有 Phase（0–10 for BIRTH，0–5 for GROW）

## Implementation

**Review**: faithful
**Date**: 2026-05-26

**检查清单**：

- [x] 在 `/home/baojie/.claude/skills/comply/SKILL.md` 中新增 PCF 检查层规范（代码/复选框/体量/占位符/结构元素五项检查）
- [x] 在 `/grow` skill 的 `init phaseN` Step 3a 中追加 PCF1–PCF3 作为 Step 3c，Step 3b 增强 PCF4+PCF5
- [x] 在 `/boot` skill 的 `init phaseN` Step 3a-2 后追加 Step 3a-3（PCF1–PCF3），Step 3b 增强 PCF4+PCF5
- [x] 定义 PCF 检查通过/不通过的判定标准（单项通过阈值 vs 必须全部通过）

**Commits**:
- baojie/memex@fb84c9b: feat(comply,grow,boot): 新增 PCF Phase Content Fidelity 五层检查
