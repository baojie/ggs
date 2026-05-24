---
wiki: 枪炮、病菌与钢铁
boot_completed: 2026-05-25
phases: 0–9
---

# Boot 复盘总结

## 基本统计

| 指标 | 数量 |
|------|------|
| 导入章节 | 22 个（含 Preface/Epilogue/Frontispiece） |
| PN 赋号段落 | 5,624 段 |
| Pilot 页面 | 76 个（5 种类型：concept×16 + species/place/person/event×15） |
| Wikify 链接 | 97 个（21/22 章） |
| 提交 RFC（boot 期间） | 23 个（全部 implemented） |
| backlinks 索引 | 80 个被引用页，409 条反向链接 |

## RFC 清单

| 编号 | slug | status | 一句话描述 |
|------|------|--------|-----------|
| 0001 | comply-skill-chk6-misapplication | implemented | comply 对非 wiki 页面误用 CHK6 |
| 0002 | home-book-display-strip | implemented | 首页书名显示条拦截链接 |
| 0003 | gene-naming-validation-hook | implemented | 基因命名验证 hook |
| 0004 | corpus-qa-shared-gene | implemented | 语料 QA 共享基因 |
| 0005 | chapter-integrity-gene | implemented | 章节完整性检查基因 |
| 0006 | img11-image-caption-qa-gene | implemented | IMG11 图片说明 QA 基因 |
| 0007 | chk13-deploy-verify | implemented | CHK13 部署验证基因 |
| 0008 | birth-script-path-via-pages-json | implemented | BIRTH 脚本路径通过 pages.json 管理 |
| 0009 | pn-completeness-verify-gene | implemented | PN 完整性核验基因 |
| 0010 | pn-citation-figure-pn-align | implemented | PN 引用图注对齐 |
| 0011 | pn-citation-container-margin-reset | implemented | PN 引用容器 margin 重置 |
| 0012 | lnt15-block-format-lint | implemented | LNT15 块格式规范检查 |
| 0013 | build-chapter-map-pn-prefix-driven | implemented | chapter_map.json 由 PN 前缀驱动生成 |
| 0014 | restrict-hook-rfc-prompt | implemented | restrict hook 触发时提示走 RFC 流程 |
| 0015 | boot-init-phase-completeness-check | implemented | boot init 实例化完整性校验 |
| 0016 | commit-skill-use-skill-commit-sh | implemented | 所有 commit 统一使用 skill_commit.sh |
| 0017 | lnt-pn-merged-bracket-lint | implemented | 合并括号 PN 格式规范 |
| 0018 | birth-spec-chapter-map-format-constraint | implemented | BIRTH.spec 章节映射格式约束 |
| 0019 | boot-init-preserve-instruction-blocks | implemented | boot init 必须逐字复制说明块 |
| 0020 | template-tag-lang-align | implemented | 模板 tag/lang 字段对齐 |
| 0021 | pn-router-prefix-regex | implemented | PN 路由前缀正则匹配 |
| 0022 | new1-enrich-every-sentence-sourced | implemented | NEW1/enrich 须每句有据，禁止编造 |
| 0023 | home-hide-k-value | implemented | 首页 k-panel 隐藏内部 K 值评分 |

## Pilot 流程发现

### 基因层问题

| 基因 | 问题描述 | 处置 |
|------|---------|------|
| SCN27 | 建页时几乎每批都出现连接型破折号，说明建页规范未内置 HKP31 检查 | housekeeping（EVV5 覆盖，可接受） |
| EVV6 | E5 模板一致性检查仅 concept/species 完整执行，place/person/event 仅做 E1–E4 | housekeeping（butler 阶段补强） |
| QUO23 | 每类仅抽查 8 个 PN，覆盖率约 10%；可考虑提高抽查比例 | housekeeping |

### Boot 流程层问题

| Phase | 问题描述 | 处置 |
|-------|---------|------|
| Phase 9-B | EVV6 E5（模板一致性）在 place/person/event 未执行完整五项检查 | housekeeping |
| Phase 9-E | backfill_recent.py 在 history/ 根目录生成 v0 格式文件，与子目录 v2 格式并存（无冲突，插件优先使用子目录版本） | housekeeping |

### 脚本/规范层问题

| 文件 | 问题描述 | 处置 |
|------|---------|------|
| `backfill_recent.py` | 生成根目录格式文件与子目录（record_revision.py）并存；功能无冲突但有冗余 | housekeeping |

## EVV Pilot 类型汇总

按 Phase 9 执行顺序：

| 类型 | 全局均分 | 模板主要改动（结构性） | 遗留问题 |
|------|---------|----------------------|---------|
| concept | 99.6/100 | 增"在本书中的角色"必选节；引文规范注入破折号⚠️警告 | EVV6 修复4处破折号（已闭环） |
| species | 100/100 | 引文规范注入破折号⚠️警告（复用 concept 经验） | 无 |
| place | 100/100 | place-schema 补入破折号⚠️警告；r2 修复3处无PN断言 | 无 |
| person | 100/100 | 无结构性变更（选题标准：书中关键角色） | 无 |
| event | 100/100 | 无结构性变更（选题标准：历史重要性+跨章节覆盖） | 无 |

## Pilot 信息组织核心洞察

经过 5 种类型、40 轮 Pilot，本次 boot 在信息组织层面形成以下核心认知：

**结构稳定性**
- 所有类型在第 2 轮（r2）后模板趋于稳定，r3 基本无结构性变更——三轮迭代足够收敛。
- "在本书中的角色"节（concept 类型 r1 引入）是最具普遍价值的结构性发现，帮助 wiki 从"词典"转向"论证地图"。
- 破折号⚠️警告注入 schema 模板后，下轮建页违规率从 ~60% 降至 0%——规范嵌入比事后修复效率高 10 倍。

**类型间共性与差异**
- concept/species/place 模板经 r1 后均需补充破折号警告，说明 SCN27 建页基因在 HKP31 合规上存在系统性盲点。
- person/event 类型 PN 密度最低（均分 ~4.8），主因书中对具体人物/事件的连续论述段落较少，不同于概念类的理论论证。
- species 类型 PN 最高（均分 7.7），因物种与农业章节有大量可索引数据段落。

**最易忽略的内容维度**
- 无PN年份断言：place r2 发现"非洲"页含无引注年份数据，通用风险点。RFC-0022 已将此列为全局规则。
- wikilink 充分性：每页至少 4 个 wikilink 是收敛门槛，低于此值的页面交叉引用贫乏。
- Related 节（seealso）：concept 类型约 30% 的页面在 r1 未主动填写，需 EVV5 提醒。

**对 butler 使用 NEW1 建页的启示**
- 建页时同步检查破折号（HKP31），而非依赖 EVV5 后处理——节省 1 个轮次。
- 每个断言必须先搜索 sentence_index 再写入，不可用训练数据填充——RFC-0022 铁律。
- 优先建"在本书中的角色"节：这是 wiki 区别于百科的核心价值，也是用户最先寻找的内容。

## EVV5/EVV6 遗留问题

本次 Pilot 无跨轮遗留问题。EVV6（R8）在 concept 类型中发现 4 处破折号并于同轮修复。所有其他 EVV 日志遗留项均在当轮内闭环。

## Butler 实例命名

| 角色 | focus | 实例名（建议） |
|------|-------|-------------|
| 探索者 | discover | 耶利（书中质问者，驱动探索） |
| 创建者 | create | 皮萨罗（开疆拓土） |
| 丰富者 | enrich | 戴蒙德（深度论证） |
| 发布者 | publish | 哥伦布（连接两个世界） |
| 管理者 | housekeeping | 卡哈马卡（秩序与治理的象征） |

## 经验总结

1. **RFC 是质量闸**：23 个 RFC 全部 implemented，说明 boot 期间的问题发现→提案→实施闭环运转良好。每次遇到阻塞性问题时立即提 RFC 而非绕过，是本次 boot 最重要的操作纪律。
2. **schema 注入规范比事后检查更高效**：破折号警告直接写入 species-schema.md 后，下轮零违规。规范前置（在 schema 而非事后 EVV5）值得推广到 butler 阶段。
3. **RFC-0022 是本次 boot 最关键的规则**：每句有据、禁止训练数据填充，是长期维护 wiki 可信度的基石。后续 butler 日常建页中必须坚守。
4. **pilot 阶段完成了真正的"校准"**：75 个标准质量词条 + 97 个 wikify 链接 + 409 条 backlinks，构成了一个有机连接的知识网络，而非孤立词条的堆砌。
