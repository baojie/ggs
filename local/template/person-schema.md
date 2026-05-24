# person 页面图式（枪炮、病菌与钢铁 Wiki）

**type**: `person`  
**预估数量**: 40–60 条  
**优先级**: P1

---

## Frontmatter 字段

```yaml
---
id: slug-kebab-case
type: person
label: 人物中文名
aliases: [英文名, 另一译名]
tags: [explorer, scholar, indigenous]   # 从下方标签集选取
description: 一句话介绍（身份 + 与本书的关联）
---
```

**专属字段**（非必填）：
- `birth`: 出生年代（如 `1478`，不确定用 `~1478`）
- `death`: 死亡年代
- `affiliation`: 所属国家/文明/机构（如 `西班牙王国`）
- `role`: 在本书中的角色（`author / scholar / explorer / ruler / native`）

**标签集**：
`explorer`, `scholar`, `indigenous`, `ruler`, `conquistador`, `scientist`, `author`

---

## 页面结构（H2 节顺序）

```markdown
## 简介

[身份 + 在本书论证中的位置，1–2段]

## 生平

[简要生平，重点放在与本书主题相关的事迹]

## 在本书中

[书中对此人的引述或以此人为例的论证，附 PN 引注]

## 相关词条

[Wikilink 到相关事件、地点、概念]
```

---

## 引文规范

- blockquote 用于书中直接引用此人言论或对其的描述
- 须附 PN 引注，格式：`（PN）`
- 历史人物词条引文密度可低于概念词条（每页 ≥2 PN 即可）

---

## 质量阈值

| 档次 | 最低要求 |
|------|---------|
| basic | frontmatter 完整 + 简介节 + ≥1 PN |
| standard | + 在本书中 节 + ≥2 PN + 相关词条 Wikilink |
| featured | + 生平节 + ≥4 PN + 所有字段填写 |

---

## 插图引用规范

人物词条通常不直接引用图表。若书中有人物相关图片（如征服场景），可引用，方式同 concept-schema。原书人物无专属图片，此项**一般不适用**。
