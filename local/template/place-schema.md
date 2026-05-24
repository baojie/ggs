# place 页面图式（枪炮、病菌与钢铁 Wiki）

**type**: `place`  
**预估数量**: 50–70 条  
**优先级**: P1

---

## Frontmatter 字段

```yaml
---
id: slug-kebab-case
type: place
label: 地名中文名
aliases: [英文名, 其他译名]
tags: [大陆, 地区, 河流, 文明]   # 从下方标签集选取
description: 一句话定位（地理位置 + 在本书中的角色）
---
```

**专属字段**（非必填）：
- `region`: 所属大区域（`africa / eurasia / americas / oceania`）
- `axis`: 大陆轴线方向（`east-west / north-south`，仅大陆级别填写）
- `latitude_band`: 纬度带（如 `temperate / tropical / mediterranean`）

**标签集**：
`大陆`, `地区`, `河流`, `河谷`, `文明`, `岛屿`, `帝国`, `路线`

---

## 页面结构（H2 节顺序）

```markdown
## 地理特征

[位置、面积、气候、纬度带，与大陆轴线走向的关联，1–3段]

## 在本书中的角色

[该地点在全书论证中的地位，附 PN 引注]

## 主要历史关联

[驯化中心、粮食生产起源、文明发展等，附 PN 引注]

## 相关词条

[Wikilink 到相关人物、事件、物种、概念]
```

---

## 引文规范

- 地名词条常作为论证例证出现，务必附 PN 引注说明来源章节
- 引文密度：每页 ≥3 PN

---

## 质量阈值

| 档次 | 最低要求 |
|------|---------|
| basic | frontmatter 完整 + 地理特征节 + ≥1 PN |
| standard | + 在本书中的角色 + ≥3 PN |
| featured | + 主要历史关联 + 轴线标注 + ≥5 PN |

---

## 插图引用规范

地点词条与书中地图类图表关联强（如图10.1轴线图、图5.1粮食生产起源图）。  
若词条对应某张地图，建议引入，方式同 concept-schema。
