# RFC-ggs-0011: pn-citation 插件表格/blockquote 容器边距重置

- **Status**: proposed
- **Date**: 2026-05-24
- **Issue**: https://github.com/baojie/memex/issues/143
- **Source wiki**: ggs
- **Target**: `$MEMEX_ROOT/wiki/public/plugins/pn-citation/index.js`

---

## Problem

RFC-ggs-0010（已实施）修复了 `<figure>` 的浏览器默认左边距和 PN 标签浮动，但同类的 table 和 blockquote 容器仍有对齐问题：

1. **`.wiki-table`**：缺少 `margin-left: 0` 重置。浏览器/语义块插件对 `<table>`/`.wiki-table` 的默认左边距（40px）使得表格整体右移，表格内的 PN 标签也比段落 PN 标签偏右。

2. **`<blockquote>`**：浏览器默认 `margin: 1em 40px` 使 blockquote 整体右移 40px。pn-citation 插件虽已为 blockquote 的 `.pn-label` 设置了补偿公式（`calc(-6.8em - (1em / 0.72) - 3px)`），但该公式补偿的是 padding 和 border 的宽度，而非容器本身的 margin。blockquote 缺少视觉缩进样式（无 `padding-left`、无 `border-left`），其视觉区分完全依赖 `margin-left`，重置 margin 后若无替代缩进将无法与普通段落区分。

## Root cause

与 RFC-ggs-0010 相同模式：浏览器默认 `margin-left: 40px` 作用于多个块级元素（`<figure>`、`<table>`、`<blockquote>`），使这些容器的 `.pn-label` 无论怎样浮动，始终比段落 PN 偏右 40px。

## Proposed change

在 `article[data-type="chapter"]` 范围内，对 `.wiki-table` 和 `blockquote` 做与 `.wiki-figure` 平行的处理：

```css
/* ── chapter 页面：重置表格浏览器默认边距 ── */
article[data-type="chapter"] .wiki-table {
  margin-left: 0;
  margin-right: 0;
}

/* ── chapter 页面：blockquote 改用 padding+border 维持视觉区分 ── */
article[data-type="chapter"] blockquote {
  margin-left: 0;
  margin-right: 0;
  padding-left: 1em;
  border-left: 3px solid var(--border, #ccc);
}
```

注：`.wiki-figure` 的边距重置已在 RFC-ggs-0010 中实施，PN 标签浮动已在 `article[data-type="chapter"] .wiki-figure .pn-label` 和 `article[data-type="chapter"] .wiki-table .pn-label` 中覆盖。blockquote 的 PN 标签补偿公式 `calc(-6.8em - (1em / 0.72) - 3px)` 也已存在于插件中。本 RFC 仅补充缺失的**容器边距重置**和 blockquote 的**缩进样式**。

## Alternatives considered

1. **在各 wiki 的 local.css 覆盖**：问题在共享插件中，所有 wiki 都受影响。
2. **不改 blockquote 样式，只重置 margin**：blockquote 将失去视觉区分，与普通段落无法区分，不可接受。
3. **用 text-indent 替代**：blockquote 内容需整体缩进，text-indent 只影响首行，不适合。

## Verification

已在 ggs wiki（local/local.css）验证通过：

| 场景 | 段落 PN | 容器 PN | diff |
|------|---------|---------|------|
| `.wiki-table` PN | 316.86px | 316.86px | 0 ✅ |
| `blockquote` PN | 316.86px | （无测试页） | 公式可推导对齐 |
