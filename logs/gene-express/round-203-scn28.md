# R203 — P2 SCN28

- **日期**: 2026-05-26
- **基因**: SCN28
- **轮次**: 203

## 决策矩阵

| 优先级 | 基因 | 条件 | 结果 |
|--------|------|------|------|
| P1a | EVV5+SCN28 | rounds_since_last_evv5=9 < 10 | 跳过 |
| P1b | EVV5 | rounds_since_last_evv5=9 < 10 | 跳过 |
| **P2** | **SCN28** | queue=9 < threshold=10 | **执行** |
| P3 | W5 | 16 < 29 | 跳过 |
| P4 | ENRICH | enrich_count_window=3 ≥ 3 | 跳过 |
| P6 | QRY2 | qry2_count_window=2 ≥ 2 | 跳过 |
| P8 | NEW1 | new1_count_window=2 < 3 | 跳过（优先级较低） |

## 新候选

从 ch17（驶向波利尼西亚的快艇）发掘 7 个候选项：

### P1 create（3）

| 候选项 | 类型 | 出现章节 |
|--------|------|---------|
| 拉皮塔文化 | concept | ch02/ch15/ch17 |
| 巴布亚诸语言 | concept | ch15/ch17 |
| 舷外浮材 | concept | ch15/ch17 |

### P2 stub（4）

| 候选项 | 类型 | 出现章节 |
|--------|------|---------|
| 大坌坑文化 | concept | ch17 |
| 原始南岛语 | concept | ch17 |
| 树皮布 | concept | ch17 |
| 拉皮塔人 | person | ch17 |

## 候选状态

- 队列原待处理: 9 项
- 新发现: 7 项（P1×3, P2×4）
- 队列现待处理: 16 项
