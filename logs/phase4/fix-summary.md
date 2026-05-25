# Phase 4 Fix 总结 — 2026-05-26

## 问题归类

### 个案（同类 < 3 处）
- **FIX8 类型一致性（7 候选）**：bailatu/person, hanniba/person, menggu-diguo/event, niandetelian/person, niluohe/place, xibanya-zhengfu-yinjia/event, xinyuewodi/place
  - 处置：需人工复核 — 可能原因：非中文 slug 页面内容量少，特征词模型未命中
  - 建议：若确认类型错误，在下一轮 enrich 时同步修正 pages.json type 字段

### 系统性（同类 ≥ 3 处）

| 问题 | 数量 | 根因 | 处置 |
|------|------|------|------|
| LNT2 标点混用 | 15 处 | 章节页脚注 `[NNN-NNN]` + 中文标点，源自原著格式 | 无需修复 |
| QUO22 裸断言 | 31 页 | `?` 档页面（Phase 2 NEW1 后未 enrich）| 排入 Phase 5 建页计划 |

## 修复前后对比

| 优先级 | 修复前 | 修复后 |
|--------|--------|--------|
| P1 | 0（待 H1 基因确认）| 0 |
| P2 | 7（待人工复核） | 7（暂缓）|
| P3 | 15（无需修复） | 15（无需修复）|
