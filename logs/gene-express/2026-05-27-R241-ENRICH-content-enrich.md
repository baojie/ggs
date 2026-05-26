# R241 ENRICH — 内容增补

- **日期**: 2026-05-27
- **触发**: P4 ENRICH（enrich=3 = max，刚达阈值不再饱和）
- **基因**: ENRICH（RCH1-enrich-content）
- **操作**: 对 5 个 stub 页追加新节，质量提升至 standard

## 决策矩阵

| 优先级 | 基因 | 判定 |
|--------|------|------|
| P1a | EVV5+SCN28 | evv5=5 < 10 → 跳过 |
| P1b | EVV5 | 同上 |
| P2 | SCN28 | discover=1, queue≈15 > 10 → 跳过 |
| P3 | W5 | 25 < 29 → 跳过 |
| **P4** | **ENRICH** | **enrich=3 = max → 可用** |
| P5 | RFT | 可用但无适合页面 |
| P6 | QRY2 | 基础索引页已存在 |
| P7 | STUB | 可用 |
| P8 | NEW1 | new1=1 < 3 → 可用 |

## 增补详情

| 页面 | slug | 追加节 | 来源 PN | 原大小 | 新大小 | 新 quality |
|------|------|--------|---------|--------|--------|-----------|
| 吸气音 | xi-qi-yin | 语言接触的遗迹 | 019-024/019-025/019-065 | 754B | 1739B | standard |
| 爪哇人 | zhao-wa-ren | 种群冲突的当代案例 | 017-004/017-003 | 1062B | 1726B | standard |
| 原始南岛语 | yuan-shi-nan-dao-yu | 重构方法 | 017-026 | 792B | 1711B | standard |
| 菲什河 | fei-shi-he | 多重边界的交汇 | 010-033/006-004/019-068 | 1185B | 1876B | standard |
| 塞伦格蒂 | sai-lun-ge-di | 生态参照系的意义 | 001-021/019-079 | 1190B | 2017B | standard |

## 状态更新

- current_round: 241→242
- rounds_since_last_evv5: 4→5
- rounds_since_last_discover: 0→1
- rounds_since_last_w5: 24→25
- last_10_genes: shift oldest "ENRICH" → push "ENRICH"
- enrich_count_window: 3（不变，仍等于阈值）
- new1_count_window: 1（不变）
