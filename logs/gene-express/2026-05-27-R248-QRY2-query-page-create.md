# R248 QRY2 — 新建 Query 聚合页

- **日期**: 2026-05-27
- **触发**: P6 QRY2（qry2_count_window=0 < 1，窗口尚无 QRY2 页）
- **基因**: QRY2（query-page-create）
- **操作**: 新建 1 个 `type=list` 查询聚合页

## 决策矩阵

| 优先级 | 基因 | 判定 |
|--------|------|------|
| P1a | EVV5+SCN28 | evv5=0 < 10 → 跳过 |
| P1b | EVV5 | 同上（刚执行）|
| P2 | SCN28 | discover=1 < 10, 队列≈13 ≥ 10 → 跳过 |
| P3 | W5 | 刚执行（1 < 29）→ 跳过 |
| P4 | 深化 enrich | new1=2 ≤ 3 → 跳过 |
| P5 | RFT | rft=0 < 2 但无长页候选（prose > 3000=0）→ 跳过 |
| P6 | **QRY2** | **qry2=0 < 1 → 已执行** |
| P7 | 深化 enrich | stub=2% < 15% → 跳过 |
| P8 | NEW1 | 未触发 |

## 新建页面

| 页面 | slug | type | 大小 | query 块数 |
|------|------|------|------|-----------|
| 词条建设状态 | ci-tiao-jian-she-zhuang-tai | list | 1434B | 3（待提升/Standard/高PN引注）|

## QRY3 验证

- ✅ query 语法：3 个块均已正确闭合
- ✅ 字段覆盖率：quality/total_refs/pn_count/wikilink_count 均为 100%
- ✅ 无硬编码 wikilink 列表
- ✅ Quality: basic

## 状态更新

- current_round: 248→249
- qry2_count_window: 0→1
- last_10_genes: shift oldest "SCN28" → push "QRY2"

## 下轮预测

R249 队列≈13，ENRICH/NEW1 各有可用槽位。
