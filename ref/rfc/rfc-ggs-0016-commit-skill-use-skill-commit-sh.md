# RFC-ggs-0016: /commit skill 应通过 skill_commit.sh 执行 git commit

- **Status**: proposed
- **Date**: 2026-05-25
- **Issue**: https://github.com/baojie/memex/issues/150
- **Source wiki**: ggs
- **Target**: `$MEMEX_ROOT/.claude/skills/commit/SKILL.md`

---

## Problem

`/commit` skill 的 SKILL.md 中直接调用 `git commit -F <tmpfile>` 执行提交。但 memex 已在 `wiki/scripts/skill_commit.sh` 中设计了统一授权入口——`/rfc`、`/evolve`、`/wiki` 等 skill 均通过此脚本提交，而非直接调用 `git commit`。

同时，各子 wiki 的 settings.json 已将 `Bash(git commit*)` 加入 deny 列表以阻止未授权提交，`skill_commit.sh` 则被加入 allow 列表作为豁免入口。`/commit` skill 直接调 `git commit` 导致：
- `/commit --auto` 被 settings.json 的 deny 规则拦截，无法自动执行
- 绕过 `skill_commit.sh` 统一入口，破坏了 memex 的授权设计

## Root cause

`/commit` skill（`$MEMEX_ROOT/.claude/skills/commit/SKILL.md`）中所有 `git commit` 调用未使用 `skill_commit.sh` 代理，而是直接调用原生 `git commit`。

## Proposed change

将 SKILL.md 中所有 `git commit` 相关指令替换为 `bash wiki/scripts/skill_commit.sh`：

1. **Step 4（交互模式）**：`git commit -F <tmpfile>` → `bash wiki/scripts/skill_commit.sh -F <tmpfile>`
2. **Step 3-AUTO（自动模式）**：`git commit -F <msgfile>` → `bash wiki/scripts/skill_commit.sh -F <msgfile>`
3. **输出示例**：交互模式展示的命令行示例同步更新

仅修改 SKILL.md，不改变 `/commit` skill 的分组逻辑或行为。
