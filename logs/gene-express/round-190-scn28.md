---
round: 190
date: 2026-05-26
gene: SCN28
pages: []
type: discover
result: accept
---

## 执行摘要

R190 P2 SCN28 从 ch13（技术与发明）发掘 6 个新候选，补充逐渐枯竭的队列。ch13 以菲斯托斯圆盘为引，讨论了技术发明的地域差异、接受新技术的文化因素，以及技术创新在各大陆的不平衡分布。

## 新候选列表

| 候选 | 类型 | 优先级 | 原因 |
|------|------|--------|------|
| 弥诺斯文明 | event | P1 | 多章（ch12/ch13/ch16），克里特岛青铜时代文明 |
| 塔斯马尼亚 | place | P1 | 多章（ch09/ch13/ch15/ch18/ch20），技术孤岛案例 |
| 水磨 | concept | P1 | 多章（ch13/ch20），早期技术案例 |
| 纳瓦霍人 | person | P1 | 多章（ch09/ch13/ch18），技术接受力的族群案例 |
| 菲斯托斯圆盘 | concept | P2 | ch13，早期印刷技术与未解之谜 |
| 阿基米德 | person | P2 | ch13，古代天才发明家案例 |

## 决策矩阵（R190）

- P1a EVV5+SCN28: rounds_since_last_evv5=7 < 10 → skip
- P1b EVV5: rounds_since_last_evv5=7 < 10 → skip
- P2 SCN28: 队列剩 6 候选，低于阈值 10 → **已执行**
- P3 W5: rounds_since_last_w5=3 < 29 → skip
- P4 enrich: enrich_count=3 ≥ 3 → skip（已达上限）
- P5 RFT: rft_count=0 < 2 → 可触发（候选不足）
- P6 QRY2: qry2_count=2 ≥ 2 → skip
- P8 NEW1: new1_count=5 > 3 → skip

## 队列状态

新增 6 候选后队列共 12 个候選（含 6 个 ch13 新候选 + 6 个现存候选）。队列恢复至正常水位。

## EXIT-GATE 检查

全部 PASS。

## 状态更新

- current_round: 190 → 191
- rounds_since_last_evv5: 7 → 8
- rounds_since_last_discover: 9 → 0（重置）
- rounds_since_last_w5: 3 → 4
- last_10_genes: pop "SCN28" → push "SCN28"
- new1_count_window: 5（不变）
- enrich_count_window: 3（不变）
- qry2_count_window: 2（不变）

## 下轮预测

R191 决策：
- P1a EVV5+SCN28: rounds_since_last_evv5=8 < 10 → skip（接近 10）
- P1b EVV5: rounds_since_last_evv5=8 < 10 → skip
- P2 SCN28: 刚执行 → skip
- P3 W5: rounds_since_last_w5=4 < 29 → skip
- P4 enrich: enrich_count=3 ≥ 3 → skip
- P5 RFT: rft_count=0 < 2 → **可触发**（候选不足）
- P6 QRY2: qry2_count=2 ≥ 2 → skip
- P7 stub: 可触发（现有 4 个 P2 stub 候选）
- P8 NEW1: new1_count=5 > 3 → skip

建议：下轮 P8 NEW1 消费队列，或 R191 待 EVV5 在 R192 达标时执行 EVV5+SCN28。
