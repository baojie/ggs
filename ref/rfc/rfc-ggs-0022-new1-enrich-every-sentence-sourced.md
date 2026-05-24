# RFC-ggs-0022: NEW1/enrich 须每句有据，禁止脱离原文编造内容

- **Status**: proposed
- **Date**: 2026-05-25
- **Source wiki**: ggs
- **Issue**: https://github.com/baojie/memex/issues/158
- **Target**: `$MEMEX_ROOT/skills/gene/NEW1-create-page.md` + `$MEMEX_ROOT/.claude/skills/enrich/SKILL.md` + `$MEMEX_ROOT/skills/gene/RCH1-enrich-page.md` + `$MEMEX_ROOT/skills/gene/RCH2-enrich-quality.md`

---

## Problem

NEW1-create-page 和 enrich 在生成 wiki 页面内容时，LLM 频繁编造无原文依据的陈述。典型表现：

1. **PN 引用与内容不匹配**："年产量约 3.7 亿吨"后标注 `（008-006）`，但原文 008-006 只说"12 种作物占 80%+ 总产量"，没有具体数字
2. **无来源的常识填充**：页面中出现"今天年产量约 X 亿吨"、"是世界上最重要的作物之一"等通用知识，没有对应原文
3. **凭空细节**：模型"知道"某个话题，就用训练数据中的知识填补，但这些知识并非来自本书语料

根本上说，现有规则只要求"引用必须来自语料"（blockquote 禁止捏造、PN 必须来自 corpus_search），但**没有要求正文中的每一句陈述本身必须有原文依据**。模型可以在引用了 2-3 个真实 PN 后，自由编造其余 80% 的正文内容。

## Proposed change

### 修改 NEW1-create-page.md

#### Step 3 中增加"每句有据"规则

在 Step 3 开头插入：

```markdown
### Step 3 — 起草页面内容

> **铁律：每句有据**。正文中的每一句断言必须满足以下条件之一：
> 1. 直接来自 corpus_search.py 命中的某个段落（可转述/拼接）
> 2. 是多个命中段落之间的逻辑推理（须标注推理所依赖的 PN）
> 3. 是 frontmatter 中已填写的元信息（如 origin_region、domestication_date）
>
> **禁止**：
> - 以训练数据中的"常识"替代原文依据
> - 在原文没有给出具体数字时自行填写产量、日期、百分比等数据
> - 编写任何无法标记 PN 来源的断言
>
> 每条断言写完后，在括号中标注其来源 PN。若一段话整合了多处来源，按顺序标注：
> `安第斯山脉独立驯化了马铃薯（005-021），其传播受南北轴线限制（010-036）。`
```

#### 后置检查中强化验证

将现有"无捏造内容"检查从建议性改为可操作性检查：

```markdown
## 后置检查

- [ ] frontmatter 含 id/type/label/description/quality
- [ ] **无捏造检查（逐句验证）**：正文中的每个断言，都可在 corpus_search.py 命中的段落中找到明确依据。不确定的依据标注 `[citation needed]` 而非假装有 PN
- [ ] 每段 prose 至少关联 1 个 PN 引用（导语段落除外）
- [ ] ≥ 2 条 wikilink 指向已有页面
- [ ] 注册表已更新
```

### 修改 enrich/SKILL.md

#### 原文引用节扩展到全文

将现有"原文引用格式"节强化，覆盖所有正文内容：

```markdown
### 原文引用格式与全文依据规则

**铁律：每句有据**。enrich 扩写的每一句话都必须有原文依据：

1. 先运行 `corpus_search.py` 收集相关段落
2. 扩写时，每个断言都必须标注其来源 PN
3. 允许对原文进行转述和拼接，但**不得添加原文没有的信息**
4. **逐句验证**：写完后，每个句子都能 traced back 到 corpus 中的某个位置

引用方式：
- **原文引用**：使用 blockquote + `（PN）`
- **转述/拼接**：使用 `（PN）` 标注来源
- **通用知识**（如"马铃薯是块茎作物"）：不加 PN，但必须是原文明确提到的内容

```bash
python3 wiki/scripts/butler/corpus_search.py "关键词" --max 5
```

**禁止捏造**：引用内容必须从 corpus_search.py 结果中复制，不得自行编写"原文"。
```

#### 禁止事项中增加对应条目

```
- ❌ 禁止捏造原文引用
- ❌ **禁止编写无原文依据的断言**——每一句正文都必须能追溯到 corpus_search.py 的命中结果
```

### 修改 RCH1-enrich-page.md

#### 后置检查中增加"每句有据"

```markdown
## 后置检查

- diff 只有追加行，无删除已有正文
- [ ] **每句有据**：新增内容中的每一句断言都有 corpus 命中结果作为依据（在句末标注 PN）
- 新增 PN 使用圆括号格式，无方括号 `[NNN-PPP]`
```

### 修改 RCH2-enrich-quality.md

#### 执行步骤中增加约束

在 Step 3 的"按缺口补充"后插入：

```markdown
3. 按缺口补充（优先级：先补 PN/引文素材 → 再写散文 → 再加节）

> **铁律：每句有据**。补充的每段散文必须基于语料搜索结果撰写，每句断言标注来源 PN。不得以通用知识填充字数——若某段话无法标注 PN，说明它不属于原文范围，不应出现在正文中。

4. 验证实际达到目标档门槛
```

#### 后置检查中增加对应项

```markdown
## 后置检查

- [ ] 质量等级从 X 升为 X+1
- [ ] append-only（已有内容完整保留）
- [ ] **每句有据**：新增内容逐句标注了 PN，无脱离原文的断言
- [ ] 新增 PN 使用圆括号格式，无方括号 `[NNN-PPP]`
```

## Implementation notes

四处修改不涉及代码逻辑，仅增强 prompt 约束。发布后需验证：
- 运行 `/enrich` 升级页面时，模型不再填充无依据的常识数据
- 运行 butler 的 NEW1 建页任务时，输出的页面不含虚构 PN 引用
- RCH1/RCH2 追加内容时逐句标注 PN 来源

CLAUDE.md 已在本项目本地添加了同步的"PN 引用防幻觉规则"作为补充。
