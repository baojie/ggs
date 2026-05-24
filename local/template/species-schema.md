# species 页面图式（枪炮、病菌与钢铁 Wiki）

**type**: `species`  
**预估数量**: 60–80 条  
**优先级**: P1

---

## Frontmatter 字段

```yaml
---
id: slug-kebab-case
type: species
label: 物种中文名
aliases: [学名, 英文名]
	# tags 必须使用 Wiki 默认语言（本 Wiki 为中文），type 字段保持英文
tags: [植物, 动物, 病原体, 农作物, 家畜]   # 从下方标签集选取
description: 一句话介绍（物种类型 + 与粮食生产/疾病的关联）
---
```

**专属字段**（非必填）：
- `category`: `plant / animal / pathogen`
- `domesticated`: 是否驯化（`true / false / partial`）
- `origin_region`: 起源/驯化地区（如 `新月沃地 / 中国 / 中美洲`）
- `domestication_date`: 驯化年代（如 `~8500 BCE`）

**标签集**：
`植物`, `动物`, `病原体`, `农作物`, `家畜`, `野生`, `入侵种`, `驯化种`

---

## 页面结构（H2 节顺序）

```markdown
## 物种简介

[分类、基本特征、野生祖先，1–2段]

## 驯化历史

[驯化地点、时间、驯化机制，附 PN 引注]

## 在本书中的角色

[该物种在全书论证中的地位（粮食生产基础、疾病来源等），附 PN 引注]

## 地理传播

[驯化后的传播路线与速度，附 PN 引注]

## 相关词条

[Wikilink 到相关地点、概念、事件]
```

**病原体变体**（type 仍为 species，但结构调整）：
```markdown
## 病原体简介
## 传播机制
## 在征服史中的角色
## 相关词条
```

---

## 引文规范

- 物种词条对应书中大量具体论据，引文密度应高：每页 ≥4 PN
- 书中对驯化标准（ANNA KARENINA）有专门论述，相关词条须引用 ch09 PN

---

## 质量阈值

| 档次 | 最低要求 |
|------|---------|
| basic | frontmatter 完整 + 物种简介 + ≥1 PN |
| standard | + 驯化历史 + ≥3 PN + category 字段 |
| featured | + 地理传播 + origin_region + ≥6 PN |

---

## 插图引用规范

物种词条可引用书中相关动植物图表（如图8.X驯化作物分布）。  
病原体词条通常无对应图，此项**不适用**。
