---
round: {{N}}
date: {{YYYY-MM-DD}}
phase: "5"
gene: {{gene}}                 # Phase 5 gene 枚举值
enrich_variant: {{variant}}    # 仅 enrich 轮填写（RCH1/RCH2/RCH3/RCH4/QUO3/RCH9）
list_type: {{type}}            # 仅 QRY2 轮填写（timeline/thematic/index/insight）
pages: [{{slug1}}, ...]
result: accept
window_snapshot: "{{new1}}N/{{enrich}}E/{{lst1}}L"
---

## 执行摘要

一段话描述本轮做了什么（建页/enrich/discover），输入是什么，产出是什么。

## 页面处理记录

| 页面 | 操作 | 结果 | 备注 |
|------|------|------|------|
| {{slug}} | create / enrich | accept | {{简短说明}} |

## EXIT-GATE 检查

**G1 优先检查（失败立即回滚，不继续后续检查）：**

| 门 | 结果 | 问题与处置 |
|----|------|---------|
| G1 内容完整性 | PASS | — |

**G2 核心格式检查（E1–E8，复用 Phase 3）：**

| 编号 | 检查项 | 结果 | 问题与处置 |
|------|--------|------|---------|
| E1 | frontmatter 结构完整 | PASS | |
| E2 | 质量档位达标 | PASS | |
| E3 | 必填字段内容非空 | PASS | |
| E4 | 标题无 wikilink | PASS | |
| E5 | PN 引注有效性 | PASS | |
| E6 | 正文规范 | PASS | |
| E7 | blockquote 有 PN | PASS | |
| E9 | QRY2 后置：wikilink 无悬空（仅 QRY2 轮） | PASS | |

## 遗留问题

{{本轮发现但未处理的问题}}
