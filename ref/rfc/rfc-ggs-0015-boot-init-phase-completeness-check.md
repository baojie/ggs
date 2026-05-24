# RFC-ggs-0015: /boot init 后应执行结构完整性校验，防止章节遗漏

- **Status**: proposed
- **Date**: 2026-05-25
- **Issue**: https://github.com/baojie/memex/issues/149
- **Source wiki**: ggs
- **Target**: `$MEMEX_ROOT/skills/SKILL_boot.md`（/boot init 流程的 Step 3 合规检查节）

---

## Problem

本次 `/boot init 9` 执行后，Phase 9 的 BIRTH.md 实例化内容严重不全：

- `9-C 全章节 Wikify` 被压缩为 3 条简化 bullet，丢失了 `9-C-1`/`9-C-2`/`9-C-3`/`9-C-4` 四个子节的完整内容
- `9-D 重建反向链接索引`、`9-E 首页建设（APP5）`、`完成条件` 三个顶级节完全缺失

事故发现方式：用户目视对照 BIRTH.md 与 BIRTH.spec.md 后人工指出。

`/comply birth phase 9` 执行了 T/L/V 语义检查，发现了 9-A 候选描述的逻辑错误（`地理决定论` → `粮食生产`），但**未能发现章节结构的批量缺失**。原因是 /comply 的检查范围是"语义合规"，不是"结构完整性"——它不对照 spec 逐节核对是否遗漏。

**事故影响**：若用户未手动发现，后续 `/boot 9` 执行至 9-C 时将缺少关键步骤引导（9-C-3/9-C-4/9-D/9-E/完成条件），极可能导致跳过 wikify 应用、backlinks 重建、首页建设等关键操作。

## Root cause

`/boot init` 的 Step 3 合规检查描述为：

> 检查内容是否忠实于 BIRTH.spec.md（无遗漏步骤、无错误参数）

但这一检查依赖 LLM 主观判断，且 **检查机制本身没有定义"如何验证忠实性"的具体方法**——没有要求对照 spec 逐节枚举标题、没有要求生成前后 diff、没有强制要求列出哪些节被包含或省略。LLM 在 init 时可能因 context 过长或注意力不足遗漏后半段内容，而 Step 3 又缺乏机制来发现这种遗漏。

根本原因可归纳为：**init 的质检步骤（Step 3）与 spec 的结构（章节标题树）之间没有锚定**，导致遗漏无法被系统性检出。

## Proposed change

在 `/boot init` Step 3 中，增加以下**结构完整性校验**子步骤，置于现有 T/L/V 语义检查之前执行：

### Step 3-pre：Spec 标题树对比

1. 从 `$MEMEX_ROOT/BIRTH.spec.md` 提取 Phase N 的所有标题（`##`/`###`/`####`），构成"spec 标题集合"
2. 从生成后的本地 `BIRTH.md` Phase N 节提取同级标题，构成"实例标题集合"
3. 计算差集：spec 中有、实例中无的标题列为 **MISSING**；实例中有、spec 中无的列为 **EXTRA**（通常是添加的 ggs 专有内容，不报错）
4. 若 MISSING 非空：**立即停止**，打印缺失清单，并补全缺失节（重新从 spec 复制对应节并填写参数），然后重新执行 Step 3-pre
5. 仅 MISSING 为空时方可继续 T/L/V 语义检查

### 检查脚本参考实现

```python
import re

def extract_phase_headings(text, phase_n):
    """提取 BIRTH.spec.md 或 BIRTH.md 中 Phase N 的所有标题"""
    # 找到 Phase N 起始位置
    phase_pat = re.compile(rf'^##\s+Phase\s+{phase_n}[\s：]', re.M)
    next_phase_pat = re.compile(rf'^##\s+Phase\s+{phase_n + 1}[\s：]', re.M)
    m = phase_pat.search(text)
    if not m:
        return []
    start = m.start()
    m2 = next_phase_pat.search(text, start + 1)
    end = m2.start() if m2 else len(text)
    block = text[start:end]
    headings = re.findall(r'^(#{2,4}\s+.+)$', block, re.M)
    return [h.strip() for h in headings]

spec_headings = set(extract_phase_headings(spec_text, N))
inst_headings = set(extract_phase_headings(birth_text, N))
missing = spec_headings - inst_headings
if missing:
    print("MISSING from instance:")
    for h in sorted(missing):
        print(f"  {h}")
```

### 输出格式

```
=== Step 3-pre：结构完整性校验 ===
Spec Phase 9 标题数：17
实例 Phase 9 标题数：12
✗ MISSING（5 项）：
  #### 9-C-3 应用链接
  #### 9-C-4 渲染验证与提交
  ### 9-D 重建反向链接索引
  ### 9-E 首页建设（APP5）
  ### 完成条件
→ 补全缺失节后重新检查。
```

或（全部命中时）：

```
=== Step 3-pre：结构完整性校验 ===
Spec Phase 9 标题数：17，实例 Phase 9 标题数：17
✓ 结构完整，无缺失标题。继续语义检查。
```

### 对 /comply 的建议

`/comply birth phase N` 应增加专门的 **S4 结构完整性** 检查项：对照 BIRTH.spec.md 提取 Phase N 的标题树，报告是否有标题缺失。此项不属于现有 T/L/V 分类，建议作为独立子检查在 CHK5 之前执行。
