#!/usr/bin/env bash
set -euo pipefail

SLAVE_LOCAL="/etc/bind/named.conf.local"

if ! sudo grep -q 'zone "juan-camilo.com"' "${SLAVE_LOCAL}"; then
cat <<'EOF' | sudo tee -a "${SLAVE_LOCAL}" >/dev/null

zone "juan-camilo.com" {
    type slave;
    file "/var/cache/bind/db.juan-camilo.com";
    masters { 192.168.50.3 key "axfr-key"; };
};
EOF
fi

sudo named-checkconf
sudo rndc reload || true
sudo systemctl restart named

for _ in {1..30}; do
    if sudo test -s /var/cache/bind/db.juan-camilo.com; then
        echo "juan-camilo.com transfer complete."
        exit 0
    fi
    sleep 2
done

echo "ERROR: juan-camilo.com not transferred to slave in time." >&2
exit 1
