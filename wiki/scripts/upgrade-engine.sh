#!/usr/bin/env bash
# upgrade-engine.sh — 从 CDN 读取最新引擎版本，更新 docs/wiki/index.html
#
# 用法:
#   bash wiki/scripts/upgrade-engine.sh          # 升级到 CDN 最新版
#   bash wiki/scripts/upgrade-engine.sh --dry-run # 只显示新版本，不修改文件

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$SCRIPT_DIR/../.."
INDEX="$ROOT/docs/wiki/index.html"
CDN="https://baojie.github.io/memex/dist"
DRY_RUN="${1:-}"

# 从 CDN 获取当前版本
VERSION_JSON=$(curl -fsSL "$CDN/dist-version.json")
NEW_JS=$(echo "$VERSION_JSON" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('js',''))")
if [ -z "$NEW_JS" ]; then
  echo "错误：CDN dist-version.json 尚无 js 字段，请先推送 memex 到 GitHub Pages。"
  exit 1
fi

# 读取 index.html 中当前版本
CURRENT_JS=$(grep -oP 'memex\.min\.[a-f0-9]+\.js' "$INDEX" | head -1 || echo "未找到")

echo "当前版本：$CURRENT_JS"
echo "最新版本：$NEW_JS"

if [ "$CURRENT_JS" = "$NEW_JS" ]; then
  echo "已是最新版，无需更新。"
  exit 0
fi

if [ "$DRY_RUN" = "--dry-run" ]; then
  echo "（dry-run，不修改文件）"
  exit 0
fi

# 替换 index.html 中的 JS 文件名
sed -i "s/memex\.min\.[a-f0-9]*\.js/$NEW_JS/g" "$INDEX"
echo "✓ 已更新 docs/wiki/index.html → $NEW_JS"
