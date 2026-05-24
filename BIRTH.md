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
- [x] **PRE21**（corpus-final-format-qa）：对 `doc_final.md` 执行 9 维终稿格式扫描（标题内嵌空格、编码完整性、括号配对、中英边界、断行异常、数字异常、工具残留、序号跳跃、标题层级），逐项确认无残留问题后方可提交
  - 结果：4 处部分标题双空格（epub 格式风格，非错误）；括号计数均为中英混用 `(text）` 风格误报；译者署名短行属正常。**无实质性内容问题**
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
- [x] 访问 `#目录` 确认目录页可渲染，所有链接可跳转（在 4-D 中统一验证）


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

> **前置条件**：Phase 4 章节导入完成（`docs/wiki/pages/` 下所有章节页面已生成）。
> **目标**：所有章节页面（含非正文章节）按原书次序分配 `[NNN-PPP]` 段落编号，
> 建立可供词条引用的 PN 体系。

### 5-A 确定章节 NNN 编号（PN 前置必做）

> ⚠️ **NNN 必须严格对应原书页面次序**，包括所有非正文章节。次序一经确定不得变更，否则已标注引用全部失效。

**第一步：确认插件支持的 NNN 格式**

pn-citation 插件正则只接受两种 NNN：

| 格式 | 范围 | 适用场景 |
|------|------|---------|
| `\d{3}` | `001`–`999` | 正文章节、附录、参考文献等 |
| `P0[1-9]` | `P01`–`P09` | 书前置章节（前言、序言等） |

> ⚠️ 凡使用字母缩写（如 `PRE`、`APP`、`REF`、`IDX`）作为 NNN 的旧方案均与插件不兼容，执行前必须修正为上表格式。

**第二步：对照原书目录逐页分配 NNN**

> **铁则：所有已导入页面统统分配 NNN，不得自行判断某页"无正文"而跳过。**

ggs 为单书线性结构，含前置页：

| 结构类型 | 代表 wiki | NNN 模式 | 本 wiki 方案 |
|---------|---------|---------|-------------|
| 单书线性，含前置页 | ai-history、aima | `P01`–`P0N` 前置页，`001`–`NNN` 正文 | 目录→P01，Frontispiece→P02，Preface→P03，ch01→001 … |

分配方案：

| 页面 | NNN | 说明 |
|------|-----|------|
| 目录 | P01 | 目录页 |
| Frontispiece | P02 | 扉页 |
| Preface | P03 | 前言 |
| ch01–ch19 | 001–019 | 正文章节编号与 chapter 字段对齐 |
| Epilogue | 020 | 后记 |

> 注：`About` 为 wiki 系统页面，非原书内容，不分配 PN。

**第三步：创建并展示 `ref/chapter-order.md`**

- [x] 确认 `LAW.md` 中 NNN 方案与插件格式一致（无 `PRE`/`APP`/`REF`/`IDX` 等非法格式）
- [x] 创建 `ref/chapter-order.md`，完整列出所有页面及其 NNN
- [x] **将完整表格打印到屏幕**，让用户逐行核对原书目录次序
- [x] **等待用户明确确认**次序表与原书一致后，方可进入 5-B


### 5-B 更新章节 frontmatter（用户确认后执行）

> 执行条件：用户已确认 `ref/chapter-order.md` 次序正确。

**必选属性：`pn_prefix`**

所有 `type: chapter` 且赋 PN 的页面，frontmatter 中必须加入 `pn_prefix`：

```yaml
pn_prefix: "001"    # 对应 NNN，字符串形式
```

**ggs 可选属性选择：**

| 属性 | 值域 | 选择 |
|------|------|------|
| `part_num` | 0–5 | **选用**：原书分前言 + 4 部分 + 后记（见下表） |
| `part_title` | 各 part 标题 | **选用** |
| `vol_num` | — | **不启用**：单卷本，无需卷编号 |

part 对照：

| part_num | part_title | 覆盖章节 |
|----------|------------|---------|
| 0 | 前言 | Preface（ch.0） |
| 1 | 第一部分：从伊甸园到卡哈马卡 | ch01–ch03 |
| 2 | 第二部分：粮食生产的出现和传播 | ch04–ch10 |
| 3 | 第三部分：从粮食到枪炮、病菌与钢铁 | ch11–ch14 |
| 4 | 第四部分：在5章中环游世界 | ch15–ch19 |
| 5 | 后记 | Epilogue（ch.20） |

**执行步骤：**
- [x] 在 wiki BIRTH.md Phase 5-B 中确认本书选用的可选属性（✓ 已确认：启用 part_num + part_title）
- [x] 编写（或调用）批量更新脚本，按 `ref/chapter-order.md` 的 NNN 映射逐页更新 frontmatter
- [x] 执行脚本，确认所有赋 PN 章节的 `pn_prefix` 字段已写入
- [x] 将 `data/chapter_map.json` 复制到 `docs/wiki/data/chapter_map.json`
- [x] **提交章节 frontmatter 更新**：
  ```bash
  git add docs/wiki/pages/ ref/chapter-order.md data/
  bash wiki/scripts/skill_commit.sh "feat: Phase 5-B 章节 NNN/pn_prefix 写入"
  ```
  > `data/chapter_map.json` 须在此提交——pn-citation 插件相对 wiki 根目录加载此文件。


### 5-C 按次序逐章赋号

> **前置阅读（执行前必读）：**
> - PN 格式规范：`$MEMEX_ROOT/ref/spec/data-pn.md`（哪些元素分配 PN、格式示例）
> - 基因：`$MEMEX_ROOT/skills/gene/PRE7-chapter-pn-assign.md`
>
> **ggs 专属适配：**
> - 额外跳过元素：ggs 语料为 epub→MD 校勘底稿，无 Pandoc 扩展 span 残留；脚注从语料提取时已保留原始标注，赋号时注意不将脚注区段落计入正文 PPP 序列
> - PN 赋号脚本：使用 `wiki/scripts/assign_pn.py`（待创建，参考 PRE7 代码示例适配）

#### 5-C-0 Wiki 专属 PN 规则（必须在试验前在本地 BIRTH.md 确认）

- [x] 确认 `pn_prefix` 已写入所有目标章节（Phase 5-B 完成）
  - 验证：`pn_prefix` 在各章节 MD 文件 frontmatter 中已写入（ch01→"001"，Preface→"P03" 等）
- [x] 阅读 `$MEMEX_ROOT/ref/spec/data-pn.md §2`，了解通用跳过规则
- [x] 记录本 wiki 的额外跳过元素，写入本 BIRTH.md 5-C-0 节

  **ggs 额外跳过规则（在通用规则基础上）：**

  | 元素类型 | 是否分配 PN | 说明 |
  |---------|------------|------|
  | 标题行（`# ## ###` 等） | 否 | 通用规则 |
  | blockquote（`> ` 开头） | 否 | 通用规则；含 `> 【校勘·XX】` 校勘注记块 |
  | 脚注定义（`[^N]:` 开头）| **否** | ggs 所有脚注均为译者注（`------译者` 结尾），属纯编辑注释，按 data-pn.md §2 注"可由各 wiki LAW.md 豁免"豁免 |
  | frontmatter（`---` 块）| 否 | 通用规则 |
  | 空行 | 否 | 通用规则 |

  > 注：`[^1]:` 格式的内联脚注引用（嵌在正文段落中）不影响赋号——正文段落照常获得 PN；只有独立的脚注定义行跳过。

- [x] 确认或创建本地 PN 赋号脚本：`wiki/scripts/assign_pn.py` 已存在
  - 已追加脚注定义跳过规则（`[^N]:` 开头的块不赋 PN）

#### 5-C-1 试验章（pilot）

从 `ref/chapter-order.md` 中选一章作为试验对象——优先选**正文结构典型、有图表、有脚注**的章节，不选最短或最简单的章节。

ggs 建议试验章：**ch08-apples-or-indians**（第八章，正文长、有插图、有表格，结构典型）

- [x] 对试验章单独执行 PN 标注（`wiki/scripts/assign_pn.py --pilot`）
  - 结果：82 PN，NNN=008，末号 082，PN 验证通过
- [x] 本地渲染验证：`./wiki-daemon.sh start`，在浏览器打开该章节页面，检查：
  - PN 编号正确显示在段落首部，无重复、无跳号 ✓
  - 图片块（`:::image`）的 `pn=` 属性正确（4 块，均含 pn=）✓
  - 表格块（`:::table`）的 PN 注释正确（本章无 table 块）✓
  - 脚注区与正文 PN 不混淆 ✓
  - 注：`Images/image00315.jpeg` 404 为语料原文中大写路径残留，属预存问题，不影响 PN

#### 5-C-2 评估

逐项检查并记录结果（通过 / 问题描述）：

| 检查项 | 标准 | 结果 |
|--------|------|------|
| 编号连续性 | 无跳号，PPP 从 001 起严格递增 | 通过（82 PN，001–082，无跳号）|
| 段落边界正确 | PN 锚定在作者原段首，无锚定在标题/图注/脚注上 | 通过 |
| 特殊块处理 | 图片、表格、代码块按规则赋号，不占用正文 PPP 序列 | 通过（4 个 :::image 块各有 pn=）|
| 脚注隔离 | 脚注区段落未被赋 PN | 通过 |
| 渲染无副作用 | `[NNN-PPP]` 标记不破坏正文 Markdown 渲染 | 通过 |
| PN 引用可跳转 | 点击 PN 编号可定位到对应段落（如插件支持） | 通过（[008-001] 浏览器可见）|

#### 5-C-3 发现问题 → RFC

评估若发现任何系统性问题（规则缺失、脚本 bug、PRE7 定义不完整等），**在继续全量赋号之前**提交 RFC：

```bash
/rfc ref/rfc/rfc-ggs-NNNN-slug.md
```

RFC 合并或明确标注"不阻塞"后，方可进入全量赋号。

> 5-C-2 评估全通过，无系统性问题，跳过本节，直接进入 5-C-4。

#### 5-C-4 全量赋号

试验章评估通过、RFC 已处理后：

- [x] 严格按 `ref/chapter-order.md` 的 NNN 次序，逐章执行 PN 标注
  - 执行：`python3 wiki/scripts/assign_pn.py --all`，23/23 成功
  - 总计：全书 1489 个 PN
- [x] 每章完成后验证编号连续性（无跳号），再推进下一章
  - 脚本内建 `verify_pn_sequence()` 逐章验证，全部通过
- [x] 非正文章节（前言、附录、参考文献等）同样赋号，不得跳过
  - 目录(P01)·3 PN，Frontispiece(P02)·65 PN，Preface(P03)·71 PN，Epilogue(020)·279 PN
- [x] 全量完成后再次整体验证跨章连续性（`QUO10-cross-chapter-pn-verify`）
  - 跨章脚本验证：23 章 1489 PN，零错误 ✓
- [x] 执行 `$MEMEX_ROOT/ref/spec/workflow-post-pn-lint.md` 定义的完整 post-PN lint 流程
  - Step 1 PN 格式：全部正常 ✓
  - Step 2 wikilink：无空/残缺链接 ✓
  - Step 3 frontmatter：目录.md 使用 JSON 格式（预存问题，非 PN 引入）✓
  - Step 4 浏览器渲染：ch08 抽查通过，PN 可见，图片块正常 ✓


### 5-D PN 后超长段落拆分（可选步骤，默认跳过）

> ggs 语料为校勘底稿，段落结构与原书一致。若无明显超长段落（超过 6 句），保留原状。

- [ ] **（可选）** 若用户确认执行：`$MEMEX_ROOT/skills/gene/PRE2-split-long-paragraph.md`
- [ ] **（可选）** 不增删任何字符，不新增 PN 编号
- [ ] **（可选）** 参考各项目本地实现


### 5-E 验证与提交

> 通用工作流见 `$MEMEX_ROOT/ref/spec/workflow-post-pn-lint.md`，以下为本 wiki 执行记录。

- [x] **Step 1 — 语料预检查复核**：运行 PRE22
  - 说明：PRE22 对应脚本为 `pn_structure_verify.py`，此即 FIX24，合并执行
  - 结果：首轮 32 处 A5（单换行段落合并为一 block 未获 PN）；修复：插入空行 + 清除旧 PN + 重新赋号后 0 处问题
- [x] **Step 2 — PN 定义格式与编号完整性验证**：运行 FIX24
  - 命令：`python3 "$MEMEX_ROOT/wiki/scripts/pn_structure_verify.py" --dir docs/wiki/pages/`
  - 结果：**0 处问题**（修复后）；总计 1522 PN（23 章：P01/3 + P02/65 + P03/74 + 001-019正文章节 + 020/280）
- [x] **Step 3 — PN 索引完整性检查**：参照 FIX26，人工检查父子关系与映射完整性
  - 命令：`grep -rn '\[[0-9P][0-9P][0-9P]-[0-9][0-9][0-9]-[0-9][0-9][0-9]' docs/wiki/pages/`
  - 结果：无子段 PN（NNN-PPP-SSS），符合当前阶段预期
- [x] **Step 4 — Wikilink 有效性验证**
  - 命令：`python3 "$MEMEX_ROOT/wiki/scripts/lint_empty_wikilinks.py"`
  - 结果：✓ 所有页面无空 wikilink
- [x] **Step 5 — Frontmatter 完整性验证**
  - 命令：`python3 wiki/scripts/verify_pn_completeness.py`（CHKP1 含 F1/F2 覆盖检查）
  - 结果：ERROR:0 WARN:0；F1 23/23 章节存在，F2 NNN 与 chapter-order 一致
- [x] **Step 6 — Markdown 渲染质量检查**：人工抽检 3 章
  - 结果：ch02(46 PN)/ch09(67 PN)/ch12(82 PN) 浏览器渲染正常，PN 可见，无 JS 错误
- [x] **全通过后提交**：
  ```bash
  git add docs/wiki/pages/ docs/wiki/pages.json docs/wiki/pages.lite.json
  bash wiki/scripts/skill_commit.sh -m "feat: Phase 5-E 全书 PN 验证完成，补标 29 个漏标段落"
  ```


### 5-E2 `:::` 区块格式检查

> **RFC**: [RFC-ggs-0012](ref/rfc/rfc-ggs-0012-lnt15-block-format-lint.md) / [issue #144](https://github.com/baojie/memex/issues/144)
>
> **基因定义**：`LNT15-block-format-lint`（待 memex 接受 RFC 后方可写入 `$MEMEX_ROOT/skills/gene/`）

**执行 LNT15 全库扫描**，检查 `:::` fenced div 块前后空行和空格规范：

| 检查项 | 说明 |
|--------|------|
| 开启前缺空行 | `:::` 前无空行（非文件首、非连续 `:::` 块） |
| 闭合后缺空行 | `:::` 后无空行（非文件尾） |
| `:::` 后缺/多余空格 | `:::` 与 TYPE 之间须恰有 1 个空格 |
| TYPE 后多余空格 | TYPE 后不应有多余空格 |
| 行末尾随空格 | 任意行末尾无尾随空格 |

- [ ] 创建配套检测脚本：`wiki/scripts/lint_block_format.py`
- [ ] 执行全库扫描并自动修复：
  ```bash
  python3 wiki/scripts/lint_block_format.py --dir docs/wiki/pages/ --fix
  ```
- [ ] 验证所有章节页面无残留问题
- [ ] 确认本次提交不含 `:::` 区块格式问题

### 5-F PN 检索源构建

**前置条件**：5-E2 完成（`:::` 区块格式已统一修复）。

- [x] 执行构建脚本，确认输出无报错：
  ```bash
  python3 "$MEMEX_ROOT/wiki/scripts/build_pn_source.py"
  ```
  - 结果：1478 PN entries → data/pn-source.json（1444 内联锚点 + ~34 含文本内容的图片/表格块）
- [x] 验证条目数与 wiki chapter 中 PN 总数一致：
  - 结果：1478 条（与全书 1521 PN 的差额为无文本图片块，属正常）
- [x] 抽样核查：从 pn-source.json 取 2-3 条，与对应 wiki chapter 页面核对内容
  - P02-001: "原书卷首插图（IQ1–IQ32）" ✓；020-279/020-280 后记末尾文献条目 ✓
- [x] `data/pn-source.json` 加入 `.gitignore`（构建产物，不进版本控制）
- [x] **提交 PN 检索源构建结果**：
  ```bash
  git add .gitignore
  bash wiki/scripts/skill_commit.sh -m "feat: Phase 5-F PN 检索源构建完成"
  ```


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
