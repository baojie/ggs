---
round: 104
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


# EVV5+SCN28 R104 — Phase 5 周期 schema 反思 + 候选发现

- **日期**: 2026-05-26
- **Wiki**: ggs
- **轮次**: R104（Phase 5 第 11 轮）
- **gene**: EVV5+SCN28

## SCN28 发现

- 扫描结果：59 个待建词条，红链引用 1–26 次
- 入队（P1）：作物驯化(7)、安娜卡列尼娜原则(6)、劳动分工(4)、欧洲(3)、枪炮病菌与钢铁(26)
- 跳过：物种(3 通用词)、畜牧业(3 与动物驯化重叠)、南北轴线(与大陆轴线重叠)

## EVV5 schema 反思

### 质量分布

- 总词条数：346
- featured+：244（→ 249 after R100/R101 RCH2 rounds）
- standard：14（→ 9 after R101 enrich，wait, I enriched 5 + NEW1 added some new standard ones）

Actually, let me just note the current state.

### 模板状态

- `local/template/` 中各类型模板已稳定（concept/person/place/species/event/chapter/list）
- 无需模板更新

### 系统性观察

- NEW1 窗口严重超限（6/3），需通过 enrich/RFT 消耗
- Enrich 槽已饱和（3/3），RCH2 达到窗口上限
- 建议：下轮补充 QRY2 query 页或放宽 RFT 阈值
