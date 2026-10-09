#!/usr/bin/env bash
# 用法:review.sh [--strict | --serve [--port 8110]] [--offline];SPEC_DEV 指向 spec-dev.py
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; PROJ="$(cd "$HERE/../../.." && pwd)"
SPEC_DEV="${SPEC_DEV:-$(cd "$PROJ/../../.." && pwd)/spec-dev.py}"
SPEC="$PROJ/specs/rd/order-cancel/spec"
if [[ "${1:-}" == "--strict" ]]; then shift; python3 "$SPEC_DEV" run "$SPEC" --to S6 "$@"
elif [[ "${1:-}" == "--serve" ]]; then shift; python3 "$SPEC_DEV" serve "$SPEC" "$@"
else python3 "$SPEC_DEV" review "$SPEC" "$@"; fi
