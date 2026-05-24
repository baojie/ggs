# RFC-ggs-0020: 中文 Wiki 标签应与默认语言一致，模板和 BIRTH spec 应声明 tag 语言选择

- **Status**: implemented
- **Date**: 2026-05-25
- **Issue**: https://github.com/baojie/memex/issues/156
- **Source wiki**: ggs
- **Target**: `$MEMEX_ROOT/ref/template/` 下各 type 的模板 + `$MEMEX_ROOT/ref/spec/birth-spec.md`

---

## Problem

在中文 Wiki（如 ggs）上，tags 字段被写为英文标签，与 Wiki 的默认语言（中文）不一致。例如词条的 tags 包含 `agriculture`、`domestication` 而非 `农业`、`驯化`。

目前页面建立流程和模板中未对 tags 的语言做任何规范：
- 各 type 的模板没有说明 tags 应该用什么语言
- BIRTH spec 没有要求各 type 模板声明 tag 语言选择
- Agent 在创建页面时凭习惯选择标签语言，导致中英混合

## Root cause

页面创建模板（`ref/template/` 下各 type）中 tags 字段仅有占位示例，未指定语言方向。BIRTH spec 也未将 tag 语言一致性列为质量要求。

## Proposed change

1. 在各 type 的模板（concept、person、event、place、species 等）的 frontmatter tags 字段中添加注释，明确要求 tags 与 Wiki 默认语言一致
2. 在 `ref/spec/birth-spec.md`（或 `BIRTH.md`）中增加一条：所有 type 模板必须声明 tag 语言选择
3. `type` 字段保留英文（为系统内部值），不随语言变化

示例模板修改：
```yaml
---
tags: []
# tags 必须使用 Wiki 默认语言（如中文 Wiki 用中文标签），type 字段保持英文。
---
```

---

## Evaluation Note

**决策**: accept-modified
**调整方向**:
- `$MEMEX_ROOT/ref/template/` → `local/template/`（type 模板在 wiki 本地目录，而非 memex ref/template/）
- `ref/spec/birth-spec.md` → `$MEMEX_ROOT/BIRTH.spec.md`（BIRTH spec 位于根目录）
- `ref/template/` 下的共用模板 About.md 无 tags 字段，跳过
- BIRTH.spec.md 质量目标表新增一行"tags 语言与 WIKI_LANG 一致"即可

---

## Implementation

**Review**: faithful
**Date**: 2026-05-25
**Commits**:
- baojie/memex@aba55a4: fix(BIRTH): RFC-ggs-0020 质量目标表增加 tags 语言一致性要求
- baojie/ggs@62ddc35: fix(template): RFC-ggs-0020 模板 tags 字段增加语言一致性注释

**说明**: 路径按 accept-modified 调整——模板注释写入 `local/template/`（per-wiki），BIRTH spec 规则写入 `BIRTH.spec.md`。
