#!/usr/bin/env bash
set -Eeuo pipefail

REPO_URL="${REPO_URL:-https://github.com/joshcheng/mini-telegram-name-timing-sync.git}"
REF="${REF:-main}"
PREFIX="${PREFIX:-/opt/telegram-name-timing-sync}"
CONFIG_DIR="${CONFIG_DIR:-/etc/telegram-name-timing-sync}"
UNIT_DIR="${UNIT_DIR:-/etc/systemd/system}"
SKIP_SYSTEMD="${SKIP_SYSTEMD:-0}"

[[ $EUID -eq 0 ]] || { echo "Run with sudo/root." >&2; exit 1; }
command -v python3 >/dev/null || { echo "python3 is required." >&2; exit 1; }
command -v git >/dev/null || { echo "git is required." >&2; exit 1; }

if [[ ! -d "$PREFIX/.git" ]]; then
  git clone --depth 1 --branch "$REF" "$REPO_URL" "$PREFIX"
else
  git -C "$PREFIX" fetch --depth 1 origin "$REF"
  git -C "$PREFIX" reset --hard FETCH_HEAD
fi

python3 -m venv "$PREFIX/venv"
"$PREFIX/venv/bin/pip" install --disable-pip-version-check "$PREFIX"
install -d -m 700 "$CONFIG_DIR"
if [[ ! -f "$CONFIG_DIR/config.json" ]]; then
  install -m 600 "$PREFIX/config.example.json" "$CONFIG_DIR/config.json"
  echo "Created $CONFIG_DIR/config.json — edit it before starting the service."
fi

if [[ "$SKIP_SYSTEMD" != "1" ]]; then
  install -m 644 "$PREFIX/packaging/telegram-name-timing-sync.service" "$UNIT_DIR/telegram-name-timing-sync.service"
  systemctl daemon-reload
  systemctl enable telegram-name-timing-sync.service
  echo "Run: sudo systemctl start telegram-name-timing-sync"
fi
