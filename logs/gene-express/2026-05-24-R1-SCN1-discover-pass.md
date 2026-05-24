---
round: 1
date: 2026-05-24
gene: SCN1-discover
pages: []
result: pass
---

## 执行摘要

首轮 butler 试跑（8-G）。运行 `discover_wanted.py --pages docs/wiki/pages --top 30`，扫描全库 broken wikilinks。发现 21 条 wikilink 引用（来自目录.md），全部指向已注册章节页（Preface/ch01-ch19/Epilogue），净新待建词条 0 条。queue.md 无新增。

## 页面处理记录

| 页面 | 操作 | 结果 | 备注 |
|------|------|------|------|
| （无） | discover scan | pass | 21 条 wikilink 均为已有页面，无新实体 |

## 遗留问题

- `discover_wanted.py` 将目录.md 中指向已有章节页的 wikilink 报为 "wanted"，疑为脚本对 pages.json 查找逻辑问题，待后续排查
- 下轮应使用语料频率扫描挖掘实体词条（concept/person/place/species），而非仅依赖 broken wikilink 检测
