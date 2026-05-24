# RFC-ggs-0021: router.js `?pn=` 正则未匹配 `P\d{2}` 前缀导致 404

- **Status**: proposed
- **Date**: 2026-05-25
- **Source wiki**: ggs
- **Target**: `$MEMEX_ROOT/wiki/public/js/router.js`
- **Issue**: https://github.com/baojie/memex/issues/157

---

## Problem

点击 wiki 页面中的 pn 引用链接（如 `（P03-064）`），生成的 URL 形如 `#Preface?pn=P03-064`，但路由器报 "Page Preface?pn=P03-064 not found"。

## Root cause

pn-citation 插件（`pn-citation/index.js:61`）生成 href 时不区分 NNN 前缀格式：

```js
const href = `#${encodeURIComponent(pageId)}?pn=${pn}`;
```

其中 `pn = "${nnn}-${ppp}"`，`nnn` 可以是 `074`（纯数字）或 `P03`（带 `P` 前缀）。`chapter_map.json` 中确实有 `P01`、`P02`、`P03` 等 key。

路由器 `router.js:40-46` 提取 `?pn=` 参数后，用正则校验其格式：

```js
// 当前：只能匹配纯数字 3+3 位 NNN
if (/^\d{3}-\d{3}$/.test(pnVal)) {
```

`P03-064` 带 `P` 前缀不通过校验 → `pendingPN` 保持 `null` → `cleanHash` 未被裁剪 → 整个 `"Preface?pn=P03-064"` 被当页面 ID → 404。

根本原因：`router.js:43` 的正则 `/^\d{3}-\d{3}$/` 过于严格——仅支持 3 位数字章号 + 3 位数字段号。而 `pn_patterns.py` 定义的完整 PN 格式为：

- 章号：`\d{3,4}`（3-4 位数字）或 `P\d{2}`（P + 2 位）
- 段号：`\d{3,4}`（3-4 位数字）
- 子段：`-\d{3}`（可选）

## Proposed change

将 `router.js:43` 的正则替换为覆盖全部格式：

```js
// 修改前
if (/^\d{3}-\d{3}$/.test(pnVal)) {

// 修改后
if (/^(?:\d{3,4}|P\d{2})-\d{3,4}(?:-\d{3})?$/.test(pnVal)) {
```

匹配规则变化：

| 输入 | 原正则 | 新正则 | 说明 |
|------|--------|--------|------|
| `074-007` | ✓ | ✓ | 3+3 位 |
| `074-0123` | ✗ | ✓ | 段号 4 位 |
| `0123-045` | ✗ | ✓ | 章号 4 位 |
| `P03-064` | ✗ | ✓ | P 前缀 |
| `P03-0999` | ✗ | ✓ | P 前缀 + 段号 4 位 |
| `074-005-001` | ✗ | ✓ | 含子段 |

### 同一文件中的关联代码

`router.js:183` 已有 `P0[1-9]` 支持（锚点回落处理），但使用更窄的 `P0[1-9]` 而非 `P\d{2}`。建议一并统一为 `P\d{2}` 以免 `P10+` 出现时再次遗漏。不过当前 `chapter_map` 只有 `P01-P03`，此问题不在本 RFC 范围内，可后续单独处理。

## Implementation notes

仅修改 `router.js` 一行正则表达式，不涉及其他文件。`pn-citation` 插件本身无需改动。

发布后需清除浏览器缓存（Service Worker 可能缓存旧版 router.js）。
