# RFC-ggs-0013: build_chapter_map.py 改为以 pn_prefix 为主键，支持中文数字序号和无数字序号

- **Status**: implemented
- **Date**: 2026-05-24
- **Issue**: https://github.com/baojie/memex/issues/145
- **Source wiki**: ggs
- **Target**: wiki/scripts/butler/build_chapter_map.py

---

## Problem

`build_chapter_map.py` 当前通过 `chapter_pattern` 正则从语料标题中提取章节号（`m.group(1)`），然后调用 `int(m.group(1))` 生成三位零填充的 `NNN`。这一设计在英文 wiki 中运作正常（如 `^# Chapter (\d+)$`），但对中文 wiki 存在两类无法处理的情况：

1. **中文数字序号**：本 wiki（ggs）的语料章节标题格式为 `## 第一章　标题`、`## 第十九章　标题`（中文数字），正则无法直接捕获可转换为 `int()` 的阿拉伯数字，导致 `m.group(1)` 的 `IndexError` 或 `int()` 的 `ValueError`，`build_chapter_map.py` 直接崩溃。

2. **无数字序号的特殊章节**：前言（前言/Preface）、后记（后记/Epilogue）、扉页（Frontispiece）等章节没有数字序号，其 `pn_prefix`（如 `P03`、`020`、`P02`）已在 `ref/chapter-order.md` 和 `docs/wiki/pages.json` 中定义，是现成的权威来源，不需要从标题中推算。当前脚本对这类章节的支持仅限于 `preface_pattern` + `preface_nnn` 两个字段，且附录 `appendix_pattern` 仅支持单字母格式（`A01`），后记完全没有对应字段（`epilogue_pattern` 不被识别）。

两类问题的共同根因是：脚本试图从语料标题推算 NNN，而不是直接读取 wiki 已有的 `pn_prefix` 权威来源。

## Root cause

`extract_sections()` 的设计假设：

```python
chapter_num = int(m.group(1))   # 正则必须有捕获组且为阿拉伯数字
nnn = f"{chapter_num:03d}"
```

这一假设排除了：
- 非阿拉伯数字的章节编号（中文、罗马数字等）
- 无编号的特殊章节（前言、后记、扉页等）
- 章节 pn_prefix 已在 wiki 元数据中定义的情况

## Proposed change

**方案：优先从 `pages.json` 读取 pn_prefix，语料正则仅用于定位章节边界**

### 修改要点

1. **新增读取 `docs/wiki/pages.json` 的逻辑**

   `build_chapter_map.py` 在生成映射表前，先加载 `docs/wiki/pages.json`，建立 `page_id → pn_prefix` 映射（利用已有的 `pn_prefix` 字段）。

2. **`chapter_pattern` 不再要求捕获组**

   正则仅用于"检测这行是否是章节标题"，不再需要 `m.group(1)` 来提取数字。章节标题与 page_id 的对应通过配置文件中的 `nnn_map` 字段或 pages.json 中的 `pn_prefix` 确定。

3. **新增 `nnn_map` 字段（butler.json）**

   当无法从 pages.json 自动匹配时，允许在 `butler.json` 中显式定义标题→NNN 的映射：

   ```json
   {
     "corpus_file": "corpus/raw/枪炮病菌与钢铁_校勘底稿.md",
     "chapter_pattern": "^## 第[一二三四五六七八九十百千万]+章",
     "preface_pattern": "^## 前言",
     "epilogue_pattern": "^## 后记",
     "nnn_map": {
       "前言　耶利的问题": "P03",
       "后记　人类史作为一门科学的未来": "020"
     }
   }
   ```

   或更简洁地，支持按顺序枚举（`ordered_nnn`）：

   ```json
   {
     "ordered_nnn": ["P03", "001", "002", ..., "019", "020"]
   }
   ```

4. **中文数字序号支持**

   内置中文数字→阿拉伯数字转换函数（`一→1, 二→2, ..., 十九→19`），在 `extract_sections()` 中优先尝试中文→阿拉伯转换，失败时回落到 `nnn_map` 或 `ordered_nnn`。

5. **`epilogue_pattern` + `epilogue_nnn` 字段支持**（最小化改动备选方案）

   若不希望大幅重构，至少应支持：
   - `epilogue_pattern`：正则匹配后记标题
   - `epilogue_nnn`：后记的 NNN 值（如 `"020"`）

   这是 `preface_pattern` + `preface_nnn` 模式的自然延伸。

### 推荐方案

方案 A（完整）：读取 pages.json 的 pn_prefix，正则仅做边界检测，NNN 来自元数据。  
方案 B（最小化）：新增 `epilogue_pattern`/`epilogue_nnn` + 内置中文数字转换，保持现有架构。

建议优先实现方案 B（改动小，风险低），并作为向方案 A 过渡的第一步。

## 本 wiki 影响

- ggs wiki `local/config/butler.json` 的 `chapter_pattern` 将修复后不再崩溃
- `epilogue_pattern: "^## 后记"` 字段将被正确识别
- `local/butler/chapter-map.md` 将包含完整 22 个章节（含前言 P03 和后记 020）

---

## Implementation

**Review**: faithful
**Date**: 2026-05-24
**Commits**:
- baojie/memex@04d08e7284b27bfac37059d1a99c9bf307de6416: implement RFC-ggs-0013
- baojie/ggs@<ggs-sha>: config: 更新 butler.json 分离前言/后记/章节配置

**实施内容**（Plan B 优先）：

1. `_parse_chinese_num()` 中文数字→阿拉伯数字转换
2. `epilogue_pattern`/`epilogue_nnn` 字段支持
3. `nnn_map` 标题→NNN 显式映射
4. `chapter_pattern` 捕获组改为可选
5. ggs `butler.json` 分离前言/后记/章节正则

**Plan A 待后续 RFC**：读取 pages.json 的 pn_prefix 作为 NNN 权威来源
