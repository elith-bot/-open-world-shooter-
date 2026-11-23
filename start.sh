#!/usr/bin/env bash
set -eu
cd -- "$(dirname -- "$0")"
if [ "${OFFLINE:-0}" != 1 ]; then
  if ! timeout 25 git pull --ff-only origin main; then
    echo "Update unavailable; using local version." >&2
  fi
fi
python3 setup_assets.py
PORT="${PORT:-8080}"
URL="http://127.0.0.1:$PORT"
python3 -m http.server "$PORT" --bind 127.0.0.1 &
PID=$!
trap 'kill "$PID" 2>/dev/null || true' EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
sleep 1
kill -0 "$PID"
echo "Game: $URL"
if command -v termux-open-url >/dev/null; then termux-open-url "$URL" || true
elif command -v xdg-open >/dev/null; then xdg-open "$URL" || true
fi
wait "$PID"
