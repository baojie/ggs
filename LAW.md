# 枪炮病菌与钢铁 Wiki — 本地法律

> 宪法（`$MEMEX_ROOT/CONSTITUTION.md`）优先。本文件是宪法之下的项目特定补充规范（法源体系 L3）。
> 如有冲突，宪法优先。

---

## 一、项目基本参数

| 参数 | 值 |
|------|-----|
| Wiki 名称 | 枪炮、病菌与钢铁 |
| WIKI_LANG | zh |
| 本地端口 | 1997（英文版出版年） |
| GitHub remote | https://github.com/baojie/ggs.git |
| 发布方案 | 待定 |

本地预览：`bash wiki/wiki.sh`，访问 `http://localhost:1997`。

---

## 二、语料声明

- `corpus/raw/枪炮病菌与钢铁_校勘底稿.md`：谢延光译本（epub）与修订版 PDF 校勘底稿，**只读，不可修改**。
- corpus 文件均受版权保护，不提交到 git（见 .gitignore）。
- 引用语料时只记录位置（章节、段落号），不复制大段原文到页面。

---

## 三、PN（段落编号）映射规则

> PN 格式规范来源：`ref/spec/data-pn.md`。

### 格式定义

```
PN = NNN-PPP
NNN = {章号:03d}         章号，纯数字 (001–020) 或 P 前缀 (P01–P03)
PPP = {段号:03d}         段号，纯数字 (001–999)
pn_prefix = NNN           每章 frontmatter 存此值
```

### 括号格式

| 场景 | 格式 | 示例 |
|------|------|------|
| 章节页段首标注 | `[NNN-PPP]` | `[001-007]正文` |
| 实体页行内引注 | 全角 `（NNN-PPP）` | `上下文（001-007）` |

### NNN 分配表

| NNN | page_id | 类型 | 说明 |
|------|---------|------|------|
| P01–P03 | 前置页 | chapter | 目录、扉页、前言 |
| 001–019 | 正文章节 | chapter | 第1章–第19章 |
| 020 | 后记 | chapter | 后记 |

完整映射见 `ref/chapter-order.md`。

### 规则

1. PN 格式为 **两段 `NNN-PPP`**。
2. 前置页 NNN = P01–P03（P 前缀，符合插件 `P0[1-9]` 格式）。
3. 各章独立计数，PPP 从 `001` 起，PN 一经分配不得变更。
4. 禁止使用 `PRE`、`APP`、`REF`、`IDX` 等非本章约定格式的代码。

---

## 四、页面类型

本 wiki 使用以下页面类型：

| 类型 | 说明 | 示例 |
|------|------|------|
| `chapter` | 原文章节页（从语料切分）| 第1章：耶利的问题 |
| `concept` | 核心概念/理论 | 地理决定论、粮食生产 |
| `person` | 人物 | 贾雷德·戴蒙德、耶利 |
| `place` | 地理区域 | 新几内亚、欧亚大陆 |
| `event` | 历史事件 | 寒武纪大爆发、农业起源 |
| `species` | 物种（动植物/病原体）| 小麦、马、天花病毒 |
| `overview` | 综述/目录页 | Contents、About |
| `organization` | 机构/政治实体 | 印加帝国、西班牙殖民地 |
| `list` | 列举性词条 | 驯化作物清单 |

> ⚠️ 所有从语料切分的页面均使用 `type: chapter`；禁止使用 `document` 等不兼容类型。
> `type: overview` 仅用于 wiki 编辑者手工创建的综述/导引页。

---

## 五、页面 slug 命名规范

页面 slug（文件名、`id` 字段）的格式依 `WIKI_LANG` 而定，**不得混用**。

**`WIKI_LANG=zh`**：slug **必须使用汉字**。

| 规则 | 说明 |
|------|------|
| ✅ 汉字 slug | `粮食生产`、`贾雷德·戴蒙德` |
| ❌ 拼音 slug | `liangshi-shengchan`、`jialeide-daimengde` — 禁止 |
| ❌ 英文 slug | `food-production` — 禁止 |
| ❌ 拼音首字母 | `lssc` — 禁止 |

**例外**：`overview` 类型的系统页面（`About`、`目录` 等）由 memex 框架定义，不受此约束。

**理由**：slug 与 wikilink 解析、文件路径一致，避免双轨并存导致的 alias 冲突和重复页面。

---

## 六、Corpus 只读声明

任何 skill、脚本、Claude 操作，均**禁止修改** `corpus/` 目录下的任何文件。
如需标注，写入 `data/` 目录，不得回写 corpus。

**例外**：BIRTH.md Phase 3（语料准备与校对）期间允许向 `corpus/` 写入。
Phase 3 最后一次提交后恢复只读，后续阶段（Phase 4 起）不再写入。

---

## 七、提交门控

- 直接 `git commit` 被 deny 拦截
- 授权提交须走：`bash wiki/scripts/wiki_commit.sh`
- Skill 提交须走：`bash wiki/scripts/skill_commit.sh`

## 八、日志格式规范

### 文件命名

`{YYYY-MM-DD}-R{轮次}-{gene}-{type}-{摘要}.md`

例：`2026-05-26-R128-NEW1-new-pages.md`

### 标准结构

每轮 gene-express 日志必须包含以下 frontmatter 字段：

| 字段 | 必填 | 说明 |
|------|------|------|
| `round` | ✅ | 轮次号 |
| `date` | ✅ | 日期 YYYY-MM-DD |
| `phase` | ✅ | Phase 编号 |
| `gene` | ✅ | gene 枚举值 |
| `enrich_variant` | 仅 enrich 轮 | RCH1/RCH2/RCH3/RCH4/QUO3/RCH9 |
| `list_type` | 仅 QRY2 轮 | timeline/thematic/index/insight |
| `pages` | ✅ | 涉及页面 slug 列表 |
| `result` | ✅ | accept/reject/defer |
| `window_snapshot` | ✅ | `"{{new1}}N/{{enrich}}E/{{lst1}}L"` |

**内容章节：**
1. `## 执行摘要` — 一段话概括本轮工作
2. `## 页面处理记录` — 表格（页面/操作/结果/备注）
3. `## EXIT-GATE 检查` — G1 优先 + G2 核心格式（E1–E8）门控表
4. `## 遗留问题` — 待处理事项

### 违反后果

不符合命名或内容规范的日志视为格式违规。提交前自检，或使用 `local/template/gene-express-log.md` 填空。

---

*本文档适用于 枪炮、病菌与钢铁 项目，受 `$MEMEX_ROOT/CONSTITUTION.md` 约束。*
