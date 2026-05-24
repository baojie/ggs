# 枪炮、病菌与钢铁 Wiki — Claude 入口

> **首先阅读宪法：** `$MEMEX_ROOT/CONSTITUTION.md`（全局不可违背规则）
> **其次阅读本地法律：** `LAW.md`（本 wiki 补充规则）
> **然后启动 BIRTH：** `BIRTH.md`（引导建设流程）
> 如有冲突，宪法优先。

---

## MEMEX_ROOT

共享代码源位于 `~/memex`（本机 symlink）。

```bash
MEMEX_ROOT="$HOME/memex"
export MEMEX_ROOT
```

## 项目配置

| 参数 | 值 |
|------|---|
| Wiki 名称 | 枪炮、病菌与钢铁 |
| WIKI_LANG | zh |
| 本地端口 | 1997 |
| GitHub remote | https://github.com/baojie/ggs.git |

---

## ⚠️ PN 引用防幻觉规则

**每次添加 PN 引用 `（NNN-PPP）` 时，必须执行以下三步，无一例外：**

1. **查证**：读取目标章节中 `[NNN-PPP]` 段落的原文，确认该段落**明确包含**被引用的事实数据或论断
2. **匹配**：引用内容须与原文范围一致——原文列举了 12 种作物就不写成"仅 3 种"；原文没给出体数字就不写"年产量 X 亿吨"
3. **标注**：仅当第 1 步验证通过后，才在陈述末尾添加 `（NNN-PPP）` 引用标记

> 本条规则优先于质量档位门槛中的"PN 引注数量"要求。**宁可缺一个引用，不可编造一个引用。** 没有确凿原文依据的事实陈述（如现代产量数据、通用常识），不加 PN 引用。

---

## ⚠️ 创建或修改 Wiki 页面后必须做的两件事

**每次**新建或修改 wiki 页面，无一例外，必须立即执行：

1. **注册页面**：更新 `docs/wiki/pages.json` 和 `docs/wiki/pages.lite.json`
2. **记录 revision**：运行以下命令：
   ```bash
   python3 "$MEMEX_ROOT/wiki/scripts/record_revision.py" \
     "页面名称" \
     --summary "新增/修改描述" \
     --author "baojie" \
     --public docs/wiki
   ```

---

## 重要安全规则

### memex 文件不可直接操作

任何涉及 `~/memex/` 或 `$MEMEX_ROOT` 路径的文件操作，**必须先提 RFC，走 `/rfc` 流程**。

### Frontmatter Fields

```yaml
---
id: entry-name
type: concept
label: 显示名称
aliases: []
tags: []
description: 一句话描述
---
```

### Page Types

| type | 说明 |
|------|------|
| concept | 核心概念/理论 |
| person | 人物 |
| chapter | 章节摘要 |
| place | 地理区域 |
| event | 历史事件 |
| species | 物种 |
| overview | 综述/目录页 |

### Workflow

```bash
# 创建新词条（必须用脚本，禁止直接 Edit/Write）
python3 "$MEMEX_ROOT/wiki/scripts/add_page.py" SLUG - --summary "add: SLUG" << 'EOF'
[frontmatter + content]
EOF

# 本地预览
bash wiki-daemon.sh start   # http://localhost:1997

# 发布
bash wiki/scripts/wiki_commit.sh
git push
```
