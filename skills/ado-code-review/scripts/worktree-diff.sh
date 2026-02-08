#!/bin/bash
# worktree-diff.sh - Worktree-based diff for Azure DevOps PRs
# Usage: ./worktree-diff.sh <repo_path> <source_branch> [target_branch]

set -e

REPO_PATH="${1:-.}"
SOURCE_BRANCH="$2"
TARGET_BRANCH="${3:-main}"

if [ -z "$SOURCE_BRANCH" ]; then
    echo "Usage: $0 <repo_path> <source_branch> [target_branch]"
    echo "Example: $0 /path/to/repo feature/user-auth main"
    exit 1
fi

cd "$REPO_PATH" || {
    echo "Error: Cannot access repository at $REPO_PATH"
    exit 1
}

echo "=== Azure DevOps PR Diff Report ==="
echo "Repository: $(pwd)"
echo "Source: $SOURCE_BRANCH"
echo "Target: $TARGET_BRANCH"
echo ""

# Fetch latest
echo "Fetching latest changes..."
git fetch origin --quiet

# Check if branches exist
if ! git rev-parse "origin/$SOURCE_BRANCH" > /dev/null 2>&1; then
    echo "Error: Branch origin/$SOURCE_BRANCH not found"
    exit 1
fi

if ! git rev-parse "origin/$TARGET_BRANCH" > /dev/null 2>&1; then
    echo "Error: Branch origin/$TARGET_BRANCH not found"
    exit 1
fi

# Calculate merge base
MERGE_BASE=$(git merge-base "origin/$TARGET_BRANCH" "origin/$SOURCE_BRANCH")
echo "Merge Base: $MERGE_BASE"
echo ""

# Get commit info
echo "=== Commits in PR ==="
git log "$MERGE_BASE".."origin/$SOURCE_BRANCH" --oneline
COMMIT_COUNT=$(git log "$MERGE_BASE".."origin/$SOURCE_BRANCH" --oneline | wc -l | tr -d ' ')
echo ""
echo "Total commits: $COMMIT_COUNT"
echo ""

# Get diff stats
echo "=== Diff Statistics ==="
git diff "$MERGE_BASE".."origin/$SOURCE_BRANCH" --stat
echo ""

# Get changed files
echo "=== Changed Files ==="
CHANGED_FILES=$(git diff "$MERGE_BASE".."origin/$SOURCE_BRANCH" --name-only)
echo "$CHANGED_FILES"
FILE_COUNT=$(echo "$CHANGED_FILES" | wc -l | tr -d ' ')
echo ""
echo "Total files changed: $FILE_COUNT"
echo ""

# Get additions/deletions
STATS=$(git diff "$MERGE_BASE".."origin/$SOURCE_BRANCH" --shortstat)
echo "Summary: $STATS"
echo ""

# Check for specific file types
echo "=== File Type Breakdown ==="
CS_FILES=$(echo "$CHANGED_FILES" | grep -c '\.cs$' || echo "0")
TEST_FILES=$(echo "$CHANGED_FILES" | grep -c 'Tests\|\.Tests\|\.Test' || echo "0")
CONFIG_FILES=$(echo "$CHANGED_FILES" | grep -c '\.json$\|\.xml$\|\.config$' || echo "0")

echo "C# files: $CS_FILES"
echo "Test files: $TEST_FILES"
echo "Config files: $CONFIG_FILES"
echo ""

# Output full diff (optional - can be large)
if [ "${FULL_DIFF:-false}" = "true" ]; then
    echo "=== Full Diff ==="
    git diff "$MERGE_BASE".."origin/$SOURCE_BRANCH" --no-color
fi

echo "=== End of Report ==="
