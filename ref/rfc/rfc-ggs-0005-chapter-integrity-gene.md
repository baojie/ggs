# RFC-ggs-0005: 建立章节完整性基因（CHK7）集成至 BIRTH.spec.md Phase 4-D

- **Status**: implemented
- **Date**: 2026-05-23
- **Issue**: https://github.com/baojie/memex/issues/131
- **Source wiki**: ggs
- **Target**: `wiki/scripts/chapter_integrity.py` + `BIRTH.spec.md` Phase 4-D

---

## Problem

Phase 4（章节导入）完成后出现多重问题：

1. **章节注册缺失/错误**：ch07、ch10、ch12、ch13 在 `pages.json` 中 `type` 为 `unknown`（非 `chapter`），`chapter` 字段缺失，label 为原始 pid 而非中文名。
2. **frontmatter 被破坏**：脚本将 `::: image` 块插入到 frontmatter 的 closing `---` 之前，导致 `yaml.safe_load()` 解析失败，`build_registry.py` 退化为 `type: unknown`。
3. **导航顺序错误**：`build_registry.py` 以 `sorted(rglob("*.md"))` 扫描文件，`pr/Preface.md` 排在 `ch/` 章节之后，而 daemon 按 `book_seq` 排序（全为 0 时稳定排序保留插入序），导致 Preface 成为末尾章节，显示"已是最后一章"。
4. **缺乏自动化检查**：BIRTH.md Phase 4-D 仅含一条弱验证（"确认 pages.json 含 chapter 字段"），上述问题全部漏检。

这些问题依赖人工浏览页面才暴露，耗时数轮排查。

## Root cause

现有验证体系缺少专门的章节完整性基因。子 wiki 的 BIRTH.md Phase 4-D 仅做最简单的存在性检查，未覆盖：
- 所有预期章节是否全部注册
- 注册的 `type`/`label`/`chapter`/`book_seq` 是否正确
- 页面文件 frontmatter 与注册表是否一致
- 语料库内容是否被完整覆盖

## Proposed change

### 1. 建立章节完整性基因脚本

在 memex 的 `wiki/scripts/` 下新建 `chapter_integrity.py`，由子 wiki 各自维护其 `EXPECTED_CHAPTERS` 列表。建议的功能框架（以 ggs 的 21 章为例）：

```
C01  全部预期章节已注册
C02  章节 type == "chapter"
C03  存在 chapter + book_seq 字段且数值连续
C04  label 与预期一致
C05  非章节页面不含 chapter 字段
C06  语料库所有 H2 被章节覆盖（无遗漏段落）
C07  页面文件 frontmatter 与 pages.json 一致
C08  语料内容覆盖率 ≥ 95%
```

支持 `--fix` 模式自动修正 `pages.json` 中的 type/label/chapter/book_seq。

### 2. 更新 BIRTH.spec.md Phase 4-D

将原弱验证替换为：

```bash
python3 wiki/scripts/chapter_integrity.py        # 检查
python3 wiki/scripts/chapter_integrity.py --fix   # 自动修复后重新检查
```

### 3. ggs 侧的实践验证

ggs 已实现 `wiki/scripts/chapter_integrity.py`（见 ggs repo），通过 8 项检查全部通过。待 RFC 批准后可将通用框架迁入 memex。

## Implementation

**Review**: faithful
**Date**: 2026-05-23
**Note**: RFC 命名 CHK7 与现有基因冲突，ADM2 修正为 CHK12
**Commits**:
- baojie/memex@7af72d27a92651dc35faf896652e112eae16393b: implement RFC-ggs-0005
- baojie/ggs@c34aeb6: rfc(ggs-0005): 创建 local/chapter_list.py
