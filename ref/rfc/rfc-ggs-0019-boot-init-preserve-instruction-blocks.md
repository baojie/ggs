# RFC-ggs-0019: /boot init 须原文保留说明性文字块，禁止摘要

- **Status**: implemented
- **Date**: 2026-05-25
- **Issue**: https://github.com/baojie/memex/issues/155
- **Source wiki**: ggs
- **Target**: `$MEMEX_ROOT/skills/SKILL_boot.md`（/boot init Step 2 实例化规则）

---

## Problem

`/boot init 9` 执行后，Phase 9-B 节丢失了 BIRTH.spec.md 中的关键操作指令：

- **丢失**：完整的 ASCII 流程图（含 ⏸ 人工审核暂停点、EXIT-GATE 说明框、"每轮建 5 页"说明）
- **丢失**：SCN27 调用 NEW1 建页、每轮 5 个实体的明确规定
- **丢失**：EXIT-GATE 的作用域描述（"E1–E5 序列，FAIL 项就地修正后重验"）
- **丢失**：日志命名格式（`logs/gene-express/*-R{R}-SCN27-{T}-r1.md`）
- **丢失**：进度表单元格填写规则（空白/`R{N} 进行中`/`R{N} ✓` 三态）

实例化后的 BIRTH.md Phase 9-B 仅有一句摘要：

> 每种类型执行独立的三轮迭代（SCN27×3 + EVV5×3 + QUO23×1 + EVV6×1 = 8 轮），每轮须人工审核后方可进入下一轮。

Agent 执行到 9-B 时无法知道每轮建多少页、EXIT-GATE 做什么检查、日志放在哪里。

## Root cause

`/boot init` Step 2 要求"从 BIRTH.spec.md 复制 Phase N 的完整规范内容"，但**没有区分两类文字的处理方式**：

- **checkbox 列表**（`- [ ] 步骤`）：可以适配本地参数，将 `{{...}}` 占位符替换为实际值
- **说明性文字块**（`###` 节描述、`>` 块引用、ASCII 流程图、代码块、表格注释）：必须原文复制，不得摘要

LLM 在 context 过长时，倾向于对"看起来像背景说明"的大段文字进行摘要，以节省 token。但这些文字恰恰是 agent 执行时的操作指令，摘要后导致关键步骤缺失。

根本原因：**Step 2 只说"复制完整内容"，没有明确禁止对说明性文字进行摘要，也没有定义哪类内容必须逐字保留**。

## Proposed change

在 `SKILL_boot.md` 的 `init phaseN` 模式 Step 2 中，增加以下明确规则：

### 增加：说明性文字保留规则

在 Step 2 开头插入：

```markdown
### Step 2 — 实例化 Phase N

> **逐字复制规则**：以下类型的内容必须从 spec 原文逐字复制，禁止摘要、改写或压缩：
> - `###`/`####` 小节标题及其紧跟的描述段落
> - `> ` 块引用（blockquote）
> - ASCII 流程图（含 `┌┐└┘│` 等字符的代码块）
> - 代码块（` ``` ` 包裹的内容）
> - 表格（含表头和注释行）
>
> **可适配的内容**：仅限 `- [ ] 步骤` 列表中的 `{{占位符}}`，替换为本项目实际参数值。
> 其他所有 `- [ ]` 步骤文字也须原文复制，不得改写。
```

### 增加：Step 3a 说明性文字校验

在现有 Step 3a（标题树结构校验）之后，增加子步骤：

```markdown
#### Step 3a-2：说明性文字完整性抽查

从实例化后的 BIRTH.md Phase N 中，随机抽取 2–3 个 `###` 小节，与 BIRTH.spec.md 对应节进行逐段比对：

1. 取 spec 中该节的第一段非 checkbox 描述文字（通常是 `###` 标题之后、第一个 `- [ ]` 之前的内容）
2. 在实例中找到对应段落
3. 若字数差异 > 30%，或 spec 中有 ASCII 图/代码块在实例中缺失，则：
   - 打印：`✗ 节 "{节标题}" 说明性文字疑似被摘要，spec 原文 N 字，实例 M 字`
   - 从 spec 补全该节说明性文字，然后重新执行 Step 3a-2
4. 全部抽查节通过，输出 `✓ 说明性文字完整性抽查通过`
```

### BIRTH.spec.md 中增加显式标注

在每个包含关键操作指令的 `###` 节标题后，加注（可选增强）：

```markdown
### 9-B 批量循环流程
<!-- MUST-COPY: 以下内容含操作指令，init 时必须原文复制 -->
```

此标注由 Step 3a-2 脚本检测，发现 `MUST-COPY` 节在实例中缺失或被摘要时强制中止。

---

## Implementation notes

本 RFC 修改目标为 `$MEMEX_ROOT/skills/SKILL_boot.md`，属于 memex 主系统文件，需走 RFC 流程。

**已知受影响的 Phase**：Phase 8 的批量循环节、Phase 9-B 的批量循环节，均含 ASCII 流程图，均在 init 时存在摘要风险。

**临时缓解**：ggs 本地已手动补全 Phase 9-B 的完整操作指令（commit `e2cc427`）。

---

## Implementation

**Review**: faithful
**Date**: 2026-05-25
**Commits**:
- baojie/memex@7bbe5cbc5fd6681abbc132c4f4a0c621e938ebd4: feat(boot): RFC-ggs-0019 /boot init 须原文保留说明性文字块 + Phase 9-B 清晰化

**说明**: SKILL_boot.md 位于 `~/.claude/skills/boot/SKILL.md`（本地 skill 目录），不在 memex git 仓库内，已直接修改。BIRTH.spec.md 同步做了 Phase 9-B 陈述清晰化（选页原则独立 + 关键操作规则显式列出）。
