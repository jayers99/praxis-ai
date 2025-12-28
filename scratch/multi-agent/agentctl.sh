#!/usr/bin/env bash
# agentctl.sh - Lightweight worktree helper for multi-agent workflows
# Usage examples:
#   ./agentctl.sh init
#   ./agentctl.sh add a my-topic
#   ./agentctl.sh list
#   ./agentctl.sh remove a my-topic

set -euo pipefail

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -z "${repo_root}" ]]; then
  echo "ERROR: Not inside a git repository." >&2
  exit 1
fi

repo_name="$(basename "${repo_root}")"

usage() {
  cat <<'EOF'
agentctl.sh - manage per-agent git worktrees

Commands:
  init
      Fetch and prune remotes (safe baseline)

  add <agent> <topic> [--base <base-branch>] [--dir <worktree-dir>]
      Create a new worktree + branch:
        branch: agent/<agent>/<topic>
        dir:    ../<repo>-agent-<agent>-<topic>   (default)

      Options:
        --base <base-branch>   Base branch (default: origin/HEAD if available, else main, else master)
        --dir  <dir>           Explicit directory path for worktree

  list
      Show existing worktrees

  remove <agent> <topic> [--dir <worktree-dir>]
      Remove a worktree directory (and prune worktree metadata)

Examples:
  ./agentctl.sh init
  ./agentctl.sh add a api-client
  ./agentctl.sh add tester authz --base main
  ./agentctl.sh list
  ./agentctl.sh remove a api-client
EOF
}

choose_base() {
  # Prefer origin/HEAD if set; otherwise main; otherwise master
  if git symbolic-ref -q refs/remotes/origin/HEAD >/dev/null 2>&1; then
    git symbolic-ref refs/remotes/origin/HEAD | sed 's#^refs/remotes/##'
    return 0
  fi
  if git show-ref --verify --quiet refs/heads/main || git show-ref --verify --quiet refs/remotes/origin/main; then
    echo "main"
    return 0
  fi
  if git show-ref --verify --quiet refs/heads/master || git show-ref --verify --quiet refs/remotes/origin/master; then
    echo "master"
    return 0
  fi
  # Last resort
  echo "main"
}

cmd="${1:-}"
shift || true

case "${cmd}" in
  ""|-h|--help|help)
    usage
    ;;
  init)
    git fetch --all --prune
    echo "OK: fetched and pruned remotes."
    ;;
  add)
    agent="${1:-}"
    topic="${2:-}"
    shift 2 || true
    if [[ -z "${agent}" || -z "${topic}" ]]; then
      echo "ERROR: add requires <agent> <topic>" >&2
      usage
      exit 2
    fi

    base="$(choose_base)"
    dir=""

    while [[ $# -gt 0 ]]; do
      case "$1" in
        --base)
          base="${2:-}"; shift 2 ;;
        --dir)
          dir="${2:-}"; shift 2 ;;
        *)
          echo "ERROR: unknown option: $1" >&2
          usage
          exit 2 ;;
      esac
    done

    branch="agent/${agent}/${topic}"
    if [[ -z "${dir}" ]]; then
      dir="../${repo_name}-agent-${agent}-${topic}"
    fi

    git fetch --all --prune

    # Resolve base ref
    base_ref="${base}"
    if git show-ref --verify --quiet "refs/remotes/origin/${base}"; then
      base_ref="origin/${base}"
    fi

    echo "Creating worktree:"
    echo "  base:   ${base_ref}"
    echo "  branch: ${branch}"
    echo "  dir:    ${dir}"

    git worktree add "${dir}" -b "${branch}" "${base_ref}"
    echo "OK: worktree created at ${dir}"
    ;;
  list)
    git worktree list
    ;;
  remove)
    agent="${1:-}"
    topic="${2:-}"
    shift 2 || true
    if [[ -z "${agent}" || -z "${topic}" ]]; then
      echo "ERROR: remove requires <agent> <topic>" >&2
      usage
      exit 2
    fi

    dir=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --dir)
          dir="${2:-}"; shift 2 ;;
        *)
          echo "ERROR: unknown option: $1" >&2
          usage
          exit 2 ;;
      esac
    done

    if [[ -z "${dir}" ]]; then
      dir="../${repo_name}-agent-${agent}-${topic}"
    fi

    if [[ ! -d "${dir}" ]]; then
      echo "ERROR: directory does not exist: ${dir}" >&2
      exit 2
    fi

    git worktree remove --force "${dir}"
    git worktree prune
    echo "OK: removed worktree ${dir}"
    ;;
  *)
    echo "ERROR: unknown command: ${cmd}" >&2
    usage
    exit 2
    ;;
esac
