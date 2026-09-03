#!/bin/sh
# unlock.sh — clear stale git *.lock files across the estate.
#
#   tools/unlock.sh            from anywhere inside the estate
#   tools/unlock.sh <root>     explicit root
#
# Runs before anything that touches git. A stale index.lock is not a warning:
# git refuses the whole operation, and in a submodule walk that means the walk
# stops halfway with some repos committed and some not.
#
# WHY find AND NOT A GLOB
#   git writes locks at four depths: .git/index.lock, .git/logs/HEAD.lock,
#   .git/refs/heads/main.lock, and .git/refs/heads/feature/x.lock when the
#   branch name has a slash. A fixed glob has to guess the depth and will be
#   wrong for one of them. The predecessors each guessed differently and each
#   missed a different set — merged here, 2026-08-30.
#
# WHY rm THEN mv
#   Agents see these trees over a FUSE mount that permits rename() but denies
#   unlink(), so `rm -f .git/index.lock` fails with "Operation not permitted"
#   while the lock stays put. Renaming ONTO an existing file works. Outside the
#   sandbox rm works normally and the fallback never fires. This was the sole
#   reason tools/unlock-fuse.sh existed; it is three lines, so it lives here now.
#
# EXITS NONZERO IF A LOCK WILL NOT CLEAR. A cleaner that reports success while
# the lock is still there is worse than no cleaner — the caller proceeds into a
# failure it was told could not happen.

set -eu

# ── Estate root ───────────────────────────────────────────────────────────────
# Resolved by walking up for .gitmodules, so `tools/unlock.sh` works from the
# estate root, from inside a submodule, and from any subdirectory. The previous
# version only ever resolved as `../tools/unlock.sh` from one level down, which
# is bugs/4-low-bernard-tools-unlock-sh-cannot-be-run-from-the-estate-root.md.
if [ $# -ge 1 ]; then
    ROOT="$1"
else
    ROOT="$(pwd)"
    while [ "$ROOT" != "/" ] && [ ! -f "$ROOT/.gitmodules" ]; do
        ROOT="$(dirname "$ROOT")"
    done
    # No .gitmodules found (single-repo checkout, or run from outside): fall
    # back to the script's own location, which is always correct for the estate
    # this copy belongs to.
    [ -f "$ROOT/.gitmodules" ] || ROOT="$(cd "$(dirname "$0")/.." && pwd)"
fi

[ -d "$ROOT" ] || { echo "unlock: no such root: $ROOT" >&2; exit 1; }

n=0
stuck=0

clear_repo() {
    repo="$1"
    git_dir="$repo/.git"

    # A submodule's .git is a FILE pointing at the real dir. Follow it, or every
    # submodule is silently skipped by a -d test that looks correct.
    if [ -f "$git_dir" ]; then
        real=$(sed -n 's/^gitdir: //p' "$git_dir")
        case "$real" in
            /*) git_dir="$real" ;;
            *)  git_dir="$repo/$real" ;;
        esac
    fi
    [ -d "$git_dir" ] || return 0

    grave="$git_dir/gravestone"
    [ -e "$grave" ] || : > "$grave" 2>/dev/null || true

    # -type f: a directory named *.lock is not a git lock, and removing one
    # would be destructive rather than corrective.
    find "$git_dir" -type f -name '*.lock' 2>/dev/null | while IFS= read -r lock; do
        if rm -f "$lock" 2>/dev/null || mv -f "$lock" "$grave" 2>/dev/null; then
            echo "  cleared $lock"
        else
            echo "  STUCK   $lock" >&2
        fi
    done
}

# Count in the parent shell: the `while` above runs in a subshell on POSIX sh,
# so counters incremented inside it are lost. Recount by asking the filesystem
# what is left, which is the honest question anyway.
#
# NO -maxdepth HERE. It must match the clearing find exactly. A shallower count
# than the clear is how a cleaner reports "0 stuck" over a lock it never looked
# at — caught on the first test run, which cleared 7 and reported 3.
count_locks() {
    find "$ROOT" -type f -name '*.lock' -path '*/.git/*' 2>/dev/null | wc -l | tr -d ' '
}

before=$(count_locks)

clear_repo "$ROOT"
for sub in "$ROOT"/*/; do
    [ -d "$sub" ] && clear_repo "${sub%/}"
done

after=$(count_locks)
n=$((before - after))
stuck=$after

if [ "$stuck" -gt 0 ]; then
    echo "unlock: $n cleared, $stuck STUCK — git will still fail." >&2
    exit 1
fi

if [ "$n" -eq 0 ]; then
    echo "unlock: no lock files found."
else
    echo "unlock: cleared $n lock file(s)."
fi
exit 0
