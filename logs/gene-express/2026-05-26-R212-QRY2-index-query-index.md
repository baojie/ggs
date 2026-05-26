---
round: 212
phase: "5"
gene: QRY2
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

| E9 | QRY2 后置：wikilink 无悬空，覆盖率 ≥ 80% | PASS |


# Round 212 — QRY2

- **Date**: 2026-05-26
- **Grow phase**: 5
- **Decision**: P6 QRY2（enrich 饱和、new1 饱和、qry2 可用）

---

## 新建 Query 聚合页

| 页面 | slug | 大小 | 说明 |
|------|------|------|------|
| 引用排行 | yin-yong-pai-hang | 1977B | 按 total_refs 聚合展示所有类型词条，含 Top 50 总榜 + 各类型 Top 30 |

### 页面结构

- 跨领域高频词条 Top 50（按 total_refs 降序）
- 概念 Top 30、人物 Top 30、地点 Top 30、物种 Top 30、事件 Top 30

---

## 决策矩阵

- P1a EVV5+SCN28: rounds_since_last_evv5=7 < 10 → skip
- P1b EVV5: 同上 → skip
- P2 SCN28: queue ~15 ≥ 10 → skip
- P3 W5: rounds_since_last_w5=25 < 29 → skip
- P4 ENRICH: enrich_count=3 ≥ 3 → 饱和
- P5 RFT: rft_count=0 < 2 → 可触发（非独立）
- P6 QRY2: qry2_count=1 < 2 → **已执行**
- P7 STUB: 备选（QRY2 优先）
- P8 NEW1: new1_count=3 ≥ 3 → 饱和

---

## 状态更新

- current_round: 212→213
- rounds_since_last_evv5: 7→8
- rounds_since_last_discover: 2→3
- rounds_since_last_w5: 25→26
- last_10_genes: pop "NEW1" → push "QRY2"
- qry2_count_window: 1→2
- new1_count_window: 3→2

---

## 下轮预测

R213 决策：
- P1a EVV5+SCN28: rounds_since_last_evv5=8 < 10 → skip
- P2 SCN28: queue ~15 ≥ 10, rounds_since_last_discover=3 < 10 → skip
- P3 W5: rounds_since_last_w5=26 < 29 → skip
- P4 ENRICH: enrich_count=3 ≥ 3 → 饱和
- P6 QRY2: qry2_count=2 ≥ 2 → 饱和
- P7 STUB: available（无 rolling max）
- P8 NEW1: new1_count=2 < 3 → **available**
- 可能路径：P7 STUB 或 P8 NEW1
