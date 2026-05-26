---
round: 222
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

# Round 222 — SCN28

- **Date**: 2026-05-27
- **Gene**: SCN28
- **Trigger**: P2 SCN28（queue_size=7 < discover_queue_threshold=10）

## Phase 1 — 红链扫描

0 个新候选（R220 已扫描，无新增红链）。

## Phase 2 — LLM 章节发现

源：ch09《斑马、不幸的婚姻和安娜·卡列尼娜原则》

通过 Phase 3 过滤的候选（5 个）：

| 候选 | 类型 | corpus 命中 | 说明 |
|------|------|------------|------|
| 灰熊 | species | 3 | 危险动物驯化案例 |
| 袋鼠 | species | 7 | 新几内亚宠物/食物 |
| 鸵鸟 | species | 3 | 大型鸟类 |
| 西貒 | species | 2 | 未驯化的美洲偶蹄类 |
| 鹤鸵 | species | 2 | 新几内亚大型鸟 |

Phase 3 跳过项：白鼬(1hit), 狒狒(1hit), 驼鹿(通用名), 鬣狗(旁证)

## New Queue Items

5 items added to queue.md (P2 stub, ch09).
