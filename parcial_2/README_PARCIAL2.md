# PARCIAL 2 - SERVICIOS TELEMATICOS

Entrega organizada para reproducir los tres puntos del segundo parcial sobre la topologia Vagrant usada en clase.

## Topologia
- `cliente`: `192.168.50.2`
- `servidor`: `192.168.50.3`

## Requisitos previos
1. Levantar las VMs:
```bash
vagrant up
```

2. Verificar estado:
```bash
vagrant status
```

3. Ejecutar los scripts desde la VM correspondiente usando la carpeta compartida `/vagrant`.

## Certificados FTPS
La carpeta `0_certificados_base/` contiene la CA y los certificados base usados para FTPS.

Si se requiere regenerarlos en laboratorio:
```bash
vagrant ssh servidor -c "bash /vagrant/parcial1_entrega/parcial_2/0_certificados_base/generate_lab_certs.sh /vagrant/parcial1_entrega/parcial_2/0_certificados_base"
```

## Estructura
- `0_enunciado/`: PDF original del parcial 2.
- `0_certificados_base/`: certificados base para FTPS.
- `1_ftps_ufw/`: scripts y evidencia de FTPS con `vsftpd` y UFW.
- `2_dot/`: scripts y evidencia de DNS over TLS con `systemd-resolved`.
- `3_sftp_ufw/`: scripts y evidencia de SFTP con OpenSSH y UFW.
- `4_comandos_sustentacion/`: comandos cortos de apoyo.
- `5_evidencia_visual/`: capturas Wireshark validadas.

## Orden sugerido de revision
1. `1_ftps_ufw/scripts/setup_ftps_ufw.sh`
2. `1_ftps_ufw/scripts/verify_ftps_ufw.sh`
3. `2_dot/scripts/setup_dot_client.sh`
4. `2_dot/scripts/verify_dot.sh`
5. `3_sftp_ufw/scripts/setup_sftp_server.sh`
6. `3_sftp_ufw/scripts/verify_sftp_ufw.sh`

## Evidencias principales
- FTPS:
  - `1_ftps_ufw/evidencia_ftps_funcional.txt`
  - `1_ftps_ufw/evidencia_ftps_bloqueo_puerto21.txt`
  - `5_evidencia_visual/11_ftps_tls_ok.pcapng`
- DNS over TLS:
  - `2_dot/evidencia_dot.txt`
  - `5_evidencia_visual/06_dot_853.pcapng`
  - `5_evidencia_visual/07_dns_53.pcapng`
- SFTP:
  - `3_sftp_ufw/evidencia_sftp_funcional.txt`
  - `3_sftp_ufw/evidencia_sftp_bloqueo_puerto22.txt`
  - `5_evidencia_visual/10_sftp_22_ok.pcapng`

## Comparacion solicitada
La tabla comparativa FTPS vs SFTP exigida por el enunciado esta en:
`3_sftp_ufw/TABLA_COMPARATIVA_FTPS_VS_SFTP.md`
