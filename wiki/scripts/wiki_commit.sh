#!/usr/bin/env bash
# wiki_commit.sh — 由 /wiki skill 调用，执行 commit（不自动 push）
# 用法: bash wiki/scripts/wiki_commit.sh "commit message"
set -euo pipefail

MSG="${1:-}"
if [[ -z "$MSG" ]]; then
  echo "用法: bash wiki/scripts/wiki_commit.sh \"commit message\"" >&2
  exit 1
fi

MEMEX_ROOT="${MEMEX_ROOT:-$HOME/memex}"
PUBLIC_DIR="docs/wiki"
REGISTRY_SCRIPT="$MEMEX_ROOT/wiki/scripts/build_registry.py"

echo "[wiki] 重建 pages.json + pages.lite.json..."
python3 "$REGISTRY_SCRIPT" "$PUBLIC_DIR/pages" \
  --out "$PUBLIC_DIR/pages.json" \
  --out-lite "$PUBLIC_DIR/pages.lite.json"

git commit -m "$MSG"
echo "→ 运行 git push 发布到远端"
