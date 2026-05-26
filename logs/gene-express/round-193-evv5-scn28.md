---
round: 193
date: 2026-05-26
gene: EVV5+SCN28
pages:
  - 闪米特人
  - 安娜卡列尼娜原则
  - 欧洲
  - 地理
  - 畜牧业
type: enrich+discover
result: accept
---

## 执行摘要

R193 P1a EVV5+SCN28：EVV5 质量评估 enrich 5 页（闪米特人、安娜·卡列尼娜原则、欧洲、地理、畜牧业），SCN28 从 ch14（从平等主义到盗贼统治）发掘 6 个新候选。

## EVV5 enrich 详情

| 页面 | 变化 | enrich 量 |
|------|------|-----------|
| 闪米特人 | 重组内容，强调闪米特人在字母诞生中的关键作用和字母传播路线 | +1126B |
| 安娜卡列尼娜原则 | 补充驯化必要条件和戴蒙德方法论的角色 | +1210B |
| 欧洲 | 补充欧洲三重地理优势和病菌优势分析 | +1193B |
| 地理 | 补充戴蒙德地理方法论和波利尼西亚微观证据 | +420B |
| 畜牧业 | 剪裁冗余表达，补充可驯化动物分布数据 | -261B |

## 决策矩阵

- P1a EVV5+SCN28: rounds_since_last_evv5=10 ≥ 10 AND rounds_since_last_discover=2 ≥ 0 → **已执行**
- P1b EVV5: 同上，合并执行
- P2 SCN28: 队列剩 2 候选，低于阈值 10 → **已执行**
- P3 W5: rounds_since_last_w5=6 < 29 → skip
- P4 enrich: enrich_count=3 ≥ 3 → skip（已达上限）
- P5 RFT: rft_count=0 < 2 → 可触发（候选不足）
- P6 QRY2: qry2_count=2 ≥ 2 → skip

## 新候选列表（SCN28 ch14）

| 候选 | 类型 | 优先级 | 原因 |
|------|------|--------|------|
| 大人物 | concept | P1 | 多章（ch03/ch14/ch15），新几内亚部落政治制度 |
| 福雷人 | person | P1 | 多章（ch08/ch11/ch14），库鲁病相关族群 |
| 伦纳尔岛 | place | P1 | 多章（ch02/ch14/ch17），波利尼西亚酋长制案例 |
| 氏族 | concept | P2 | ch14，社会组织基本单位 |
| 盗贼统治 | concept | P2 | ch14，集中社会财富的上层统治 |
| 伊努特人 | person | P2 | ch14，北极狩猎采集族群 |

## 队列状态

新增 6 候选后队列共 8 个候選（含 6 个 ch14 新候选 + 冰川 + 安娜-卡列尼娜原则深链）。队列恢复至接近正常水位。

## EXIT-GATE 检查

全部 PASS。

## 状态更新

- current_round: 193 → 194
- rounds_since_last_evv5: 10 → 0（重置）
- rounds_since_last_discover: 2 → 0（重置）
- rounds_since_last_w5: 6 → 7
- last_10_genes: pop "NEW1" → push "EVV5+SCN28" → [EVV5+SCN28, QRY2, NEW1, NEW1, W5-REFLECT, ENRICH, ENRICH, QRY2, SCN28, NEW1]

## 下轮预测

R194 决策：
- P1a EVV5+SCN28: rounds_since_last_evv5=0 < 10 → skip
- P1b EVV5: rounds_since_last_evv5=0 < 10 → skip
- P2 SCN28: 刚执行 → skip
- P3 W5: rounds_since_last_w5=7 < 29 → skip
- P4 enrich: enrich_count=3 ≥ 3 → skip
- P5 RFT: rft_count=0 < 2 → 可触发
- P6 QRY2: qry2_count=2 ≥ 2 → skip
- P8 NEW1: new1_count=4 > 3 → skip（已达 rolling_max 3）
