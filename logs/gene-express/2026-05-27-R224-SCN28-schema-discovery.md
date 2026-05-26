---
round: 224
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

# Round 224 — SCN28

- **Date**: 2026-05-27
- **Gene**: SCN28
- **Trigger**: P2 SCN28（queue_size=7 < discover_queue_threshold=10）

## Phase 1 — 红链扫描

无新候选（所有红链已在 queue 中）。

## Phase 2 — LLM 章节发现

源：ch06《种田还是不种田》

通过 Phase 3 过滤的候选（5 个）：

| 候选 | 类型 | corpus 命中 | 说明 |
|------|------|------------|------|
| 长颈鹿 | species | 4 | 猎人动机分析案例 |
| 利尼尔班克拉米克文化 | concept | 2 | LBK 新石器文化 |
| 西谷椰子 | species | 6 | 新几内亚半管理作物 |
| 阿帕切族 | person | 1 | 美国西南部游牧农业 |
| 科罗拉多河 | place | 1 | 北美河流，族群接触边界 |

## New Queue Items

5 items added to queue.md (P2 stub, ch06).
