#!/usr/bin/env bash
# Shortcut: delegates to wiki/scripts/publish.sh
exec "$(dirname "$0")/wiki/scripts/publish.sh" "$@"
