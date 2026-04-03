#!/usr/bin/env bash
set -euo pipefail

SFTP_USER="${SFTP_USER:-telematico}"
SFTP_PASS="${SFTP_PASS:-Telemat1cos!}"
SFTP_ROOT="${SFTP_ROOT:-/srv/ftps/${SFTP_USER}}"

sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y openssh-server ufw

sudo mkdir -p "$(dirname "${SFTP_ROOT}")"

if ! id -u "${SFTP_USER}" >/dev/null 2>&1; then
    sudo useradd -m -d "${SFTP_ROOT}" -s /bin/bash "${SFTP_USER}"
fi

echo "${SFTP_USER}:${SFTP_PASS}" | sudo chpasswd
sudo mkdir -p "${SFTP_ROOT}/upload"
sudo chown -R "${SFTP_USER}:${SFTP_USER}" "${SFTP_ROOT}"

if [[ ! -f /etc/ssh/sshd_config.bak.codex ]]; then
    sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak.codex
fi

sudo sed -i 's/^#\?PasswordAuthentication .*/PasswordAuthentication yes/' /etc/ssh/sshd_config
sudo sed -i 's|^Subsystem[[:space:]]\+sftp.*|Subsystem sftp internal-sftp|' /etc/ssh/sshd_config

sudo sshd -t
sudo ufw allow 22/tcp
sudo systemctl enable --now ssh ufw
sudo systemctl restart ssh

echo "== ssh status =="
sudo systemctl --no-pager --full status ssh | sed -n '1,12p'
echo
echo "== UFW rules =="
sudo ufw status numbered
