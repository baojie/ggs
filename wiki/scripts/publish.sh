#!/usr/bin/env bash
# publish.sh — Wiki 发布脚本模板
#
# 放置位置：wiki/scripts/publish.sh（宪法 §0.2）
# 用法：
#   bash wiki/scripts/publish.sh           # 仅构建，不推送
#   bash wiki/scripts/publish.sh --push    # 构建 + 推送到 gh-pages（Droplet 部署专用）
#
# 目录约定（不再有 wiki/public/，docs/wiki/ 是唯一发布目录）：
#   docs/wiki/pages/      ← 页面源文件（同时是构建输入和输出）
#   docs/wiki/history/    ← 修订历史（由本脚本更新）
#   docs/wiki/pages.json  ← 注册表（由本脚本重建）
#   docs/wiki/local/      ← 本 wiki 插件配置（源文件，无需 copy）
#
# CSS/JS 说明：
#   开发阶段：serve.js 从 ~/memex/wiki/public/ fallback 提供引擎文件
#   线上部署：index.html 的 onerror 机制自动切换到 CDN
#   → publish.sh 无需做任何 CSS/JS 复制或路径替换

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
WIKI_DIR="$ROOT/docs/wiki"
MEMEX_ROOT="${MEMEX_ROOT:-$HOME/memex}"
SCRIPTS="$MEMEX_ROOT/wiki/scripts"

# ── 前置检查 ──────────────────────────────────────────────────────────────────

if [[ ! -d "$WIKI_DIR/pages" ]]; then
  echo "Error: $WIKI_DIR/pages 不存在，请确认在正确的 wiki 根目录执行" >&2
  exit 1
fi

# ── 1. PN 格式校验（可选，需本 wiki 提供 wiki/scripts/lint_pn.py）────────────

LOCAL_LINT="$ROOT/wiki/scripts/lint_pn.py"
if [[ -f "$LOCAL_LINT" ]]; then
  echo "[publish] PN 格式校验..."
  python3 "$LOCAL_LINT" "$WIKI_DIR/pages"
fi

# ── 2. 重建注册表 ─────────────────────────────────────────────────────────────

echo "[publish] 重建 pages.json + pages.lite.json..."
python3 "$SCRIPTS/build_registry.py" "$WIKI_DIR/pages" \
  --out      "$WIKI_DIR/pages.json" \
  --out-lite "$WIKI_DIR/pages.lite.json"

# ── 2-B. 构建全文索引 ────────────────────────────────────────────────────────

echo "[publish] 构建全文索引 (FTS)..."
python3 "$MEMEX_ROOT/wiki/scripts/build_fts_index.py" "$ROOT"

# ── 3. 记录修订（仅处理本次变更的页面）──────────────────────────────────────

echo "[publish] 记录修订到 history/ ..."
{
  git -C "$ROOT" -c core.quotePath=false diff --cached --name-only HEAD 2>/dev/null
  git -C "$ROOT" -c core.quotePath=false diff --name-only 2>/dev/null
  git -C "$ROOT" -c core.quotePath=false ls-files --others --exclude-standard 2>/dev/null
} | grep '^docs/wiki/pages/.*\.md$' | sort -u | while read -r fpath; do
  slug=$(basename "$fpath" .md)
  echo "  record_revision: $slug"
  python3 "$SCRIPTS/record_revision.py" "$slug" --author butler || true
done

# ── 4. 重建反向引用索引 ───────────────────────────────────────────────────────

echo "[publish] 重建反向引用索引..."
python3 "$SCRIPTS/build_backlinks.py"

# ── 5. 更新知识量快照 ─────────────────────────────────────────────────────────

echo "[publish] 更新知识量快照..."
python3 "$SCRIPTS/compute_knowledge.py"

# ── 完成提示 ──────────────────────────────────────────────────────────────────

echo ""
echo "[publish] 完成。下一步："
echo "  git add docs/wiki/"
echo "  bash wiki/scripts/wiki_commit.sh \"wiki: 发布\""

# ── 可选：Droplet 部署推送（--push）─────────────────────────────────────────
# 仅适用于 sys-deploy.md 的"Droplet 方案"，GitHub Pages / Cloudflare Pages 无需此步

if [[ "${1:-}" == "--push" ]]; then
  BRANCH=$(git -C "$ROOT" rev-parse --abbrev-ref HEAD)
  if [[ "$BRANCH" != "main" ]]; then
    echo "Error: --push 只在 main 分支执行（当前在 $BRANCH）" >&2
    exit 1
  fi
  if [[ -n "$(git -C "$ROOT" status --porcelain)" ]]; then
    echo "Error: 工作区有未提交的更改，请先 commit 再 --push" >&2
    exit 1
  fi
  echo "[publish] 推送 main → origin..."
  git -C "$ROOT" push origin main
  echo "[publish] 推送 docs/wiki/ → gh-pages 分支..."
  git -C "$ROOT" subtree push --prefix=docs/wiki origin gh-pages
  echo "[publish] 已推送，wiki-1 将在 5 分钟内同步。"
fi
