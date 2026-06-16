#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/audit-defensive-code.sh [--staged|--worktree] [--fail-on-match] [--config PATH] [PATH...]

Find defensive-code candidates. This script only reports candidates; it does
not decide whether a guard is valid or edit files.

Modes:
  --worktree       Scan git worktree diff. Default when no PATH is provided.
  --staged         Scan staged diff.
  PATH...          Scan files/directories directly.

Options:
  --config PATH    Optional newline-delimited regex patterns to include.
  --fail-on-match  Exit 1 when candidates are found.
  -h, --help       Show this help.
EOF
}

mode="worktree"
fail_on_match=0
config=""
paths=()

while (($#)); do
  case "$1" in
    --staged)
      mode="staged"
      shift
      ;;
    --worktree)
      mode="worktree"
      shift
      ;;
    --fail-on-match)
      fail_on_match=1
      shift
      ;;
    --config)
      if (($# < 2)); then
        echo "--config requires a path" >&2
        exit 2
      fi
      config="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      while (($#)); do
        paths+=("$1")
        shift
      done
      ;;
    -*)
      echo "unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
    *)
      paths+=("$1")
      shift
      ;;
  esac
done

patterns=(
  'string-normalization:(^|[^[:alnum:]_])(TrimSpace|trim|Trim|strip|Strip|normalize|Normalize|isBlank|string\.IsNullOrWhiteSpace)([^[:alnum:]_]|$)'
  'empty-check:(==[[:space:]]*(nil|null|undefined|None|""|'"'"''"'"')|!=[[:space:]]*(nil|null|undefined|None|""|'"'"''"'"')|is[[:space:]]+None|is_none\(|isEmpty\(|is_empty\(|\.length[[:space:]]*===[[:space:]]*0|len\([^)]*\)[[:space:]]*==[[:space:]]*0|Count[[:space:]]*==[[:space:]]*0)'
  'dependency-guard:(if[[:space:]]+[^[:space:]]*(repo|repository|dao|client|service|logger|config|provider|manager|store)[^[:space:]]*[[:space:]]*(==|is)[[:space:]]*(nil|null|None|undefined)|Objects\.requireNonNull\([^)]*(repo|repository|dao|client|service|logger|config|provider|manager|store))'
  'default-fallback:(unwrap_or_default\(|orElse\(|getOrDefault\(|defaultIfEmpty\(|\?\?|:[[:space:]]*""|=[[:space:]]*[^;#]*(default|Default|fallback|Fallback))'
  'error-wrapping:(fmt\.Errorf\([^)]*%w|errors\.Wrap|wrap_err|with_context|raise[[:space:]]+.*from|throw[[:space:]]+new)'
  'logging:(logger\.(debug|info|warn|error)|log\.(Debug|Info|Warn|Error)|console\.(log|warn|error)|print\()'
)

if [[ -n "$config" ]]; then
  if [[ ! -f "$config" ]]; then
    echo "config not found: $config" >&2
    exit 2
  fi
  while IFS= read -r line; do
    [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]] && continue
    if [[ "$line" != *:* ]]; then
      echo "config pattern must be type:regex: $line" >&2
      exit 2
    fi
    patterns+=("$line")
  done < "$config"
fi

scan_stream() {
  local line type regex
  while IFS= read -r line; do
    for entry in "${patterns[@]}"; do
      type="${entry%%:*}"
      regex="${entry#*:}"
      if [[ "$line" =~ $regex ]]; then
        printf '%s\t%s\n' "$type" "$line"
      fi
    done
  done
}

found=0
output=""

if ((${#paths[@]})); then
  if rg --version >/dev/null 2>&1; then
    output="$({ rg -n '.*' "${paths[@]}" || true; } | scan_stream)"
  else
    for path in "${paths[@]}"; do
      if [[ -d "$path" ]]; then
        while IFS= read -r file; do
          output+="$({ grep -nE '.*' "$file" || true; } | sed "s#^#$file:#" | scan_stream)"
          output+=$'\n'
        done < <(find "$path" -type f)
      elif [[ -f "$path" ]]; then
        output+="$({ grep -nE '.*' "$path" || true; } | sed "s#^#$path:#" | scan_stream)"
        output+=$'\n'
      fi
    done
  fi
else
  if [[ "$mode" == "staged" ]]; then
    output="$(git diff --cached --unified=0 --no-ext-diff | awk '/^\+\+\+ / { file=$2; sub(/^b\//, "", file); next } /^\+[^+]/ { print file ":" substr($0, 2) }' | scan_stream)"
  else
    output="$(git diff --unified=0 --no-ext-diff | awk '/^\+\+\+ / { file=$2; sub(/^b\//, "", file); next } /^\+[^+]/ { print file ":" substr($0, 2) }' | scan_stream)"
  fi
fi

if [[ -z "${output//$'\n'/}" ]]; then
  echo "no defensive-code candidates found"
  exit 0
fi

printf '%s\n' "$output" | sed '/^$/d'
echo
echo "Candidates found. Classify each as keep-boundary, remove-redundant, move-to-boundary, or needs-evidence before editing."

if ((fail_on_match)); then
  exit 1
fi
