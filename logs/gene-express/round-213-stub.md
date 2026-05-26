# Round 213 — STUB

- **Date**: 2026-05-26
- **Grow phase**: 5
- **Decision**: P7 STUB（enrich/qry2 饱和，new1 未饱和但 stub 优先）

---

## 新建存根页（5 stub）

| 页面 | slug | type | size |
|------|------|------|------|
| 尼日尔-刚果语系 | ni-ri-er-gang-guo-yu-xi | concept | 749B |
| 阿非罗-亚细亚语系 | a-fei-luo-ya-xi-ya-yu-xi | concept | 729B |
| 闪语族 | shan-yu-zu | concept | 781B |
| 吸气音 | xi-qi-yin | concept | 755B |
| 赫雷罗人 | he-lei-luo-ren | person | 747B |

---

## 决策矩阵

- P1a EVV5+SCN28: rounds_since_last_evv5=8 < 10 → skip
- P1b EVV5: 同上 → skip
- P2 SCN28: queue ~10 ≥ 10 → skip
- P3 W5: rounds_since_last_w5=26 < 29 → skip
- P4 ENRICH: enrich_count=3 ≥ 3 → 饱和
- P5 RFT: rft_count=0 < 2 → 可触发（非独立）
- P6 QRY2: qry2_count=2 ≥ 2 → 饱和
- P7 STUB: 无上限 → **已执行**
- P8 NEW1: new1_count=2 < 3 → 可用（stub 优先）

---

## 状态更新

- current_round: 213→214
- rounds_since_last_evv5: 8→9
- rounds_since_last_discover: 3→4
- rounds_since_last_w5: 26→27
- last_10_genes: pop "SCN28" → push "STUB"
- 队列减少5项，pending约10项

---

## 下轮预测

R214 决策：
- P1a EVV5+SCN28: rounds_since_last_evv5=9 < 10 → skip（即将触发）
- P2 SCN28: queue ~10 ≥ 10 → skip（边界）
- P3 W5: rounds_since_last_w5=27 < 29 → skip
- P4 enrich: enrich_count=3 ≥ 3 → 饱和
- P6 QRY2: qry2_count=2 ≥ 2 → 饱和
- P8 NEW1: new1_count=2 < 3 → **available**
- 可能路径：P8 NEW1（新建 basic 页）
