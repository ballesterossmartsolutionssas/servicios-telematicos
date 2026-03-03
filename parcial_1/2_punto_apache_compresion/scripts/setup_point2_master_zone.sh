#!/usr/bin/env bash
set -euo pipefail

ZONE_DIR="/etc/bind"
ZONE_FILE="${ZONE_DIR}/db.juan-camilo.com"
MASTER_LOCAL="/etc/bind/named.conf.local"

if ! sudo grep -q 'zone "juan-camilo.com"' "${MASTER_LOCAL}"; then
cat <<'EOF' | sudo tee -a "${MASTER_LOCAL}" >/dev/null

zone "juan-camilo.com" {
    type master;
    file "/etc/bind/db.juan-camilo.com";
    notify yes;
    allow-transfer { key "axfr-key"; };
};
EOF
fi

cat <<'EOF' | sudo tee "${ZONE_FILE}" >/dev/null
$TTL 86400
@   IN  SOA maestro.empresa.local. admin.empresa.local. (
        2026030301 ; Serial
        3600
        1800
        604800
        86400 )

@       IN  NS      maestro.empresa.local.
@       IN  NS      esclavo.empresa.local.
parcial IN  A       192.168.50.3
EOF

sudo named-checkconf
sudo named-checkzone juan-camilo.com "${ZONE_FILE}"
sudo rndc reload || true
sudo systemctl restart named
