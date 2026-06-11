#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLUGIN="$ROOT/plugins/engineering-workflow"

cd "$ROOT"

python3 -m json.tool "$PLUGIN/.codex-plugin/plugin.json" >/dev/null
python3 -m json.tool "$ROOT/.agents/plugins/marketplace.json" >/dev/null

ruby -e 'require "yaml"; Dir["plugins/engineering-workflow/skills/*/agents/openai.yaml"].sort.each { |f| YAML.load_file(f); puts "ok #{f}" }'

python3 "$ROOT/scripts/validate-workflow.py"
