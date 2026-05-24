# concept 页面图式（枪炮、病菌与钢铁 Wiki）

**type**: `concept`  
**预估数量**: 70–90 条  
**优先级**: P1

---

## Frontmatter 字段

```yaml
---
id: slug-kebab-case
type: concept
label: 概念中文名
aliases: [别名1, 别名2]
tags: [geography, agriculture, technology]   # 从下方标签集选取
description: 一句话定义（20–60字）
---
```

**专属字段**（非必填）：
- `related_chapters`: 出现的主要章节（如 `[ch05, ch10]`）
- `domain`: 学科领域（`geography / biology / sociology / history / technology`）

**标签集**（从中选取，可多选）：
`geography`, `agriculture`, `biology`, `technology`, `social-organization`, `language`, `disease`, `trade`, `warfare`, `evolution`

---

## 页面结构（H2 节顺序）

```markdown
## 定义

[一句话核心定义，来源于书中章节，附 PN 引注]

## 在本书中的角色

[该概念在全书论证中的位置与作用，2–4段]

## 主要论点

[书中对该概念的核心论述，分要点，含 PN 引注]

## 相关概念

[Wikilink 到其他相关概念页，简述关联]

## 延伸阅读

[如有，引用书中脚注或参考文献]
```

---

## 引文规范

- blockquote 用于直接引用书中原文，须在独立 `>` 行附 `（PN）`
- 每 3–5 段应有 1 处 PN 引注，最低密度：每段落至少 1 个出处 PN
- 图表引用：若概念与书中图表强相关（如轴线走向图），用 `:::image` 块引入

---

## 质量阈值

| 档次 | 最低要求 |
|------|---------|
| basic | frontmatter 完整 + 定义节 + ≥1 PN 引注 |
| standard | + 主要论点节 + ≥3 PN + 相关概念 Wikilink |
| featured | + 延伸阅读 + ≥6 PN + 引文规范全符合 |

---

## 插图引用规范

本书原书含 32 幅插图（IQ1–IQ32），存于 `docs/wiki/images/`。  
概念词条如与某图高度相关（如"轴线走向"对应图10.1），引入方式：

```markdown
::: image fig="IQ10A1" pn=NNN-PPP
![IQ10A1](../images/image00XXX.jpeg)
图10．1　各大陆的主轴线（…说明…）
:::
```
