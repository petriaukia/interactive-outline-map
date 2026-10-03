#!/usr/bin/env bash
# Mechanical checks for a generated outline map. Everything here is something a
# script can see; the judgement calls stay in SKILL.md.
set -u

file="${1:-}"
if [ -z "$file" ] || [ ! -f "$file" ]; then
  echo "usage: scripts/check.sh <map.html>" >&2
  exit 2
fi

fail=0
report() { printf '%-8s %s\n' "$1" "$2"; [ "$1" = "FAIL" ] && fail=1; return 0; }

# 1. Leftover template text
if grep -qE 'Replace the map title|Replace this with one line|its source and a link to it|The main proposition or the purpose|first qualification' "$file"; then
  report FAIL "sample text from the template is still in the file"
else
  report ok "no leftover sample text"
fi

# 2. Storage key
if grep -q 'data-map-key="replace-with-a-stable-map-key"' "$file"; then
  report FAIL "data-map-key is still the placeholder"
elif grep -q 'data-map-key="[^"]\+"' "$file"; then
  report ok "data-map-key replaced"
else
  report FAIL "data-map-key is missing"
fi

# 3. Branch ids: present, unique, ASCII
ids=$(grep -o 'data-branch-id="[^"]*"' "$file" | sed 's/.*="//;s/"//')
count=$(printf '%s\n' "$ids" | grep -c . || true)
unique=$(printf '%s\n' "$ids" | sort -u | grep -c . || true)
if [ "$count" -eq 0 ]; then
  report FAIL "no branches found"
elif [ "$count" -ne "$unique" ]; then
  report FAIL "duplicate data-branch-id values"
elif printf '%s' "$ids" | LC_ALL=C grep -q '[^a-zA-Z0-9_-]'; then
  report FAIL "a data-branch-id is not plain ASCII"
else
  report ok "$count branches, ids unique and ASCII"
fi

# 4. Branch count is inside the range the skill asks for
if [ "$count" -lt 4 ] || [ "$count" -gt 7 ]; then
  report warn "$count top-level branches (SKILL.md asks for 4-7)"
fi

# 5. At most one key idea per branch
if command -v python3 >/dev/null 2>&1; then
  if msg=$(python3 - "$file" <<'PYCHECK'
import re, sys
html = open(sys.argv[1], encoding='utf-8').read()
branches = re.findall(r'<article class="branch".*?(?=<article class="branch"|</section>)', html, re.S)
bad = [i + 1 for i, b in enumerate(branches) if len(re.findall(r'class="leaf highlight"', b)) > 1]
if bad:
    print('branch %s carries more than one leaf highlight' % ', '.join(map(str, bad)))
    sys.exit(1)
PYCHECK
  ); then
    report ok "at most one leaf highlight per branch"
  else
    report FAIL "$msg"
  fi
fi

# 6. Language declared
grep -q '<html lang="[a-z]' "$file" && report ok "lang declared" || report FAIL "<html lang> is missing"

# 7. Self-contained: no remote resources (links in the running text are fine)
if grep -qE '<link[^>]+href=|<(script|img|iframe|source|video|audio)[^>]+src="https?:|@import|url\(https?:' "$file"; then
  report FAIL "the file loads something from a remote host"
else
  report ok "no remote dependencies"
fi

# 8. The embedded script parses
if command -v node >/dev/null 2>&1; then
  tmp=$(mktemp -t iom-check).js
  python3 - "$file" > "$tmp" <<'PYEXTRACT'
import re, sys
html = open(sys.argv[1], encoding='utf-8').read()
# every inline script, one block each, so a small head script cannot hide the main one
sys.stdout.write('\n;\n'.join('{' + s + '\n}' for s in re.findall(r'<script>(.*?)</script>', html, re.S)))
PYEXTRACT
  if node --check "$tmp" >/dev/null 2>&1; then report ok "embedded script parses"; else report FAIL "embedded script does not parse"; fi
  rm -f "$tmp"
else
  report warn "node not found, skipped the script parse check"
fi

exit $fail
