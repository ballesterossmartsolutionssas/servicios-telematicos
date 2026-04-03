#!/usr/bin/env bash
set -euo pipefail

ACTION="${1:-status}"

case "${ACTION}" in
    close)
        printf 'y\n' | sudo ufw delete allow 21/tcp || true
        ;;
    open)
        sudo ufw allow 21/tcp
        ;;
    status)
        ;;
    *)
        echo "Uso: $0 {close|open|status}" >&2
        exit 1
        ;;
esac

sudo ufw status numbered
