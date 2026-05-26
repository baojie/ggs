# R199 — P2 SCN28

- **日期**: 2026-05-26
- **基因**: SCN28
- **轮次**: 199

## 决策矩阵

| 优先级 | 基因 | 条件 | 结果 |
|--------|------|------|------|
| P1a | EVV5+SCN28 | rounds_since_last_evv5=5 < 10 | 跳过 |
| P1b | EVV5 | rounds_since_last_evv5=5 < 10 | 跳过 |
| **P2** | **SCN28** | queue=7 < threshold=10 | **执行** |
| P3 | W5 | 12 < 29 | 跳过 |
| P4 | ENRICH | enrich_count_window=2 < 3 | 跳过（优先级较低） |
| P6 | QRY2 | qry2_count_window=2 ≥ 2 | 跳过 |
| P8 | NEW1 | new1_count_window=3 ≥ 3 | 跳过 |

## 新候选

从 ch16（中国是怎样成为中国人的中国）发掘 7 个候选项：

### P1 create（3）

| 候选项 | 类型 | 出现章节 |
|--------|------|---------|
| 南岛语系 | concept | ch02/ch05/ch15/ch16/ch17/ch18/ch19 |
| 黍 | species | ch05/ch07/ch08/ch15/ch16/ch18/ch19 |
| 矮小黑人 | person | ch16/ch17/ch19 |

### P2 stub（4）

| 候选项 | 类型 | 出现章节 |
|--------|------|---------|
| 和平文化 | concept | ch16 |
| 秦朝 | event | ch16 |
| 夏朝 | event | ch16 |
| 安达曼群岛 | place | ch15/ch16 |

## 候选状态

- 队列原待处理: 7 项
- 新发现: 7 项（P1×3, P2×4）
- 队列现待处理: 14 项
