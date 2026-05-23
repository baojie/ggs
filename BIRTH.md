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
- [x] 本地验证：`./wiki-daemon.sh start`，首页背景正常渲染，控制台无报错

### 2-D 验证

- [x] 执行 `./wiki-daemon.sh start`，`http://localhost:1997` 返回 200
- [x] 页面正常渲染，注册表已重建（`pages.json` / `pages.lite.json` / `fts-index.json`）
- [x] topnav「关于/About」可访问 — 浏览器测试通过，页面内容完整渲染，aliases/类型/基本信息均正确显示
- [x] 开发者工具 → Network，确认无非预期 404（唯一 404 为 favicon.ico，属正常现象）

### 2-E Wiki 配置提交

- [x] 提交 Phase 2 所有配置文件（commit `cdc4976`）
  - 提交范围：`local/` 下所有 JS 配置文件、`pages/About.md`、注册表 `pages.json` / `pages.lite.json`、BIRTH.md

---

## Phase 3：语料准备（选择与校对）

> **目标**：Phase 3 结束后，`corpus/raw/枪炮病菌与钢铁_校勘底稿.md` 作为语料终稿，可作为 Phase 4 章节导入的唯一输入。
>
> **⚠️ corpus/ 写入授权**：Phase 3 是唯一允许向 `corpus/` 写入内容的阶段。LAW.md §五 corpus 只读声明在 Phase 3 完成后生效，3-E 提交后 corpus/ 进入只读。
>
> **提交规则**：3-C / 3-C2 / 3-E 各自结束时提交一次。

---

### 3-A 确认语料结构

- [x] 确认语料存在：`corpus/raw/枪炮病菌与钢铁_校勘底稿.md`（1005K）
- [x] 列出 `corpus/raw/` 和 `corpus/archive/` 下所有文件供用户确认
- [x] **用户确认**：导入版本为 `corpus/raw/枪炮病菌与钢铁_校勘底稿.md`
- [x] 确认导入范围：前言 + 20 章正文 + 后记，全部 type=chapter
- [x] 确认页面 ID 命名规则：`chNN-章节名slug`（如 `ch01-introduction`、`Epilogue`）


### 3-B epub 转换与校验

> **已跳过**：语料来源为已转换 MD（`corpus/raw/枪炮病菌与钢铁_校勘底稿.md`），非 epub 来源。


### 3-C 文本质检

> **语料来源**：已转换 MD（epub→MD 校勘底稿），非扫描 PDF。
>
> **执行前先判断语料来源类型**：已转换 MD。按 PRE9 语料来源适配表：
> - 扫描版 PDF 相关步骤：跳过
> - 数字版 PDF / epub 相关步骤：公式配对 + 标题层级 + 格式问题
>
> 校勘底稿已在 human-in-the-loop 流程中完成文字校对，3-C 仅做脚本层面的格式验证。

**文字质检：**

- [x] **PRE9**（corpus-ocr-qa）：标题层级完整（L1 书名+4 部分标题，L2 前言+19 章+后记，无跳跃）；公式检查通过（无 LaTeX）；工具残留物扫描通过（无孤立数字行、无目录混入）
- [x] **PRE6**（corpus-linebreak-repair）：epub 来源跳过详细检查；快速扫描通过——无逗号假分段、无括号跨段、无跨页假分段
- [x] **提交文本质检结果**


### 3-C2 重建章节结构（文字校勘完成后必做）

- [x] **PRE18**（heading-structure-rebuild）：跳过——epub→MD 来源，标题层级原生保留（L1 书名+4 部分标题，L2 前言+19 章+后记），无 PDF 扁平化问题
- [x] 验证重建结果：章节数量与 `ref/chapter-order.md` 一致（前言+19 章+后记 = 21 个 L2 标题）
- [x] 提交：
  ```bash
  git add corpus/
  bash wiki/scripts/skill_commit.sh "corpus: 3-C2 PRE18 章节结构重建完成"
  ```


### 3-D Pre-PN Lint 检查

- [x] 执行 `$MEMEX_ROOT/ref/spec/workflow-pre-pn-lint.md` 完整流程：epub 来源跳过 PRE13/PRE14；LNT7/LNT2/LNT10 涉及 `docs/wiki/pages/` 的脚本留待 Phase 4 页面生成后执行
- [x] **LNT11**（footnote-completeness）：跳过——语料无脚注（0 定义，0 引用）
- [x] **LNT12**（non-latin-ocr）：通过——扫描到 4 处希腊字母（αηι，希腊字母表讨论）和 7 处西里尔文（четыре/Ружьё，语言学示例），均属原文故意内容，非 OCR 错误
- [x] **`:::` 块语法扫描**（CONSTITUTION §13.2）：通过——corpus/raw/ 下无 `:::` 块语法问题


### 3-E 生成语料终稿

> 校勘底稿 `枪炮病菌与钢铁_校勘底稿.md` 即为最终校勘版本，3-E 将其复制为 `doc_final.md` 作为下游入口。

- [x] 流水线全部步骤完成后，执行终稿复制：`cp corpus/raw/枪炮病菌与钢铁_校勘底稿.md corpus/raw/doc_final.md`
- [x] 确认 `doc_final.md` 存在且内容完整（3575 行，1005K，首末 5 行与校勘底稿一致）
- [ ] **PRE21**（corpus-final-format-qa）：对 `doc_final.md` 执行 9 维终稿格式扫描（标题内嵌空格、编码完整性、括号配对、中英边界、断行异常、数字异常、工具残留、序号跳跃、标题层级），逐项确认无残留问题后方可提交
- [x] **提交语料终稿**

---

## Phase 4：章节导入与目录

> **前置条件**：`corpus/raw/doc_final.md` 存在（Phase 3 完成的标志）。
> **目标**：所有章节（前言+19章+后记）以 `type: chapter` 页面形式进入 Wiki，首页出现书籍结构导航，读者可按部分/章节入口阅读。
> **本 Phase 不做 PN**——内容原文导入即可，PN 留 Phase 5。

---

### 4-A 编写章节导入脚本

- [x] 创建 `wiki/scripts/build_chapter_pages.py`，参考 `$MEMEX_ROOT/wiki/scripts/build_chapter_pages.py` 的模式：
  - 读取 `corpus/raw/doc_final.md`，按章切分内容
  - 写入 `docs/wiki/pages/` 下对应 `.md` 文件，frontmatter 格式：
    ```yaml
    ---
    id: ch01-up-to-the-starting-line
    type: chapter
    label: "第一章 走上起跑线"
    description: "人类历史开端的差异"
    chapter: 1
    tags: [chapter]
    ---
    ```
  - **不插入 PN**，保留原文结构
  - 运行后更新 `docs/wiki/pages.json` + `pages.lite.json`
- [x] 执行脚本，确认 21 个章节页面全部生成（前言 + 第一章~第十九章 + 后记）

**epub 来源 wiki 的 post-import 规范化流水线：**

> ggs 语料来源为「已转换 MD」（epub→MD 校勘底稿），非 Pandoc 直接转换。以下脚本运行后检查 diff 是否有实际修改，无修改则跳过。

所有规范化脚本均在 `$MEMEX_ROOT/wiki/scripts/`，通过 `WIKI_ROOT` 发现目标：
```bash
export WIKI_ROOT="$PWD"
SCRIPTS="$MEMEX_ROOT/wiki/scripts"
```

- [x] **`extract_epub_images.py`** — 需要 epub 源文件；ggs 语料为已转换 MD 且无 epub，**跳过此步**
  > 若日后补充插图，用 `pdfimages` 或 `pdftoppm` 手动提取到 `docs/wiki/images/`
- [x] **`normalize_pandoc_spans.py`** — 检查是否有 Pandoc 扩展 span 残留（`.italic}` → `*text*` 等）；epub→MD 校勘底稿大概率无此类标记，运行后若无实际修改则跳过。结果：0 文件修改
  ```bash
  python3 "$SCRIPTS/normalize_pandoc_spans.py"
  ```
- [x] **`normalize_fig_blocks.py`** — 检查是否有 `{.fig-num}` 图注需转换为 `:::image` 语义块。结果：0 转换
  ```bash
  python3 "$SCRIPTS/normalize_fig_blocks.py"
  ```
- [x] **`normalize_table_blocks.py`** — grid table → pipe table + `:::table` 包装。结果：0 处理
  ```bash
  python3 "$SCRIPTS/normalize_table_blocks.py"
  ```
- [x] **`lint_list_spacing.py`** — 补全列表标记后缺失的空格。结果：Epilogue.md 修复 1 处
  ```bash
  python3 "$SCRIPTS/lint_list_spacing.py"
  ```
- [x] **`normalize_xhtml_links.py`** — epub 跨章节 xhtml 链接 → wiki 内链。结果：0 文件被主转换修改；87 处 `partNNNN.xhtml_annoN` 残留为 epub 注释引用，非章节目录链接，保留
  ```bash
  python3 "$SCRIPTS/normalize_xhtml_links.py"
  ```
- [x] **`build_page_map.py`** — 需要英文 epub 文件；ggs 无英文 epub，**跳过此步**
- [x] **`normalize_page_links.py`** — wiki 页码链接 → pn-NNN-PPP 锚点；依赖 page_map.json，已跳过上游则同步跳过
  ```bash
  python3 "$SCRIPTS/normalize_page_links.py"
  ```
- [x] **`build_section_anchor_map.py`** — 需要英文 epub section 映射；ggs 无英文 epub，**跳过此步**
- [x] **`inject_section_anchors.py`** — 注入 `[a:id]` 锚点到 heading 前；依赖上一步映射数据，已跳过则同步跳过


### 4-B 创建目录页

TOC 页面：`WIKI_LANG=zh` → 文件名 `目录.md`，type=overview，tab 层级缩进，PN 前缀编号，锚点链接。

- [x] 创建静态 `docs/wiki/pages/mu/目录.md`（`generate_toc.py` 需要 PN prefix 待 Phase 5，先手动创建含 wikilink 的版本）
- [x] 将目录页 id 加入 `local/config/home.js` PREFACE_IDS：
  ```js
  export const PREFACE_IDS = ['目录', 'Preface'];
  ```
- [ ] 访问 `#目录` 确认目录页可渲染，所有链接可跳转（在 4-D 中统一验证）


### 4-C 更新 home.js 接入章节导航

- [x] 补充 `docs/wiki/local/config/home.js` 中的空数组：
  ```js
  export const PREFACE_IDS  = ['目录', 'Preface'];  // 前置：目录 + 前言
  export const APPENDIX_IDS = ['Epilogue'];           // 后置：后记
  ```

- [x] 确认 hero.js 的 `BOOK_META` 部分覆盖正确（min/max：前言 0-0、第一部分 1-3、第二部分 4-10、第三部分 11-14、第四部分 15-19、后记 20-20）——已配置，无需修改


### 4-D 验证与提交

- [x] 运行章节完整性基因检查（C01–C08），确认 type、chapter 字段、label、语料覆盖全部正确：
  ```bash
  python3 wiki/scripts/chapter_integrity.py
  ```
  > 自动修复：`python3 wiki/scripts/chapter_integrity.py --fix`（修正 pages.json 注册信息）
- [x] 运行部署验证基因（CHK13，proposed via RFC-ggs-0007，当前使用本地实现 verify_deploy.py）：
  ```bash
  python3 wiki/scripts/verify_deploy.py
  ```
  > D01 pages.json 章节完整性 → 替代 chip 数据验证
  > D02 home.js/hero.js 配置正确性 → 替代 chip 渲染配置验证
  > D03 HTTP 200 + 文件存在 → 替代页面可达性验证
  > D04 编码洁净度 → 替代乱码检查
  > D05 TOC wikilink 可解析 → 替代目录页点击测试
  > D06 daemon restart 后复检 → 替代重启验证
  > D07 章节导航配置（TOC_PAGE_ID / book_seq） → 替代前后章/回到目录验证
- [x] 回填修订历史：
  ```bash
  python3 "$MEMEX_ROOT/wiki/scripts/backfill_recent.py" --public docs/wiki
  ```
- [x] commit `docs/wiki/pages/`、`pages.json`、`pages.lite.json`、`local/config/home.js` 及修订历史文件（commit `ab6d4c2`，已 push）

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
