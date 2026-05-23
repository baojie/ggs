# RFC-ggs-0003: restrict_to_project.py 增加基因命名校验

- **Status**: implemented
- **Date**: 2026-05-23
- **Issue**: https://github.com/baojie/memex/issues/129
- **Source wiki**: ggs
- **Target**: `$MEMEX_ROOT/.claude/hooks/restrict_to_project.py`

---

## Problem

当在 sub-wiki 中创建 local gene 时，Claude 可能错误地使用 `PRE`、`HKP`、`CHK` 等 memex 全局 prefix，或将文件放到 `ref/gene/` 而非 `local/gene/`。

当前 `restrict_to_project.py` hook 只拦截**文件路径范围**（限制写入本 wiki 目录），不校验**文件命名是否符合 `CONSTITUTION.md §3.1`**。这意味着命名违规在被 commit 审查之前不会被发现——修复成本更高（需要 rename、更新引用）。

具体断裂：
1. Claude 观察到 `ref/gene/PRE9-*.md` 等已有文件，误以为 `PRE` prefix 是通用命名格式
2. `restrict_to_project.py` 允许向 `ref/gene/` 写入（该目录在本 wiki 范围内），不检查命名规则
3. `local/gene/` 目录已存在，但没有机制主动提示 Claude 这是 local gene 的正确位置

## Root cause

`CONSTITUTION.md §3.1` 定义了基因命名规则，但这些规则没有对应的自动化校验。Claude 不"知道"自己不知道——只有当用户明确指出时才会意识到违反约定。hook 层是捕获此类违规的最佳位置，但目前只做路径限制，不做语义校验。

## Proposed change

在 `$MEMEX_ROOT/.claude/hooks/restrict_to_project.py` 中增加 `PreToolWrite` 阶段的文件名校验。

核心逻辑（伪代码）：

```python
def validate_gene_name(file_path: str) -> list[str]:
    """检查基因文件命名是否符合 CONSTITUTION §3.1。返回警告列表。"""
    warnings = []
    path = Path(file_path)

    # 只检查 gene 目录下的 .md 文件
    if 'gene' not in path.parts or path.suffix != '.md':
        return warnings

    filename = path.name
    parent_dir = path.parent.name  # 紧邻的父目录名

    # 规则 1: local gene 必须在 local/gene/ 下，命名 LOCAL-<wiki><NN>-slug.md
    if parent_dir == 'gene' and 'local' not in path.parts:
        # 在 ref/gene/ 或 skills/gene/ 下的 .md 文件，检查是否应该是 local gene
        if re.match(r'^(PRE|HKP|CHK)\d{2,}', filename):
            if (path.parent.parent.name == 'gene' and
                path.parent.name in ('local', 'skills')):
                pass  # 这是正确的 memex 全局基因位置
        elif re.match(r'^LOCAL-', filename):
            warnings.append(
                f"LOCAL- 前缀基因应放在 local/gene/ 目录，"
                f"当前路径: {file_path}"
            )
    elif parent_dir == 'gene' and 'local' in path.parts:
        # 在 local/gene/ 下的文件，必须符合 LOCAL-<wiki><NN>-slug.md
        if not re.match(r'^LOCAL-[a-z]+\d{2}-', filename):
            warnings.append(
                f"local/gene/ 下的文件必须使用 LOCAL-<wiki><NN>- 前缀，"
                f"当前文件名: {filename}。详见 CONSTITUTION §3.1"
            )

    return warnings
```

### 设计原则

- **warn-level 而非 block-level**：hook 不应阻止有意识的非常规操作。输出警告到 stderr，让用户（执行者）在 commit 前注意到。
- **只校验文件名和路径，不读文件内容**：保持 hook 轻量，避免副作用。
- **提示中引用 CONSTITUTION §3.1**：帮助 Claude 和人类执行者追溯到具体条款。

### 附加建议

在 `CONSTITUTION.md §3` 末尾添加一条注释，指向该校验逻辑的位置，使宪法条文有自动化检查对应。

---

## 备注

本 RFC 源于 ggs wiki 实践：在 Phase 3（语料准备）中将质检流程包装为 gene 时，Claude 创建了 `ref/gene/PRE21-corpus-final-format-qa.md`，违反了 CONSTITUTION §3.1 的规定（local gene 应命名为 `LOCAL-ggs<NN>-slug.md`，放在 `local/gene/` 下）。

## Implementation

**Review**: faithful
**Date**: 2026-05-23
**Commits**:
- baojie/memex@eddb102a8709a0040eca51d91c341eaa3a262759: implement RFC-ggs-0003: hook 增加基因命名校验（warn-level）
