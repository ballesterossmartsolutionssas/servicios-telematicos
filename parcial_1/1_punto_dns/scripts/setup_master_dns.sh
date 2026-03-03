#!/usr/bin/env bash
set -euo pipefail

MASTER_IP="192.168.50.3"
SLAVE_IP="192.168.50.2"
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
    type master;
    file "/etc/bind/db.empresa.local";
    notify yes;
    allow-transfer { key "axfr-key"; };
};

zone "50.168.192.in-addr.arpa" {
    type master;
    file "/etc/bind/db.192.168.50";
    notify yes;
    allow-transfer { key "axfr-key"; };
};
EOF

sudo tee /etc/bind/db.empresa.local >/dev/null <<EOF
\$TTL 86400
@   IN  SOA maestro.empresa.local. admin.empresa.local. (
        2026030301 ; Serial
        3600       ; Refresh
        1800       ; Retry
        604800     ; Expire
        86400 )    ; Minimum TTL

@                   IN  NS      maestro.empresa.local.
@                   IN  NS      esclavo.empresa.local.

maestro             IN  A       ${MASTER_IP}
maestro             IN  AAAA    fd00:50::3
esclavo             IN  A       ${SLAVE_IP}
esclavo             IN  AAAA    fd00:50::2
www                 IN  CNAME   maestro
app                 IN  CNAME   esclavo
EOF

sudo tee /etc/bind/db.192.168.50 >/dev/null <<EOF
\$TTL 86400
@   IN  SOA maestro.empresa.local. admin.empresa.local. (
        2026030301 ; Serial
        3600
        1800
        604800
        86400 )

@       IN  NS      maestro.empresa.local.
@       IN  NS      esclavo.empresa.local.

3       IN  PTR     maestro.empresa.local.
2       IN  PTR     esclavo.empresa.local.
EOF

sudo named-checkconf
sudo named-checkzone empresa.local /etc/bind/db.empresa.local
sudo named-checkzone 50.168.192.in-addr.arpa /etc/bind/db.192.168.50
sudo systemctl enable --now named
sudo systemctl restart named
sudo systemctl --no-pager --full status named | sed -n '1,8p'
