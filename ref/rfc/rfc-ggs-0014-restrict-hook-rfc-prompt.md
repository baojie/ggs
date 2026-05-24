# RFC-ggs-0014: restrict_to_project.py 拒绝信息中提示 /rfc 路径

- **Status**: implemented
- **Date**: 2026-05-24
- **Issue**: https://github.com/baojie/memex/issues/146
- **Source wiki**: ggs
- **Target**: memex `.claude/hooks/` 下所有含拒绝返回信息的钩子脚本

---

## Problem

memex 的多个安全钩子在拒绝越界操作时，仅返回拒绝信息，未告知 wiki agent 正确的操作方法。Agent 在遇到拦截后可能尝试用其他方式绕过（如改用 heredoc、python -c、perl -e 等），而不知应走 `/rfc` 流程。

涉及的钩子包括但不限于：
- `restrict_to_project.py` — 拒绝 Write/Bash 越界
- 其他所有含拒绝返回信息的钩子脚本

当前拒绝信息仅说明"被拒绝"，缺少后续指导。

## Proposed change

在所有含拒绝返回信息的钩子脚本中，在拒绝信息的末尾追加一行提示：

```
  ⚠️ 对 memex 路径的修改必须通过 /rfc 流程，禁止其他任何形式的直接写入。
```

扫描 `$MEMEX_ROOT/.claude/hooks/` 下所有脚本，找到所有输出拒绝信息的代码行逐一修改。仅修改字符串内容，不改变钩子的逻辑或行为。

---

## Implementation

**Review**: faithful
**Date**: 2026-05-24
**Commits**:
- baojie/memex@888da17422edafab8c05844c77b087be057b6031: implement RFC-ggs-0014

**修改位置**：`wiki/hooks/restrict_to_project.py`
- Bash 拒绝信息追加 /rfc 提示
- Edit/Write 拒绝信息追加 /rfc 提示
