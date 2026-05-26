# RFC-ggs-0034: 在 add_page.py / edit_page.py 中增加 PN 引用有效性校验

- **Status**: proposed
- **Date**: 2026-05-27
- **Issue**: https://github.com/baojie/memex/issues/200
- **Source wiki**: ggs
- **Target**: `~/memex/wiki/scripts/pn_validator.py`（新增）、`add_page.py`、`edit_page.py`

---

## Problem

GROW 流程中 AI 生成的 wiki 页面频繁包含与所引段落内容无关的 PN（段落引用）。例如 `013-022` 被用于蒸汽机页面和技术积累页面，但该段实际内容为"新几内亚人通过反复试验发现技术"，与引文所述（蒸汽机作为欧洲关键技术的例证、技术积累的累积性结论）毫无关联。

当前无任何机制在写入页面时校验 PN 引用的内容匹配性，导致：

1. 模型"幻觉引用"直接进入 wiki，不被拦截
2. 用户只能通过人工审核发现，效率低且不可靠
3. 同类问题在不同页面反复出现（经查 `013-022` 在 3 个页面共 5 处引用全部错误）

## Root cause

1. `add_page.py` 和 `edit_page.py` 在写入页面时不做 PN 校验——只检查文件存在性、破折号密度、段落长度等格式规范，但不验证 `（NNN-PPP）` 引用是否与 sentence_index 中对应段落的实际内容相关
2. AI 模型生成 PN 时基于语义相关性猜测段落编号，而非查证 sentence_index 原文，产生"漂移引用"
3. 项目缺乏跨页面的 PN 质量审计工具，无法系统性地发现和纠正此类错误

## Proposed change

### 新增 `wiki/scripts/pn_validator.py` 模块

对所有写入页面中的 `（NNN-PPP）` 格式引用执行以下校验：

**1. 段落存在性检查**：确认 `data/sentence_index/{nnn}.jsonl` 中存在 `pn=PPP` 的条目。若不存在，报错。

**2. 关键词重叠检查**：提取引文所在句子的中文双字/三字词集合，与目标段落的词集合计算交集，重叠词数低于阈值（建议 2-3）时判定为"可能无关"。

**3. 通过/拒绝策略**（通过 `--pn-validate` 参数控制）：
- `off`：跳过校验（默认保持当前行为）
- `warn`（建议默认值）：校验不通过时记录 warning 日志并输出到 stderr，不阻止写入
- `strict`：校验不通过时报错并拒绝写入（exit code ≠ 0）

### 修改 `add_page.py`

在写入文件前调用 `pn_validator.validate()`，传入页面内容和 `--pn-validate` 参数值。

### 修改 `edit_page.py`

在写入文件前同样调用 `pn_validator.validate()`，传入新内容。

### 执行时机建议

建议分两阶段部署：
- **Phase 1**：新增 `pn_validator.py`，默认 `--pn-validate warn`，记录 warning 但不阻止写入，以便观察误报率
- **Phase 2**：调优阈值后，对人工编辑（`edit_page.py`）默认改为 `strict` 模式，对批量新建（`add_page.py`）保持 `warn`
