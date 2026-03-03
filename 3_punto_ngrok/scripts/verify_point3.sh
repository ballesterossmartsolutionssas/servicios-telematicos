#!/usr/bin/env bash
set -euo pipefail

if [[ ! -f /tmp/ngrok_api.json ]]; then
  echo "No existe /tmp/ngrok_api.json. Ejecuta primero start_point3_ngrok_tunnel.sh" >&2
  exit 1
fi

URL="$(jq -r '.tunnels[0].public_url // empty' /tmp/ngrok_api.json)"
if [[ -z "${URL}" ]]; then
  echo "No hay URL publica en /tmp/ngrok_api.json" >&2
  exit 1
fi

echo "Probando URL publica: ${URL}"
curl -I "${URL}/pagina_personalizada.html" | sed -n '1,15p'
echo
curl -s "${URL}/pagina_personalizada.html" | head -n 10
