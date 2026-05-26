---
round: 217
phase: "5"
gene: ENRICH
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


# Round 217 — ENRICH

- **Date**: 2026-05-26
- **Grow phase**: 5
- **Decision**: P4 ENRICH（恢复常规，enrich_count=2 < 3）

---

## ENRICH 批量富化（5 standard → standard）

| 页面 | slug | type | 旧大小 | 新大小 | 增量 |
|------|------|------|--------|--------|------|
| 地理 | 地理 | place | 2112B | 4240B | +2128B |
| 走出非洲 | zou-chu-fei-zhou | event | 2195B | 4237B | +2042B |
| 大狐猴 | da-hu-hou | species | 2230B | 4388B | +2158B |
| 希克索斯 | xi-ke-suo-si | event | 2532B | 4569B | +2037B |
| 黄热病 | huang-re-bing | concept | 2580B | 4586B | +2006B |

## 新增内容

**地理** — 变量体系（多组可量化地理变量与比较框架）、因果链（地理→粮食生产→人口→技术→军事）、决定论争议（地理设限但不剥夺创造性）、现代相关性（晶体管跨洋但未跳跃到扎伊尔）

**走出非洲** — 线粒体DNA与线粒体夏娃、方法论意义（统一起源为全书铺垫）、种族概念消解（外表差异只是适应）、与农业起源的时间关系

**大狐猴** — 岛屿巨型动物灭绝普遍模式、碳十四测定精确时间线、大陆灭绝的启示、与大陆动物的警惕性差距对比

**希克索斯** — 战车技术起源与传播、军事代差的示范效应、统治遗产（埃及吸收战车技术）、在论证框架中的位置

**黄热病** — 与疟疾的协同效应、跨大西洋传播途经奴隶贸易、殖民时间表的调节器、病原体持续性导致的根除困难

---

## 决策矩阵

- P1a EVV5+SCN28: rounds_since_last_evv5=1 < 10 → skip
- P2 SCN28: rounds_since_last_discover=1 < 10 → skip
- P3 W5: 刚执行 → skip
- **P4 ENRICH**: enrich_count=2 < 3 → **已执行**
- P6 QRY2: qry2_count=1 < 2 → 可用（优先级低）
- P7 STUB: 无上限 → 可用（优先级低）
- P8 NEW1: new1_count=1 < 3 → 可用（优先级低）

---

## 状态更新

- current_round: 217→218
- rounds_since_last_evv5: 1→2
- rounds_since_last_discover: 1→2
- rounds_since_last_w5: 0→1
- last_10_genes: pop "NEW1" → push "ENRICH"
- new1_count_window: 1→0（NEW1 出窗）
- enrich_count_window: 2→3（**已达 rolling_max**）

---

## 下轮预测

R218 决策：
- P1a EVV5+SCN28: 2 < 10 → skip
- P2 SCN28: 2 < 10 → skip
- P3 W5: 1 < 29 → skip
- P4 ENRICH: enrich_count=3 ≥ 3 → **饱和**
- P6 QRY2: qry2_count=1 < 2 → **触发！**
- 预计执行 QRY2（引用排行页）
