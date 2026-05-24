# 枪炮病菌与钢铁 Wiki — 本地法律

> 宪法（`~/memex/CONSTITUTION.md`）优先。本文件是宪法之下的项目特定补充规范。

---

## 一、项目基本参数

| 参数 | 值 |
|------|---|
| Wiki 名称 | 枪炮、病菌与钢铁 |
| WIKI_LANG | zh |
| 本地端口 | 1997（英文版出版年） |
| GitHub remote | https://github.com/baojie/ggs.git |
| 发布方案 | 待定 |

---

## 二、语料声明

- `corpus/raw/枪炮病菌与钢铁_校勘底稿.md`：谢延光译本（epub）与修订版 PDF 校勘底稿，**只读，不可修改**。
- corpus 文件均受版权保护，不提交到 git（见 .gitignore）。
- 引用语料时只记录位置（章节、段落号），不复制大段原文到页面。

---

## 三、PN（段落编号）映射规则

- PN 格式：`（NNN-PPP）`，NNN = 3位章节号，PPP = 3位段落号
- 前置页（目录、扉页、前言）：NNN = P01–P03（P 前缀，符合插件 `P0[1-9]` 格式）
- 正文章节：NNN = 001–019（与 chapter 字段 1–19 对齐）
- 后记：NNN = 020
- 各章独立计数，PPP 从 001 起
- 章节标识 NNN 一览见 `ref/chapter-order.md`

---

## 四、页面类型（词条类型）

| 类型 | 说明 | 示例 |
|------|------|------|
| `concept` | 核心概念/理论 | 地理决定论、粮食生产 |
| `person` | 人物 | 贾雷德·戴蒙德、耶利 |
| `chapter` | 章节摘要 | 第1章：耶利的问题 |
| `place` | 地理区域 | 新几内亚、欧亚大陆 |
| `event` | 历史事件 | 寒武纪大爆发、农业起源 |
| `species` | 物种（动植物/病原体）| 小麦、马、天花病毒 |
| `overview` | 综述/目录页 | Contents、About |
| `organization` | 机构/政治实体 | 印加帝国、西班牙殖民地 |
| `list` | 列举性词条 | 驯化作物清单 |

---

## 五、corpus 只读声明

任何 skill、脚本、Claude 操作，均**禁止修改** `corpus/` 目录下的任何文件。
如需标注，写入 `data/` 目录，不得回写 corpus。

---

## 六、提交门控

- 直接 `git commit` 被 deny 拦截
- 授权提交须走：`bash wiki/scripts/wiki_commit.sh`
- Skill 提交须走：`bash wiki/scripts/skill_commit.sh`
