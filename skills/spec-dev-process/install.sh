#!/usr/bin/env bash
# 安裝 spec-dev-process 為 Claude Code skill。
#   ./install.sh          符號連結(預設)
#   ./install.sh --copy   複製整份
#   ./install.sh --dest <dir>  指定 skills 目錄(預設 ~/.claude/skills)
#   ./install.sh --force  目標是實體資料夾時,先備份成 <目標>.bak-<時間> 再覆蓋(沒加就拒絕,不會刪你的東西)
#   ./install.sh --all-tests   安裝前跑完整測試(預設只跑快的一組,約 20 秒)
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${HOME}/.claude/skills"; MODE="link"; FORCE=0; TESTS="fast"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --copy) MODE="copy"; shift;;
    --dest) DEST="$2"; shift 2;;
    --force) FORCE=1; shift;;
    --all-tests) TESTS="all"; shift;;
    *) echo "unknown option $1"; exit 2;;
  esac
done
command -v python3 >/dev/null || { echo "需要 python3 (>= 3.9)"; exit 1; }
python3 - <<'PY' || exit 1
import sys; v=sys.version_info
assert v >= (3, 9), f"python3 版本 {v.major}.{v.minor} 太舊,需要 3.9+"
print(f"python3 {v.major}.{v.minor}.{v.micro} OK")
PY
echo "執行測試($TESTS)..."; (cd "$HERE" && python3 tests/run.py "$TESTS") || { echo "測試失敗,停止安裝"; exit 1; }
mkdir -p "$DEST"
TARGET="$DEST/spec-dev-process"
if [[ -L "$TARGET" ]]; then
  echo "已存在符號連結 $TARGET → $(readlink "$TARGET"),改指到新版"; rm "$TARGET"     # 只移除連結本身,不碰它指向的東西
elif [[ -e "$TARGET" ]]; then
  if [[ "$(cd "$TARGET" && pwd -P)" == "$(cd "$HERE" && pwd -P)" ]]; then echo "目標就是這份套件本身,不用安裝"; exit 0; fi
  if [[ "$FORCE" != 1 ]]; then
    echo "已存在實體資料夾 $TARGET,為了不刪到你的東西,停止安裝。"
    echo "  要覆蓋:./install.sh --force(會先備份成 $TARGET.bak-<時間>)"; exit 1
  fi
  BAK="$TARGET.bak-$(date +%Y%m%d-%H%M%S)"; mv "$TARGET" "$BAK"; echo "已備份舊版到 $BAK"
fi
if [[ "$MODE" == "link" ]]; then ln -s "$HERE" "$TARGET"; echo "linked  $TARGET -> $HERE"
else cp -R "$HERE" "$TARGET"; echo "copied  $TARGET"; fi
echo "試跑範例..."; python3 "$TARGET/spec-dev.py" check "$TARGET/examples/avatar-upload" >/dev/null || true
echo "完成。Claude Code 內用 /spec-dev-process;CLI 用 python3 $TARGET/spec-dev.py"
