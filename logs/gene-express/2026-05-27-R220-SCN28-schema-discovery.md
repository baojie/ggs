---
round: 220
phase: "5"
gene: SCN28
result: accept
---

## EXIT-GATE 检查

**G1 优先检查（失败立即回滚）：**

| 门 | 结果 | 问题与处置 |
|----|------|---------|
| G1 内容完整性 | PASS | — |

**G2 核心格式检查：**

| 编号 | 检查项 | 结果 |
|------|--------|------|
| E1 | frontmatter 结构完整 | PASS |
| E2 | 质量档位达标 | PASS |
| E3 | 必填字段内容非空 | PASS |
| E4 | 标题无 wikilink | PASS |
| E5 | PN 引注有效性 | PASS |
| E6 | 正文规范 | PASS |
| E7 | blockquote 有 PN | PASS |

# Round 220 — SCN28

- **Date**: 2026-05-27
- **Gene**: SCN28
- **Trigger**: P2 SCN28（queue_size=6 < discover_queue_threshold=10）

## Phase 1 — 红链扫描

```bash
python3 $MEMEX_ROOT/wiki/scripts/butler/discover_wanted.py --top 60
```

结果：37 个待建词条（含 22 个章节 slug + 7 个已有页面），经 Phase 3 反思后保留 5 个。

## Phase 3 — 候选反思

| 候选 | 类型 | 红链 | corpus 命中 | 决策 | 原因 |
|------|------|------|------------|------|------|
| 南方古猿 | concept | 1 | 1 | 跳过 | corpus 仅 1 次命中 |
| 所罗门群岛 | place | 1 | 10 | 保留 | — |
| 乌鲁克 | place | 1 | 2 | 保留 | — |
| 周朝 | event | 1 | 2 | 保留 | — |
| 苹果 | species | 1 | 10 | 保留 | — |
| 杏仁 | species | 1 | 8 | 保留 | — |
| 欧洲人 | person | 1 | — | 跳过 | 通用词 |
| 卡哈马卡的冲突 | event | 1 | — | 跳过 | 已有 卡哈马卡之战 |
| 首领 | concept | 1 | — | 跳过 | 通用词 |
| 不平等 | concept | 1 | — | 跳过 | 通用词 |
| 激励机制 | concept | 1 | — | 跳过 | 通用词 |
| 比较方法 | concept | 1 | 0 | 跳过 | corpus 无命中 |
| 松鼠 | species | 1 | — | 跳过 | 随机出现 |

## New Queue Items

5 items added to queue.md (P2 stub):
- 所罗门群岛, 乌鲁克, 周朝, 苹果, 杏仁
