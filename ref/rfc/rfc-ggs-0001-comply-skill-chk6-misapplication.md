# RFC-ggs-0001: comply skill 对非 wiki 页面误输出 CHK6 检查

- **Status**: proposed
- **Date**: 2026-05-23
- **Issue**: https://github.com/baojie/memex/issues/127
- **Source wiki**: ggs
- **Target**: `.claude/skills/comply/skill.md`（comply skill 定义文件）

---

## Problem

comply skill 的 CHK6（C1–C8 格式检查）在设计上只应针对 `docs/wiki/pages/` 下的 wiki 页面执行。实际使用中，当对 `BIRTH.md`（项目根目录下的非 wiki 文件）执行 `/comply` 时，输出报告中仍然包含了 `CHK6 格式检查` 一节（标注为"跳过"或"不适用"），容易让用户误以为该文件存在格式问题需要修复。

## Root cause

comply skill 的执行逻辑中，CHK5（T/L/V）和 CHK6（C1–C8）的区分条件在代码实现中存在表述模糊——虽然规定了"仅当目标位于 `docs/wiki/pages/` 下时执行 CHK6"，但在实际输出模板中始终包含 CHK6 章节，对非 wiki 文件仅标注为"跳过"。这种"始终输出 CHK6 章节"的设计让用户困惑：为什么一个不相关的检查会出现在报告中？

## Proposed change

在 comply skill 的输出模板中，对非 `docs/wiki/pages/` 下的文件**完全省略 CHK6 章节**（不输出 `=== CHK6 格式检查 ===` 标题，不标注"跳过"）。两种情况的输出：

**非 wiki 页面**（如 `BIRTH.md`、`*.py`、`*.spec.md` 等）：
```
comply: <文件路径>

=== CHK5 语义检查 ===
✓/✗ T 过时错误
✓/✗ L 逻辑错误
✓/✗ V 违宪违法
```

**wiki 页面**（`docs/wiki/pages/*.md`）：
```
comply: <文件路径>

=== CHK5 语义检查 ===
✓/✗ T 过时错误
✓/✗ L 逻辑错误
✓/✗ V 违宪违法

=== CHK6 格式检查 ===
✓/✗ C1 破折号滥用
...
```

### 具体实现方式

1. 在 comply skill 的执行脚本/提示词中，先判断目标文件路径是否以 `docs/wiki/pages/` 开头
2. 若是 → 输出完整报告（CHK5 + CHK6）
3. 若否 → 输出仅 CHK5 的报告，完全省略 CHK6 章节和任何提及

### 验收标准

- [ ] 对 `BIRTH.md` 执行 `/comply`，输出中无 `CHK6`、`C1`、`C2` 等字眼
- [ ] 对 `docs/wiki/pages/About.md` 执行 `/comply`，输出包含完整 CHK6 章节
