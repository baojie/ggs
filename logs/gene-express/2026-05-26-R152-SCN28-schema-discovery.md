---
round: 152
phase: "5"
gene: SCN28
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


# Round 152 — SCN28

- **Date**: 2026-05-26
- **Gene**: SCN28
- **Decision**: P2（queue_size=3 < threshold=10，发现新候选）

## SCN28 候选发现

| 候选词 | 建议优先级 | 红链数 | 入队 |
|--------|-----------|--------|------|
| 物种保护 | P2 stub | ×2 | ✓ |

**说明**：本次扫描发现 27 个待建词条，其中 25 个为已有页面的 chapter slug 或别名别名，1 个合格候选入队。

## 状态更新

- discover_since: 2 → 0（重置）
- enrich_count_window: 3 → 2（RCH4 弹出，释放 1 槽）
- new1_count_window: 5（不变）
- 窗口：pop RCH4 → push SCN28

## 备注

- 候选池趋近枯竭——连续两轮 SCN28 仅发现 3–4 个合格候选
- Enrich 槽已释放（2/3），下轮可执行 enrich 变体
