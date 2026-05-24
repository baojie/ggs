# RFC-ggs-0017: 增加 LNT 规则检测括号内逗号分隔的合并 PN 格式

- **Status**: implemented
- **Date**: 2026-05-25
- **Issue**: https://github.com/baojie/memex/issues/151
- **Source wiki**: ggs
- **Target**: `$MEMEX_ROOT/skills/gene/LNT2-punctuation-format-lint.md`（或新建 `LNT16-pn-format-lint.md`）

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

现有所有 LNT 基因（LNT1–LNT15）均未包含对此格式的检测规则，导致：

1. PN lint 在建页后未发现此违规
2. `/comply` 的 CHK6 格式检查也未覆盖此规则
3. 只能靠用户目视发现

## Root cause

现有 lint 基因检测的是段落格式、标点、frontmatter、wikilink 等，但**没有任何基因专门检测 PN 引注格式本身**。CONSTITUTION §7.1 的 PN 格式规则（独立括号、禁止合并、禁止省略括号等）在 LNT 体系中存在空白。

## Proposed change

在 LNT 体系中增加 PN 格式检查规则，建议扩展 `LNT2-punctuation-format-lint.md` 或新建 `LNT16-pn-format-lint.md`，包含以下检测：

### P1 — 括号内逗号分隔合并 PN（高优先级，本次触发）

**正则**：`（[0-9P][0-9][0-9]-[0-9]+，[0-9P]`

```python
import re, sys
txt = open(sys.argv[1]).read()
body = txt.split('---', 2)[-1] if txt.startswith('---') else txt
issues = []
pat = re.compile(r'（([0-9P][0-9]{2}-[0-9]+)，([0-9P][0-9]{2}-[0-9]+)）')
for i, line in enumerate(body.splitlines(), 1):
    for m in pat.finditer(line):
        issues.append(
            f'  - line {i}: 合并 PN 格式违规（CONSTITUTION §7.1）: {m.group(0)!r}'
            f' → 应改为 （{m.group(1)}）（{m.group(2)}）'
        )
print('\n'.join(issues) if issues else 'OK')
```

**修复**：将 `（A，B）` 拆分为 `（A）（B）`（可自动修复）。

### P2 — 括号内顿号分隔合并 PN

**正则**：`（[0-9P][0-9][0-9]-[0-9]+、[0-9P]`（同上逻辑，分隔符为顿号）

### P3 — 半角括号用于 zh wiki PN

**正则**：`\([0-9P][0-9]{2}-[0-9]+\)`（zh wiki 应用全角括号）

### 与 /comply CHK6 的关系

建议同步在 `/comply` CHK6 中增加 **C10 PN 格式** 检查项，对 wiki 页面执行上述 P1–P3 规则，报告格式如下：

```
✓/✗ C10 PN 格式   （列出每处违规，或"无"）
```

### 自动修复（--fix 模式）

P1（逗号合并）和 P2（顿号合并）可安全自动修复：

```python
import re, pathlib
txt = pathlib.Path(path).read_text()
# 合并 PN → 独立括号（支持 2 个 PN 合并的情况）
new_txt = re.sub(
    r'（([0-9P][0-9]{2}-[0-9]+)[，、]([0-9P][0-9]{2}-[0-9]+)）',
    r'（\1）（\2）',
    txt
)
```

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
