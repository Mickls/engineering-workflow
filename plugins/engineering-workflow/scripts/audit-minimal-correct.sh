#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: audit-minimal-correct.sh [--staged|--base REF|--strict]

Report minimal-correct implementation candidates in the current git diff.
This is a heuristic audit: it does not edit files and does not fail by default
when candidates are found.

Modes:
  --staged       Audit staged diff only.
  --base REF     Audit changes from REF to HEAD/worktree.

Options:
  --strict       Exit 1 when warn-level candidates are found.
  -h, --help     Show this help.
EOF
}

mode="worktree"
base_ref=""
strict=0

while (($#)); do
  case "$1" in
    --staged)
      mode="staged"
      shift
      ;;
    --base)
      if (($# < 2)); then
        echo "--base requires a ref" >&2
        exit 2
      fi
      mode="base"
      base_ref="$2"
      shift 2
      ;;
    --strict)
      strict=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

diff_cmd=(git diff --unified=0 --no-ext-diff)
name_cmd=(git diff --name-only --no-ext-diff)
status_cmd=(git diff --name-status --no-ext-diff)

if [[ "$mode" == "staged" ]]; then
  diff_cmd=(git diff --cached --unified=0 --no-ext-diff)
  name_cmd=(git diff --cached --name-only --no-ext-diff)
  status_cmd=(git diff --cached --name-status --no-ext-diff)
elif [[ "$mode" == "base" ]]; then
  diff_cmd=(git diff --unified=0 --no-ext-diff "$base_ref")
  name_cmd=(git diff --name-only --no-ext-diff "$base_ref")
  status_cmd=(git diff --name-status --no-ext-diff "$base_ref")
fi

tmp_added="$(mktemp)"
tmp_names="$(mktemp)"
tmp_status="$(mktemp)"
trap 'rm -f "$tmp_added" "$tmp_names" "$tmp_status"' EXIT

"${diff_cmd[@]}" | awk '
  /^\+\+\+ / { file=$2; sub(/^b\//, "", file); next }
  /^\+[^+]/ { print file ":" substr($0, 2) }
' > "$tmp_added"

"${name_cmd[@]}" > "$tmp_names"
"${status_cmd[@]}" > "$tmp_status"

if [[ "$mode" != "staged" ]]; then
  while IFS= read -r file; do
    [[ -f "$file" ]] || continue
    printf '%s\n' "$file" >> "$tmp_names"
    printf 'A\t%s\n' "$file" >> "$tmp_status"
    sed "s#^#$file:#" "$file" >> "$tmp_added"
  done < <(git ls-files --others --exclude-standard)
fi

declare -a findings=()
warn_count=0

add_finding() {
  local level="$1"
  local type="$2"
  local detail="$3"
  findings+=("${level}"$'\t'"${type}"$'\t'"${detail}")
  if [[ "$level" == "warn" ]]; then
    warn_count=$((warn_count + 1))
  fi
}

match_added() {
  local level="$1"
  local type="$2"
  local regex="$3"
  local message="$4"
  local matches
  matches="$(grep -E "$regex" "$tmp_added" \
    | grep -Ev '(^|/)audit-minimal-correct\.sh:' \
    | grep -v '^scripts/audit-minimal-correct\.sh:.*unknown option' || true)"
  if [[ -n "$matches" ]]; then
    while IFS= read -r line; do
      add_finding "$level" "$type" "$message: $line"
    done <<< "$matches"
  fi
}

dependency_regex='(^|/)(package(-lock)?\.json|pnpm-lock\.yaml|yarn\.lock|go\.(mod|sum)|pyproject\.toml|poetry\.lock|requirements.*\.txt|Pipfile(\.lock)?|Cargo\.(toml|lock)|Gemfile(\.lock)?|pom\.xml|build\.gradle|gradle\.properties|composer\.(json|lock))$'
while IFS= read -r file; do
  [[ -z "$file" ]] && continue
  if [[ "$file" =~ $dependency_regex ]]; then
    add_finding "warn" "dependency-change" "$file changed; explain why existing code, stdlib, framework/native feature, or installed deps were insufficient."
  fi
done < "$tmp_names"

new_files="$(awk '$1 ~ /^A/ { print $2 }' "$tmp_status" || true)"
new_file_count="$(printf '%s\n' "$new_files" | sed '/^$/d' | wc -l | tr -d ' ')"
if [[ "${new_file_count:-0}" -ge 3 ]]; then
  add_finding "info" "multi-file-expansion" "${new_file_count} new files; confirm this is not speculative structure."
fi

match_added "warn" "abstraction-candidate" '(^|[^[:alnum:]_])(interface|Interface|Factory|factory|Strategy|strategy|Adapter|adapter|Wrapper|wrapper|Provider|provider|Manager|manager)([^[:alnum:]_]|$)' "abstraction-like term added"
match_added "info" "config-flexibility" '(^|[^[:alnum:]_])(feature[_-]?flag|FeatureFlag|config|Config|option|Option|toggle|Toggle|enable[A-Z_]|disable[A-Z_]|template field)([^[:alnum:]_]|$)' "config/flexibility term added"
match_added "info" "test-helper-stack" '(^|[^[:alnum:]_])(mock|Mock|fixture|Fixture|testHelper|TestHelper|builder|Builder|stub|Stub)([^[:alnum:]_]|$)' "test helper/mock/fixture term added"
match_added "info" "native-stdlib-candidate" '(date picker|color picker|debounce|deep clone|csv|CSV|url params|URLSearchParams|rate limit|RateLimiter|email validation|EmailValidator)' "possible stdlib/native feature candidate"

if ((${#findings[@]} == 0)); then
  echo "ok: no minimal-correct implementation candidates found"
  exit 0
fi

printf '%s\n' "${findings[@]}" | awk -F '\t' '{ printf "%s\t%s\t%s\n", $1, $2, $3 }'
echo
echo "Review candidates before delivery. Keep only complexity backed by current requirements, project contracts, safety, or a documented defer-with-trigger."

if ((strict)) && ((warn_count > 0)); then
  exit 1
fi
