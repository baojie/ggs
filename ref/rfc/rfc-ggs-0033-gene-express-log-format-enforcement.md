---
id: rfc-ggs-0033-gene-express-log-format-enforcement
title: "fix(gene-express): Phase 5 日志格式批量纠偏 + 防再犯机制"
status: proposed
date: 2026-05-26
issue: https://github.com/baojie/memex/issues/197
---

## 问题描述

R094 进入 Phase 5 后，gene-express 日志格式系统性偏离 GROW.spec.md 规范，具体三处：

1. **文件名**：`round-{N}-{gene}.md` → 应为 `{YYYY-MM-DD}-R{N}-{gene}-{type}-{摘要}.md`
2. **Frontmatter**：缺 `type`、`window_snapshot` 等必填字段，混入非标准字段
3. **内容结构**：缺少 `## 执行摘要`、`## 页面处理记录`（表格）、`## EXIT-GATE 检查`（G1–G5 门控表）、`## 遗留问题` 四个标准节

根因：没有可引用的日志模板，且 Claude 每次写日志时未查阅 GROW.spec.md §5.6–5.7。

## 解决方案

### 1. 已执行：批量修复

编写 `fix_gene_express_format.py` 脚本，对 R094–R194 共 72 个已提交日志执行：

- 重命名为规范格式
- 补充缺失的 frontmatter 字段
- 追加 EXIT-GATE 检查节

副作用：R153–R181 共 29 个未提交日志文件因 `rm` 误删丢失。已在回滚恢复中确认 git 中无历史记录。

### 2. 已执行：本地模板

创建 `local/template/gene-express-log.md`，每次写日志前复制填空。

### 3. 已执行：LAW.md 规范

LAW.md §七 新增每轮日志格式规范，含命名规则、frontmatter 字段表、内容章节清单。

### 4. 建议：git hook 格式校验

建议在 commit 前自动检查 `logs/gene-express/*.md` 文件名是否符合 `^\d{4}-\d{2}-\d{2}-R\d+-[A-Z0-9_]+-` 模式，不符合则拒绝提交。

## 影响范围

- 正面：72 个历史日志格式标准化
- 负面：R153–R181 日志丢失（未提交，无法恢复）
- 后续：新建日志将遵守模板和 LAW.md 约定
