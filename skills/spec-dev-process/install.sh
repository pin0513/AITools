#!/usr/bin/env bash
# 安裝 spec-dev-process 為 Claude Code skill。
#   ./install.sh          符號連結(預設)
#   ./install.sh --copy   複製整份
#   ./install.sh --dest <dir>  指定 skills 目錄(預設 ~/.claude/skills)
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${HOME}/.claude/skills"; MODE="link"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --copy) MODE="copy"; shift;;
    --dest) DEST="$2"; shift 2;;
    *) echo "unknown option $1"; exit 2;;
  esac
done
command -v python3 >/dev/null || { echo "需要 python3 (>= 3.9)"; exit 1; }
python3 - <<'PY' || exit 1
import sys; v=sys.version_info
assert v >= (3, 9), f"python3 版本 {v.major}.{v.minor} 太舊,需要 3.9+"
print(f"python3 {v.major}.{v.minor}.{v.micro} OK")
PY
echo "執行測試..."; (cd "$HERE" && python3 -m unittest discover -s tests -t . -q) || { echo "測試失敗,停止安裝"; exit 1; }
mkdir -p "$DEST"
TARGET="$DEST/spec-dev-process"
if [[ -e "$TARGET" || -L "$TARGET" ]]; then
  echo "已存在 $TARGET,先移除再裝"; rm -rf "$TARGET"
fi
if [[ "$MODE" == "link" ]]; then ln -s "$HERE" "$TARGET"; echo "linked  $TARGET -> $HERE"
else cp -R "$HERE" "$TARGET"; echo "copied  $TARGET"; fi
echo "試跑範例..."; python3 "$TARGET/spec-dev.py" check "$TARGET/examples/avatar-upload" >/dev/null || true
echo "完成。Claude Code 內用 /spec-dev-process;CLI 用 python3 $TARGET/spec-dev.py"
