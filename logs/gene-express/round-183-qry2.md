---
round: 183
date: 2026-05-26
phase: "5"
gene: QRY2
list_type: most-referenced
pages: [被引用最多页面]
result: accept
window_snapshot: "2N/2E/1L/0R"
---

## 执行摘要

P6 QRY2 命中 — `qry2_count_window`(0) < 1。新建「被引用最多页面」query 聚合页，以 `::: query` 块列出全库引用数最高的 50 个词条。

## 决策矩阵评估

| 优先级 | 条件 | 评估 | 结论 |
|--------|------|------|------|
| P1a | evv5(0) ≥ interval(10) 且 discover到期 | 均不满足 | — |
| P1b | evv5(0) ≥ interval(10) | 不满足 | — |
| P2 | discover(2) ≥ 10？queue(131) < 10？ | 均不满足 | — |
| P3 | w5(26) ≥ w5_interval(29)？ | 不满足 | — |
| P4 | new1_window(3) > rolling_max(3)？ | 不满足(相等) | — |
| P5 | rft_window(0) < max(2) 且长页候选存在？| 无 >1500 字长页 | — |
| **P6** | **qry2_window(0) < 1？** | **满足** | **→ QRY2** |
| P7 | stub% ≥ 15%？ | 0% | — |
| P8 | 默认 | 兜底 | — |

## 页面处理记录

| 页面 | 操作 | 结果 | 备注 |
|------|------|------|------|
| 被引用最多页面 | QRY2 create | accept | query 聚合页，total_refs 排序 Top 50 |

## 后置检查

| 检查 | 结果 |
|------|------|
| QRY3 lint | PASS（无 error） |
| query 渲染非空 | ✓（全库 497 词条，total_refs 有值） |
| 无硬编码词条列表 | ✓（::: query 为主体） |
| 引言无无据断言 | ✓ |
| frontmatter 完整 | ✓ |
| 质量档位 basic | ✓ |
