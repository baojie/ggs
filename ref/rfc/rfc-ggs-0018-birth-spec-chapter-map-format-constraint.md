# RFC-ggs-0018: BIRTH.spec.md Phase 5-B 须显式约束 chapter_map.json 输出格式

- **Status**: proposed
- **Date**: 2026-05-25
- **Issue**:
- **Source wiki**: ggs
- **Target**: `$MEMEX_ROOT/BIRTH.spec.md`（Phase 5-B 章节 frontmatter 写入节）

---

## Problem

ggs Phase 5-B 执行后，`docs/wiki/data/chapter_map.json` 的格式为：

```json
{
  "Preface": { "nnn": "P03", "label": "前言", "chapter": null, ... },
  "ch01-up-to-the-starting-line": { "nnn": "001", ... }
}
```

而 pn-citation 插件（`buildCitationLink` 函数，第 56 行）的实际消费方式为：

```js
const pageId = chapterMap[nnn];   // 以 NNN 为 key 查 page_id
```

插件期望格式为 `nnn → page_id`：

```json
{
  "P03": "Preface",
  "001": "ch01-up-to-the-starting-line"
}
```

两者格式相反，导致所有 PN 引注（`（P03-062）`、`（001-038）` 等）完全无法渲染为可跳转链接，静默退化为纯文本。

同样依赖此格式的还有：
- `normalize_page_links.py`：`chap_num_to_page_id()` 做 `chapter_map.get(chap_num)` 查找
- `build_registry.py`：PN 链接合规检查

此错误在 Phase 9-A 试建页时才被用户目视发现（`/why` 诊断）。从 Phase 5-B 产生到 Phase 9-A 发现，中间跨越四个 Phase，修复成本极高。

## Root cause

**BIRTH.spec.md Phase 5-B 只要求"生成 chapter_map.json 并复制到 docs/wiki/data/"，没有定义该文件的规范格式**。

Phase 5-B 原文（行 1028）：
> 将 `data/chapter_map.json` 复制到 `docs/wiki/data/chapter_map.json`

没有任何关于 key 结构、value 结构的约束，也没有格式验证步骤。实现方（wiki 本地脚本 `assign_nnn_prefix.py` 的 `build_chapter_map()`）从自身视角出发，以 `page_id` 为 key 生成富对象（含 nnn、label、chapter 等字段），逻辑自洽，但与下游消费格式相反。

根本原因可归纳为：**Phase 5-B 只定义了"产物"（章节 frontmatter + chapter_map.json），没有定义产物的接口契约（格式规范 + 格式验证）**，导致实现端与消费端之间存在隐式约定，无法被系统性检出。

## Proposed change

在 BIRTH.spec.md Phase 5-B 的 `chapter_map.json` 生成步骤中，增加以下约束：

### 1. 格式规范（内联注释）

在"将 `data/chapter_map.json` 复制到 `docs/wiki/data/chapter_map.json`"一行前，插入格式规范：

```markdown
- [ ] 确认 `data/chapter_map.json` 格式正确——必须为 **`nnn → page_id`** 映射：
  ```json
  {
    "P03": "Preface",
    "001": "ch01-up-to-the-starting-line",
    "002": "ch02-natural-experiment-of-history"
  }
  ```
  > **禁止**使用 `page_id → {nnn, label, ...}` 格式——pn-citation 插件以 NNN 为 key 查询 page_id，格式反转导致所有 PN 引注静默失效。
```

### 2. 格式验证脚本（格式内联）

在格式规范之后，增加验证步骤：

```markdown
- [ ] 执行格式验证：
  ```bash
  python3 - <<'EOF'
  import json, sys
  from pathlib import Path
  cm = json.loads(Path('docs/wiki/data/chapter_map.json').read_text())
  errors = []
  for k, v in cm.items():
      if not isinstance(v, str):
          errors.append(f'  key {k!r}: value 应为 str（page_id），实为 {type(v).__name__}')
  if errors:
      print('✗ chapter_map.json 格式错误：')
      for e in errors: print(e)
      sys.exit(1)
  print(f'✓ chapter_map.json 格式正确（{len(cm)} 条目，nnn→page_id）')
  EOF
  ```
```

### 3. 修复 assign_nnn_prefix.py（本地脚本）

`wiki/scripts/assign_nnn_prefix.py` 中 `build_chapter_map()` 函数（第 125-145 行）须同步修改，输出 `nnn → page_id` 格式：

```python
def build_chapter_map() -> dict:
    """构建 data/chapter_map.json（格式：nnn → page_id）."""
    cmap = {}
    for nnn, pid in NNN_MAP.items():
        cmap[nnn] = pid
    return cmap
```

此修复针对本 wiki 本地脚本，不需要走 memex RFC 流程，可直接修改。

### 修改后的 Phase 5-B 执行顺序

```
5-B:
  → 批量更新章节 frontmatter（pn_prefix 字段写入）
  → 生成 data/chapter_map.json（格式：nnn → page_id）
  → 验证格式（内联脚本，失败则中止）
  → 复制到 docs/wiki/data/chapter_map.json
  → git add + commit
```

### 与 Phase 9 的关系

本 RFC 在 Phase 5-B 建立**前置拦截**，确保 chapter_map.json 在生成时即符合消费格式。Phase 9-A 的 CHK7 检查 PN 渲染，是事后验证，两者互补，不冲突。

---

## Implementation notes

本 RFC 包含两个独立部分：

1. **BIRTH.spec.md 修改**（memex，需走 RFC 流程）：Phase 5-B 增加格式规范 + 验证步骤
2. **assign_nnn_prefix.py 修改**（ggs 本地，可直接执行）：`build_chapter_map()` 输出格式修正

第 2 项可立即在本地执行，无需等待 memex RFC 审批。
