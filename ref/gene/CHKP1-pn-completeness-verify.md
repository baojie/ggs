---
id: CHKP1-pn-completeness-verify
group: CHK
scope: ggs-local
applicable: true
origin: Phase 5 全量赋号完成后的验收需求；QUO10 依赖 pn-source.json 且检查语义，本 gene 只检查结构与格式层面
tags: [audit, pn, lint]
born: 2026-05-24
---

# CHKP1 pn-completeness-verify — PN 完整性结构验收

**定义**：在章节页完成 PN 赋号（Phase 5-C）后，对全书执行一次结构层面的完整性验收。
检查范围：语法正确性、编号连续性、特殊块赋号合规性、不当赋号检测。

> 与 QUO10 的分工：本 gene 检查**结构层面**（格式/连续性/赋号规则）；
> QUO10 检查**语义层面**（PN 所指原文与引文是否一致）。
> 本 gene 在 Phase 5-E 之后、QUO10 之前执行。

---

## 检查项总览

| 编号 | 分类 | 检查内容 | 严重度 |
|------|------|---------|--------|
| A1 | 语法 | `[NNN-PPP]` 锚点格式合规（NNN 与 pn_prefix 一致，PPP 三位）| ERROR |
| A2 | 语法 | 所有 `:::TYPE pn=NNN-PPP` 属性格式合规 | ERROR |
| A4 | 语法 | 无半角括号 PN `(NNN-PPP)`（会被误认为引用格式）| ERROR |
| A5 | 语法 | PN 锚点与正文之间无多余空格（`[NNN-PPP]正文`，非 `[NNN-PPP] 正文`）| WARN |
| A6 | 语法 | `:::` 与块类型名之间必须有空格（`::: image` 正确，`:::image` 错误）| ERROR |
| B1 | 连续性 | 每章 PPP 从 001 起严格递增，无跳号 | ERROR |
| B2 | 连续性 | 无重号（同 NNN 下同 PPP 出现两次）| ERROR |
| B3 | 连续性 | 每章至少有 1 个 PN | WARN |
| C1 | 特殊块 | 所有 `:::TYPE` 语义块开启行必须有 `pn=NNN-PPP` 属性 | ERROR |
| D1 | 不当赋号 | 标题行（`# ## ###`）不得有 PN | ERROR |
| D2 | 不当赋号 | frontmatter 内不得有 PN | ERROR |
| D3 | 不当赋号 | 脚注定义行（`[^N]:` 开头）不得有 PN（ggs 豁免规则）| ERROR |
| D4 | 不当赋号 | `:::` 闭合行（单独一行 `:::`）不得有 `[NNN-PPP]` 锚点 | ERROR |
| D5 | 不当赋号 | blockquote 行（`>` 开头）不得有 PN 锚点 | ERROR |
| E1 | 引文完整性 | 连续 blockquote 块（诗/引文）前的段落应有 PN，块内不应有 PN | WARN |
| F1 | 覆盖 | ref/chapter-order.md 中所有章节均已赋 PN | ERROR |
| F2 | 覆盖 | 含 pn_prefix 的页面 NNN 与 chapter-order.md 一致 | ERROR |

---

## 执行方式

```bash
python3 wiki/scripts/verify_pn_completeness.py           # 全量检查（所有章节）
python3 wiki/scripts/verify_pn_completeness.py ch08      # 单章检查
python3 wiki/scripts/verify_pn_completeness.py --errors  # 只输出 ERROR 级别
```

---

## 各检查项规则说明

### A1 锚点格式

合法格式：`[NNN-PPP]`，其中：
- NNN 为 `P01`–`P09`（前置页）或 `001`–`999`（正文章节）
- PPP 为三位数字 `001`–`999`
- NNN 必须与该页面 frontmatter 的 `pn_prefix` 一致

### A4 半角括号

`(001-038)` 是 WIKI_LANG=en 的引用格式，ggs 为 zh wiki，章节页锚点必须用方括号 `[NNN-PPP]`，全角括号 `（NNN-PPP）` 为概念页引用格式，均不应出现在章节页段落锚点中。

### B1 连续性

每章 PPP 序列：
- 起始必须为 001
- 相邻两个 PPP 差值为 1（`:::image pn=` 和 `[NNN-PPP]` 混合计入同一序列）
- 末号 = 总 PN 数

### C1 语义块属性文法

所有 `:::TYPE` 语义块（`:::image`、`:::table`、`:::note`、`:::query` 等）的**开启行**必须含 `pn=NNN-PPP` 属性：

```
::: image fig="IQ8A1" pn=008-017
::: table pn=008-025
::: note pn=008-033
```

PN 作为属性写在开启行，与块类型和其他属性并列，顺序不限。`:::` 闭合行不写 PN（由 D4 保证）。

### D4 `:::` 闭合行

`:::image`、`:::table` 等语义块的**开启行**由 C1/C2 处理，要求含 `pn=` 属性或注释。
D4 针对的是**闭合行**——单独一行 `:::`——它本身不承载内容，不赋 `[NNN-PPP]` 锚点。
若检测到 `[NNN-PPP]:::` 形式（锚点误加到闭合行），报 ERROR。

> PN 的两种形式不要混淆：
> - `[NNN-PPP]` — 段落锚点，前置于普通段落行首
> - `pn=NNN-PPP` — 语义块属性，写在 `:::image` 开启行内

### D5 blockquote

ggs 规则：所有 `>` 开头行（包括校勘注记 `> 【校勘·XX】`）均不赋 PN。
若检测到 `[NNN-PPP]>` 形式（PN 紧跟 blockquote），报 ERROR。

### E1 诗/引文完整性

连续多行 blockquote（如诗歌逐行引用）应视为一个引用单元，**整体不赋 PN**（ggs 规则）。
检测方式：统计连续 blockquote 块的行数，若 > 4 行且前一个段落无 PN 锚点，提示可能漏赋上文。

> ggs 的处理哲学：诗歌/多行对话属于引用块，整块跳过；不逐行赋 PN，也不为引用块本身赋 PN。
> 若需要为引用内容建立 PN 锚点，应在引用块**前**的导语段落赋 PN。

---

## 输出格式

```
CHKP1 PN 完整性检查 — 2026-05-24

=== 覆盖检查 (F) ===
✓ F1  23/23 章节均已赋 PN
✓ F2  所有 pn_prefix 与 chapter-order.md 一致

=== 语法检查 (A) ===
✓ A1  全部锚点格式合规
✓ A2  全部 :::image 块含 pn=
  A5  [WARN] ch03 line 47: PN 后有空格 → [003-012] 用地...

=== 连续性检查 (B) ===
✓ B1  所有章节编号连续（无跳号）
✓ B2  无重号

=== 特殊块检查 (C) ===
✓ C1  所有 :::image 块有 pn=
  C2  [WARN] ch07 line 203: :::table 块无 pn 注释

=== 不当赋号检查 (D) ===
✓ D1–D5 无标题/frontmatter/脚注/:::闭合标签/blockquote 被赋 PN

=== 引文完整性 (E) ===
✓ E1  无可疑诗/引文块

---
ERROR: 0  WARN: 2  INFO: 0
```
