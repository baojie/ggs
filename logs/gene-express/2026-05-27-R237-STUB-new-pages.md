# R237 STUB — 新建存根页

- **日期**: 2026-05-27
- **触发**: P7 STUB（所有主要基因饱和：NEW1=3/3, ENRICH=4/3, QRY2=2/2, RFT 无候补）
- **基因**: STUB
- **操作**: 新建 5 个 stub 页面，清理队列

## 新建存根页

| 页面 | slug | type | 大小 | 来源 |
|------|------|------|------|------|
| 科罗拉多河 | ke-luo-la-duo-he | place | 701B | ch06 SCN28 R224 |
| 阿帕切族 | a-pa-qie-zu | person | 684B | ch06 SCN28 R224 |
| 恒河平原 | heng-he-ping-yuan | place | 879B | ch10 SCN28 R235 |
| 葫芦 | hu-lu | species | 684B | ch10 SCN28 R235 |
| 文化特质 | wen-hua-te-zhi | concept | 818B | ch20 SCN28 R215 |

## 决策矩阵

| 优先级 | 基因 | 判定 |
|--------|------|------|
| P1a | EVV5+SCN28 | evv5=0 < 10 → 跳过 |
| P1b | EVV5 | 同上 |
| P2 | SCN28 | discover=1, queue≈7>10 → 跳过 |
| P3 | W5 | 20 < 29 → 跳过 |
| P4 | ENRICH | enrich=4 > 3 → 饱和 |
| P5 | RFT | 可用但无适合页面 |
| P6 | QRY2 | qry2=2 = max → 饱和 |
| **P7** | **STUB** | **无上限 → 已执行** |
| P8 | NEW1 | new1=3 = max → 饱和 |

## 状态更新

- current_round: 237→238
- rounds_since_last_evv5: 0→1
- rounds_since_last_discover: 1→2
- rounds_since_last_w5: 20→21
- last_10_genes: shift → push "STUB"
- new1_count_window: 3→2（旧 NEW1 出窗）

## 下轮预测

R238 后 new1_count_window 将降至 2，NEW1 基因可用：
- P1a EVV5+SCN28: evv5=1 < 10 → skip
- P2 SCN28: discover=2, queue≈7 < 10 → 可能触发
- P4 ENRICH: enrich=4 > 3 → 仍饱和
- P8 NEW1: new1=2 < 3 → 可用

建议：NEW1 从队列新建 basic 页面
