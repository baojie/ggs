# 枪炮、病菌与钢铁 Wiki — 启动流程 (BIRTH)

> 阅读顺序：
> 1. `$MEMEX_ROOT/CONSTITUTION.md` — 宪法
> 2. `LAW.md` — 本地法律
> 3. 本文档 — 启动引导
>
> 通用流程见 `$MEMEX_ROOT/BIRTH.spec.md`，本文档记录 ggs 项目的具体参数与完成状态。

---

## Phase 0：前置决策与基础文件

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
- [ ] 创建 `README.md`
- [ ] 创建 `CHANGELOG.md`

### 0-C 安全初始化

- [x] 初始化 `.claude/settings.json`（`init_security.py`，25条 deny，15条 allow）
- [x] PreToolUse hook 已注册（`restrict_to_project.py`）
- [x] 复制 `skill_commit.sh` / `wiki_commit.sh`

### 0-D 发布配置

- [ ] 确认 GitHub Pages / Droplet 发布方案

### 0-E 初始提交

- [ ] `git add` 所有基础文件并提交

---

## Phase 1：引擎接通

> 状态：未开始

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
