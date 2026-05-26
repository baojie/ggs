# Round 218 — QRY2

- **Date**: 2026-05-26
- **Grow phase**: 5
- **Decision**: P6 QRY2（引用索引页，qry2_count=1 < 2）

---

## QRY2 新建索引页

| 页面 | slug | type | 大小 |
|------|------|------|------|
| 页面大小排行 | ye-mian-da-xiao-pai-hang | list | 2508B |

按正文长度（prose_chars）排名的页面索引，含 Top 50 总排行、最短 Top 30、及各类型 Top 20。与已有的引用排行（按 total_refs）互补。

---

## 决策矩阵

- P1a EVV5+SCN28: rounds_since_last_evv5=2 < 10 → skip
- P2 SCN28: rounds_since_last_discover=2 < 10 → skip
- P3 W5: rounds_since_last_w5=1 < 29 → skip
- P4 ENRICH: enrich_count=3 ≥ 3 → 饱和
- **P6 QRY2**: qry2_count=1 < 2 → **已执行**
- P7 STUB: 无上限 → 可用（优先级低）
- P8 NEW1: new1_count=0 < 3 → 可用（优先级低）

---

## 状态更新

- current_round: 218→219
- rounds_since_last_evv5: 2→3
- rounds_since_last_discover: 2→3
- rounds_since_last_w5: 1→2
- last_10_genes: pop "STUB" → push "QRY2"
- qry2_count_window: 1→2（**已达 rolling_max**）

---

## 下轮预测

R219 决策：
- P1a EVV5+SCN28: 3 < 10 → skip
- P2 SCN28: 3 < 10 → skip
- P3 W5: 2 < 29 → skip
- P4 ENRICH: 饱和 → skip
- P6 QRY2: 饱和 → skip
- **P7 STUB**: 无上限 → **触发！**（消减队列约12项）
- P8 NEW1: new1_count=0 < 3 → 可用（stub 优先）
