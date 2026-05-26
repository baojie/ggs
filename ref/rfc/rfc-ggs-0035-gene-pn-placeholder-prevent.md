# RFC-ggs-0035: 在 NEW1/RCH2 gene 提示词中明确禁止 PN 占位符

- **Status**: accepted
- **Date**: 2026-05-27
- **Issue**: https://github.com/baojie/memex/issues/203
- **Source wiki**: ggs
- **Target**: `$MEMEX_ROOT/skills/gene/NEW*.md` 全部 25 个 + `$MEMEX_ROOT/skills/gene/RCH*.md` 全部 9 个

---

## Problem

GROW 流程中 AI 生成的 wiki 页面频繁出现 `（NNN-PN）` 格式的段落引用——章节号（NNN）正确，但段落号位置写的是字面量 "PN" 而非三位数字。例如 `（001-PN）`、`（015-PN）` 等。经全面排查，共约 327 处此类占位符分布在 ~120 个页面中。

根本原因是 gene 提示词措辞导致 AI 将 "PN" 理解为可填入的值而非段落编号的概念名称。

## Root cause

两处 gene 文件的铁律区均使用"标注其来源 PN"的措辞（见 NEW1-create-page.md 第 64 行、RCH2-enrich-grade.md 第 35 行）：

- "PN" 在提示词中同时扮演两个角色：概念名（"段落编号"的缩写）和格式占位符（类似 `{placeholder}`）
- AI 模型倾向于将缩写词理解为可输出的值，尤其在不确定具体数字时，直接输出字面量 "PN"
- 各 wiki 的 PN 格式约定在各自 `LAW.md` 中已有明确定义（ggs 为 `（NNN-PPP）`，NNN/P 均为三位数字），但 gene 提示词未引用该约定

## Proposed change

在所有 NEW* 前缀（25 个）和 RCH* 前缀（9 个）gene 文件中各新增一个独立节，引用 LAW.md §三 作为 PN 格式的权威规范，要求所有 PN 引用必须严格遵循该格式。

### 新增节模板

在各 gene 文件的铁律区之后、执行步骤之前（若无铁律区则在前置条件之后），插入以下独立节：

```
### PN 格式规范

- PN 格式必须严格遵循对应 wiki 的 LAW.md 中"PN（段落编号）映射规则"节的规定
- 通用格式：`（NNN-PPP）`，NNN = 三位章节号，PPP = 三位段落号
- 示例：`（005-021）`、`（013-011）`、`（P01-003）`
- 段落号必须是三位数字（如 022、110），**禁止将字面量 "PN" 填入段落号位置**
- 写完后逐条自查：检查所有 PN 引用，段落号是否为三位数字
```

### 详细插入位置

**NEW1-create-page.md**：Step 3 铁律区之后、起草正文之前

**其他 NEW* 文件**：在文件已有 PN 相关说明的节之后插入；若无则在前置条件/执行步骤之间插入

**RCH2-enrich-grade.md**：铁律区之后、执行步骤之前

**其他 RCH* 文件**：在铁律区或执行步骤之前插入

### 变更清单

| 范围 | 文件数 | 操作 |
|------|--------|------|
| `NEW*.md` | 25 | 新增 `### PN 格式规范` 节 |
| `RCH*.md` | 9 | 新增 `### PN 格式规范` 节 |
