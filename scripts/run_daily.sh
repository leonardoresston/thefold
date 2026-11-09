#!/bin/bash
# Daily run for The Fold on the Mac Mini: Gemini 4 Argon (agy) writes the
# edition; this script checks it, rebuilds feed.xml, commits and pushes.
# Usage: scripts/run_daily.sh [YYYY-MM-DD]
set -uo pipefail
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
REPO="$(cd "$(dirname "$0")/.." && pwd)"
MODEL="${FOLD_MODEL:-gemini-4-argon-high}"
cd "$REPO" || exit 1

DATE="${1:-$(TZ=Europe/London date +%F)}"
YEAR="${DATE%%-*}"; MMDD="${DATE#*-}"
ARCHIVE="archive/$YEAR/$MMDD.html"
echo "=== The Fold $DATE · $(date) ==="

git pull --ff-only origin main || { echo "FAIL: git pull"; exit 1; }
if [ -f "$ARCHIVE" ]; then echo "Already published: $ARCHIVE"; exit 0; fi
mkdir -p "archive/$YEAR"

PROMPT="$(sed -e "s/{{DATE}}/$DATE/g" -e "s/{{YEAR}}/$YEAR/g" -e "s/{{MMDD}}/$MMDD/g" scripts/daily_prompt.md)"
agy --model "$MODEL" --dangerously-skip-permissions --print-timeout 2400s -p="$PROMPT"

for round in 1 2 3; do
  [ -f index.html ] && [ -f "$ARCHIVE" ] || { echo "FAIL: edition files missing"; git checkout -- index.html 2>/dev/null; exit 1; }
  cp index.html "$ARCHIVE"
  if CHECK="$(python3 scripts/check_edition.py index.html 2>&1)"; then echo "$CHECK"; break; fi
  echo "$CHECK"
  if [ "$round" = 3 ]; then echo "FAIL: check still has errors"; git checkout -- index.html; rm -f "$ARCHIVE"; exit 1; fi
  agy --model "$MODEL" --dangerously-skip-permissions --print-timeout 1200s --continue \
    -p="The pre-publish check failed. Fix every ERROR in index.html, copy it to $ARCHIVE, and re-run the check. Output:
$CHECK"
done

python3 scripts/build_feed.py || { echo "FAIL: build_feed"; exit 1; }
xmllint --noout feed.xml || { echo "FAIL: feed.xml is not well-formed"; exit 1; }

git add index.html "$ARCHIVE" feed.xml
git commit -m "Publish The Fold $DATE" || { echo "FAIL: commit"; exit 1; }
git push origin main || { sleep 30; git pull --rebase origin main && git push origin main; } || { echo "FAIL: push"; exit 1; }
echo "OK: $(git rev-parse --short HEAD) · https://leonardoresston.github.io/thefold/$ARCHIVE · feed https://leonardoresston.github.io/thefold/feed.xml"
