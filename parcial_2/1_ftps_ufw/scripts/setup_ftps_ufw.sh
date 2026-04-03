#!/usr/bin/env bash
set -euo pipefail

SERVER_IP="${SERVER_IP:-192.168.50.3}"
FTP_USER="${FTP_USER:-telematico}"
FTP_PASS="${FTP_PASS:-Telemat1cos!}"
CERT_DIR="${CERT_DIR:-/vagrant/parcial1_entrega/parcial_2/0_certificados_base}"
CA_CERT="${CA_CERT:-${CERT_DIR}/ca.crt}"
SERVER_CERT="${SERVER_CERT:-${CERT_DIR}/server.crt}"
SERVER_KEY="${SERVER_KEY:-${CERT_DIR}/server.key}"
FTP_ROOT="${FTP_ROOT:-/srv/ftps/${FTP_USER}}"

for required_file in "${CA_CERT}" "${SERVER_CERT}" "${SERVER_KEY}"; do
    if [[ ! -f "${required_file}" ]]; then
        echo "Falta el archivo requerido: ${required_file}" >&2
        exit 1
    fi
done

sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y vsftpd ufw openssl

sudo mkdir -p "$(dirname "${FTP_ROOT}")"

if ! id -u "${FTP_USER}" >/dev/null 2>&1; then
    sudo useradd -m -d "${FTP_ROOT}" -s /bin/bash "${FTP_USER}"
fi

echo "${FTP_USER}:${FTP_PASS}" | sudo chpasswd
sudo mkdir -p "${FTP_ROOT}/upload"
sudo chown -R "${FTP_USER}:${FTP_USER}" "${FTP_ROOT}"
sudo chmod 755 "${FTP_ROOT}"
sudo chmod 775 "${FTP_ROOT}/upload"

sudo install -d -m 755 /etc/ssl/telematicos
sudo install -m 644 "${CA_CERT}" /etc/ssl/telematicos/ca.crt
sudo install -m 644 "${SERVER_CERT}" /etc/ssl/telematicos/server.crt
sudo install -m 600 "${SERVER_KEY}" /etc/ssl/telematicos/server.key

if [[ ! -f /etc/vsftpd.conf.bak.codex ]]; then
    sudo cp /etc/vsftpd.conf /etc/vsftpd.conf.bak.codex
fi

sudo tee /etc/vsftpd.conf >/dev/null <<EOF
listen=YES
listen_ipv6=NO
anonymous_enable=NO
local_enable=YES
write_enable=YES
local_umask=022
dirmessage_enable=YES
use_localtime=YES
xferlog_enable=YES
connect_from_port_20=YES
chroot_local_user=YES
allow_writeable_chroot=YES
pam_service_name=vsftpd
ssl_enable=YES
allow_anon_ssl=NO
force_local_logins_ssl=YES
force_local_data_ssl=YES
ssl_tlsv1=YES
ssl_sslv2=NO
ssl_sslv3=NO
require_ssl_reuse=NO
ssl_ciphers=HIGH
rsa_cert_file=/etc/ssl/telematicos/server.crt
rsa_private_key_file=/etc/ssl/telematicos/server.key
pasv_enable=YES
pasv_min_port=50000
pasv_max_port=50010
pasv_address=${SERVER_IP}
user_sub_token=\$USER
local_root=${FTP_ROOT}
seccomp_sandbox=NO
EOF

sudo ufw --force reset
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw allow 21/tcp
sudo ufw allow 50000:50010/tcp
sudo ufw --force enable

sudo systemctl enable --now vsftpd ufw
sudo systemctl restart vsftpd

echo "== vsftpd status =="
sudo systemctl --no-pager --full status vsftpd | sed -n '1,12p'
echo
echo "== UFW rules =="
sudo ufw status numbered
echo
echo "Usuario FTPS listo: ${FTP_USER}"
echo "Directorio de trabajo: ${FTP_ROOT}"
