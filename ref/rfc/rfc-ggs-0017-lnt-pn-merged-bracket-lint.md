# RFC-ggs-0017: NEW1 建页后强制执行 QUO7 PN 格式质检

- **Status**: proposed
- **Date**: 2026-05-25
- **Issue**: https://github.com/baojie/memex/issues/151
- **Source wiki**: ggs
- **Target**: `$MEMEX_ROOT/skills/gene/NEW1-create-page.md`

---

## Problem

在建设 9-A 试建页 `粮食生产` 时，生成了以下违规格式：

```
（P03-066，P03-067）
（002-029，002-033）
（005-001，005-002）
```

CONSTITUTION §7.1 明确规定：

> ✗ 错误：`（001-038，003-001）`  
> 血泪教训：麦卡锡词条（2026-05-10）写出这种格式，pn-citation 插件只能识别独立括号，合并写法导致两个 PN 都无法跳转。

**QUO7-pn-format-lint.md 已存在**，其 Pattern A 正好覆盖逗号合并 PN 问题，并支持自动修复。但 NEW1（建页基因）建页后没有调用 QUO7，导致格式错误在进入 git 之前未被拦截，只能靠用户目视发现。

## Root cause

**NEW1 建页流程缺少 PN 格式质检步骤。** QUO7 作为 butler 循环基因，只在 9-B 的 QUO23 步骤中被批量调用；9-A 单页试建走 NEW1 → CHK7 流程，CHK7 检查页面渲染，不检查内容格式，QUO7 从未被触发。

## Proposed change

在 `NEW1-create-page.md` 的建页流程末尾，增加 **强制 QUO7 质检步骤**：

```
建页完成后，在提交前对新建页面执行 QUO7-pn-format-lint，
自动修复 PN 格式违规（Pattern A 逗号合并、Pattern E 半角括号等），
有修复时重新 record_revision，无问题则直接进入 CHK7。
```

### 执行顺序

```
NEW1 建页
  → QUO7（PN 格式 lint，--fix 自动修复）
  → 若有修复：record_revision（summary: "fix: QUO7 auto-fix PN format"）
  → CHK7（系统链路检查）
  → commit
```

### QUO7 调用方式

```bash
# 对单页执行 QUO7 并自动修复
WIKI_ROOT=$PWD python3 "$MEMEX_ROOT/wiki/scripts/quo7.py" \
  --page <slug> --fix
```

若 QUO7 脚本不支持 `--page` 单页模式，退化为对文件直接调用：

```bash
python3 "$MEMEX_ROOT/wiki/scripts/quo7.py" \
  docs/wiki/pages/<bucket>/<slug>.md --fix
```

### 与 /comply CHK6 的关系

/comply CHK6 的 C10（已由 memex 实现）是事后诊断工具；本 RFC 要求的是**建页时的主动拦截**，两者互补，不冲突。

---

## Evaluation Note (ADM1)

**决策**: accept-modified

**调整方向**:
1. P1（逗号分隔）已在 memex QUO7-pn-format-lint.md Pattern A 中实现，不复用 LNT 前缀
2. P3（半角括号）已在 QUO7 Pattern E 中实现
3. P2（顿号分隔）作为补充并入 QUO7 Pattern G（该模式在脚本中存在但基因文档遗漏）
4. 核心增量：新增 C10 整合到 /comply CHK6，引用 QUO7 检测模式

**理由**: RFC 问题真实但方案与现有 QUO7 基因重叠，调整为整合方向而非新建独立规则体系。

---

## Implementation

**Review**: faithful
**Date**: 2026-05-25
**Commits**:
- 用户设置文件 ~/.claude/skills/comply/SKILL.md（非 git 仓库）

**实施说明**:
- P1/P3: 已在 QUO7-pn-format-lint.md 中存在，跳过
- P2: 已由 RFC-memex-0028 覆盖（补充 QUO7 Pattern G 文档），跳过
- C10: 新增到 /comply CHK6，含检测（逗号/顿号合并 PN + 半角括号）和 --fix 自动修复
