#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec "$ROOT/plugins/engineering-workflow/scripts/audit-minimal-correct.sh" "$@"
