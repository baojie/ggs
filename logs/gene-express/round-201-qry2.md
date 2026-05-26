# R201 — P6 QRY2

- **日期**: 2026-05-26
- **基因**: QRY2
- **轮次**: 201

## 决策矩阵

| 优先级 | 基因 | 条件 | 结果 |
|--------|------|------|------|
| P1a | EVV5+SCN28 | rounds_since_last_evv5=7 < 10 | 跳过 |
| P1b | EVV5 | rounds_since_last_evv5=7 < 10 | 跳过 |
| P2 | SCN28 | queue=14 ≥ 10; periodic=1 < 10 | 跳过 |
| P3 | W5 | 14 < 29 | 跳过 |
| P4 | ENRICH | enrich_count_window=3 ≥ 3 | 跳过 |
| **P6** | **QRY2** | qry2_count_window=1 < 2 | **执行** |
| P8 | NEW1 | new1_count_window=3 ≥ 3 | 跳过 |

## 执行内容

新建类型索引页（lei-xing-suo-yin）：

| 页面 | 大小 | 说明 |
|------|------|------|
| 类型索引 | 1018B | 按 type 分组的 5 个 query 块（concept/person/place/event/species） |

## 状态变更

```json
{
  "current_round": "201→202",
  "rounds_since_last_evv5": "7→8",
  "rounds_since_last_discover": "1→2",
  "qry2_count_window": "1→2",
  "rounds_since_last_w5": "14→15",
  "last_10_genes": "pop NEW1, push QRY2"
}
```
