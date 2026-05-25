# RFC-ggs-0027: backfill_recent.py 忽略分桶结构，将 history 文件写入平铺路径

- **Status**: proposed
- **Date**: 2026-05-25
- **Issue**: https://github.com/baojie/memex/issues/169
- **Source wiki**: ggs
- **Target**: wiki/scripts/backfill_recent.py

---

## Problem

`backfill_recent.py` 在读写 per-page history 文件时，始终使用平铺路径
`history/<slug>.jsonl`，而没有镜像 `pages/` 目录的分桶结构。

当页面文件已按前两字符分桶存放（如 `pages/zh/中国.md`），正常路径
`record_revision.py` 会正确写入 `history/zh/中国.jsonl`；但若随后执行
`backfill_recent.py`，则会在 `history/中国.jsonl`（平铺路径）创建第二份
history 文件，导致同一页面存在两份 history，修订记录被分裂。

在 ggs wiki 中，Phase 9-E 执行 `backfill_recent.py` 时，pages 已全部分桶，
因此产生了 100 个平铺的 `.jsonl` 文件与已有的分桶版本并存。

## Root cause

`backfill_recent.py` 中两处路径构造均使用裸 slug 拼接：

```python
# 读：load_existing_history()
p = HIST / f"{page}.jsonl"          # 忽略分桶，应为 HIST / bucket / f"{page}.jsonl"

# 写：主循环末尾
p = hist_dir / f"{page}.jsonl"      # 同上
```

而 `record_revision.py` 的正确做法是：

```python
rel = src.relative_to(pages_dir)           # 如 zh/中国.md
page_jsonl = hist_dir / rel.with_suffix(".jsonl")  # → history/zh/中国.jsonl
```

`backfill_recent.py` 未调用 `find_page_file()` 来获取页面的实际路径，
也未用 `relative_to(pages_dir)` 推算带 bucket 的 history 路径。

## Proposed change

在 `backfill_recent.py` 中，将 history 路径构造逻辑改为与 `record_revision.py`
保持一致：通过 `find_page_file(page, PAGES)` 获取页面文件的实际路径，
再用 `src.relative_to(PAGES)` 推算出带分桶的 history 路径。

```python
# 修复 load_existing_history()
def load_existing_history(page: str) -> list[dict]:
    src = find_page_file(page, PAGES)
    if src is None:
        return []
    rel = src.relative_to(PAGES)
    p = HIST / rel.with_suffix(".jsonl")
    ...

# 修复写入路径
rel = find_page_file(page, PAGES).relative_to(PAGES)
p = hist_dir / rel.with_suffix(".jsonl")
p.parent.mkdir(parents=True, exist_ok=True)
```

同时建议提供一次性迁移脚本，将现有平铺 history 文件的内容合并至对应
分桶路径后删除，避免历史记录继续分裂。
