#!/usr/bin/env bash
set -euo pipefail

DNS_PRIMARY_1="${DNS_PRIMARY_1:-1.1.1.1#cloudflare-dns.com}"
DNS_PRIMARY_2="${DNS_PRIMARY_2:-8.8.8.8#dns.google}"
DNS_FALLBACK_1="${DNS_FALLBACK_1:-1.0.0.1#cloudflare-dns.com}"
DNS_FALLBACK_2="${DNS_FALLBACK_2:-8.8.4.4#dns.google}"
RESOLVED_CONF="/etc/systemd/resolved.conf"

sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y dnsutils tshark

if [[ ! -f "${RESOLVED_CONF}.bak.codex" ]]; then
    sudo cp "${RESOLVED_CONF}" "${RESOLVED_CONF}.bak.codex"
fi

sudo tee "${RESOLVED_CONF}" >/dev/null <<EOF
[Resolve]
DNS=${DNS_PRIMARY_1} ${DNS_PRIMARY_2}
FallbackDNS=${DNS_FALLBACK_1} ${DNS_FALLBACK_2}
DNSOverTLS=yes
Domains=~.
EOF

sudo systemctl enable --now systemd-resolved
sudo ln -sf /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf
sudo systemctl restart systemd-resolved

sudo resolvectl dns eth0 "${DNS_PRIMARY_1}" "${DNS_PRIMARY_2}"
sudo resolvectl dnsovertls eth0 yes
sudo resolvectl domain eth0 '~.'
sudo resolvectl flush-caches

echo "== resolved.conf =="
cat "${RESOLVED_CONF}"
echo
echo "== resolvectl status =="
resolvectl status | sed -n '1,80p'
