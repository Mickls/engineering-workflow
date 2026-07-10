#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLUGIN="$ROOT/plugins/engineering-workflow"

cd "$ROOT"

python3 -m json.tool "$PLUGIN/.codex-plugin/plugin.json" >/dev/null
python3 -m json.tool "$ROOT/.agents/plugins/marketplace.json" >/dev/null

ruby "$ROOT/scripts/validate-agent-metadata.rb"

python3 "$ROOT/scripts/validate-workflow.py"
python3 "$ROOT/scripts/check-workflow-rule-sync.py"
"$ROOT/scripts/audit-minimal-correct.sh" --help >/dev/null
"$PLUGIN/scripts/audit-minimal-correct.sh" --help >/dev/null
