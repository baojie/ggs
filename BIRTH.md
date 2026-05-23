# 枪炮、病菌与钢铁 Wiki — 启动流程 (BIRTH)

> 阅读顺序：
> 1. `$MEMEX_ROOT/CONSTITUTION.md` — 宪法
> 2. `LAW.md` — 本地法律
> 3. 本文档 — 启动引导
>
> 通用流程见 `$MEMEX_ROOT/BIRTH.spec.md`，本文档记录 ggs 项目的具体参数与完成状态。

---

## Phase 0：前置决策与基础文件

### 0-0 Bootstrap（第一步，无依赖）

> spec 定义见 `$MEMEX_ROOT/BIRTH.spec.md §0-0`，本 wiki 将其内容合入 0-B 执行。

- [x] **链接共享 skills**（在 0-B 中通过 `init_skills.sh` 完成）
  - 已链接 16 个：`boot` `butler` `chapter-scan` `commit` `comply` `daily` `editor` `enrich` `evolve` `grow` `msg` `open` `rfc` `serendipity` `why` `wiki`

### 0-A 两个前置决策

- [x] **WIKI_LANG = `zh`**（谢延光译本，中文）
- [x] **主语料**：`corpus/raw/枪炮病菌与钢铁_校勘底稿.md`（3575行，epub 校勘底稿）
  - 语料来源类型：已转换 MD，**跳过 3-B**
  - Git remote：`https://github.com/baojie/ggs.git`

### 0-B 基础文件

- [x] 创建 `LAW.md`
- [x] 创建 `CLAUDE.md`
- [x] 更新 `.gitignore`
- [x] 创建完整目录结构（docs/、ref/、logs/、data/、local/、wiki/scripts/）
- [x] 创建 `local/config.md`
- [x] 共享 skills 链接（`init_skills.sh`）
- [x] 创建 `README.md`
- [x] 创建 `CHANGELOG.md`

### 0-C 安全初始化

- [x] 初始化 `.claude/settings.json`（`init_security.py`，25条 deny，15条 allow）
- [x] PreToolUse hook 已注册（`restrict_to_project.py`）
- [x] 复制 `skill_commit.sh` / `wiki_commit.sh`

### 0-D 发布配置

- [x] 确认发布方案：**方案 B — Droplet**
  - `DEPLOY_TARGET=droplet` 已写入 `local/config.md`
  - `wiki/scripts/publish.sh` 已包含 `--push` 段（git subtree → gh-pages）
  - `docs/` 为普通目录（非 submodule）
  - 服务器端 `git clone --branch gh-pages` 待 Phase 1 首次推送后执行

### 0-E 初始提交

- [x] `git add` 所有基础文件并提交（commit `8af6ecd`）
  - 提交范围：BIRTH.md / CLAUDE.md / LAW.md / README.md / CHANGELOG.md / .gitignore
  - 目录：`local/` `ref/` `logs/` `data/` `docs/` `wiki/scripts/`
  - 安全配置：`.claude/settings.json` `.claude/skills/` `.claude/hooks/`
  - 注：`.claude/commands/` 本 wiki 暂不使用，不在此次提交范围内

---

## Phase 1：引擎接通

### 1-A 确认本地调试端口

- [x] 端口 **1997**（《枪炮、病菌与钢铁》出版年）
  - 已写入 `local/config.md`：`PORT=1997`
  - 已追加到 `$MEMEX_ROOT/ref/spec/sys-ports.md` 已分配表

### 1-A2 确认引擎 CDN 来源

- [x] 选择方案 A（默认）：`CDN_BASE=https://baojie.github.io/memex/dist`
  - 已写入 `local/config.md`

### 1-B 建立 docs/ 结构

- [x] 创建 `docs/index.html`（重定向到 `wiki/`）
- [x] 创建 `docs/wiki/index.html`（从模板生成，替换 Wiki Name 和 Footer）
  - `cdn-base` = `https://baojie.github.io/memex/dist`
  - Footer: 基于 Jared Diamond《Guns, Germs, and Steel》（1997）谢延光中译本
  - CSS/JS 路径验证通过（`css/main.css` / `js/core.js`）
- [x] `docs/wiki/pages/`、`docs/wiki/data/`、`docs/wiki/images/`、`docs/wiki/local/` 已存在

### 1-C 适配 wiki-daemon.sh

- [x] 从 `wiki-daemon.sh.example` 创建 `wiki-daemon.sh`
  - `WIKI_NAME=ggs`、`PORT=1997`、`PUBLIC_DIR=docs/wiki`
  - `ENGINE_DIR=$MEMEX_ROOT/wiki/public`（serve.js fallback）

### 1-D 确认共享脚本可用

- [x] `$MEMEX_ROOT/wiki/scripts/page_utils.py` 存在

### 1-E 引擎接通提交

- [x] 提交 Phase 1 建立的所有文件（commit `6eb2ca6`）

---

## Phase 2：Wiki 配置

> **目标**：Phase 2 结束后，空 Wiki 完整可用：页面正常渲染，About 页可访问，控制台无报错。
> 本 Phase 所有含用户可见字符串的文件，必须按 Phase 0-A 确认的 `WIKI_LANG=zh` 书写。

### 2-A 本地 JS 配置文件初始化

引擎插件通过 **静态 import** 或 **动态 import** 读取 `docs/wiki/local/` 下的配置，
缺失静态 import 文件会导致插件模块加载失败，页面卡在「载入中」。

**必须创建（被插件静态 import，缺失直接崩溃）：**

- [x] `docs/wiki/local/LocalSettings.js` — 已创建，`wgSiteName='枪炮、病菌与钢铁'`，已启用插件：
  - `i18n`（多语言）、`category`（分类）、`chapter`（章节导航）、`hero`（首页 Hero）、所有 `localConfig:no` 的 core 插件
  - **未启用**：`event-linkify`（需创建配置文件）、地图系列插件（需地理数据）
- [x] `docs/wiki/local/config/i18n.config.js` — 已创建，`defaultLang = 'zh'`
- [x] `docs/wiki/local/config/chapter.config.js` — 已创建，`TOC_PAGE_ID = '目录'`
- [x] `docs/wiki/local/config/types.js` — 已创建，类型体系：
  - concept → 概念、person → 人物、event → 事件、organization → 机构
  - place → 地点、species → 物种、overview → 综述、chapter → 章节、list → 列表
- [x] `docs/wiki/local/config/infobox.js` — 已创建，含中文标签，两组分组（基本信息 / 学术信息）
- [x] `docs/wiki/local/config/hero.js` — 已创建，书籍结构：
  - 前言（耶利的问题）· 第一部分（第1–3章，从伊甸园到卡哈马卡）
  - 第二部分（第4–10章，粮食生产的出现和传播）
  - 第三部分（第11–14章，从粮食到枪炮、病菌与钢铁）
  - 第四部分（第15–19章，在5章中环游世界）
  - 后记（人类史作为一门科学的未来）
- [x] `docs/wiki/local/config/home.js` — 已创建，首页分区：核心概念 / 重要人物 / 地理区域 / 物种
- [x] `docs/wiki/local/config/variables.js` — 已创建，`AUTHOR=贾雷德·戴蒙德`、`TRANSLATOR=谢延光`、`YEAR=1997`

**插件动态配置（`{id}.config.js`）：**

`localConfig: required` 插件（必须创建对应 `.config.js` 才能启用）：
| 插件 | 配置键 | 配置文件 | 状态 |
|------|--------|---------|------|
| `i18n` | `defaultLang` | `i18n.config.js` | ✅ 已创建，`'zh'` |
| `event-linkify` | `LINKIFY_FIELDS` | `event-linkify.config.js` | ⬜ 未创建（按需启用） |

- [x] 已决定：暂不启用 `event-linkify`（当前无事件页，后续需要时再启用）

### 2-B 创建 About 页面

- [x] 创建 `docs/wiki/pages/About.md` — 已创建并通过 `add_page.py` 注册
  - 路径：`docs/wiki/pages/ab/About.md`（已分桶）
  - 注册表 `pages.json` 中已包含 About 条目

### 2-C Hero 视觉设计

- [x] 构思首页背景视觉隐喻 — 已完成：大地色系漂流粒子动画，模拟作物/牲畜/病菌在大陆间扩散，沿东西轴线漂移，随机分裂繁殖
- [x] 实现 `docs/wiki/local/config/hero.config.js` — 已实现，含 `buildHeroBackground()` 和 `startHeroAnimation(setStop)`
- [ ] 本地验证：`./wiki-daemon.sh start`，首页背景正常渲染，控制台无报错

### 2-D 验证

- [x] 执行 `./wiki-daemon.sh start`，`http://localhost:1997` 返回 200
- [x] 页面正常渲染，注册表已重建（`pages.json` / `pages.lite.json` / `fts-index.json`）
- [ ] topnav「关于/About」可访问（需浏览器测试）
- [ ] 开发者工具 → Network，确认无非预期 404（需浏览器测试）

### 2-E Wiki 配置提交

- [ ] 提交 Phase 2 所有配置文件：
  ```bash
  git add docs/wiki/local/ docs/wiki/pages/ docs/wiki/pages.json docs/wiki/pages.lite.json
  bash wiki/scripts/skill_commit.sh "chore: Phase 2 Wiki 配置与 About 页"
  ```
  > 提交范围：`local/` 下所有 JS 配置文件、`pages/About.md`、注册表 `pages.json` / `pages.lite.json`。

---

## Phase 3：语料准备

> 语料已校勘完成（`corpus/raw/枪炮病菌与钢铁_校勘底稿.md`）
> 跳过 3-B（已转换 MD）
> 状态：未开始

---

## Phase 4：章节导入与目录

> 状态：未开始

---

## Phase 5：PN 段落编号

> 状态：未开始

---

## Phase 6：基础数据建设

> 状态：未开始

---

## Phase 7：知识结构摸底与类型体系调整

> 状态：未开始

---

## Phase 8：Butler 准备期

> 状态：未开始

---

## Phase 9：类型 Pilot

> 状态：未开始

---

## Phase 10：总结复盘与启动 Butler

> 状态：未开始
