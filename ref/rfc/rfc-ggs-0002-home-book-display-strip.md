# RFC-ggs-0002: 首页 BOOK_DISPLAY 默认应使用 'strip' 模式

- **Status**: proposed
- **Date**: 2026-05-23
- **Issue**: https://github.com/baojie/memex/issues/128
- **Source wiki**: ggs
- **Target**: `plugins/home/index.js`

---

## Problem

GGS wiki 首页渲染出多个 book card（每部分一个），而不是像 investor wiki 那样将所有章节集中在一个 book card 中。当前 `hero.js` 配置 `BOOK_DISPLAY = 'card'`，导致 `BOOK_META` 中的每个条目（前言、第一部分、第二部分……）各自生成独立卡片，视觉效果分散。

预期行为：无论 `BOOK_META` 有多少条目，所有章节应集中在一个 book card 中展示，类似 investor 的 `strip` 模式效果。

## Root cause

`plugins/home/index.js` 第 94–97 行的渲染逻辑：

```js
bookCardsHtml: BOOK_DISPLAY === 'strip'
  ? renderBookStrip(pages)
  : BOOK_META.map(m => renderBookCard(m, pages)).join(''),
```

- `'strip'` → 调用 `renderBookStrip()`，生成单一 book card
- 其他值（包括 `'card'`）→ 遍历 `BOOK_META`，每条目一张卡片

`'card'` 模式对章节类内容不适配——它适用于多个独立主题各成一卡，而一本书的各部分是连续的。'strip' 模式才是书籍类 wiki 的合理默认值。

## Proposed change

将 `hero.js` 配置文件中的 `BOOK_DISPLAY` 值改为 `'strip'`：

```diff
- export const BOOK_DISPLAY = 'card';
+ export const BOOK_DISPLAY = 'strip';
```

### 备选方案

若认为命名不直观，可在 `plugins/home/index.js` 中将默认行为改为 strip-like：

```diff
  bookCardsHtml: BOOK_DISPLAY === 'strip'
    ? renderBookStrip(pages)
+   : BOOK_DISPLAY === 'card'
    : BOOK_META.map(m => renderBookCard(m, pages)).join(''),
+   : renderBookStrip(pages),
```

但最简单的方案是直接在 `hero.js` 中改值，无需修改引擎代码。
