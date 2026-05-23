# RFC-ggs-0004: 语料终稿格式质检流程作为 memex 共享基因

- **Status**: implemented
- **Date**: 2026-05-23
- **Issue**: https://github.com/baojie/memex/issues/130
- **Source wiki**: ggs
- **Target**: `skills/gene/`（新建共享基因）

---

## Problem

ggs wiki 在 Phase 3（语料准备）中沉淀了一套**语料终稿格式质检流程**，涵盖 9 个检查维度：

| 维度 | 检测目标 |
|------|---------|
| 标题内嵌空格 | epub→MD 换行转换导致的章节标题多余空格 |
| 编码完整性 | Unicode 替换字符 `�`、控制字符 |
| 括号配对 | 全半角混用、左右不对称 |
| 中英边界 | 英文小写直连中文字符 |
| 断行异常 | 逗号后跟小写英文、括号跨段 |
| 数字异常 | 语义可疑的数字开头行、序号跳跃 |
| 工具残留 | 孤立页码行、目录条目混入正文 |
| 标题层级 | 跳级、缺级 |
| 脚注完整性 | 脚注定义与引用计数匹配 |

这些检查项**不依赖 ggs 特定语料**——epub、数字版 PDF、扫描版 PDF 的语料终稿均可执行，各检查项按来源类型自动适配。

当前该流程仅存在于 `ggs/local/gene/LOCAL-ggs01-corpus-final-format-qa.md`，其他 sub-wiki 无法发现或复用。

## Root cause

ggs wiki 在 Phase 3 执行到实际质检时，需要将流程形式化为 gene。当时没有现成的 memex 共享基因可用，因此创建了 local gene。实践表明该流程具有通用价值。

## Proposed change

将 `LOCAL-ggs01` 的核心质检流程提取为 memex `skills/gene/` 下的共享基因，供所有 sub-wiki 使用。具体方案：

### 方案 A（推荐）：提取为独立共享基因

1. 基于 LOCAL-ggs01 的内容，在 `$MEMEX_ROOT/skills/gene/` 下创建共享基因（编号由 memex 维护者分配）
2. ggs 本地的 `LOCAL-ggs01` 精简为 stub，通过链接或引用指向共享基因
3. 保留 ggs 特定配置（如 `doc_final.md` 路径）在 local/gene/ 中

### 方案 B：基因模板化

在 `$MEMEX_ROOT/skills/gene/` 下创建参数化版本，各 wiki 通过传入变量（语料路径、来源类型等）复用同一套检查脚本，无需各自维护 local copy。

---

## 备注

本基因源于 ggs Phase 3 实践。9 项检查的脚本可直接运行（Python/bash 单文件），已在 `corpus/raw/doc_final.md` 上验证通过。

## Implementation

**Review**: faithful
**Date**: 2026-05-23
**Commits**:
- baojie/memex@9c2f616（共享基因 PRE21 创建）
- baojie/ggs@1820b8e（LOCAL-ggs01 精简为 stub）
