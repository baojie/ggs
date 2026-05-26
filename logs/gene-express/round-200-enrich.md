# R200 — P4 ENRICH

- **日期**: 2026-05-26
- **基因**: ENRICH
- **轮次**: 200

## 决策矩阵

| 优先级 | 基因 | 条件 | 结果 |
|--------|------|------|------|
| P1a | EVV5+SCN28 | rounds_since_last_evv5=6 < 10 | 跳过 |
| P1b | EVV5 | rounds_since_last_evv5=6 < 10 | 跳过 |
| P2 | SCN28 | queue=14 ≥ 10; rounds_since_last_discover=0 | 跳过 |
| P3 | W5 | 13 < 29 | 跳过 |
| **P4** | **ENRICH** | enrich_count_window=2 < 3 | **执行** |
| P6 | QRY2 | qry2_count_window=1 < 2 | 跳过（P4 优先） |
| P8 | NEW1 | new1_count_window=3 ≥ 3 | 跳过 |

## 执行内容

Enrich 5 standard 页面（追加新节）：

| 页面 | 原大小 | 新大小 | 增量 | 新增节 |
|------|--------|--------|------|--------|
| 征服 | 1992B | 2732B | +740 | 被征服者的困境 |
| 美索不达米亚 | 1943B | 2613B | +670 | 粮食生产的生态基础 |
| 南岛人扩张 | 1811B | 2483B | +672 | 南岛人扩张与班图人扩张的比较 |
| 免疫 | 2553B | 3248B | +695 | 免疫差距的历史后果 |
| 斑疹伤寒 | 2261B | 3020B | +759 | 斑疹伤寒与其他流行病的比较 |

**总计**: +3536B

## 状态变更

```json
{
  "current_round": "200→201",
  "rounds_since_last_evv5": "6→7",
  "rounds_since_last_discover": "0→1",
  "enrich_count_window": "2→3",
  "rounds_since_last_w5": "13→14",
  "last_10_genes": "pop SCN28, push ENRICH"
}
```

## 队列状态

队列无变化。
