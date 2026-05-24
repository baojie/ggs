# RFC-ggs-0023: 首页知识量面板隐藏 K 值

- **Status**: implemented
- **Date**: 2026-05-25
- **Issue**: https://github.com/baojie/memex/issues/159
- **Source wiki**: ggs
- **Target**: `$MEMEX_ROOT/wiki/public/plugins/home/index.js`（k-panel 注入段）

---

## Problem

首页底部的知识量面板（k-panel）显示一个大号数字如 `1,103`（K 值），但没有说明该数字的含义。对普通浏览者而言，这是一个令人费解的统计数字：

```
知识量
1,103
[sparkline]
39 页 · 0 premium · 链接命中 100% · 1037.2 KB
```

K 值是内部质量评分，对外展示没有实际意义。用户在首页不需要看到这个数字。

## Proposed change

删除 k-panel 中 K 值的显示，保留面板其他信息（页面数、premium 数、链接命中率、大小）。

具体改动：在 `home/index.js` 的 `injectKPanel` 函数中，将：

```html
<h3>
  <a href="#Special:Statistics" class="k-title-link">知识量</a>
  <span class="k-value">${(latest.K ?? '?').toLocaleString()}</span>
  ${sparkline}
</h3>
```

改为：

```html
<h3>
  <a href="#Special:Statistics" class="k-title-link">知识量</a>
  ${sparkline}
</h3>
```

即移除 `<span class="k-value">` 元素。不影响 Special:Statistics 统计页的 K 值显示（那是另一个渲染路径）。

## Implementation notes

仅修改首页 k-panel 的 K 值渲染，不涉及数据采集或统计页。

## Implementation

**Review**: faithful
**Date**: 2026-05-25
**Commits**:
- baojie/memex@2a20616684b5e7cb822e82acf83b32417607aeaa: fix(home): 首页 k-panel 隐藏 K 值数字——内部评分对外无意义
