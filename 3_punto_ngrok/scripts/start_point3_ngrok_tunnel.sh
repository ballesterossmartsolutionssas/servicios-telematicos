#!/usr/bin/env bash
set -euo pipefail

# Optional: export NGROK_AUTHTOKEN="your_token" or pass as first arg.
TOKEN="${NGROK_AUTHTOKEN:-${1:-}}"
if [[ -n "${TOKEN}" ]]; then
  ngrok config add-authtoken "${TOKEN}" >/dev/null
fi

pkill -f "ngrok http 80" || true
nohup ngrok http 80 --log=stdout > /tmp/ngrok_http80.log 2>&1 &
sleep 6

if curl -fsS http://127.0.0.1:4040/api/tunnels >/tmp/ngrok_api.json 2>/dev/null; then
  URL="$(jq -r '.tunnels[0].public_url // empty' /tmp/ngrok_api.json)"
  if [[ -n "${URL}" ]]; then
    echo "NGROK_PUBLIC_URL=${URL}"
    exit 0
  fi
fi

echo "No se obtuvo URL publica. Revisa /tmp/ngrok_http80.log" >&2
tail -n 40 /tmp/ngrok_http80.log >&2 || true
exit 1
