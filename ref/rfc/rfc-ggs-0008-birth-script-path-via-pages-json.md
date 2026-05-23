# RFC-ggs-0008: BIRTH 脚本应通过 pages.json path 字段定位页面文件

- **Status**: implemented
- **Date**: 2026-05-24
- **Issue**: https://github.com/baojie/memex/issues/134
- **Source wiki**: ggs
- **Target**: wiki/BIRTH.md（Phase 5-B 节）、wiki/public/plugins/pn-citation/（或相关共享脚本）

---

## Problem

BIRTH.md Phase 5-B 要求编写批量更新脚本（如 `assign_nnn_prefix.py`），但对脚本如何定位页面文件没有约束。
自然的写法是取 page id 的前两个字符作为子目录前缀（`prefix = pid[:2]`），对 ASCII id（如 `ch01` → `ch/ch01.md`）有效，但对纯中文 id（如 `目录`）失效——中文字符截取无法得到有效路径。

ggs wiki 中存在中文 id 的页面（`目录`），导致脚本在处理该页面时找不到文件，输出 `- 目录: 文件不存在，跳过`。

## Root cause

1. **BIRTH.md 无约束**：Phase 5-B 节要求"编写批量更新脚本"，但没有指定文件路径的标准推导方式，实现者自由选择。
2. **pages.json 已有 path 字段**：`pages.json` 中每个页面都有 `path` 字段（如 `"path": "mu/目录.md"`），是定位文件的权威来源，但 BIRTH 文档未引导使用。
3. **潜在蔓延**：其他项目的 BIRTH 衍生脚本若沿用同样模式（`pid[:2]` 推导路径），面对 CJK id 时会同样失效。

## Proposed change

### 1. BIRTH.md Phase 5-B 新增约束

在 Phase 5-B 的脚本编写说明中加一条规范：

> **铁律**：所有批量操作脚本定位页面文件时，**必须读取 `pages.json` 的 `path` 字段**，不得自行从 page id 推导路径。
>
> ```python
> pages = json.loads((WIKI_ROOT / 'docs/wiki/pages.json').read_text())['pages']
> entry = pages.get(pid)
> fpath = PAGES_DIR / entry['path']   # 正确
> # fpath = PAGES_DIR / pid[:2] / f'{pid}.md'  # 禁止
> ```

### 2. 审查 memex 共享脚本

检查 `~/memex/wiki/scripts/` 和 `~/memex/ref/` 下的脚本是否有 `pid[:2]`、`id[:2]` 等路径推导写法，统一改为读 `pages.json.path`。

### 3. 可选：CONSTITUTION.md 加约定

在 CONSTITUTION.md 中加一条技术约定：
> 所有访问 wiki 页面文件的脚本，必须以 pages.json 为单一可信来源获取路径。

## Implementation

**Review**: faithful
**Date**: 2026-05-24
**Commits**:
- baojie/memex@dc0cf7fae97e7cba0f33b35ab51004406a9c6ce5: implement RFC-ggs-0008: 批量脚本必须通过 pages.json path 定位页面文件
