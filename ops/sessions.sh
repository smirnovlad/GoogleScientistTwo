#!/bin/bash
# The task sessions' tmux: one session called "gs2", one window per task session, named T<n>.
# How it is used, and why: docs/process/worktrees-and-sessions.md, "Running task sessions in tmux".
#
#   ops/sessions.sh list
#   ops/sessions.sh start   T<n> <worktree> claude --permission-mode auto --effort max "'<prompt>'"
#   ops/sessions.sh restart T<n> claude --permission-mode auto --effort max --resume <id>
#
# ⛔ WHY NOT a plain `tmux new-window`, from the shell an agent is running in?
# That shell carries the launching session's own variables (CLAUDE_CODE_SESSION_ID, its account,
# ANTHROPIC_BASE_URL). A window that got them would hand them to the task's session, which would
# then act as the wrong session. Two guards:
#   - every tmux call here runs under `env -i`, so a server this script starts begins clean;
#   - each window's shell itself starts from an empty environment (PANE_SHELL), because a window
#     inherits the SERVER's environment, and the server may already run, started by anyone.
#
# ⚠️ `restart` types /exit into the window. Run it only when that session is IDLE: anything still
# running under it (a review agent, a background command) dies with it. The conversation itself
# survives, because --resume reloads it.
set -euo pipefail
S=gs2

T() {
  env -i HOME="$HOME" USER="$USER" LOGNAME="$USER" SHELL=/bin/zsh TERM=xterm-256color \
    LANG="${LANG:-en_US.UTF-8}" PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin \
    tmux "$@"
}
# Run by the window's own shell, so the variables below are read inside the window: its account
# basics, and the terminal variables tmux sets for that window. Nothing else passes.
PANE_SHELL='exec env -i HOME="$HOME" USER="$USER" LOGNAME="$LOGNAME" SHELL=/bin/zsh'
PANE_SHELL+=' LANG="${LANG:-en_US.UTF-8}" TERM="$TERM" TMUX="$TMUX" TMUX_PANE="$TMUX_PANE"'
PANE_SHELL+=' ${COLORTERM:+"COLORTERM=$COLORTERM"} ${TERM_PROGRAM:+"TERM_PROGRAM=$TERM_PROGRAM"}'
PANE_SHELL+=' ${TERM_PROGRAM_VERSION:+"TERM_PROGRAM_VERSION=$TERM_PROGRAM_VERSION"}'
PANE_SHELL+=' PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin /bin/zsh -l'
usage() {
  echo "usage: $0 list | start T<n> <worktree> <command…> | restart T<n> <command…>" >&2
  exit 2
}
ensure() {
  T has-session -t "$S" 2>/dev/null || T new-session -d -s "$S" -n home -c "$HOME" "$PANE_SHELL"
  T set -g mouse on    # click a window name in the status bar to switch; scroll with the wheel
}
# Output is captured before grep reads it: with pipefail, `tmux … | grep -q` can fail on a match
# when grep exits first and tmux dies of SIGPIPE.
has_window() {
  local names
  names=$(T list-windows -t "$S" -F '#{window_name}' 2>/dev/null) || return 1
  grep -qx -- "$1" <<<"$names"
}
# "zsh" means no Claude runs in the window; a version number (e.g. 2.1.286) means one does.
running() { T display -p -t "$S:$1" '#{pane_current_command}'; }

cmd=${1:-list}
shift || true
case "$cmd" in
  start)
    [[ $# -ge 3 ]] || usage
    w=$1 d=$2
    shift 2
    [[ -d "$d" ]] || { echo "⛔ no such worktree: $d" >&2; exit 1; }
    ensure
    if has_window "$w"; then
      echo "⛔ window $w exists already: restart it, or choose another name" >&2
      exit 1
    fi
    T new-window -d -t "$S" -n "$w" -c "$d" "$PANE_SHELL"
    sleep 2
    T send-keys -t "$S:$w" -l -- "$*"
    T send-keys -t "$S:$w" Enter
    ;;
  restart)
    [[ $# -ge 2 ]] || usage
    w=$1
    shift
    has_window "$w" || { echo "⛔ no window $w in session $S" >&2; exit 1; }
    T send-keys -t "$S:$w" -l -- "/exit"
    sleep 1
    T send-keys -t "$S:$w" Enter
    for _ in $(seq 1 30); do
      sleep 1
      [[ "$(running "$w")" == zsh ]] && break
    done
    if [[ "$(running "$w")" != zsh ]]; then
      # /exit opens a dialog instead of exiting when the session has background tasks.
      echo "⛔ $w did not exit: it is busy, or it shows a dialog. Look before retrying:" >&2
      echo "   tmux capture-pane -p -t $S:$w | tail -8" >&2
      exit 1
    fi
    T send-keys -t "$S:$w" -l -- "$*"
    T send-keys -t "$S:$w" Enter
    ;;
  list)
    ensure
    T list-windows -t "$S" -F '#{window_index} #{window_name} #{pane_current_command} #{pane_current_path}'
    ;;
  *)
    usage
    ;;
esac
