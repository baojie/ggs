---
round: 228
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

# Round 228 — SCN28

- **Date**: 2026-05-27
- **Gene**: SCN28
- **Trigger**: P2 SCN28（queue_size=8 < discover_queue_threshold=10）

## Phase 1 — 红链扫描

无新候选（所有红链已在 queue 中）。

## Phase 2 — LLM 章节发现

源：ch07《怎样识别杏仁》

通过 Phase 3 过滤的候选（5 个）：

| 候选 | 类型 | corpus 命中 | 说明 |
|------|------|------------|------|
| 橡树 | species | 8 | 未驯化坚果树的典型案例，因生长缓慢和松鼠竞争而失败 |
| 兵豆 | species | 5 | 新月沃地最早驯化的豆类之一，谷物-豆类组合的核心 |
| 鹰嘴豆 | species | 3 | 新月沃地驯化，起源土耳其东南部 |
| 大麻 | species | 4 | 古代重要纤维作物，茎纤维制绳织布 |
| 向日葵 | species | 8 | 美洲东部驯化的特有油料作物 |

## New Queue Items

5 items added to queue.md (P1 create, ch07).
