#!/usr/bin/env bash
# Commit each file individually with a descriptive message, then push.
# Run from inside the what_i_know/ directory.

set -euo pipefail

# Sanity check: are we in the right place?
if [ ! -d "monorepo" ] || [ ! -d "cron-job" ]; then
  echo "Error: run this from inside what_i_know/ (where monorepo/ and cron-job/ exist)"
  exit 1
fi

# Initialize repo if it doesn't exist yet
if [ ! -d ".git" ]; then
  echo "Initializing git repo..."
  git init
fi

# Helper: stage one file and commit with a message
commit_one() {
  local path="$1"
  local msg="$2"
  if [ -f "$path" ]; then
    git add "$path"
    git commit -m "$msg"
    echo "  ✓ $path"
  else
    echo "  ⚠ skipping $path (not found)"
  fi
}

echo ""
echo "=== Committing root files ==="
commit_one ".gitignore" "chore: add gitignore"

echo ""
echo "=== Committing workflow ==="
commit_one ".github/workflows/daily-email.yml" "ci: add daily knowledge email workflow"

echo ""
echo "=== Committing cron-job ==="
commit_one "cron-job/README.md"               "docs(cron-job): add README"
commit_one "cron-job/requirements.txt"        "chore(cron-job): add Python dependencies"
commit_one "cron-job/scripts/send_daily.py"   "feat(cron-job): add daily email script with LLM enhancement"

echo ""
echo "=== Committing monorepo README ==="
commit_one "monorepo/README.md" "docs(monorepo): add knowledge base README"

echo ""
echo "=== Committing system-design notes ==="
commit_one "monorepo/system-design/api-gateway.md"              "docs(system-design): add API Gateway concept"
commit_one "monorepo/system-design/load-balancer.md"            "docs(system-design): add Load Balancer concept"
commit_one "monorepo/system-design/caching-strategies.md"       "docs(system-design): add caching strategies concept"
commit_one "monorepo/system-design/cdn.md"                      "docs(system-design): add CDN concept"
commit_one "monorepo/system-design/database-sharding.md"        "docs(system-design): add database sharding concept"
commit_one "monorepo/system-design/message-queues.md"           "docs(system-design): add message queues concept"
commit_one "monorepo/system-design/database-replication.md"     "docs(system-design): add database replication concept"
commit_one "monorepo/system-design/consistent-hashing.md"       "docs(system-design): add consistent hashing concept"
commit_one "monorepo/system-design/video-streaming-security.md" "docs(system-design): add video streaming security concept"

echo ""
echo "=== Committing dsa notes ==="
commit_one "monorepo/dsa/dijkstra.md"           "docs(dsa): add Dijkstra's algorithm"
commit_one "monorepo/dsa/a-star.md"             "docs(dsa): add A* search algorithm"
commit_one "monorepo/dsa/sliding-window.md"     "docs(dsa): add sliding window pattern"
commit_one "monorepo/dsa/slow-fast-pointer.md"  "docs(dsa): add slow-fast pointer pattern"

echo ""
echo "=== Catching any leftover files ==="
if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -m "chore: add remaining files"
  echo "  ✓ committed leftovers"
else
  echo "  (nothing left)"
fi

echo ""
echo "=== Setting up remote and pushing ==="
git branch -M main

# Add remote only if it doesn't already exist
if git remote get-url origin > /dev/null 2>&1; then
  echo "Remote 'origin' already exists, skipping add"
else
  git remote add origin https://github.com/Rahul1038402/what_i_know.git
fi

git push -u origin main

echo ""
echo "Done. Repo pushed to https://github.com/Rahul1038402/what_i_know"