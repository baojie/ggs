# Phase 4 Lint Audit — 2026-05-26

## 扫描概要

- 扫描范围：全库 293 非章节词条（concept/species/place/person/event）
- 扫描模式：dry-run / 报告模式，未修改任何文件

## 4-A-1 格式规范性扫描

| Gene | 结果 | 说明 |
|------|------|------|
| compute_quality.py | 293 页 | 精品 234、标准 29、基础 30、存根 0 |
| LNT14 空 wikilink | 0 处 | ✓ 全部正常 |
| LNT3 frontmatter | ✓ 全部完整 | 无缺失字段 |
| FLD1 description | 22 处缺失 | 全部为 chapter/overview 页（ch01–ch19, Frontispiece, Epilogue, Preface），非词条页面，可接受 |
| FIX8 类型一致性 | 7 处候选 | bailatu/person, hanniba/person, menggu-diguo/event, niandetelian/person, niluohe/place, xibanya-zhengfu-yinjia/event, xinyuewodi/place — 多为非中文 slug 页面，内容量较少导致特征词未命中 |
| LNT2 标点格式 | 15 处 | 全半角混用，多为章节页脚注标记 |
| HKP22 格式巡检 | ✓ | frontmatter 全部完整；一级标题检查不适用（本 wiki 使用 frontmatter label 机制） |

## 4-A-2 幻觉专项扫描

| 分类 | Gene | 状态 | 结果 |
|------|------|------|------|
| H1 引文 | COR9/CHK8/FIX9 | 待执行 | 需语料原文比对 |
| H2 事实 | QUO22 | 已完成 | 31 页裸断言 > 40%（30 页 `?` 档 = 未 enrich，1 页 basic）|
| H2 事实 | RSN3/KLG4 | 待执行 | 跨篇章/抽样评估 |
| H3 归因 | QUO6/10/23/24 | 待执行 | 语义一致性（WU15-30）|
| 文风 | FIX6 | 已完成 | 49 处（含章节页原文引文）|
| 文风 | QLT9 | 已完成 | 2 处 |

> **强制停轮阈值核查**：QUO22 31 页（阈值 3）和 FIX6 49 处（阈值 10）虽然超阈值，但根因分别为「未 enrich 页」和「原著引文过渡语」，非典型幻觉。其余 H1/H3 基因待执行后再做最终判定。
> 详细分析见 `logs/phase4/hallucination-report.md`。

## 4-A-3 语料自适应套件

CORPUS_TYPE = 史书/历史叙事，追加 LNT1（段落格式）、NER1（人名消歧）。

## 4-A-4 优先级分级（初步）

| 优先级 | 数量 | 说明 |
|--------|------|------|
| P1 | 待 4-A-2 确定 | 幻觉类问题 |
| P2 | 7 候选 | FIX8 类型一致性（需人工复核）|
| P3 | 15 处 | LNT2 标点格式（章节页脚注）|

> 注意：Phase 3 无遗留任务（4-0 结果），4-B 工作量全部来自本 Lint 扫描发现。
