# R251 RCH2: stub→basic 升档

- **Date**: 2026-05-27
- **Gene**: RCH2 (stub→basic enrichment)
- **Phase**: 5 (Decision Matrix: P4 enrich > RCH2)
- **Source**: Phase 5 enrich sub-decision → RCH2 (stub→basic upgrade), 12 stubs available

## 执行内容

从 Phase 2 队列中选取 5 个 stub 页面进行 enrich 升档（stub→basic）：

| 页面 | 来源章节 | 原大小 | 新大小 | 状态 |
|------|---------|--------|--------|------|
| 阿帕切族 | ch06 | 684B | 1416B | ✓ |
| 赫雷罗人 | ch19 | 746B | 1389B | ✓ |
| 亨德森岛 | ch02 | 1108B | 1591B | ✓ |
| 回溯试验法 | ch20 | 981B | 1394B | ✓ |
| 科罗拉多河 | ch06 | 701B | 1450B | ✓ |

### 遇到的问题

- **赫雷罗人**初版因散文质量检查（退出码 7）被拦截——段中含两个 `——`。修复后重试通过
- **回溯试验法**同样因散文质量检查失败——方法论段含 `——` 作为插入语。替换为逗号后通过

### 质量数据

- 总计新增：~2884 字内容
- 所有页面均添加了「方法论意义 / 地理经济 / 对比价值」等深层分析节
- 所有页面均包含 3 个相关词条链接
- 所有页面均使用 PN 引注

## 状态更新

```json
{
  "current_round": 252,
  "enrich_count_window": 3,
  "rounds_since_last_w5": 5
}
```

## 下一步

Phase 5 决策矩阵下一优先：P2 SCN28（queue_size < discover_queue_threshold）。
