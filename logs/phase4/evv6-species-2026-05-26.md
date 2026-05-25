---
phase: "4-C"
type: species
completed: 2026-05-26
pages: 49
featured: 15
standard: 9
basic: 25
template_revised: false
---

# EVV6 反思：species

## 质量分布

- 精品 15, 标准 9, 基础 25
- 均分 28.0/40（70%），为所有类型最低
- 基础档占 51%（25/49），均未 enrich

## 主要扣分模式

1. **PN 引注缺失**：抽查 basic 和 standard 页面中多数 PN=0，远低于 schema 要求的 ≥1（basic）/ ≥3（standard）
2. **content 深度不足**：basic 页面虽有结构（物种简介/驯化历史/相关词条），但每节仅 1-2 句
3. **category/domesticated/origin_region 字段缺失**：basic 页面普遍缺少专属字段

## 根因分析

- 25 个 basic 页面多为 Phase 2 后期（R63-R73）批量 NEW1 创建，仅完成了 frontmatter 和骨架结构
- Phase 3 为 enrich 轮次但 priority 给了 concept 类型（standard→featured），species basic 未纳入
- 模板 schema 定义明确，但缺乏 enforce 机制确保新建页达到 PN 门槛

## 建议

- species 的 basic 页面应在 Phase 5 作为 enrich 优先批次处理
- 模板无需修订（schema 定义充分）
- 建议在 `local/template/species-schema.md` 中补充"每句有据"铁律提醒（RCH1）
