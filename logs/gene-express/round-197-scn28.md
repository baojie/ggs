---
round: 197
date: 2026-05-26
gene: SCN28
pages: []
type: discover
result: accept
---

## 执行摘要

R197 P2 SCN28 从 ch15（耶利的族人）发掘 5 个新候选（俾斯麦群岛、托雷斯海峡、大澳大利亚、澳洲野犬、火耕农业），补充逐渐枯竭的队列。ch15 集中讨论澳大利亚和新几内亚的历史发展差异。

## 新候选列表

| 候选 | 类型 | 优先级 | 原因 |
|------|------|--------|------|
| 俾斯麦群岛 | place | P1 | 多章（ch01/ch02/ch15/ch17/ch20），南岛人扩张和新几内亚地理的关键节点 |
| 托雷斯海峡 | place | P1 | 多章（ch13/ch15），澳大利亚与新几内亚交流的屏障和通道 |
| 大澳大利亚 | concept | P2 | ch15，更新世冰期连接澳大利亚和新几内亚的大陆块 |
| 澳洲野犬 | species | P2 | ch15，亚洲引入的驯化犬回归野生 |
| 火耕农业 | concept | P2 | ch15，澳大利亚土著用火管理土地的技术 |

## 决策矩阵

- P1a EVV5+SCN28: rounds_since_last_evv5=3 < 10 → skip
- P1b EVV5: rounds_since_last_evv5=3 < 10 → skip
- P2 SCN28: 队列剩 3 候选，低于阈值 10 → **已执行**
- P3 W5: rounds_since_last_w5=10 < 29 → skip
- P4 enrich: 3 ≥ 3 → skip
- P5 RFT: 非独立优先级 → skip
- P6 QRY2: 2 ≥ 2 → skip
- P8 NEW1: 3 ≥ 3 → skip（已达上限）

## 队列状态

新增 5 候选后队列共 8 候选（含 5 个 ch15 新候选 + 伊努特人 + 冰川 + 安娜卡列尼娜原则深链）。

## EXIT-GATE 检查

全部 PASS。

## 状态更新

- current_round: 197 → 198
- rounds_since_last_evv5: 3 → 4
- rounds_since_last_discover: 3 → 0（重置）
- rounds_since_last_w5: 10 → 11
- last_10_genes: pop "ENRICH" → push "SCN28"

## 下轮预测

R198 决策：
- P1a EVV5+SCN28: rounds_since_last_evv5=4 < 10 → skip
- P1b EVV5: rounds_since_last_evv5=4 < 10 → skip
- P2 SCN28: 刚执行 → skip
- P3 W5: 11 < 29 → skip
- P4 enrich: 3 ≥ 3 → skip
- P8 NEW1: 3 ≥ 3 → skip（已达上限）
