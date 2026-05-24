# RFC-ggs-0010: pn-citation 插件图片 PN 标签左侧边距对齐

- **Status**: proposed
- **Date**: 2026-05-24
- **Issue**: https://github.com/baojie/memex/issues/142
- **Source wiki**: ggs
- **Target**: `$MEMEX_ROOT/wiki/public/plugins/pn-citation/index.js`

---

## Problem

pn-citation 插件的 CSS 注入代码中，以下规则将图片 PN 标签强制为 `display: block`，使其脱离章节页左侧边距对齐体系：

```css
.wiki-figure .pn-label,
.wiki-table  .pn-label { display: block; margin-bottom: .3em; }
```

在宽屏 chapter 页面（≥1200px）中，段落 PN 标签通过 `article[data-type="chapter"] .pn-label` 的浮动规则（`float: left; margin-left: -6.8em`）对齐到段落左侧外部边距。但图片 PN 标签因 `.wiki-figure .pn-label` 的 `display: block` 声明特异性更高，覆盖了浮动规则，导致图片 PN 显示在图片上方（`margin-bottom: .3em`），而非左侧边距，与段落 PN 视觉不一致。

## Root cause

选择器特异性冲突：
- `article[data-type="chapter"] .pn-label`（0,1,1）→ 设置 `float: left`
- `.wiki-figure .pn-label`（0,2,0）→ 设置 `display: block`，覆盖 float

图片和表格的 PN 标签无法继承 chapter 页面的浮动左对齐规则。

## Root cause 补充

除了 CSS 特异性冲突外，浏览器默认 `<figure>` 的 `margin: 1em 40px` 也导致图片整体向右偏移 40px，即使 `.pn-label` 浮动到左边距，也会比段落 PN 偏右 40px。

## Proposed change

在 `$MEMEX_ROOT/wiki/public/plugins/pn-citation/index.js` 的 CSS 注入中：

1. 重置 chapter 页面下 `.wiki-figure` 的浏览器默认边距
2. 为 chapter 下的 `.wiki-figure .pn-label` 补充与段落 PN 一致的浮动规则

```css
/* ── 图片/表格 PN 标签：非 chapter 页面保留块级展示 ── */
.wiki-figure .pn-label,
.wiki-table  .pn-label { margin-bottom: .3em; }

/* ── chapter 页面：重置浏览器默认 figure 边距 ── */
article[data-type="chapter"] .wiki-figure {
  margin-left: 0;
  margin-right: 0;
}

/* ── chapter 页面：图片/表格 PN 与段落 PN 一致左对齐 ── */
article[data-type="chapter"] .wiki-figure .pn-label,
article[data-type="chapter"] .wiki-table  .pn-label {
  float: left;
  margin-left: -6.8em;
  width: 6.2em;
  text-align: right;
  clear: both;
}
```

## Alternatives considered

1. **仅在各 wiki 的 local.css 覆盖**：问题在共享插件中，所有使用 pn-citation 的 wiki 都受影响，应修复上游。
2. **直接删除 `display: block`**：非 chapter 页面上的图片 PN 标签可能失去已定义的块级布局，scope 到 `article[data-type="chapter"]` 更安全。

## Verification

已在 ggs wiki（local/local.css）验证通过：

| 维度 | 段落 PN | 图片 PN | 一致？ |
|------|---------|---------|--------|
| `margin-left` | -6.8em | -6.8em | ✅ |
| `float` | left | left | ✅ |
| `text-align` | right | right | ✅ |
| 标签 left 位置 | 316.86px | 316.86px | ✅ diff=0 |
| `display` | block | block | ✅ |
