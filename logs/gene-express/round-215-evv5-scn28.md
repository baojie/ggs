# Round 215 — EVV5+SCN28

- **Date**: 2026-05-26
- **Grow phase**: 5
- **Decision**: P1a EVV5+SCN28（质量评估 + 章节发掘，rounds_since_last_evv5=10 达阈值触发）

---

## EVV5 质量评估（5 featured 页面富化）

| 页面 | slug | type | 旧大小 | 新大小 | 增量 |
|------|------|------|--------|--------|------|
| 抵抗 | 抵抗 | concept | 2063B | 3792B | +1729B |
| 黑死病 | 黑死病 | event | 2109B | ~ | ~ |
| 马的驯化 | 马的驯化 | event | 2094B | ~ | ~ |
| 船只 | 船只 | concept | 2208B | 4037B | +1829B |
| 旧大陆 | 旧大陆 | concept | 2041B | 3850B | +1809B |

## EVV5 新增内容

**抵抗** — 成功抵抗实例（马匹和枪炮缩小技术差距的部落）、抵抗与疾病时间差（传染病先于军队抵达）、莫里奥里人的社会组织分析、抵抗失败的心理连锁效应

**黑死病** — 社会后果（劳动力短缺与农奴制瓦解）、病菌起源与动物宿主（啮齿动物与贸易路线）、免疫经验的双刃剑（检疫制度）、与天花和麻疹的比较分析

**马的驯化** — 考古证据（博泰文化马骨与马奶残留）、马匹在战争中的决定性作用（骑兵冲击力）、各大陆动物驯化对比、马匹对农业的革命性影响

**船只** — 欧洲远洋帆船技术基础（卡拉维尔船）、波利尼西亚双体独木舟对比、中国宝船技术高度、船只作为制度能力的延伸

**旧大陆** — 大陆内部差异（东西轴线与南北轴线）、动物驯化优势的量化对比、新月沃地生态自杀、中国统一与欧洲分裂的对比分析

---

## SCN28 章节发掘

- **章节**: ch20 后记 人类史作为一门科学的未来
- **发现**: 1 P1 create + 6 P2 stub = 7 候选项

### P1 create（1）
- 政治分裂（多章：ch13/ch18/ch20）

### P2 stub（6）
- 郑和（person）
- 宝船队（event）
- 生态自杀（concept）
- 文化特质（concept）
- 历史科学（concept）
- 回溯试验法（concept）

---

## 决策矩阵

- **P1a EVV5+SCN28**: rounds_since_last_evv5=10 ≥ 10 → **已执行**
- P1b EVV5: 同上
- P2 SCN28: 已合并执行
- P3 W5: rounds_since_last_w5=28 < 29 → skip
- P4 ENRICH: enrich_count=2 < 3 → 可用（evv5 优先）
- P6 QRY2: qry2_count=2 ≥ 2 → 饱和
- P7 STUB: 无上限 → 可用（已执行 P1a）
- P8 NEW1: new1_count=2 < 3 → 可用（已执行 P1a）

---

## 状态更新

- current_round: 215→216
- rounds_since_last_evv5: 10→0（已触发重置）
- rounds_since_last_discover: 5→0（执行 SCN28）
- rounds_since_last_w5: 28→29
- last_10_genes: pop "STUB" → push "EVV5+SCN28"
- new1_count_window: 2（不变，无 NEW1）
- enrich_count_window: 2（不变，执行的是 EVV5 而非 ENRICH）
- 队列新增7项，pending 约12项

---

## 下轮预测

R216 决策：
- P1a EVV5+SCN28: rounds_since_last_evv5=0 < 10 → skip
- P2 SCN28: rounds_since_last_discover=0 < 10 → skip
- P3 W5: rounds_since_last_w5=29 ≥ 29 → **触发！**
- 预计执行 W5（全局质量评估）
