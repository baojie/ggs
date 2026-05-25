# RFC-ggs-0028: wiki_commit.sh 提交前自动重建 pages.json + pages.lite.json

- **Status**: implemented
- **Date**: 2026-05-26
- **Issue**: https://github.com/baojie/memex/issues/170
- **Source wiki**: ggs
- **Target**: wiki/scripts/wiki_commit.sh (各 wiki 项目) / wiki/scripts/ (引擎模板)

## 问题

`build_registry.py` 更新后，各 wiki 项目的 `pages.json` / `pages.lite.json` 可能过时。

2026-05-17 的 commit `2bae3d4` 在 `strip_lite()` 中加入了 `path` 字段。但 GGS 的 `pages.lite.json` 是旧脚本生成的，315 个条目全部缺失 `path`。由于 `_pageFile(pid, meta)` 依赖 `meta.path` 定位分桶路径（如 `pages/ab/About.md`），缺失时 fallback 到 `pid + '.md'`（`pages/About.md`），所有页面都无法加载。

**原因链：**

1. `build_registry.py` 输出格式变更 → `pages.lite.json` 自动过时
2. 各 wiki 的 `wiki_commit.sh` 提交前不重建 registry
3. wiki server 持续运行时也不重建（`wiki-daemon.sh start` 虽然重建，但重启后才生效）
4. 无法检测到输出已过时（registry JSON 无 schema 版本号）

影响范围：所有使用 memex 引擎的 wiki（ggs、investor、aima）。

## 提案

### 方案 A（推荐）：wiki_commit.sh 提交前自动重建

在各 wiki 的 `wiki_commit.sh` 中，在 `git commit` 之前加入 registry 重建：

```bash
MEMEX_ROOT="${MEMEX_ROOT:-$HOME/memex}"
PUBLIC_DIR="docs/wiki"
REGISTRY_SCRIPT="$MEMEX_ROOT/wiki/scripts/build_registry.py"

python3 "$REGISTRY_SCRIPT" "$PUBLIC_DIR/pages" \
  --out "$PUBLIC_DIR/pages.json" \
  --out-lite "$PUBLIC_DIR/pages.lite.json"
```

优点：
- 改动极小，每个 wiki 只需改 5 行
- 每次提交都确保 registry 最新
- server 是否重启不影响

### 方案 B（补充）：build_registry.py 输出 schema 版本号

在 registry JSON 顶层加 `_schema_version` 字段，每次输出格式变更时递增。客户端 `loadRegistry()` 可据此检测过时。

```
_schema_version: 2  (路径字段引入后)
```

这需要前端的配合检查（需同时修改 core.js / registry.js）。

### 方案 C（长期）：memex 引擎提供标准 wiki_commit.sh 模板

引擎提供 `wiki/scripts/wiki_commit.template.sh`，各 wiki 引用或复制。模板中包含 registry 重建 + 标准 commit 流程。

## 受影响的 wiki

| Wiki | 状态 |
|------|------|
| ggs | ✅ 已修复（本地 wiki_commit.sh 已加重建步骤） |
| investor | ✅ 已修复（RFC-ggs-0028） |
| aima | ✅ 已修复（RFC-ggs-0028） |

## 建议实施

1. 先应用方案 A（低风险，零依赖）
2. memex 引擎考虑方案 C 作为长期规范

## Implementation

**Review**: faithful
**Date**: 2026-05-26
**Commits**:
- baojie/memex@cbce949: feat(registry): build_registry.py 输出加 _schema_version + wiki_commit 模板
- baojie/investor@7c7cf1a: fix: wiki_commit.sh 提交前自动重建
- baojie/aima@8dd3ce9: fix: wiki_commit.sh 提交前自动重建
