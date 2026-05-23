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
  - 已链接 15 个：`butler` `chapter-scan` `commit` `comply` `daily` `editor` `enrich` `evolve` `grow` `msg` `open` `rfc` `serendipity` `why` `wiki`

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

> 状态：未开始

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
