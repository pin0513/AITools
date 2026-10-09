#!/usr/bin/env bash
# 載入 specs/rd/<issue>/spec 與 spec-review,跑 spec-dev-process 全流程。用法:review.sh <issue> [--strict | --watch] [--offline]
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; PROJ="$(cd "$HERE/../../.." && pwd)"
ISSUE="${1:?issue 名稱,例 issue-c}"; shift || true
SPEC_DEV="${SPEC_DEV:-$(cd "$PROJ/../.." && pwd)/spec-dev.py}"   # 套件內 examples/ 時的預設;部署時設 SPEC_DEV 環境變數
[[ -f "$SPEC_DEV" ]] || { echo "找不到 spec-dev.py,請設 SPEC_DEV=/path/to/spec-dev-process/spec-dev.py"; exit 2; }
if [[ "${1:-}" == "--strict" ]]; then shift; python3 "$SPEC_DEV" run "$PROJ/specs/rd/$ISSUE/spec" --to S6 "$@"
elif [[ "${1:-}" == "--watch" ]]; then shift; python3 "$SPEC_DEV" review "$PROJ/specs/rd/$ISSUE/spec" --watch "$@"   # md 一改就重建看板
else python3 "$SPEC_DEV" review "$PROJ/specs/rd/$ISSUE/spec" "$@"; fi
