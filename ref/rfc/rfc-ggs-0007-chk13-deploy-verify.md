# RFC-ggs-0007: 建立部署验证基因 CHK13 并更新 BIRTH.spec.md Phase 4-D

- **Status**: implemented
- **Date**: 2026-05-24
- **Issue**: https://github.com/baojie/memex/issues/133
- **Source wiki**: ggs
- **Target**: `$MEMEX_ROOT/skills/gene/CHK13-deploy-verify.md` + `$MEMEX_ROOT/BIRTH.spec.md §4-D`

---

## Problem

BIRTH.spec.md Phase 4-D 包含 4 项浏览器人工检查：

```
- [ ] ./wiki-daemon.sh start，访问首页，确认 book card 中章节 chip 正常显示
- [ ] ./wiki-daemon.sh restart 后章节 chip 仍然显示
- [ ] 访问 #Contents，确认目录页所有 wikilink 可点击跳转
- [ ] 确认章节页面正文渲染无乱码
```

这些检查在 ggs Phase 4 执行时发现存在以下问题：

1. **人工依赖**：每次 Phase 4 完成、或 daemon 重启、或章节结构调整后，都必须人工打开浏览器逐项确认，耗时且易遗漏
2. **不可回归**：没有自动化手段在后续修改后快速回归验证
3. **覆盖面不全**：人工检查只验证了"看起来正常"，未验证底层数据的完整性——如 frontmatter 与 pages.json 一致、home.js/hero.js 配置正确、章节导航所需字段完整等
4. **各 wiki 重复劳动**：每个 wiki 在 Phase 4 都要执行相同的人工检查，没有共享的自动化工具

## Root cause

BIRTH.spec.md 在设计 Phase 4-D 时没有可用的部署验证基因。CHK11（homepage-deploy-check）侧重于首页和通用部署检查，CHK12（chapter-integrity-check）侧重于章节注册表检查，均不覆盖 TOC wikilink 解析、编码洁净度、重启持久化、导航配置等 Phase 4 特有的验证需求。

## Proposed change

### 1. 建立 CHK13 部署验证基因

路径：`$MEMEX_ROOT/skills/gene/CHK13-deploy-verify.md`

定义 7 项自动检查，替代 Phase 4-D 的 4 项人工浏览器检查：

| 基因检查 | 替代的人工检查 | 验证方式 |
|---------|---------------|---------|
| D01 — pages.json 章节完整性 | chip 显示 | 注册表字段校验 |
| D02 — home.js/hero.js 配置 | chip 显示 | PREFACE_IDS / APPENDIX_IDS / BOOK_META |
| D03 — HTTP 可达 + 文件存在 | 页面可访问 | curl 首页 + 静态资源 + 文件系统 |
| D04 — 编码洁净度 | 无乱码 | UTF-8 解码 + U+FFFD 检测 |
| D05 — TOC wikilink 可解析 | 目录页可点击 | wikilink 目标 → pages.json |
| D06 — daemon restart 后复检 | 重启后正常 | restart → 复检 D03 |
| D07 — 章节导航配置 | 上一章/下一章/回到目录 | TOC_PAGE_ID / book_seq |

### 2. 创建共享脚本

路径：`$MEMEX_ROOT/wiki/scripts/verify_deploy.py`

wiki 通用脚本，从以下本地配置读取参数：
- `local/chapter_list.py`（已有，CHK12 使用）→ EXPECTED_CHAPTERS
- `local/config/chapter.config.js`（已有）→ TOC_PAGE_ID
- `local/config/home.js`（已有）→ PREFACE_IDS / APPENDIX_IDS
- `local/config/hero.js`（已有）→ BOOK_META

### 3. 更新 BIRTH.spec.md Phase 4-D

将 4 项人工检查替换为 CHK13 引用：

```markdown
- [ ] **CHK13**（deploy-verify）：执行部署验证检查：
  ```bash
  python3 wiki/scripts/verify_deploy.py
  ```
  确认 D01–D07 全部通过（章节数据完整性、首页可达、编码洁净、TOC wikilink 可解析、重启持久化、导航配置正确）。
```

保留「回填修订历史」和「commit」步骤不变。

## Impact

- **正面**：Phase 4-D 验证从 4 项人工操作 + 约 5 分钟浏览器检查，缩减为 1 条命令 + 约 10 秒自动执行。后续回归验证成本趋近于零。
- **负面**：自动检查无法验证视觉样式（如 chip 颜色、字体、布局），极端情况下样式 CSS 被破坏仍需人工发现。但此场景属部署范畴（Phase 9-E CHK11 L6），不应由 Phase 4-D 承担。
- **迁移成本**：各 wiki 需确保 `local/chapter_list.py` 已存在（CHK12 前置条件），无需额外配置。

## Gene 草稿

详见 RFC 文件附件。

## Implementation

- **commit**: `764e36c`（memex main）
- **日期**: 2026-05-24
- **实施内容**:
  1. 新增 `skills/gene/CHK13-deploy-verify.md`（D01–D07 七项检查定义，D06 标注为可选）
  2. 新增 `wiki/scripts/verify_deploy.py`（共享验证脚本，配置路径修正为 `docs/wiki/local/config/`）
  3. 更新 `BIRTH.spec.md §4-D`：4 项人工检查 → CHK13 一条命令
- **ADM3 结论**: faithful
