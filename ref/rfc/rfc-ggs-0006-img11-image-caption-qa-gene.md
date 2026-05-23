# RFC-ggs-0006: 建立插图 caption 完整性基因（IMG11）并集成至 /comply

- **Status**: proposed
- **Date**: 2026-05-24
- **Issue**: https://github.com/baojie/memex/issues/132
- **Source wiki**: ggs
- **Target**: `$MEMEX_ROOT/skills/gene/IMG11-image-caption-qa.md` + `CHK7`（或新增 IMG 合规通道）

---

## Problem

Phase 2/3（章节配图插入）完成后，31 幅插图中有 21 幅缺少 caption。逐幅核查原书 epub 后发现：

| 类型 | 数量 | 示例 |
|------|------|------|
| 原书有图注但 wiki 未收录 | 3 幅 | IQ8A3、IQZ5、IQ20A1 |
| 原书无独立 caption | 18 幅 | 照片、地图、示意图等 |
| 语法错误（`::::` 而非 `:::`）| 2 处 | IQ20A1、IQZ5 |

问题根因：
1. **无自动化检查**：插入图像后没有工具验证 caption 存在性
2. **原书 caption 未溯源**：插入者未查阅 epub 的 `imagenote` 元素
3. **语法校验缺失**：`::::` 与 `:::` 在 diff 中肉眼难辨

## Proposed change

### 1. 在 memex 建立 IMG11 基因

路径：`$MEMEX_ROOT/skills/gene/IMG11-image-caption-qa.md`

定义三类检查：

```
C1  语法：`::: image` 必须为 3 冒号（非 4）
C2  caption：`::: image` 块内 `![]` 与 `:::` 之间必须有非空文本
C3  原书可查：对无 caption 的图，自动标记是否在 epub 中发现 imagenote
```

### 2. 在 /comply 中集成 IMG11 检查

当 `/comply` 的目标是 `docs/wiki/pages/` 下的文件时，在现有 CHK5/CHK6 之后追加 IMG11 检查。

### 3. ggs 侧记录

ggs 已实际完成修复（补 3 幅 caption、删 1 处重复文本）。待 RFC 批准后将 IMG11 基因迁入 memex，各子 wiki 可复用。

## Gene 草稿

```markdown
---
id: IMG11-image-caption-qa
group: IMG
wu: 10
diff_limit: 每次一个 wiki 全部页面
sources: [ggs]
scope: general
applicable: true
origin: ggs 章节配图完成后发现 21/31 幅无 caption
tags: [image, caption, qa]
born: 2026-05-24
---

# IMG11 image-caption-qa — 插图 caption 完整性检查

### C1 冒号数

```python
import re
pat = re.compile(r'^:{3,4}\s+image\s+fig=', re.MULTILINE)
for m in pat.finditer(text):
    if m.group(0).count(':') != 3:
        issues.append(f"  line {line_no}: {m.group(0).strip()[:40]!r} 为 {m.group(0).count(':')} 冒号，应为 3")
```

### C2 caption 存在性

```python
for m in pat.finditer(text):
    end = re.search(r'^:::+$', text[m.end():], re.MULTILINE)
    inner = text[m.end():m.end()+(end.start() if end else 0)].strip()
    if not inner:
        issues.append(f"  line {line_no}: {m.group(1)} 无 caption")
```

### C3 原书可查（可选）

```bash
grep -A4 "$IMAGE_FILE" "$EPUB_DIR"/*.xhtml | grep -q 'imagenote' \
  && echo "原书有 caption" || echo "原书无 caption"
```
```
