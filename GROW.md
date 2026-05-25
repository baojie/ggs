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

- [x] 确认 `boot_summary.md` 包含 Pilot EVV 汇总：
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

- [x] 确认每种已 Pilot 类型满足种子层最低标准：
  - Pilot 页数 ≥ 2（至少有对比参照）
  - EVV 最终轮均分 ≥ 75（低于此值说明语料不足或模板有问题，不可进入 Phase 2）
  - 模板经 ≥ 2 轮 EVV 后无结构性变动（template frozen）

  > 若某类型 EVV 均分 < 75 → 该类型不进入 Phase 2 批量建设，先定位根因：
  > 语料不足（接受现状，Phase 2 筛候选）/ 模板问题（修模板后再跑 1 轮 EVV）。

---

### 1-B 确认图式模板

每种已 Pilot 类型必须有对应图式模板文件，且内容已根据 EVV 反馈稳定：

- [x] 列出 `local/template/` 下已有模板：
  ```bash
  ls local/template/
  ```
  确认每个主要类型均有 `{type}-schema.md`，且文件内容反映了 EVV 最终轮的模板约定。

  已有模板：concept-schema.md / event-schema.md / person-schema.md / place-schema.md / species-schema.md（共 5 种，全部 P1 类型覆盖）

- [x] 对每个模板文件确认以下内容存在：
  - `## frontmatter 字段`（含必填/可选标注）
  - `## 标准节结构`（列出各 `## 节名`，注明必选/可选）
  - `## 写作约束`（篇幅上限、引文密度、wikilink 要求等）
  - `## 质量评分标准`（本类型的 EVV 评分维度，从 EVV6 日志提取）

  > 若模板缺失上述任一部分 → 补全后再进入 Phase 2，Phase 2 批量建设的质量一致性依赖于此。

- [x] 识别 **type-survey 中有但尚无模板的类型**（新类型）：
  ```bash
  grep -E "^###|估算数量" logs/butler/type-survey.md 2>/dev/null
  ```
  对照 `local/template/`，列出：新类型 = organization、list（均为 P3，暂不建立 Mini-Pilot；type-survey 已记录，Phase 2.1-A 不纳入扩张队列）

---

### 1-C 确认首批纠错 Gene 归档

种子层的核心产出之一是从 Pilot 错误中提炼的纠错 gene。按纠错 gene 演化机制：

> 发现批量错误 → 写 gene → 批量修复存量 → gene 归档 → 下轮 W4 加入检查
> （详见 `$MEMEX_ROOT/ref/spec/butler-phased-strategy-seed.md §纠错 gene 演化机制`）

- [x] 检查是否有 EVV 日志记录的错误模式已转化为 gene 文件：
  ```bash
  ls local/gene/ 2>/dev/null || echo "local/gene/ 不存在"
  ls ref/spec/ | grep -i "rule\|lint\|fix\|error" 2>/dev/null || true
  ```
  local/gene/ 现有：LOCAL-ggs01-corpus-final-format-qa.md（语料格式 QA 基因，非纠错 gene）

- [x] 对照 EVV6 各类型日志，列出已知批量错误模式：

  | 错误模式 | 来源类型 | 已有 gene/规则 | 待归档 |
  |---------|---------|-------------|--------|
  | 连接型破折号（HKP31 违规）| concept/species/place | ✓（HKP31 warning 已注入 schema 模板，下轮建页违规率→0%）| 无需单独 gene |
  | QUO23 引文核验覆盖率约 10%（抽查不足）| 全类型 | ✗（无专门 gene）| 记为 housekeeping，butler 阶段提高抽查比例 |

- [x] 每个已识别的批量错误模式，确认处理路径之一：
  - 破折号 → 路径 b：已在 schema 模板中注入 ⚠️ 警告（等价于 gene 前置注入）
  - QUO23 覆盖率 → 路径 c：记录为 housekeeping，Phase 2 中逐步提升

---

### 1-D 处理新类型（如有）

若 1-B 发现 type-survey 中存在未 Pilot 的类型（event / index / place 等）：

- [x] 对每个新类型，在 Phase 2.1-A 开始时执行 **Mini-Pilot**（不阻塞 Phase 1 验收）：
  1. 参考现有最相似类型的模板，起草新类型 `{type}-schema.md`
  2. 使用 NEW1 建 2–3 个代表性词条（手选语料最丰富的候选）
  3. 执行 1 轮 EVV5（schema 反思）
  4. 根据 EVV5 结论更新模板，记录本类型质量上限
  5. 若均分 ≥ 75 → 模板可用，可进入 Phase 2 批量建设
  6. 若均分 < 75 → 分析根因（通常是语料稀薄），决定是否纳入 Phase 2

- [x] 记录新类型 Mini-Pilot 计划（写入 wiki 的 GROW.md Phase 2.1-A 节）：
  - organization（P3，15–25 条）：Phase 2 不纳入扩张队列，Phase 3 重新评估
  - list（P3，~5 条）：候选稀少，暂不建模板

---

### 1-E 完整执行种子层（BIRTH Phase 9 未做时）

> 已完成 BIRTH Phase 9（R1–R40），本节跳过。

---

### 1-X 退出条件

Phase 1 完成的标志（全部满足方可进入 Phase 2）：

- [x] 所有主要类型各有 ≥ 2 个 standard 页面作为质量基准
- [x] 每种类型有稳定的 `local/template/{type}-schema.md`（EVV 后无结构变动）
- [x] `local/memory/boot_summary.md` 或 GROW.md 中记录了各类型 EVV 均分基线
- [x] 所有 Pilot 遗留的批量错误模式已分类（已归档 gene / 已记录待处理 / 已确认可接受）
- [x] `grow_baseline.md` 已填写 Phase 1 完成状态（通常在 Phase 0 已完成）
- [x] 新类型（如有）的 Mini-Pilot 计划已写入 GROW.md Phase 2.1-A

---

## Phase 2：广度扩张（Phase 2.1 起）（Expansion，R~50–500）

> **目标**：按类型顺序逐一扩张，每种类型的主要候选耗尽后再推进下一种，
> 最终 stub% < 20%，主要类型覆盖率 > 60%。
>
> **广度:深度 = 7:3**。建页为主，每类完成后立即提质一批，不让 stub 积压。
> 参考 `$MEMEX_ROOT/ref/spec/butler-phased-strategy-seed.md §Phase 2` 和 `§每轮质量门`。

---

### 2.1-0 基本配置（Phase 2 开始前一次性执行）

在进入批量建设前，与用户确认每轮工作量上限，写入 `local/config/butler.json`。

#### 2.1-0-A 展示常用任务 WU 参考表

向用户打印以下参考值（来源：`$MEMEX_ROOT/skills/SKILL_W2_Butler基因表达.md §WU计费概览`）：

| 任务类型 | 代表 gene | WU | 说明 |
|---------|----------|-----|------|
| 新建词条（standard 档）| NEW1-create-page | **100** | 包含 corpus_search + 写作 + frontmatter |
| 质量提升（basic→standard）| RCH2-enrich-grade | **50** | 补引文 + 扩散文 |
| 发现候选 | SCN28-wanted-discover | **30** | 扫描红链 + LLM 候选发现 |
| wikilink 注入（单页）| BLK3-wikilink-pass | **50** | 全页 plain text → `[[...]]` |
| schema 反思 | EVV5-schema-reflect | **80** | 扫描全类型 + 输出反思报告 |
| frontmatter 字段补全 | FLD1-update-description | **5** | 单字段批量写入 |
| 格式修复（PN/wikilink）| FIX10/FIX11 | **2–10** | 逐条修复 |

**典型轮次 WU 消耗**：

| 轮次模式 | 包含操作 | 预估 WU |
|---------|---------|---------|
| 轻量轮 | 1 页 NEW1 新建 | ~100–130 |
| 标准轮 | 1 页 NEW1 新建 + 1 页 enrich | ~150–180 |
| 重型轮 | 2 页 NEW1 新建 | ~200–230 |
| 发现轮 | discover + 队列整理 | ~50–80 |
| wikify 轮 | 10 页 wikilink pass | ~200–300 |

#### 2.1-0-B 与用户确认 WU quota

询问用户：

```
每轮 WU 上限建议设为多少？

  推荐选项：
  A — 200 WU/轮（标准轮 × 1，适合稳健推进）
  B — 300 WU/轮（可容纳重型轮，速度更快）
  C — 500 WU/轮（批量建设模式，适合集中建站期）
  D — 自定义

  说明：WU 上限只是软约束，butler 在单轮内不会因为 WU 超限而中断；
  超限时 W3 自评会记录超支，下轮优先选轻量任务补偿。
```

用户确认后，记录：`wu_quota_per_round = 1000`

#### 2.1-0-C 写入 butler.json

在现有 `local/config/butler.json` 中追加 `wu_quota_per_round` 字段：

```json
{
  "corpus_file": "...",
  "chapter_pattern": "...",
  "wu_quota_per_round": 1000,
  "grow_phase": 2
}
```

> `grow_phase` 字段供 butler 和 /grow skill 读取当前阶段，无需每次重新做 Phase 0 摸底。

- [x] 确认字段已写入且 JSON 合法：
  ```bash
  python3 -c "import json; print(json.load(open('local/config/butler.json')))"
  ```
- [x] 提交配置变更：
  ```bash
  git add local/config/butler.json
  bash wiki/scripts/skill_commit.sh "config: Phase 2 WU quota 配置（1000 WU/轮）"
  ```

---

### 2.1-A 新类型 Mini-Pilot（如有）

若 Phase 1 发现了尚无模板的新类型（type-survey 中有但未 Pilot）：

**对每个新类型，在扩张该类型前执行 Mini-Pilot（2–3 页 + 1 轮 EVV5）**：

- [x] 参考最相近类型的 `*-schema.md`，起草 `local/template/{type}-schema.md`
- [x] 手选 2–3 个语料最丰富的候选，使用 NEW1 建页至 standard（走完整写作流程）
- [x] 执行 EVV5：扫描这 2–3 页，识别系统性问题，更新模板
- [x] 均分 ≥ 75 → 模板可用，**将该类型加入 2.1-B 串行扩张队列，后续使用 NEW1 建页全部走 2.1-B 标准流程**
- [x] 均分 < 75 → 分析根因后决定是否继续（接受 stub 档 / 暂不纳入 Phase 2 / 补语料后重测）

> **N/A**：Phase 1 无新类型（organization/list 标注为 P3，不进入 Phase 2）。以上均跳过。

> Mini-Pilot 同样须执行每轮 EXIT-GATE（见 §2.1-C），并写入日志（见 §2.1-D）。
> Mini-Pilot 的 2–3 页计入 2.1-B 的建页总数，无需另行统计。

- [x] mini-pilot 完成后，初始化 state 文件：
  ```python
  import json, os
  os.makedirs('local/state', exist_ok=True)
  state = {
    "schema_version": 1,
    "wiki": "枪炮、病菌与钢铁",
    "grow_phase": "2.1",
    "phase2_iteration": 1,
    "phase2_closed": False,
    "current_type": "concept",
    "type_queue": ["species", "place", "person", "event"],  # 按 2.1-B 确认的顺序
    "closed_types": [  # Pilot 已饱和类型（如 strategy）若存在，预登记到此列表
    ],
    "counters": {
      "current_round": 40,
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
    "last_updated_round": 40
  }
  json.dump(state, open('local/state/grow_state.json', 'w'), ensure_ascii=False, indent=2)
  print('state 初始化完成')
  ```

- [x] 验证文件合法：
  ```bash
  python3 -c "import json; s=json.load(open('local/state/grow_state.json')); print(s['grow_phase'], s['current_type'])"
  ```

- [x] 提交（与 mini-pilot 同批或单独提交）：
  ```bash
  git add local/state/grow_state.json
  bash wiki/scripts/skill_commit.sh "config: 初始化 GROW state 文件（Phase 2.1 起点）"
  ```

---

### 2.1-B 类型扩张顺序

类型扩张采用**串行模式**：一种类型的主要候选耗尽后，再开始下一种。不同类型不混合建页。

**顺序由以下原则决定（在具体 wiki 的 GROW.md 中记录实际顺序）**：

1. **新类型优先**：Mini-Pilot 未做的类型先做，建立质量基准后再批量
2. **基础实体在前**：对其他类型有高引用价值的类型先建（概念 > 人物 > 公司 > 事件）
3. **候选充足优先**：剩余候选 < 5 条的类型跳到队列末尾，避免强行扩张枯竭类型

**候选耗尽判断**：

> 当某类型连续 3 轮 discover 发现的新候选 < 3 条时，判定该类型候选基本耗尽，
> 停止扩张，转入下一类型。不要强行凑数。
> 耗尽后的类型在 GROW.md 中标记「候选耗尽，已关闭」。

**discover 轮次调度规则**：

> discover 本身消耗一个完整轮次（`SCN28-wanted-discover`，约 30–50 WU），
> 应在以下时机主动安排，而非等候选池见底才发现：
>
> - **触发条件 A**：当前类型队列有效候选 < 10 条（近三轮建页速率下此数量约够 5 轮）
> - **触发条件 B**：每完成 10 轮建页轮次（定期刷新），不论候选是否充足
>
> discover 轮次同样须写日志（格式同 2.1-D），EXIT-GATE 只需执行 G4（记录完整性），
> 跳过 G1/G2/G3/G5（本轮无 NEW1 新建/修改页）。

**EVV5 周期检查节奏**：每完成 10 轮建页轮次，安排一次 EVV5（`EVV5-schema-reflect`，约 80 WU）。

> - 对当前正在扩张的类型执行：扫描该类型全部已建页面，反思模板是否需要调整
> - EXIT-GATE：仅执行 G4（记录完整性），跳过 G1/G2/G3/G5（本轮无 NEW1 新建/修改页）
> - **若发现结构性问题**（某节约束不清、字段普遍缺失等）→ 更新 `local/template/{type}-schema.md`，对存量页执行 backfill，写 RFC
> - **若无结构变动** → 日志记录「模板稳定，无需更新」，继续建页节奏
> - EVV5 轮次写日志（格式同 2.1-D，`gene: EVV5`，`type: 当前类型`）
>
> EVV5 与 discover 可合并为同一轮（约 110–130 WU），避免两个轻量轮占据两个日志。

---

### 2.1-B-pre · 每轮 pre-flight check（强制，每轮第一步）

> **每句有据**：本轮建页时须遵守"每句有据"铁律——正文每一句断言必须来自 corpus_search 命中段落，逐句标注 PN，禁止以训练数据常识替代原文依据（详见 NEW1-create-page.md Step 3）。

butler 启动每一轮前，必须先读 state，决定本轮任务类型，再执行任何操作。

**第一步：读 state**

```bash
python3 -c "
import json
s = json.load(open('local/state/grow_state.json'))
print(f'phase={s[\"grow_phase\"]}  type={s[\"current_type\"]}  type_round={s[\"counters\"][\"type_round\"]}')
print(f'evv5_due_in={s[\"thresholds\"][\"evv5_interval\"]-s[\"counters\"][\"rounds_since_last_evv5\"]} 轮')
print(f'discover_streak_low={s[\"counters\"][\"discover_streak_low\"]}')
print(f'pending_new_types={s[\"pending_new_types\"]}')
"
```

同时检查 state 与 pages.json 一致性（reconciliation，完整规则见 `grow-state-machine.md §7`）：
```python
import json
from collections import Counter
s = json.load(open('local/state/grow_state.json'))
d = json.load(open('docs/wiki/pages.json'))
entries = {k: v for k, v in d['pages'].items()
           if v.get('type') not in ('chapter', 'overview', 'list')}

actual_types = set(v['type'] for v in entries.values())
known_types = (
    set(s['type_queue'])
    | ({s['current_type']} if s['current_type'] else set())
    | {e['type'] for e in s['closed_types']}
)
untracked = actual_types - known_types
missing   = known_types - actual_types
if untracked:
    print(f"WARN: pages.json 中有 state 未跟踪的类型: {untracked}")
if missing:
    print(f"WARN: state 中有 pages.json 无对应页面的类型: {missing}")
# current_type 页数核验
if s['current_type']:
    actual_count = Counter(v['type'] for v in entries.values()).get(s['current_type'], 0)
    for entry in s['closed_types']:
        if entry['type'] == s['current_type'] and entry['final_count'] != actual_count:
            print(f"WARN: state reconciled — {s['current_type']} "
                  f"final_count {entry['final_count']} → {actual_count}")
            entry['final_count'] = actual_count
```

**第二步：null-guard**

```python
if s['current_type'] is None:
    # 类型队列已空，进入 Phase 2.N-Z 处理流程，本轮停止决策
    raise SystemExit("current_type is None → 执行 2.N-Z 总结流程")
```

**第三步：决定本轮任务类型**（按优先级，第一个命中即决定；完整算法见 `grow-state-machine.md §3`）

| 优先级 | 条件 | 本轮 gene |
|--------|------|---------|
| 1a | `rounds_since_last_evv5 >= evv5_interval` 且 `rounds_since_last_discover >= discover_periodic_interval` | `EVV5+SCN28`（两者同时到期，合并执行）|
| 1b | `rounds_since_last_evv5 >= evv5_interval` | `EVV5` |
| 2 | `discover_streak_low >= type_close_streak` | `CLOSE+SCN28`（关闭当前类型 + discover） |
| 3 | `queue_size < discover_queue_threshold` 或 `rounds_since_last_discover >= discover_periodic_interval` | `SCN28` |
| 4 | `stub% >= 20%` | `RCH2`（强制 enrich 2–3 页，暂停 NEW1 新建）|
| 5 | `stub% in [15%, 20%)` | `NEW1+RCH2`（标准轮：1 新建 + 1 enrich）|
| 6 | 默认 | `NEW1` |

> **gene 枚举**：`NEW1` / `RCH2` / `SCN28` / `EVV5` / `EVV5+SCN28` / `CLOSE+SCN28` / `NEW1+RCH2` / `BLK3` / `EVV6`。
> 日志 frontmatter 的 `gene` 字段必须是以上枚举值之一，不得随意命名。
>
> **优先级 2 说明**：关闭动作（写 closed_types、更新 current_type、重置计数器）先于 discover 执行，确保 discover 结果进入新类型的候选队列。

**第四步：本轮日志 frontmatter 扩展**（在 2.1-D 格式基础上新增字段）

```yaml
---
round: 47
date: 2026-05-22
type_round: 12               # 该类型内第几轮
phase: "2.1"
current_type: concept
gene: EVV5+SCN28             # 必须是 gene 枚举值
new_candidates: 5            # 仅含 SCN28 的轮必填，其余省略
pages: [...]
result: accept
---
```

**第五步：EXIT-GATE 通过后更新 state**

```python
import json

s = json.load(open('local/state/grow_state.json'))
gene = "{{本轮 gene}}"           # 必须是 gene 枚举值之一
new_candidates = None            # SCN28 / CLOSE+SCN28 / EVV5+SCN28 轮填实际数值，其余填 None

s['counters']['current_round'] += 1
s['counters']['type_round'] += 1

# 使用 'in' 子串匹配支持复合 gene（EVV5+SCN28 / CLOSE+SCN28）
if 'EVV5' in gene:
    s['counters']['rounds_since_last_evv5'] = 0
else:
    s['counters']['rounds_since_last_evv5'] += 1

if 'SCN28' in gene or 'CLOSE' in gene:
    s['counters']['rounds_since_last_discover'] = 0
    if new_candidates is not None:
        if new_candidates < s['thresholds']['type_close_new_candidate_min']:
            s['counters']['discover_streak_low'] += 1
        else:
            s['counters']['discover_streak_low'] = 0

s['last_updated_round'] = s['counters']['current_round']
json.dump(s, open('local/state/grow_state.json', 'w'), ensure_ascii=False, indent=2)
```

**第六步：state 与页面文件同批 commit**

```bash
git add local/state/grow_state.json docs/wiki/pages.json logs/gene-express/{{本轮日志}}
bash wiki/scripts/skill_commit.sh "R{{N}}: {{gene}} {{type}} {{slug}}"
```

> state 更新必须与页面变更同批 commit，不拆分两步，避免 session 中断导致 state 滞后。

---

### 2.1-C 每轮 EXIT-GATE（必做，不可跳过）

每轮使用 NEW1 建页完成后、写日志和 commit 之前，按以下顺序执行五道检查门。
**G1 失败立即回滚，不继续后续检查。任一门未通过，当轮阻塞，修复后才能开启下一轮。**

来源：`$MEMEX_ROOT/ref/spec/butler-phased-strategy-seed.md §每轮质量门`，
以及 butler W2 执行框架（`$MEMEX_ROOT/skills/SKILL_W2_Butler基因表达.md`）。

#### G1 · 内容完整性（对本轮所有修改页）

| 条件 | 检测 | 处置 |
|------|------|------|
| 字数缩减 ≥ 20% | `QLT6-size-loss-detection` | **Critical**：`git checkout` 回滚，重新执行 |
| 关键节丢失 | `QLT6` 关键节白名单 | **Critical**：同上 |
| 字数缩减 10–20% | `QLT6` Warning | 人工确认合理后放行，否则回滚 |

#### G2 · 格式与质量重点检查（对本轮 NEW1 新建/修改页）

> 以下 **E1–E7** 直接来自 BIRTH Phase 9 EXIT-GATE，是每轮必须过的核心关卡。
> 任一项未通过，当轮阻塞，修复后方可写日志和 commit。

| 编号 | 检查项 | 检测 gene | 修复 gene |
|------|--------|----------|----------|
| **E1** | frontmatter 结构完整（所有 key 存在，无缺失字段）| `CHK9` | 补全所有字段；quality 按实际档位填写 |
| **E2** | 质量档位达到本轮目标档 | `QLT6` | 补散文/引文/节直至达标 |
| **E3** | 必填字段内容非空（id/type/label/description/quality 均有实际值）| `CHK6-N3` | `FLD1-update-description` |
| **E4** | 标题行无 wikilink（`## [[...]]` 非法）| `CHK6-N5` | 移除标题内 `[[]]`，保留纯文字 |
| **E5** | PN 引注有效性（引用的段落真实存在）| `QUO23` | 修正 PN 编号或删除无效引注 |
| **E6** | 正文规范通过 | `LNT14` | 按 LNT14 逐项修复 |
| **E7** | blockquote 均有 PN 标注 | 人工扫描 `^>` 行 / `QUO23` | 补 `[NNN-PPP]` 或确认来源 |

**补充检查项**（E 项全部通过后执行）：

| 条件 | 检测 gene | 修复 gene |
|------|----------|----------|
| PN 引注格式错误（括号类型/多PN合并）| `CHK6-N1` / `QUO7` | `FIX10-pn-format-repair` |
| wikilink 截断或格式错误 | `CHK6-N2` / `LNT9` | `FIX11/15-wikilink-repair` |
| label 与已有页面重名 | `CHK6-N4` | `NEW19-homonym-disambig` |
| 段落超长（> 200 字无换行）| `LNT1` | `PRE2-split-long-paragraph` |
| 破折号密度超标 | `LNT2` | `HKP31-fix-dash-density` |

#### G3 · 写作质量（对本轮 NEW1 新建/修改页）

| 条件 | 检测 gene | 修复 gene |
|------|----------|----------|
| 叙述段无 PN 支撑 | `CHK6-C4` / `QUO22` | 补引文或删无据叙述 |
| 废话：复读引文 | `QLT11-T1` | 删叙述，留引文 |
| 废话：主观评价语（"最X之一"）| `QLT11-T2` | 加 PN 或删除 |
| AI 链式表达（"此外…不仅…还…"）| `CHK6-C3` | `FIX6-cot-text-repair` |

#### G4 · 记录完整性（每轮必查）

| 条件 | 说明 | 处置 |
|------|------|------|
| recent.jsonl 未更新 | 本轮 NEW1 新建/修改页未写入 | 补写 recent 条目（含时间戳和摘要）|
| history 记录缺失 | NEW1 新建页无首次修订记录 | `FIX12-backfill-revision-history` |
| 账本未记账 | actions.jsonl 本轮行动未写入 | 补写（动作类型/WU/slug）|
| 队列未更新 | 本轮消费的任务仍留在队列 | 移除已处理条目 |

#### G5 · 系统集成（NEW1 新建页首次必查，或每 5 页抽查 1 页）

对应 `CHK7-new-page-system-check` S1–S7：

| 检查项 | 通过条件 |
|--------|---------|
| S1 页面渲染 | 能正常加载，无空白/崩溃 |
| S2 PN 引注插件 | `[NNN-PPP]` 被插件识别并渲染 |
| S3 Infobox | 字段无 undefined/null/空行 |
| S4 Wikilink | `[[...]]` 渲染为可点击链接，已有目标无 404 |
| S5 History 入口 | 有 History 入口且本次修订可见 |
| S6 Recent 收录 | `Special:Recent` 中本页可见 |
| S7 交叉验证 | Recent 与 History 时间戳一致 |

**执行顺序**：G1 → G2 → G3 → G4 → G5（按频率）。G1 失败直接回滚，不继续。

**stub% 控制规则（与 EXIT-GATE 并行执行）**：

每轮 EXIT-GATE 通过后，检查当前 stub%：

```python
python3 -c "
import json
from collections import Counter
d = json.load(open('docs/wiki/pages.json'))
entries = {k:v for k,v in d['pages'].items() if v.get('type') not in ('chapter','overview','list')}
q = Counter(v.get('quality','?') for v in entries.values())
stub_pct = q.get('stub',0) / max(len(entries),1) * 100
print(f'stub%: {stub_pct:.1f}%  ({q.get(\"stub\",0)}/{len(entries)})')
"
```

| stub% 触发条件 | 动作 |
|--------------|------|
| stub% ≥ 20% | ⚠️ 下一轮强制安排 enrich 批次（RCH2，2–3 页），暂停 NEW1 新建 |
| stub% 15–20% | 下一轮安排 1 页 enrich + 1 页 NEW1 新建（标准轮）|
| stub% < 15% | 正常建页节奏，无需特殊处置 |

> **目的**：将 stub% 控制在 20% 以内是 Phase 2 退出条件之一。
> 每轮轮次日志中记录当前 stub%，形成可追踪的趋势曲线。

---

### 2.1-D 每轮日志（必做，与 BIRTH Pilot 格式一致）

每轮完成 EXIT-GATE 后，写入 `logs/gene-express/` 一个日志文件。

**文件命名**：`{YYYY-MM-DD}-R{N}-{gene}-{type}-{slug或摘要}.md`

例：`2026-05-22-R35-NEW1-{{type}}-{{slug}}.md`、`2026-05-22-R40-RCH2-{{type}}-batch-enrich.md`

**日志格式**：

```markdown
---
round: {{N}}
date: {{YYYY-MM-DD}}
gene: {{gene-id}}
pages: [{{slug1}}, {{slug2}}]
type: {{type}}
result: accept / reject / defer
---

## 执行摘要

一段话描述本轮做了什么（建页/enrich/discover），输入是什么，产出是什么。

## 页面处理记录

| 页面 | 操作 | 结果 | 备注 |
|------|------|------|------|
| {{slug}} | create / enrich | accept | {{简短说明}} |

## EXIT-GATE 检查

**G1 优先检查（失败立即回滚，不继续后续检查）：**

| 门 | 结果 | 问题与处置 |
|----|------|---------|
| G1 内容完整性 | PASS / FAIL | {{如 FAIL 说明回滚原因}} |

**G2 核心格式检查（E1–E7，来自 BIRTH Phase 9 EXIT-GATE）：**

| 编号 | 检查项 | 结果 | 问题与处置 |
|------|--------|------|---------|
| E1 | frontmatter 结构完整（所有 key 存在）| PASS / FAIL | |
| E2 | 质量档位达标 | PASS / FAIL | |
| E3 | 必填字段内容非空 | PASS / FAIL | |
| E4 | 标题无 wikilink | PASS / 修复 N 处 | |
| E5 | PN 引注有效性 | PASS / 修复 N 处 | |
| E6 | 正文规范（LNT14）| PASS / 修复 N 处 | |
| E7 | blockquote 有 PN | PASS / 修复 N 处 | |

**G2 补充格式 / G3 写作质量 / G4 记录 / G5 系统集成：**

| 门 | 结果 | 问题与处置 |
|----|------|---------|
| G2 补充格式检查 | PASS / 修复 N 处 | {{问题类型}} |
| G3 写作质量 | PASS / 修复 N 处 | {{问题类型}} |
| G4 记录完整性 | PASS | — |
| G5 系统集成 | PASS / 抽查 {{slug}} | — |

## 遗留问题

{{本轮发现但未处理的问题，写入下轮待处理队列}}
```

> **日志是问责机制**：EXIT-GATE 结果必须如实记录，不得只写 PASS 略过检查。
> 如某门发现问题并修复，在「问题与处置」栏写清楚修了什么。

---

### 2.1-E 类型完成后 Wikify

每种类型的候选耗尽（扩张关闭）后，**立即执行一次该类型的 wikify pass**，不积压到最后。

> 时机依据：`$MEMEX_ROOT/ref/spec/butler-phased-strategy-seed.md §Wikify 与断链补全的时机`
> —— 首次 wikify 在每类批次建完后，命中率高；积压越久，后续修复代价越大。

执行步骤：

```bash
# 1. 对该类型所有页面执行 wikilink 注入（BLK3-wikilink-pass）
python3 wiki/scripts/butler/bulk_wikilink.py --type {{type}}

# wikify 完成后立即补录历史（bulk_wikilink.py 绕过了 record_revision.py）
git diff --name-only HEAD -- ':(glob)docs/wiki/pages/**/*.md' | while read f; do
  slug=$(basename "$f" .md)
  python3 wiki/scripts/record_revision.py "$slug" \
    --summary "wikify: BLK3 wikilink 注入（{{type}}）" --author butler
done

# 2. 扫描断链（断链 = gap 候选，直接入队）
python3 "$MEMEX_ROOT/wiki/scripts/scan_broken_links.py" \
  --pages-dir docs/wiki/pages >> logs/butler/queue.md

# 3. 重建 backlinks
python3 "$MEMEX_ROOT/wiki/scripts/build_backlinks.py" --stats
git add docs/wiki/backlinks.json

# 4. 写入日志（格式同 2.1-D，gene: BLK3）
```

> ⚠️ `bulk_wikilink.py` 内置跳过标题行的保护，但执行后**必须补录 record_revision.py**，否则 recent / history 界面不显示本次变更（见 `BLK3-wikilink-pass.md §写入铁律`）。
> 断链条目入队前执行 SCN6 质量门（过滤通用词/过短词）。

- [ ] wikify 完成后，关闭该类型并更新 state：
  ```python
  import json
  s = json.load(open('local/state/grow_state.json'))
  closed_type = s['current_type']
  d = json.load(open('docs/wiki/pages.json'))
  final_count = sum(1 for v in d['pages'].values() if v.get('type') == closed_type)

  s['closed_types'].append({
      'type': closed_type,
      'closed_at_round': s['counters']['current_round'],
      'final_count': final_count,
      'evv6_score': None   # Phase 2.N-Z-0 时填写
  })
  s['type_queue'] = [t for t in s['type_queue'] if t != closed_type]
  s['current_type'] = s['type_queue'][0] if s['type_queue'] else None
  # 重置所有类型级计数器；EVV5 间隔从新类型第 0 轮开始计
  s['counters']['type_round'] = 0
  s['counters']['discover_streak_low'] = 0
  s['counters']['rounds_since_last_evv5'] = 0
  json.dump(s, open('local/state/grow_state.json', 'w'), ensure_ascii=False, indent=2)
  print(f'{closed_type} 已关闭，下一类型：{s["current_type"]}，剩余队列：{s["type_queue"]}')
  ```

- [ ] 若 `type_queue` 已空（`current_type == None`）→ 触发 Phase 2.N 全局退出检查（见 2.1-X），不再启动新的类型轮次

---

### 2.1-X 退出条件

以下全部满足，Phase 2.1 完成，进入 2.1-Z 总结报告（由 2.1-Z 决定下一步进入 Phase 2.2 还是 Phase 3）：

- [ ] 所有主要类型的候选均已耗尽或标记「关闭」
- [ ] stub% < 20%（create:enrich 至少 2:1 保证）
- [ ] 各主要类型覆盖率 > 60%（候选天然枯竭的类型除外）
- [ ] 新类型（如有）Mini-Pilot 均分 ≥ 75，模板可用
- [ ] 每种已关闭类型均已执行 wikify pass + 断链入队
- [ ] backlinks.json 已重建，链接密度 > 5 条/词条
- [ ] 所有轮次日志完整写入 `logs/gene-express/`

**关键判断点**：

> **外层提前退出触发器**（与 2.1-B 的单类型耗尽判断互补）：
> 当连续 3 轮 discover 全类型新候选合计 < 5 条时，
> 不等候选彻底归零，立即关闭 Phase 2.1，直接进入 2.1-Z 总结。
> （对比：2.1-B 的「某类型连续 3 轮 < 3 条」是关闭单个类型；此处是所有类型同时枯竭的全局信号。）
> 经验：强行等候选彻底归零往往导致 stub 积压成巨额维护债务；提前转比强行铺面代价小得多。

---

### 2.1-Z Phase 2.1 总结报告

> 类比 BIRTH Phase 10（boot_summary），在 2.1-X 验收通过后立即执行。
> **产出文件**：`local/memory/grow_phase2_summary.md`
> 此文件是下一阶段（Phase 2.N+1 或 Phase 3）启动的前置依据，butler `/grow` skill 读取它确认本轮广度扩张已结案。

---

#### 2.1-Z-PHQ Phase 级综合质检（分析开始前必须完成）

> 执行 Phase 级综合质检：`$MEMEX_ROOT/ref/spec/workflow-phase-quality-check.md`
> 产出：`logs/phase-quality-check/{YYYY-MM-DD}-phase2-phq.md`

PHQ-A FAIL（注册不一致）→ 先修复，再继续后续步骤。
PHQ 高优先级问题须在 2.1-Z-0 EVV6 之前修复完毕；中/低优先级记录后可继续。

---

#### 2.1-Z-0 EVV6 全库评审（Phase 2.1 关闭前唯一一次）

在汇总日志和写总结之前，对 Phase 2.1 期间扩张的每种类型执行一次 `EVV6-schema-close`。
这是 Phase 2.1 的质量基线封存，为下一阶段的 enrich 优先级提供数据依据。

- 对每种已关闭类型（含 Mini-Pilot 新类型）各执行一轮 EVV6：

  ```
  EVV6-schema-close → type: {{type}}
  输入：该类型全部页面
  输出：综合质量均分（0–100）+ 主要扣分模式（1–3 条）
  ```

- 每种类型写独立日志（`gene: EVV6`，`type: {{type}}`），EXIT-GATE 只需 G4
- 记录结果：

  | 类型 | EVV6 均分 | 主要扣分模式 | Phase 3 优先级 |
  |------|---------|-----------|-------------|
  | {{type}} | {{score}} | {{模式描述}} | 高（< 75）/ 中（75–85）/ 低（> 85）|

- 均分 < 75 → 该类型列为 Phase 3 最高 enrich 优先级，Phase 3 开始前先批量 enrich 至 75+
- 均分 ≥ 75 且 < 85 → 正常进入 Phase 3 enrich 队列
- 均分 ≥ 85 → Phase 3 可降低优先级，资源优先分配给低分类型

> EVV6 是 Phase 2.1 的质量封存点，相当于 BIRTH Phase 9 EVV6 的角色。
> Phase 2.1 期间每 10 轮的 EVV5 是「过程检查」，2.1-Z-0 EVV6 是「阶段关闭评审」，两者互补。

- [ ] 每种类型 EVV6 完成后，将均分回填至 state：
  ```python
  import json
  s = json.load(open('local/state/grow_state.json'))
  evv6_results = {
      "{{type1}}": {{score1}},
      "{{type2}}": {{score2}},
  }
  for entry in s['closed_types']:
      if entry['type'] in evv6_results:
          entry['evv6_score'] = evv6_results[entry['type']]
  json.dump(s, open('local/state/grow_state.json', 'w'), ensure_ascii=False, indent=2)
  ```

---

#### 2.1-Z-A 汇总轮次日志与 RFC

从 `logs/gene-express/` 汇总 Phase 2.1 期间的所有轮次数据：

```bash
# 统计 Phase 2.1 期间的轮次日志数量（将 N_start 替换为实际起始轮次）
ls logs/gene-express/ | grep -E "^[0-9]{4}-[0-9]{2}-[0-9]{2}-R[0-9]+" | \
  awk -F'-R' '{n=$2+0; if(n>=N_start) print}' | wc -l  # N_start = Phase 2.1 实际起始轮

# 统计各类型建页数（从日志 frontmatter 中 gene: NEW1 的条目）
grep -l "gene: NEW1" logs/gene-express/*.md 2>/dev/null | wc -l

# 统计 enrich 轮次
grep -l "gene: RCH2" logs/gene-express/*.md 2>/dev/null | wc -l
```

汇总 Phase 2.1 期间的 RFC：
```bash
# 列出 Phase 2.1 期间提交的 RFC（按日期过滤）
ls ref/rfc/ | xargs -I{} head -5 ref/rfc/{} 2>/dev/null | grep -A4 "status:"
```

提取每轮日志中 EXIT-GATE 发现的问题（跨轮统计高频错误类型）：
```bash
grep -h "FAIL\|修复" logs/gene-express/*.md 2>/dev/null | sort | uniq -c | sort -rn | head -20
```

---

#### 2.1-Z-B Phase 2 过程复盘

回顾五个层面，判断是否需要提 RFC 或更新文档：

**1. Gene 层**：Phase 2.1 期间新增或修改了哪些 gene？

```bash
# 列出 Phase 2.1 期间新增的 gene 文件（按 git log 过滤）
git log --since="2026-05-25" --name-only --diff-filter=A -- 'local/gene/**' 'ref/spec/**' \
  | grep -E "\.(md|json)$"
```

对每个新增 gene：确认触发来源（哪轮 EXIT-GATE）、覆盖的错误模式、是否已在 W4 门控中注册。

---

**2. 流程层**：EXIT-GATE 高频 FAIL 分析

从 2.1-Z-A 的汇总结果中，找出触发次数 ≥ 3 的检查项，逐一回答：
- 该项频繁 FAIL 的根本原因是什么？（写作习惯？模板约束不够清晰？）
- 现有 gene 是否足够覆盖这个错误？还是需要新增或加强？

---

**3. 模板层**：各类型 schema 是否需要修订？

从所有 Phase 2 轮次日志中提取模板相关的反馈：
```bash
# 搜索日志中出现"模板""schema""结构""节"相关讨论
grep -h -i "模板\|schema\|节结构\|新增节\|删除节\|字段" logs/gene-express/*.md 2>/dev/null \
  | grep -v "^|" | sort -u
```

对每种类型逐一判断：
- 有无词条反复在同一节扣分（说明该节约束描述不清）
- 有无词条因某节「可选」但实际上每个 standard 词条都有（说明应改为「建议」甚至「必选」）
- 有无词条某节内容持续偏薄（说明模板的写作示例或字数下限不够指导）

结论之一的格式：`{{type}}-schema.md：{{建议改动}} → 是否提 RFC`

---

**4. 新类型发现**：Phase 2 discover 轮次中有无新类型候选？

```bash
# 从 discover 轮次日志中提取「新类型」相关记录
grep -h "新类型\|未知类型\|type.*未知\|建议新增.*type" logs/gene-express/*.md 2>/dev/null
```

同时检查 Phase 2.1 期间 discover 发现的候选中，是否有不属于现有任何 type 的词条（若某类候选词条反复出现但无对应 type，可能是新 type 信号）：
- 发现 ≥ 3 个同类未归类候选 → 考虑新类型，写入 `logs/butler/type-survey.md`，Phase 3 建立 Mini-Pilot
- 发现 1–2 个 → 暂归入最近似类型，在候选备注中标记

- [ ] 将本节发现的新类型写入 state（无新类型则写空数组）：
  ```python
  import json
  s = json.load(open('local/state/grow_state.json'))
  s['pending_new_types'] = [
      # 示例：{'type': '{{new_type}}', 'candidate_count': {{N}}, 'corpus_check': 'ok'}
      # 无新类型时留空数组 []
  ]
  json.dump(s, open('local/state/grow_state.json', 'w'), ensure_ascii=False, indent=2)
  ```

---

**5. 规范层**：`GROW.spec.md` 有无歧义或缺失？

执行 Phase 2 过程中遇到的规范不明确之处（如 discover 节奏边界、stub% 控制阈值合理性、wikify 时机判断），
整理后判断是否需要提 RFC 更新 spec。

---

#### 2.1-Z-C 提交复盘 RFC（按需）

基于 2.1-Z-B 五层分析，汇总需要提 RFC 的变更：

| 变更来源 | 目标文件 | 变更描述 | 优先级 |
|---------|---------|---------|--------|
| 模板层 | `local/template/{{type}}-schema.md` | {{改动描述}} | 高/中/低 |
| Gene 层 | `local/gene/{{gene-id}}.md` | {{改动描述}} | 高/中/低 |
| 规范层 | `$MEMEX_ROOT/GROW.spec.md` | {{改动描述}} | 高/中/低 |
| 新类型 | `logs/butler/type-survey.md` | {{新类型名称及候选数}} | 中/低 |

- 高优先级：Phase 3 启动前必须处理（阻塞正确执行）
- 中优先级：Phase 3 期间处理（影响质量但不阻塞）
- 低优先级：写入 housekeeping 队列，不阻塞 Phase 3

对每个高/中优先级变更，用 `/rfc` 提交并记录 issue URL。

---

#### 2.1-Z-D 写入总结文档

将以下内容写入 `local/memory/grow_phase2_summary.md`：

```markdown
---
wiki: 枪炮、病菌与钢铁
phase2_completed: {{YYYY-MM-DD}}
butler_round_start: R{{N_start}}
butler_round_end: R{{N_end}}
---

# Phase 2.1 广度扩张总结

## 基本统计

| 指标 | 数值 |
|------|------|
| Phase 2.1 总轮次 | {{N}} 轮（R{{start}}–R{{end}}）|
| 新建词条数 | {{N}} 页 |
| enrich 轮次 | {{N}} 轮（{{N}} 页提质）|
| discover 轮次 | {{N}} 轮 |
| wikify 轮次 | {{N}} 轮（覆盖 {{N}} 页）|
| 提交 RFC（Phase 2.1 期间）| {{N}} 个 |
| 词条总数（Phase 2.1 结束）| {{N}} 页（含 Pilot {{N_pilot}} 页）|
| stub% 变化 | {{start%}} → {{end%}} |

## 类型扩张数据

| 类型 | 起始页数 | 新建页数 | 结束页数 | enrich 页 | wikify 状态 | 关闭日期 |
|------|---------|---------|---------|----------|-----------|---------|
| {{type}} | {{n}} | {{n}} | {{n}} | {{n}} | ✓/✗ | {{date}} |

## EVV6 全库评审结果（Phase 2 关闭评审）

| 类型 | 页数 | EVV6 均分 | 主要扣分模式 | Phase 3 优先级 |
|------|------|---------|-----------|-------------|
| {{type}} | {{n}} | {{score}} | {{模式}} | 高/中/低 |

## 质量演化（stub% 趋势）

| 时间节点 | 词条总数 | stub 数 | stub% |
|---------|---------|--------|-------|
| Phase 2.1 开始（R{{N}}）| {{n}} | {{n}} | {{%}} |
| 中期检查（R{{N}}）| {{n}} | {{n}} | {{%}} |
| Phase 2.1 结束（R{{N}}）| {{n}} | {{n}} | {{%}} |

## EXIT-GATE 高频问题汇总

> 跨 Phase 2 所有轮次，哪些检查项最常 FAIL，说明写作流程中的系统性弱点。

| 检查项 | 触发次数 | 处置模式 | 是否新增 gene |
|--------|---------|---------|------------|
| {{E/G 编号}} | {{N}} 次 | {{修复方式}} | ✓/✗ |

**纠错 gene 演化（Phase 2.1 期间新增）**：

| gene 文件 | 触发来源 | 归档状态 |
|----------|---------|---------|
| {{gene-id}} | {{错误模式}} | ✓ 已归档 |

## 链接网络成效

| 指标 | Phase 2.1 开始 | Phase 2.1 结束 | 变化 |
|------|-----------|-----------|------|
| wikilink 总数 | {{N_start}} 条 | {{N_end}} 条 | +{{N}} |
| 平均每词条链接数 | {{avg_start}} 条 | {{avg_end}} 条 | +{{N}} |
| backlinks 覆盖率 | {{%_start}} | {{%_end}} | +{{%}} |

## 模板修订意见（来自日志分析）

> 对每种类型的 schema 文件，记录 Phase 2 实践中发现的改进点。

| 类型 | schema 文件 | 问题描述 | 建议改动 | 优先级 | RFC 编号 |
|------|-----------|---------|---------|--------|---------|
| {{type}} | `{{type}}-schema.md` | {{频繁扣分的节/字段}} | {{具体改动}} | 高/中/低 | {{RFC-N 或 —}} |

## 新类型发现（Phase 2 discover 产出）

> discover 轮次中发现的、不属于现有 type 的候选词条归纳。

| 候选词条群 | 建议新 type 名 | 候选数 | 语料充足性 | 处理决策 |
|----------|-------------|--------|---------|---------|
| {{词条1/词条2/词条3}} | {{type-name}} | {{N}} | ✓/△/✗ | Phase 3 Mini-Pilot / 暂归入 {{existing-type}} / 搁置 |

> 无新类型候选 → 本节填「Phase 2 discover 未发现新类型，现有 type 体系完整」。

## RFC 清单（Phase 2.1 期间）

| 编号 | slug | status | 目标文件 | 描述 |
|------|------|--------|---------|------|
| {{RFC-N}} | {{slug}} | proposed/implemented | {{file}} | {{一句话}} |

## 对 Phase 3 的启示

**质量偏低词条**（优先 enrich 目标）：
- {{slug}}（{{原因：语料薄/引文少/节不完整}}）

**类型间质量差异**：
- {{type1}} 词条整体偏弱，原因：{{}}
- {{type2}} 词条质量稳定，Phase 3 可降低优先级

**高频 EXIT-GATE 问题的根因**：
- {{问题}} → Phase 3 开始前先修复存量，再制定预防 gene

**butler 使用 NEW1 建页建议（对 Phase 3）**：
- {{1–3 条最有价值的操作建议，来自 Phase 2 实践}}

## 下一阶段判断

> **规则**：Phase 2.1 结束后，下一步取决于是否发现了新类型。

| 条件 | 下一步 |
|------|--------|
| 2.1-Z-B 发现新类型（候选 ≥ 3 条）| **启动 Phase 2.N**（N = 上一轮序号 + 1，从 2.2 开始）|
| 无新类型，2.1-X 全部满足 | **进入 Phase 3**（深度提升）|
| 无新类型，2.1-X 部分未满足 | **修复后进入 Phase 3** |

- [ ] 按判断结论更新 state 的 `grow_phase`：
  ```python
  import json
  s = json.load(open('local/state/grow_state.json'))
  if s['pending_new_types']:                        # 有新类型
      s['phase2_iteration'] += 1
      s['grow_phase'] = f"2.{s['phase2_iteration']}"
      s['type_queue'] = [t['type'] for t in s['pending_new_types']]
      s['current_type'] = s['type_queue'][0]
      s['pending_new_types'] = []
      s['counters']['type_round'] = 0
      s['counters']['discover_streak_low'] = 0
  else:                                             # 无新类型 → Phase 3
      s['grow_phase'] = "3"
      s['phase2_closed'] = True
  json.dump(s, open('local/state/grow_state.json', 'w'), ensure_ascii=False, indent=2)
  ```
  同步更新 `local/config/butler.json` 的 `grow_phase` 字段。

**Phase 2.N 命名规则与结构**：

> Phase 2 是广度扩张系列。首次扩张为 Phase 2.1（子节 2.1-A / 2.1-B / … / 2.1-X / 2.1-Z）。
> 每发现一批新类型，启动下一个子阶段：Phase 2.2 / Phase 2.3 / …，各自拥有独立的子节编号：
>
> ```
> Phase 2.2：
>   2.2-A  新类型 Mini-Pilot
>   2.2-B  扩张顺序
>   2.2-C  每轮 EXIT-GATE
>   2.2-D  每轮日志
>   2.2-E  类型完成后 Wikify
>   2.2-X  退出条件
>   2.2-Z  总结报告（PHQ + EVV6 + 汇总 + 分析）
>         └ 2.2-Z 的「下一阶段判断」：
>             有新类型 → Phase 2.3
>             无新类型 → Phase 3
> ```
>
> 所有 Phase 2.N 复用 Phase 2 的所有规范（2-C EXIT-GATE、2-D 日志格式、2-E Wikify、PHQ workflow），
> 子节编号只是加了版本前缀，执行逻辑完全相同。
> GROW.md 中为每个 Phase 2.N 新增独立章节，参数速查表的「当前阶段」字段同步更新。

**结论**：{{进入 Phase 3 / 发现新类型 N 种，启动 Phase 2.2（新类型：{{type-list}}）}}
```

- [ ] 写入完成，提交：
  ```bash
  git add local/memory/grow_phase2_summary.md
  bash wiki/scripts/skill_commit.sh "docs: GROW Phase 2 总结报告完成"
  ```

---

### 2.1-Z-X 验收标准

- [ ] PHQ 日志存在（`logs/phase-quality-check/{date}-phase2-phq.md`），高优先级问题已修复
- [ ] 所有类型均有 EVV6 均分记录（2-Z-0 完成）
- [ ] `local/memory/grow_phase2_summary.md` 存在且无 `{{占位符}}`
- [ ] 所有类型在文件中均标记「已关闭」且有关闭日期
- [ ] EXIT-GATE 高频问题已分析根因（非简单列举）
- [ ] 各类型 schema 修订意见已填写（无需修改则明确注明「无」）
- [ ] 新类型发现已填写（无发现则明确注明「无」）
- [ ] 高/中优先级 RFC 均已提交或记录到 housekeeping
- [ ] 下一阶段判断结论明确（进入 Phase 3 / 启动 Phase 2.2）
- [ ] `local/config/butler.json` 中 `grow_phase` 已按判断结论更新

> **2.1-Z 完成后**：凭总结报告的「下一阶段判断」结论：
> - 无新类型 → 正式启动 Phase 3，`butler.json` 中 `grow_phase` 更新为 `3`
> - 发现新类型 → 启动 Phase 2.2，GROW.md 新增 Phase 2.2 章节，`grow_phase` 保持 `2`
>
> 每个 Phase 2.N 完成后重复此判断，直到无新类型为止，再进入 Phase 3。

---

## Phase 3：深度扩张（Deep Expansion）

> **目标**：将 Phase 2 构建的 standard 页面批量 enrich 至 featured，提升全库质量基线。
> 由于 Phase 2 结束时 stub% = 0%、featured% ≈ 65%，系统直接进入 Phase 3 的提质阶段，
> 且因候选池在 Phase 2 已近枯竭（无新类型发现），Phase 3 未执行 NEW1 新建，专做 RCH2 enrich。
>
> **广度:深度 = 0:10**（纯 enrich 模式，不新建页面）。
>
> **启动前提**：Phase 2 已全部完成，`local/memory/grow_phase2_summary.md` 存在。

---

### 3.0 前置核验

#### 3.0-A Phase 2 完成确认

- [x] Phase 2 总结报告存在且无 `{{占位符}}`：
  确认字段：`phase2_completed: 2026-05-25`、各类型 `final_count`、EVV6 均分记录。

- [x] Phase 2 退出条件满足：
  - stub% < 20% ✓（0%）
  - 各主要类型覆盖率 > 60% ✓（候选天然枯竭的类型已标注）

- [x] state 文件中 Phase 2 已关闭（`phase2_closed == True`）。

- [x] 轮次计数器持续增长（R88 → R93）。

#### 3.0-B 基线指标

| 指标 | 数值 |
|------|------|
| Phase 2 结束时页面总数 | 291 |
| 当前 stub% | 0.0% |
| 当前 featured+% | ~65% |
| 链接密度 | ~5.6 条/页 |

---

### 3.1-0 Phase 3 初始化

#### 3.1-0-A WU quota

Phase 3 为纯 enrich 模式（RCH2），每轮 5 页 enrich，预估 WU 60–100/轮。

#### 3.1-0-B 执行方案

集中 enrich 所有 standard 页面至 featured（共 26 页），分 5 轮执行（R89–R93）。
- **enrich 格式**：concept-schema（定义/在本书中的角色/主要论点/相关概念/延伸阅读）
- **PN 门槛**：≥6 条/页
- **每轮 5 页**，逐页串行写入

---

### 3.1-B 执行记录

#### 执行摘要

| 轮次 | 操作 | 页面 | 结果 |
|------|------|------|------|
| R89 | RCH2 | 一年生植物、专业化分工、人口扩张、再分配、定居 | 5/5 featured |
| R90 | RCH2 | 巨型动物、技术积累、平民、政治竞争、移民 | 5/5 featured |
| R91 | RCH2 | 民族、游牧、玻璃、生态适应、纬度 | 5/5 featured |
| R92 | RCH2 | 自然选择、语言、遗传、部落、酋长 | 5/5 featured |
| R93 | RCH2 | 行政、鼠疫、莱特兄弟、詹姆士·瓦特、达尔文 | 5/5 featured |

#### 质量变化

| 指标 | Phase 3 前 | Phase 3 后 | 变化 |
|------|-----------|-----------|------|
| 词条总数 | 291 | 291 | 0 |
| Standard | 26 | 0 | −26 |
| Featured | 169 | 195 | +26 |
| Featured+% | ~65.0% | 67.0% | +2.0% |
| Stub% | 0% | 0% | 0% |

---

### 3.1-X 退出条件

| 条件 | 评估 | 状态 |
|------|------|------|
| 所有 standard 页面已 enrich 至 featured | 26/26 页完成 | ✅ |
| stub% < 5% | 0.0% | ✅ |
| featured+% > 50% | 67.0% | ✅ |

**退出原因**：目标达成——退出条件全部满足。

---

### 3.1-Z 总结

#### 基本统计

| 指标 | 数值 |
|------|------|
| Phase 3 总轮次 | 5（R89–R93）|
| enrich 轮次（RCH2）| 5 轮 |
| enrich 页数 | 26（21 concept + 2 其他 + 3 person）|
| 词条总数（Phase 3 结束）| 291 |
| stub% | 0.0% |
| featured+% | 67.0% |

#### 类型 enrich 数据

| 类型 | Phase 2 页数 | Phase 3 enrich | 结束页数 |
|------|------------|--------------|---------|
| concept | 153 | 21 | 153 |
| person | 25 | 3 | 25 |
| species | 49 | 0 | 49 |
| place | 44 | 0 | 44 |
| event | 20 | 0 | 20 |

#### 下一阶段判断

| 条件 | 评估 |
|------|------|
| stub% < 5% | 0.0% ✅ |
| featured% > 50% | 67.0% ✅ |
| 候选枯竭 | 是 |
| 新类型发现 | 无 |

→ 根据 GROW.spec.md 阶段定位规则，当前满足 **Phase 4（洞察层）** 进入条件。
