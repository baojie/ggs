# RFC-ggs-0024: backfill_recent.py 应与 v2 历史格式保持一致

- **Status**: implemented
- **Date**: 2026-05-25
- **Issue**: https://github.com/baojie/memex/issues/162
- **Source wiki**: ggs
- **Target**: `$MEMEX_ROOT/wiki/scripts/backfill_recent.py`

---

## Problem

`backfill_recent.py` 从 git 历史回填修订记录时，固定使用 v0 格式写入 `recent.lite.jsonl`、`recent.diff.jsonl` 和 `history/<page>.jsonl`：

```python
def rev_id(ts_str, content):
    return f"{dt.strftime('%Y%m%d-%H%M%S')}-{sha[:6]}"  # v0 格式
```

而 `record_revision.py --format v2`（默认）则使用 base62 短 hash 作为 `rev_id`（如 `nuNLWJ`）。导致同一份 `recent.diff.jsonl` 中两种格式并存（约 288 条 v1 + 207 条 v2），`recent.lite.jsonl` 同样如此。

## Root cause

`backfill_recent.py` 在实现时未同步采用 v2 格式（`record_revision.py` 于 commit 16c8465 默认改为 v2 line-hash，但 backfill 未跟进）。

## Current v2 format conventions

### 1. rev_id 格式

v2 使用 base62(sha256[:6]) 的 6 位短 hash：

```python
_BASE62 = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
def _base62_id(sha256_hex: str) -> str:
    return _hex_to_base62(sha256_hex)[:6]
```

### 2. History 条目格式

**snap 条目**（每 26 个 delta 插入一个全量快照）：

| 字段 | 含义 |
|------|------|
| `v` | 版本号（恒为 2） |
| `t` | 类型（`"snap"`） |
| `id` | rev_id（base62 6 位） |
| `ts` | Unix 时间戳（整数） |
| `au` | 作者 |
| `su` | summary 的 line hash |
| `sz` | 内容字节数 |
| `lc` | 行数 |
| `ln` | 所有行的 line hash（空格分隔） |

**delta 条目**：

| 字段 | 含义 |
|------|------|
| `v` | 版本号（恒为 2） |
| `t` | 类型（`"delta"`） |
| `id` | rev_id（base62 6 位） |
| `ts` | Unix 时间戳（整数） |
| `au` | 作者 |
| `su` | summary 的 line hash |
| `sz` | 内容字节数 |
| `lc` | 行数 |
| `parent` | 父修订的 id |
| `szb` | 父修订的字节数 |
| `la` | 新增行数 |
| `lr` | 删除行数 |
| `dl` | delta 操作列表：`["del", index]` 或 `["ins", index, line_hash]` |

### 3. line_index 文件

位于 `docs/wiki/line_index/`，JSONL 文件，记录 line hash 到原文的映射：

```json
{"h": "Mcb6if", "l": "原文内容"}
```

只追加新 hash，不做全量重建。

### 4. recent.lite.jsonl 条目

使用 v0 风格的字段名（`rev_id`/`timestamp`/`author`/`summary`）：

| 字段 | 说明 |
|------|------|
| `page` | 页面 ID |
| `label`（可选）| 页面显示标签 |
| `rev_id` | rev_id（v2 为 base62 6 位） |
| `timestamp` | ISO 8601 时间戳 |
| `author` | 作者 |
| `summary` | 修订摘要 |
| `size_before` / `size` | 修改前/后字节数 |
| `diff_add` / `diff_del` | 新增/删除行数 |

### 5. recent.diff.jsonl 条目

v2 模式下 diff 文本替换为 line hash：

```json
{"page": "...", "rev_id": "nuNLWJ", "diff": [["+", "hash"], ["-", "hash"]]}
```

JS 端通过 `resolveLineHash(hash)` 解析回原文。

## Proposed change

### A. backfill_recent.py 改为 v2 格式输出

1. **复用 record_revision.py 的函数**（提取为共享模块，或直接 import）：
   - `_base62_id(sha)` → rev_id
   - `_line_hash(line, regs)` → line hash
   - `_compute_delta` / `_apply_delta`
   - `_load_registries` / `SNAP_INTERVAL`

2. **history 文件写入逻辑**：
   - 读取已有 entries 确定 last entry（兼容 v0/v2）
   - 按 `SNAP_INTERVAL` 决定 snap/delta
   - 写入 v2 格式条目 + 更新 line_index

3. **recent.lite.jsonl**：包含 `label` 字段，省略 `parent_rev`/`content_hash`

4. **recent.diff.jsonl**：diff 使用 line hash

### B. 函数抽取

将 v2 核心函数从 `record_revision.py` 抽取到共享模块（如 `wiki/scripts/v2_history.py`），供两个脚本共同使用。

### C. 测试

在 `wiki/tests/` 下创建 `test_backfill_recent.py`：

1. **单元测试**：rev_id 格式、line hash 一致性、snap/delta 结构
2. **集成测试**：临时 git 仓库 → 运行 backfill → 验证输出格式与 `record_revision.py --format v2` 一致

## Implementation notes

- backfill 从 git 获取完整快照，snap 的 `ln` 通过 `_line_hash` 逐行计算，delta 通过 `_compute_delta` 计算
- 已有 v1 条目不需迁移——随滚动窗口自然淘汰，且 diff/index.js 兼容双格式

## Implementation

**Review**: faithful
**Date**: 2026-05-25
**Commits**:
- baojie/memex@43f74705418f721e3d8f499139fa18042dee1229: feat(ggs): implement RFC-ggs-0024 — backfill_recent.py v2 格式对齐
