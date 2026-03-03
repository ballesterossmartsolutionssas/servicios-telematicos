#!/usr/bin/env bash
set -euo pipefail

MASTER_IP="192.168.50.3"
TSIG_SECRET="/A39HXgLEpVmfTRAlsn+FhjExOzpZjbj/r/eanLR9PU="

sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y bind9 bind9utils dnsutils

sudo tee /etc/bind/named.conf.options >/dev/null <<'EOF'
options {
    directory "/var/cache/bind";

    recursion no;
    allow-recursion { none; };
    allow-query { any; };
    allow-transfer { none; };

    dnssec-validation auto;
    listen-on-v6 { any; };
};
EOF

sudo tee /etc/bind/named.conf.local >/dev/null <<EOF
key "axfr-key" {
    algorithm hmac-sha256;
    secret "${TSIG_SECRET}";
};

zone "empresa.local" {
    type slave;
    file "/var/cache/bind/db.empresa.local";
    masters { ${MASTER_IP} key "axfr-key"; };
};

zone "50.168.192.in-addr.arpa" {
    type slave;
    file "/var/cache/bind/db.192.168.50";
    masters { ${MASTER_IP} key "axfr-key"; };
};
EOF

sudo named-checkconf
sudo systemctl enable --now named
sudo systemctl restart named
sudo systemctl --no-pager --full status named | sed -n '1,8p'

# Wait for first transfer from master.
for _ in {1..30}; do
    if sudo test -s /var/cache/bind/db.empresa.local && sudo test -s /var/cache/bind/db.192.168.50; then
        echo "Zone transfer complete on slave."
        exit 0
    fi
    sleep 2
done

echo "ERROR: Zone files not transferred to slave within timeout." >&2
exit 1
