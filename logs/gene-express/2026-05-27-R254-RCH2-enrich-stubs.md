# R254 RCH2: stub→basic 升档（第二批）

- **Date**: 2026-05-27
- **Gene**: RCH2 (stub→basic enrichment)
- **Phase**: 5 (Decision Matrix: 各优先级均阻塞，走 enrich 余量)

## 决策逻辑

```
Phase 5 矩阵排查:
  P1a EVV5+SCN28: rounds_since_last_evv5=6 < 10 → 跳过
  P1b EVV5: 同上
  P2 SCN28: rounds_since_last_discover=0, queue_size=10 → 跳过
  P3 W5: rounds_since_last_w5=7 < 29 → 跳过
  P4 NEW1超限: new1=3, not > 3 → 跳过
  P5 RFT: 无长页候选 → 跳过
  P6 QRY2: qry2_count_window=1 → 跳过
  P7 stub%: 0% → 跳过
  → enrich 余量: enrich_count_window=2 < rolling_enrich_max=3 → 走 enrich

Enrich 子决策: 仍有 7 个 stub → RCH2 (stub→basic)
```

## 执行内容

| 页面 | 类型 | 原大小 | 新大小 | 增量 |
|------|------|--------|--------|------|
| 树皮布 | concept | 724B | 1428B | +704 |
| 斯克里林人 | person | 643B | 1420B | +777 |
| 雅诺马马人 | person | 804B | 1523B | +719 |
| 亚希人 | person | 690B | 1452B | +768 |
| 郑和 | person | 786B | 1477B | +691 |

- 总计新增: ~3659 字
- 剩余 stub: 2（阿非罗-亚细亚语系、尤他-阿兹特克诸语言）
- 所有页面均通过散文质量检查 ✓

## 状态更新

```json
{
  "current_round": 255,
  "enrich_count_window": 3,
  "rch2_count_window": 1,
  "rounds_since_last_evv5": 7,
  "rounds_since_last_discover": 1,
  "rounds_since_last_w5": 8
}
```

## 下一步

new1=3, enrich=3, 下一轮可能走 RFT 或 QRY2。
