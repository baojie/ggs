# 枪炮、病菌与钢铁 — 增长流程 (GROW)

> 前置：`BIRTH.md` Phase 0–10 全部完成，butler 日常循环已启动。
> BIRTH Phase 9（类型 Pilot）等同于 GROW Phase 1（种子层），无需重复执行。
>
> **参考文献**：`$MEMEX_ROOT/ref/spec/butler-phased-strategy-seed.md`
> 本文档的分阶段策略、螺旋生长模型、Gene 库阶段映射和每轮质量门均源于此文件。
> 执行前建议先读该文件，理解各决策背后的跨 wiki 数据依据。

---

## 使用方式

1. **GROW.spec.md**（位于 `$MEMEX_ROOT`）：通用模板，`{{占位符}}` 待具体 wiki 填写
2. **GROW.md**（本文件，位于 wiki 根目录）：按本模板复制并记录实际执行状态与参数

> **写作原则**：做一步写一步。各 wiki 的 GROW.md 只记录已执行的步骤，未执行的 Phase 待真正启动时才从本模板复制。

---

## grow_state.json — Phase 2 显式状态机

> Phase 2 是三层嵌套循环（外层 Phase 2.N、中层类型轮次、内层单轮 butler），控制状态以机读 JSON 文件存储，避免 butler 每轮扫描历史日志重建上下文。
>
> **权威设计文档**：`$MEMEX_ROOT/ref/spec/grow-state-machine.md`
> 本节为摘要，字段语义、决策算法、状态转移规则、Reconciliation、不变式断言均以该文件为准。

**文件路径**：`local/state/grow_state.json`

**初始化模板**（见 `$MEMEX_ROOT/templates/grow_state.template.json`）：

```json
{
  "schema_version": 1,
  "wiki": "枪炮、病菌与钢铁",
  "grow_phase": "2.1",
  "phase2_iteration": 1,
  "phase2_closed": false,

  "current_type": "concept",
  "type_queue": ["species", "place", "person", "event"],
  "closed_types": [],

  "counters": {
    "current_round": 0,
    "type_round": 0,
    "rounds_since_last_evv5": 0,
    "rounds_since_last_discover": 0,
    "discover_streak_low": 0
  },

  "thresholds": {
    "evv5_interval": 10,
    "discover_queue_threshold": 10,
    "discover_periodic_interval": 10,
    "type_close_streak": 3,
    "type_close_new_candidate_min": 3
  },

  "pending_new_types": [],
  "last_updated_round": 0
}
```

**字段速查**（完整语义见 `grow-state-machine.md §1.2`）：

| 字段 | 说明 |
|------|------|
| `grow_phase` | 字符串，当前子阶段（`"2.1"` / `"2.2"` / `"3"`）；与 `butler.json.grow_phase`（整数）含义不同，不互相赋值 |
| `current_type` | 正在扩张的类型；仅 2.N-Z 处理期间为 `null` |
| `counters.discover_streak_low` | 连续 discover 低产轮次数，达 `type_close_streak` 时触发类型关闭 |
| `counters.rounds_since_last_evv5` | 距上次 EVV5 轮数；**类型切换时重置为 0** |
| `thresholds.discover_periodic_interval` | 定期 discover 间隔（默认 10），与队列低水位触发互为补充 |
| `pending_new_types` | 2.N-Z-B 总结写入；非空 → 必须启动 Phase 2.N+1 |
| `last_updated_round` | 最后写入轮次，用于检测 state 是否与日志同步 |

---

## Phase 0：基线摸底

> **目标**：在进入任何建设阶段之前，准确掌握当前 wiki 的页面库现状、候选池深度、
> 质量分布，并据此确定应从 GROW 哪个 Phase 开始推进。
>
> **执行时机**：BIRTH Phase 10 完成后立即执行，或 butler 运行一段时间后重新摸底。
> Phase 0 可反复执行——每次重新定相（re-phase）都从此开始。
>
> **产出**：`local/memory/grow_baseline.md`，包含完整现状快照和阶段定位结论。

---

### 0-A 前置验证

确认 BIRTH 已真正完成，butler 基础设施就绪：

- [x] `local/memory/boot_summary.md` 存在（BIRTH Phase 10 的标志）：
  ```bash
  cat local/memory/boot_summary.md
  ```
  确认字段：`boot_completed`（日期）、`phases: 0–10`、`Pilot 页面`（类型数量）

- [x] butler 轮次计数文件存在：
  ```bash
  cat logs/butler/round_counter.txt
  ```
  记录当前轮次 R_current = 40

- [x] 基础数据文件完整：
  ```bash
  ls docs/wiki/pages.json         # 页面注册表
  ls data/sentence_index/         # 句子库（Phase 6-A 产物）
  ls logs/butler/queue.md         # butler 候选队列
  ls local/template/              # 各类型图式模板
  ```
  以上任一缺失说明 BIRTH 未完成，不可进入 GROW。

- [x] （Phase 2 及以后）state 文件存在且 schema 合法：
  ```python
  import json
  try:
      s = json.load(open('local/state/grow_state.json'))
      assert s['schema_version'] == 1
      print(f'phase={s["grow_phase"]}  type={s["current_type"]}  round={s["counters"]["current_round"]}')
  except FileNotFoundError:
      print('state 文件不存在——Phase 2 开始前在 2.1-A 末尾初始化')
  ```
  若文件不存在但已处于 Phase 2 → 按改动 2 的初始化脚本补建，从当前 pages.json 重建 closed_types。

---

### 0-B 页面库现状扫描

量化当前页面库的规模与质量分布：

- [x] **统计页面总数和类型分布**：
  ```python
  python3 -c "
  import json
  from collections import Counter
  d = json.load(open('docs/wiki/pages.json'))
  pages = d['pages']
  types = Counter(v.get('type','?') for v in pages.values())
  quals = Counter(v.get('quality','?') for v in pages.values())
  print('总页数:', len(pages))
  print('按类型:', dict(sorted(types.items())))
  print('按质量:', dict(sorted(quals.items())))
  "
  ```
  记录结果：
  - 总页数 = 100
  - 章节类页面（type=chapter）= 22（不参与 GROW 质量统计）
  - 词条类页面（非 chapter/overview/list）= 76
  - 质量分布（stub/basic/standard/featured/premium）= standard×76

- [x] **计算关键比率**：
  - stub 比率 = 0/76 × 100% = **0.0%**（目标 Phase 2 结束时 < 20%）
  - featured 及以上比率 = 0/76 × 100% = **0.0%**（目标 Phase 3 结束时 > 50%）

- [x] **类型覆盖完整性**：
  对照 `local/template/` 下的模板文件，确认每种主要类型当前有多少词条：
  ```bash
  ls local/template/
  ```
  填写覆盖表：

  | type | 模板存在 | 当前词条数 | 预估总量 | 覆盖率 |
  |------|---------|---------|---------|--------|
  | concept | ✓ | 16 | 70–90 | 18–23% |
  | species | ✓ | 15 | 60–80 | 19–25% |
  | place | ✓ | 15 | 50–70 | 21–30% |
  | person | ✓ | 15 | 40–60 | 25–38% |
  | event | ✓ | 15 | 20–35 | 43–75% |

- [x] **确认 type 标签映射完整**：
  对照 `docs/wiki/local/config/types.js` 中的 `TYPE_LABELS`，确认 `docs/wiki/pages.json` 中出现的每个 type 均有对应中文标签。缺失的立即补录，否则页面底部类型标签将显示为空白。
  ```bash
  # 列出 pages.json 中所有出现的 type
  python3 -c "
  import json
  d = json.load(open('docs/wiki/pages.json'))
  types = sorted(set(v.get('type','?') for v in d['pages'].values()))
  print(types)
  "
  # 对比 local/config/types.js 中已注册的 TYPE_LABELS key
  grep -oP "(?<=  )\w+(?=:)" docs/wiki/local/config/types.js
  ```
  不在 `TYPE_LABELS` 中的 type → 立即在 `docs/wiki/local/config/types.js` 补录，格式：`typeName: '中文标签'`

---

### 0-C Pilot 信息读取

从 BIRTH 产出中提取已建立的质量基线和模板约定：

- [x] 读取 `local/memory/boot_summary.md` 的 Pilot EVV 汇总表：
  ```bash
  grep -A 20 "Pilot EVV" local/memory/boot_summary.md
  ```
  提取每种类型的：
  - EVV 轮次均分（r1/r2/r3 → 趋势是否收敛）
  - 主要模板改动（写入 grow_baseline.md 的「类型模板约定」）
  - 遗留问题（写入 grow_baseline.md 的「已知债务」）

- [x] 确认 Pilot 遗留问题的处理状态：
  对 boot_summary.md 中每个「遗留问题」判断：
  - 已修复 → 记录修复方式
  - 未修复但不阻塞扩张 → 记入「已知债务」，GROW Phase 2 扩张前处理
  - 阻塞扩张 → 必须先修复，再进入 Phase 2

---

### 0-D 候选池评估

评估还有多少可通过 NEW1 建词条，判断候选池是否充足：

- [x] **查看当前队列**：
  ```bash
  wc -l logs/butler/queue.md
  grep -c "^\-" logs/butler/queue.md  # 候选条目数
  ```
  记录：当前队列条目数 = 0（队列文件存在但尚无候选条目，需 discover 轮次填充）

- [x] **估算各类型剩余候选量**：
  查看 `logs/butler/type-survey.md`（BIRTH Phase 7-A 产物）：
  ```bash
  cat logs/butler/type-survey.md
  ```
  对照当前词条数，计算各类型的「理论剩余量」：
  - concept 估算总量 70–90 - 已建 16 = 剩余 54–74
  - species 估算总量 60–80 - 已建 15 = 剩余 45–65
  - place 估算总量 50–70 - 已建 15 = 剩余 35–55
  - person 估算总量 40–60 - 已建 15 = 剩余 25–45
  - event 估算总量 20–35 - 已建 15 = 剩余 5–20

- [x] **判断候选充足性**：
  - 各类型剩余 > 10 条 → 候选充足，Phase 2 可正常推进
  - 某类型剩余 < 5 条 → 该类型接近枯竭，需提前准备 gap scan（SCN9/SCN18）
  - 多数类型剩余 < 5 条 → 跳过 Phase 2，直接进入 Phase 3（深度提升）

---

### 0-E 链接网络密度评估

评估词条之间的链接密度，为 wikify 时机决策提供依据：

- [x] **检查现有 wikilink 数量**：
  ```bash
  grep -roh '\[\[[^\]]*\]\]' docs/wiki/pages/ --include="*.md" | wc -l
  ```
  记录：当前 wikilink 总数 = 422

- [x] **检查 backlinks 索引**（如已构建）：
  ```bash
  python3 -c "
  import json
  try:
      d = json.load(open('docs/wiki/backlinks.json'))
      covered = len([k for k, v in d.items() if v])
      print(f'被引用页: {covered}/{len(d)}, 总反链: {sum(len(v) for v in d.values())}')
  except FileNotFoundError:
      print('backlinks.json 不存在，尚未构建')
  "
  ```
  记录：被引用页 80/80，总反链 409 条

- [x] **判断 wikify 优先级**：
  - wikilink 总数 / N_entries = 422 / 76 ≈ **5.6 条/词条** → 链接密度适中
  - 有类型已完成但未 wikify → Phase 2 开始前先补做一次该类型的 wikify

---

### 0-F GROW 阶段定位

基于以上扫描结果，确定当前处于 GROW 哪个阶段：

> **判断规则（按优先级）**：

| 条件 | 结论 |
|------|------|
| Pilot（Phase 9）未完成，且 BIRTH Phase 9 从未执行 | 🌱 **GROW Phase 1**（种子层）— 执行 1-E 完整建设 |
| Pilot（Phase 9）未完成，BIRTH Phase 9 正在进行中 | ⛔ 返回 BIRTH，完成 Phase 9 后重新做 Phase 0 |
| Pilot（Phase 9）已完成，存在阻塞扩张的遗留问题 | ⛔ 先修复遗留问题，修复完成后重新做 Phase 0 |
| Pilot 已完成，stub% = 0，N_entries < 80 | 🌱 **GROW Phase 2**（广度扩张）— 候选充足时直接开始 |
| Pilot 已完成，stub% 0–20%，featured% < 20% | 🌱 **GROW Phase 2**（广度扩张）— 继续铺广度 |
| Pilot 已完成，stub% < 5%，featured% < 50% | 📈 **GROW Phase 3**（深度提升）— 广度基本到位 |
| Pilot 已完成，stub% < 5%，featured% > 50% | 💡 **GROW Phase 4**（洞察层）— 质量基线已高 |

- [x] 根据规则确认阶段：当前应从 **GROW Phase 2**（广度扩张）开始
- [x] 记录定位理由：Pilot 已完成（BIRTH Phase 9，R1–R40），stub%=0%，N_entries=76 < 80，候选充足（各类型剩余 5–74 条）

---

### 0-G 基线快照写入

将以上所有信息写入 `local/memory/grow_baseline.md`：

- [x] 创建或更新文件（每次重新摸底覆盖上次）：

```markdown
# GROW 基线摸底 — 枪炮、病菌与钢铁

date: 2026-05-25
butler_round: R40
grow_phase: Phase 2（广度扩张）

## 页面库现状

总页数: 100（含章节 22 个，overview 2 个）
词条类页面: 76（concept 16 / species 15 / place 15 / person 15 / event 15）
质量分布: standard 76
stub 比率: 0.0%
featured+ 比率: 0.0%

## 候选池评估

当前队列条目数: 0（需首轮 discover 填充）
各类型估算剩余候选量:
- concept: 54–74
- species: 45–65
- place: 35–55
- person: 25–45
- event: 5–20
总体判断: 候选充足（各类型预估剩余均 > 5）

## Pilot 遗留债务

（见 boot_summary.md Pilot 流程发现节）
- SCN27 建页时未内置 HKP31 破折号检查 → 非阻塞，housekeeping
- EVV6 E5 在 place/person/event 未完整执行 → 非阻塞，butler 阶段补强
- QUO23 抽查覆盖率约 10% → 非阻塞，housekeeping

## 链接网络

wikilink 总数: 422
平均每词条: 5.6 条
backlinks 覆盖: 80/80 页，409 条反链

## 阶段定位

定位结论: Phase 2 — 广度扩张
理由: Pilot 已完成（BIRTH Phase 9），stub%=0%，N_entries=76 < 80，候选池充足（最小类型 event 尚余 5–20 条）

## 下一步优先动作（Top 3）

1. 初始化 grow_state.json，启动 Phase 2.1 concept 类型扩张
2. 安排第一轮 discover（SCN28），填充队列候选
3. Phase 2.1-0 与用户确认 WU quota，写入 butler.json
```

- [x] 提交基线文档：
  ```bash
  git add local/memory/grow_baseline.md
  bash wiki/scripts/skill_commit.sh "docs: GROW Phase 0 基线摸底完成"
  ```

---

### 0-X 验收标准

Phase 0 完成的标志：

- [x] `local/memory/grow_baseline.md` 存在且填写完整（无 `{{占位符}}`）
- [x] 阶段定位明确（Phase 2 / 3 / 4）
- [x] 遗留债务已分类（阻塞 / 非阻塞）
- [x] 非阻塞债务已记录到 butler 队列或 housekeeping 任务
- [x] 阻塞债务已处理（或确认可接受跳过）

---

> **Phase 0 完成后**：按 0-F 的阶段定位，跳转至对应 Phase 开始建设。

---

## Phase 1：种子层（Seed，R1–R50）

> **对应关系**：BIRTH Phase 9（类型 Pilot）即为 Phase 1 的执行体。
> 已完成 BIRTH Phase 9 的 wiki **不重新执行**，只做核验（1-A / 1-B / 1-C）和补建（1-D）。
> 未做过类型 Pilot 的 wiki（如直接从 BIRTH Phase 8 跳入 GROW）需完整执行 1-E。
>
> **目标**：每个主要类型有 2–5 个 standard 质量词条作为质量基线，图式模板稳定，
> 首批纠错 gene 归档，可支撑 Phase 2 批量建设。
>
> **广度:深度 = 0:10**（先立质量标尺，不铺面）。
> 参考 `$MEMEX_ROOT/ref/spec/butler-phased-strategy-seed.md §Phase 1`。

---

### 1-A 读取 Pilot 产出

从 BIRTH Phase 9 / `local/memory/boot_summary.md` 提取种子层完成状态：

- [ ] 确认 `boot_summary.md` 包含 Pilot EVV 汇总：
  ```bash
  grep -A 20 "Pilot EVV" local/memory/boot_summary.md
  ```
  提取并记录（填入 `grow_baseline.md` 如未填写）：

  | 类型 | Pilot 页数 | EVV 均分（最终轮）| 模板稳定 | 遗留问题 |
  |------|----------|----------------|---------|---------|
  | concept | 16 | 99.6/100 | ✓ | EVV6 修复4处破折号（已闭环）|
  | species | 15 | 100/100 | ✓ | 无 |
  | place | 15 | 100/100 | ✓ | 无 |
  | person | 15 | 100/100 | ✓ | 无 |
  | event | 15 | 100/100 | ✓ | 无 |

- [ ] 确认每种已 Pilot 类型满足种子层最低标准：
  - Pilot 页数 ≥ 2（至少有对比参照）
  - EVV 最终轮均分 ≥ 75（低于此值说明语料不足或模板有问题，不可进入 Phase 2）
  - 模板经 ≥ 2 轮 EVV 后无结构性变动（template frozen）

  > 若某类型 EVV 均分 < 75 → 该类型不进入 Phase 2 批量建设，先定位根因：
  > 语料不足（接受现状，Phase 2 筛候选）/ 模板问题（修模板后再跑 1 轮 EVV）。

---

### 1-B 确认图式模板

每种已 Pilot 类型必须有对应图式模板文件，且内容已根据 EVV 反馈稳定：

- [ ] 列出 `local/template/` 下已有模板：
  ```bash
  ls local/template/
  ```
  确认每个主要类型均有 `{type}-schema.md`，且文件内容反映了 EVV 最终轮的模板约定。

  已有模板：concept-schema.md / event-schema.md / person-schema.md / place-schema.md / species-schema.md（共 5 种，全部 P1 类型覆盖）

- [ ] 对每个模板文件确认以下内容存在：
  - `## frontmatter 字段`（含必填/可选标注）
  - `## 标准节结构`（列出各 `## 节名`，注明必选/可选）
  - `## 写作约束`（篇幅上限、引文密度、wikilink 要求等）
  - `## 质量评分标准`（本类型的 EVV 评分维度，从 EVV6 日志提取）

  > 若模板缺失上述任一部分 → 补全后再进入 Phase 2，Phase 2 批量建设的质量一致性依赖于此。

- [ ] 识别 **type-survey 中有但尚无模板的类型**（新类型）：
  ```bash
  grep -E "^###|估算数量" logs/butler/type-survey.md 2>/dev/null
  ```
  对照 `local/template/`，列出：新类型 = organization、list（均为 P3，暂不建立 Mini-Pilot；type-survey 已记录，Phase 2.1-A 不纳入扩张队列）

---

### 1-C 确认首批纠错 Gene 归档

种子层的核心产出之一是从 Pilot 错误中提炼的纠错 gene。按纠错 gene 演化机制：

> 发现批量错误 → 写 gene → 批量修复存量 → gene 归档 → 下轮 W4 加入检查
> （详见 `$MEMEX_ROOT/ref/spec/butler-phased-strategy-seed.md §纠错 gene 演化机制`）

- [ ] 检查是否有 EVV 日志记录的错误模式已转化为 gene 文件：
  ```bash
  ls local/gene/ 2>/dev/null || echo "local/gene/ 不存在"
  ls ref/spec/ | grep -i "rule\|lint\|fix\|error" 2>/dev/null || true
  ```
  local/gene/ 现有：LOCAL-ggs01-corpus-final-format-qa.md（语料格式 QA 基因，非纠错 gene）

- [ ] 对照 EVV6 各类型日志，列出已知批量错误模式：

  | 错误模式 | 来源类型 | 已有 gene/规则 | 待归档 |
  |---------|---------|-------------|--------|
  | 连接型破折号（HKP31 违规）| concept/species/place | ✓（HKP31 warning 已注入 schema 模板，下轮建页违规率→0%）| 无需单独 gene |
  | QUO23 引文核验覆盖率约 10%（抽查不足）| 全类型 | ✗（无专门 gene）| 记为 housekeeping，butler 阶段提高抽查比例 |

- [ ] 每个已识别的批量错误模式，确认处理路径之一：
  - 破折号 → 路径 b：已在 schema 模板中注入 ⚠️ 警告（等价于 gene 前置注入）
  - QUO23 覆盖率 → 路径 c：记录为 housekeeping，Phase 2 中逐步提升

---

### 1-D 处理新类型（如有）

若 1-B 发现 type-survey 中存在未 Pilot 的类型（event / index / place 等）：

- [ ] 对每个新类型，在 Phase 2.1-A 开始时执行 **Mini-Pilot**（不阻塞 Phase 1 验收）：
  1. 参考现有最相似类型的模板，起草新类型 `{type}-schema.md`
  2. 使用 NEW1 建 2–3 个代表性词条（手选语料最丰富的候选）
  3. 执行 1 轮 EVV5（schema 反思）
  4. 根据 EVV5 结论更新模板，记录本类型质量上限
  5. 若均分 ≥ 75 → 模板可用，可进入 Phase 2 批量建设
  6. 若均分 < 75 → 分析根因（通常是语料稀薄），决定是否纳入 Phase 2

- [ ] 记录新类型 Mini-Pilot 计划（写入 wiki 的 GROW.md Phase 2.1-A 节）：
  - organization（P3，15–25 条）：Phase 2 不纳入扩张队列，Phase 3 重新评估
  - list（P3，~5 条）：候选稀少，暂不建模板

---

### 1-E 完整执行种子层（BIRTH Phase 9 未做时）

> 已完成 BIRTH Phase 9（R1–R40），本节跳过。

---

### 1-X 退出条件

Phase 1 完成的标志（全部满足方可进入 Phase 2）：

- [ ] 所有主要类型各有 ≥ 2 个 standard 页面作为质量基准
- [ ] 每种类型有稳定的 `local/template/{type}-schema.md`（EVV 后无结构变动）
- [ ] `local/memory/boot_summary.md` 或 GROW.md 中记录了各类型 EVV 均分基线
- [ ] 所有 Pilot 遗留的批量错误模式已分类（已归档 gene / 已记录待处理 / 已确认可接受）
- [ ] `grow_baseline.md` 已填写 Phase 1 完成状态（通常在 Phase 0 已完成）
- [ ] 新类型（如有）的 Mini-Pilot 计划已写入 GROW.md Phase 2.1-A

---

## Phase 2：广度扩张

> 状态：未开始

---
