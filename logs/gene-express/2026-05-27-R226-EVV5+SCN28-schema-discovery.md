---
round: 226
phase: "5"
gene: EVV5+SCN28
result: accept
---

## EXIT-GATE 检查

**G1 优先检查（失败立即回滚）：**

| 门 | 结果 | 问题与处置 |
|----|------|---------|
| G1 内容完整性 | PASS | — |

**G2 核心格式检查：**

| 编号 | 检查项 | 结果 |
|------|--------|------|
| E1 | frontmatter 结构完整 | PASS |
| E2 | 质量档位达标 | PASS |
| E3 | 必填字段内容非空 | PASS |
| E4 | 标题无 wikilink | PASS |
| E5 | PN 引注有效性 | PASS |
| E6 | 正文规范 | PASS |
| E7 | blockquote 有 PN | PASS |

# Round 226 — EVV5+SCN28

- **Date**: 2026-05-27
- **Grow phase**: 5
- **Decision**: P1a EVV5+SCN28（质量评估 + 章节发掘，rounds_since_last_evv5=10 达阈值触发，queue_size=7 < discover_queue_threshold=10）

---

## EVV5 质量评估（5 basic 页面富化）

| 页面 | slug | type | 旧大小 | 新大小 | 增量 |
|------|------|------|--------|--------|------|
| 利尼尔班克拉米克文化 | li-ni-er-ban-ke-la-mi-ke-wen-hua | concept | 1303B | 2113B | +810B |
| 西谷椰子 | xi-gu-ye-zi | species | 1406B | 1944B | +538B |
| 西貒 | xi-tuan | species | 1209B | 1598B | +389B |
| 鸵鸟 | tuo-niao | species | 1097B | 1614B | +517B |
| 长颈鹿 | chang-jing-lu | species | 1168B | 1657B | +489B |

### EVV5 新增内容

- **利尼尔班克拉米克文化** (basic→standard)：新增"主要论点"节（工具限制→农业传播瓶颈）+ "延伸阅读"节
- **西谷椰子** (basic)：新增"半管理机制"节（驯化连续序列分析）
- **西貒** (basic)：新增"驯化失败的原因"节（安娜·卡列尼娜原则具体应用）
- **鸵鸟** (basic)：新增"人类利用历史"节（蛋壳珠子首饰→现代养殖）
- **长颈鹿** (basic)：新增"驯化尝试"节（古埃及驯养尝试→安娜·卡列尼娜原则）

---

## SCN28 章节发掘

- **章节**: ch05 历史上的穷与富 + 红链扫描
- **Phase 1**: 红链扫描 34 个结果，新候选：有袋动物(2 hits)
- **Phase 2**: LLM 阅读 ch05 发掘
- **Phase 3/4**: 去重+corpus≥2过滤

### 通过候选项（6 个）

| 候选 | 类型 | corpus 命中 | 说明 |
|------|------|------------|------|
| 罂粟 | species | 5 | 地中海西部本地驯化，多章出现 |
| 芝麻 | species | 3 | 印度次大陆驯化油料作物 |
| 放射性碳定年法 | concept | 4 | 考古学测年方法，全书多处引用 |
| 瘤牛 | species | 2 | 印度特有牛种 |
| 非洲薯蓣 | species | 3 | 非洲驯化的薯蓣类作物 |
| 有袋动物 | concept | 2 | 红链扫描发现 |

---

## 决策矩阵

- **P1a EVV5+SCN28**: rounds_since_last_evv5=10 ≥ 10 AND discover到期 → **已执行**
- P1b EVV5: 同上
- P2 SCN28: 已合并执行
- P3 W5: rounds_since_last_w5=9 < 29 → skip
- P4 ENRICH: enrich_count=3 ≥ 3 → 饱和
- P6 QRY2: qry2_count=2 ≥ 2 → 饱和
- P8 NEW1: new1_count=3 ≥ 3 → 饱和（rolling_max）
- P7 STUB: stub% 待查

---

## 状态更新

- current_round: 226→227
- rounds_since_last_evv5: 10→0（已触发重置）
- rounds_since_last_discover: 1→0（执行 SCN28）
- new1_count_window: 3（不变，无 NEW1）
- enrich_count_window: 3（不变，执行的是 EVV5 而非 ENRICH）
- 队列新增6项，pending 约13项

---

## 下轮预测

R227 决策：
- P1a EVV5+SCN28: rounds_since_last_evv5=0 < 10 → skip
- P2 SCN28: rounds_since_last_discover=0 → skip（除非 queue < 10）
- P3 W5: rounds_since_last_w5=9 < 29 → skip
- P4 ENRICH: enrich_count_window=3 ≥ 3 → 饱和
- P6 QRY2: qry2_count_window=2 ≥ 2 → 饱和
- P8 NEW1: new1_count_window=3 ≥ rolling_new1_max=3 → 超过上限
- P7 STUB: 需查 stub%
- → 可能触发 STUB 或需等待 ENRICH/NEW1 窗口释放
