# RFC-GGS-0031: PCF6 逐小节实例化深度检查

- **Status**: implemented
- **Date**: 2026-05-26
- **Issue**: https://github.com/baojie/memex/issues/183
- **Source wiki**: ggs
- **Target**: `~/.claude/skills/comply/SKILL.md`（PCF 检查模块）

---

## Problem

RFC-0030 为 `/comply` 新增了 PCF1–PCF5 五层检查，覆盖代码块数、复选框数、全局体量、占位符残留和结构性节存在性。但这五层检查均在 Phase 整体层面进行，无法检测**个别小节内部的实例化不足**。

Phase 3 的事故根源正是如此：全局行数正常（PCF3 通过），代码块和复选框总数达标（PCF1/PCF2 通过），但某些 `###`/`####` 小节仅复制了 spec 的标题，正文未实例化为本 wiki 的具体内容。

## Root cause

PCF1–PCF5 都是集合级（aggregate）指标，对单个小节的骨架化不敏感。一个 Phase 可能包含 20 个小节，其中 3 个严重骨架化，但只要其他 17 个小节正常，全局指标不会触发阈值。

需要一种**逐小节**（per-subsection）的独立验证维度，分别检查每个小节的体量和内容独立性。

## Proposed change

在 `/comply` 的 PCF 检查模块中新增 **PCF6——逐节实例化深度检查**，位于 PCF5 之后：

### PCF6 检查项

1. 提取 Phase N 下所有 `###`/`####` 小节
2. 逐小节对比 spec 与 instance 的行数体量
3. 体量 < spec 的 50% → 报错（疑似骨架未实例化）
4. 体量 < spec 的 70% → 警告（偏薄，建议核查）
5. 内容与 spec 完全一致 → 报错（逐字复制，未实例化）
6. 实例中缺失 spec 有的小节 → 报错
7. 实例额外的 spec 没有的小节 → 提示（专有扩展，不报错）

### 代码块

PCF6 代码已编写完成，见 `/tmp/PCF6_addendum.py`。需插入到 `SKILL.md` 中 PCF5 代码块之后（第 232 行后），并在汇总输出中追加 PCF6 条目。

### 输出格式扩展

```
=== PCF Phase Content Fidelity ===
✓/✗ PCF1 代码块完整性  ...
✓/✗ PCF2 复选框完整性  ...
✓/✗ PCF3 内容体量偏差  ...
✓/✗ PCF4 占位符残留   ...
✓/✗ PCF5 结构性节缺失  ...
✓/✗ PCF6 逐节实例化验证: spec 12 小节 → 实例 12 小节
  ✗ "3.1-0-A 参数配置": 体量 15%（45→7 行）— 疑似骨架未实例化
  △ "3.1-B pre-flight": 体量 55%（20→11 行）— 偏薄，建议核查
  ⚠ "3.1-Z 复盘": 内容与 spec 完全一致（逐字复制，未实例化）
```

## Implementation

**Review**: faithful
**Date**: 2026-05-26

**检查清单**：

- [x] PCF6 代码块插入 SKILL.md PCF5 后（80 行，get_subsections + 六项检查）
- [x] 输出格式追加 PCF6 行

**Commits**:
- baojie/memex@3fbc88a: feat(comply): 新增 PCF6 逐小节实例化深度检查
