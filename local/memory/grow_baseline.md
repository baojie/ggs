# GROW 基线摸底 — 枪炮、病菌与钢铁

date: 2026-05-25
butler_round: R40
grow_phase: Phase 2（广度扩张）

## 页面库现状

总页数: 100（含章节 22 个，overview 2 个）
词条类页面: 76（concept 16 / species 15 / place 15 / person 15 / event 15）
质量分布: standard 76
stub 比率: 0.0%
featured+ 比率: 0.0%

## 候选池评估

当前队列条目数: 0（需首轮 discover 填充）
各类型估算剩余候选量:
- concept: 54–74
- species: 45–65
- place: 35–55
- person: 25–45
- event: 5–20
总体判断: 候选充足（各类型预估剩余均 > 5）

## Pilot 遗留债务

来源：boot_summary.md §Pilot 流程发现

| 问题 | 类型 | 处理状态 |
|------|------|---------|
| SCN27 建页未内置 HKP31 破折号检查 | 基因层 | 非阻塞，butler 阶段执行 EVV5 时补强 |
| EVV6 E5 模板一致性在 place/person/event 未完整执行 | 流程层 | 非阻塞，Phase 2 每 10 轮 EVV5 时补检 |
| QUO23 引文核验覆盖率约 10% | 基因层 | 非阻塞，housekeeping |

**阻塞性债务：无**

## 链接网络

wikilink 总数: 422
平均每词条: 5.6 条
backlinks 覆盖: 80/80 页，409 条反链

## 阶段定位

定位结论: Phase 2 — 广度扩张
理由: Pilot（BIRTH Phase 9）已完成（R1–R40），所有类型均分 ≥ 99.6，模板稳定；stub%=0%，N_entries=76 < 80，候选池充足（最小类型 event 尚余 5–20 条）

## 下一步优先动作（Top 3）

1. `/grow init 2`：实例化 Phase 2，完成 2.1-0 WU quota 配置，初始化 grow_state.json
2. 第一轮 SCN28 discover：填充队列候选（当前队列为空）
3. 启动 concept 类型扩张（Phase 2.1 第一批 NEW1 建页）
