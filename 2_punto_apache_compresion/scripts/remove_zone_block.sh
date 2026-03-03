#!/usr/bin/env bash
set -euo pipefail

ZONE_NAME="${1:-juan-camilo.com}"
CONF="/etc/bind/named.conf.local"
TMP="/tmp/named.conf.local.cleaned"

sudo awk -v z="${ZONE_NAME}" '
BEGIN { skip=0 }
$0 ~ "zone \"" z "\"[[:space:]]*\\{" { skip=1; next }
skip && $0 ~ /^[[:space:]]*};[[:space:]]*$/ { skip=0; next }
skip { next }
{ print }
' "${CONF}" | sudo tee "${TMP}" >/dev/null

sudo mv "${TMP}" "${CONF}"
sudo named-checkconf
sudo systemctl restart named
sudo grep -n 'zone "' "${CONF}" || true
