# R239 STUB — 新建存根页

- **日期**: 2026-05-27
- **触发**: P7 STUB（P5 RFT 无适合页面，P6 QRY2 增量有限——基础类型索引已存在）
- **基因**: STUB
- **操作**: 新建 5 个 stub 页面，清理队列

## 决策矩阵

| 优先级 | 基因 | 判定 |
|--------|------|------|
| P1a | EVV5+SCN28 | evv5=3 < 10 → 跳过 |
| P1b | EVV5 | 同上 |
| P2 | SCN28 | discover=0, queue≈12 > 10 → 跳过 |
| P3 | W5 | 23 < 29 → 跳过 |
| P4 | ENRICH | enrich=3 = max → 刚好饱和（本轮后降为 3）|
| P5 | RFT | 可用但无适合页面 |
| P6 | QRY2 | 基础类型索引页已存在，增量有限 |
| **P7** | **STUB** | **无上限 → 已执行** |
| P8 | NEW1 | new1=2 < 3 → 可用 |

## 新建存根页

| 页面 | slug | type | 大小 | 来源 |
|------|------|------|------|------|
| 亨德森岛 | heng-de-sen-dao | place | 1108B | ch02 SCN28 R238 |
| 回溯试验法 | hui-su-shi-yan-fa | concept | 981B | ch20 SCN28 R215 |
| 菲什河 | fei-shi-he | place | 1185B | ch06/10/19 SCN28 R235 |
| 塞伦格蒂 | sai-lun-ge-di | place | 1190B | ch01/10/19 SCN28 R235 |
| 爪哇人 | zhao-wa-ren | concept | 1062B | ch01/17/18 SCN28 R238 |

## 状态更新

- current_round: 239→240
- rounds_since_last_evv5: 2→3
- rounds_since_last_discover: 0→1
- rounds_since_last_w5: 22→23
- last_10_genes: shift oldest "ENRICH" → push "STUB"
- enrich_count_window: 4→3（等于阈值，ENRICH 不再饱和）
- new1_count_window: 2（不变）

## 下轮预测

R240 后 enrich_count_window=3 不再饱和，ENRICH 可用：
- P2 SCN28: discover=1, queue≈7 < 10 → 可能触发
- P4 ENRICH: enrich=3 = max → 可用
- P8 NEW1: new1=2 < 3 → 可用
