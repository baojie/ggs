# RFC-ggs-0029: toc 插件支持 h1-h4 多级标题 + 层级缩进

- **Status**: implemented
- **Date**: 2026-05-26
- **Issue**: https://github.com/baojie/memex/issues/175
- **Source wiki**: ggs
- **Target**: memex/wiki/public/plugins/toc/index.js + memex/wiki/public/css/sidebar.css

---

## Problem

当前 toc 插件只处理 `h2, h3` 两级标题。对于内容层次较深的页面（如有多级子节的 wiki 条目），h4 标题不会出现在目录中，用户无法通过 TOC 导航到三级子节。

此外，树构建算法使用硬编码的 2 级栈（h2 为根、h3 挂到上一个 h2），HTML 渲染也是非递归的模板字符串拼接，无法扩展支持更深层级。CSS 只定义了 `.toc-h2` 和 `.toc-h3` 样式，缺少更深层级的缩进规则。

## Root cause

1. `index.js:30` — `querySelectorAll('h2, h3')` 显式排除了 h4
2. `index.js:53` — level 映射只处理了 H2→2 / H3→3，无 H4→4
3. `index.js:57-66` — 树构建用 2 级栈（`tree` / `stack.children`），硬编码了 h2→h3 的父子关系
4. `index.js:68-83` — HTML 渲染用 `tree.map()` + 字符串模板，非递归，无法渲染 3 层以上
5. `sidebar.css` — 只有 `.toc-h2` / `.toc-h3`，无 `.toc-h4`

## Proposed change

### 1. 扩大标题选择器

```
30c30
<   const headings = article.querySelectorAll('h2, h3');
---
>   const headings = article.querySelectorAll('h2, h3, h4');
```

决定：h1 作为页面标题不纳入 TOC（当前行为保持不变）。只增加到 h4，以控制 TOC 长度。

### 2. level 映射加 H4

```
53c53
<   entries.push({ level: h.tagName === 'H2' ? 2 : 3, id: h.id, text });
---
>   const levelMap = { H2: 2, H3: 3, H4: 4 };
>   entries.push({ level: levelMap[h.tagName] || 2, id: h.id, text });
```

### 3. 树构建改为多级栈算法

替换当前的 2 级硬编码栈，用通用多级栈：每个条目找到最近的、级别比自己低的条目作为父节点。

```js
// 多级栈：栈底到栈顶级别递增，新条目找到第一个级别比自己低的作为父节点
const tree = [];
const stack = []; // { level, node }
for (const e of entries) {
  while (stack.length && stack[stack.length - 1].level >= e.level) stack.pop();
  const node = { id: e.id, text: e.text, children: [] };
  if (stack.length) stack[stack.length - 1].node.children.push(node);
  else tree.push(node);
  stack.push({ level: e.level, node });
}
```

### 4. HTML 渲染改为递归函数

```js
function renderTree(nodes, level) {
  return nodes.map(n => {
    const href = `$${encodeURIComponent(n.id)}`;
    const link = `<a href="${href}">${escapeHtml(n.text)}</a>`;
    const cls = `toc-h${level}`;
    if (n.children.length === 0) {
      return `<div class="${cls}">${link}</div>`;
    }
    return `<details class="toc-section" open>
      <summary>${link}</summary>
      <div class="toc-children">
        ${renderTree(n.children, level + 1)}
      </div>
    </details>`;
  }).join('');
}
const html = renderTree(tree, 2);
```

h2→`toc-h2`，h3→`toc-h3`，h4→`toc-h4`，层级不对应标签名但对应实际嵌套深度，以保证折叠展开的交互一致性。

### 5. CSS 追加 `.toc-h4`

```css
.toc-h4 { font-size: .8em; margin: .08em 0; padding-left: 1.6em; }
.toc-h4 a { font-weight: 400; }
.toc-h4.toc-current > a { color: var(--accent); }
```

同时将 `.toc-children` 的选择器改为通用匹配，使其能作用于任意深度的子容器。

### 不修改的范围

- `generate_toc.py` — server 端 TOC 生成独立，不在本 RFC 范围内
- Scrollspy — 已用通用 `a[href^="$"]` 选择器，自动支持新层级
- 侧栏布局 — 不涉及

## 受影响的文件

| 文件 | 改动 |
|------|------|
| `memex/wiki/public/plugins/toc/index.js` | 选择器、映射、树算法、渲染函数 |
| `memex/wiki/public/css/sidebar.css` | 追加 `.toc-h4` 样式 |

## 建议实施

1. 先在 toc/index.js 中重构树构建和渲染（纯 JS 改动，可立即测试）
2. 验证 h1-h4 页面 TOC 渲染正确
3. 再补 CSS 样式

## Implementation

**Review**: faithful
**Date**: 2026-05-26
**Commits**:
- baojie/memex@a637958: feat(toc): 支持 h1-h4 多级标题 + 层级缩进
