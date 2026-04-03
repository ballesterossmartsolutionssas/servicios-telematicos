# PARCIAL 2 - SERVICIOS TELEMATICOS

Entrega organizada para reproducir los tres puntos del segundo parcial sobre la topologia Vagrant ya usada en clase:

- `cliente`: `192.168.50.2`
- `servidor`: `192.168.50.3`

## Antes de ejecutar

1. Copiar los certificados OpenSSL generados en clase dentro de `0_certificados_base/` con estos nombres:
- `ca.crt`
- `server.crt`
- `server.key`

Si no aparecen los de clase, puedes generar unos funcionales de laboratorio con:
```bash
vagrant ssh servidor -c "bash /vagrant/parcial1_entrega/parcial_2/0_certificados_base/generate_lab_certs.sh /vagrant/parcial1_entrega/parcial_2/0_certificados_base"
```

2. Levantar las VMs:
```bash
vagrant up
```

3. Ejecutar los scripts desde la VM correspondiente usando la carpeta compartida `/vagrant`.

## Estructura

- `0_enunciado/`: PDF original del parcial 2.
- `0_certificados_base/`: lugar para la CA y el certificado del servidor FTPS.
- `1_ftps_ufw/`: scripts para FTPS con `vsftpd`, UFW y captura TLS.
- `2_dot/`: scripts para DNS over TLS con `systemd-resolved`.
- `3_sftp_ufw/`: scripts para SFTP con OpenSSH y UFW.
- `4_comandos_sustentacion/`: comandos cortos para mostrar el parcial en vivo.
- `5_evidencia_visual/`: carpeta reservada para capturas Wireshark y pantallazos.

## Orden recomendado

1. En `servidor`, correr `1_ftps_ufw/scripts/setup_ftps_ufw.sh`
2. En `cliente`, correr `1_ftps_ufw/scripts/verify_ftps_ufw.sh`
3. En `cliente`, correr `2_dot/scripts/setup_dot_client.sh`
4. En `cliente`, correr `2_dot/scripts/verify_dot.sh`
5. En `servidor`, correr `3_sftp_ufw/scripts/setup_sftp_server.sh`
6. En `cliente`, correr `3_sftp_ufw/scripts/verify_sftp_ufw.sh`

## Nota practica

Durante esta revision el `cliente` si responde bien, pero el `servidor` quedo en un estado inconsistente: la VM enciende, aunque no responde por red. Por eso esta entrega quedo preparada de forma reproducible desde cero para que la apliques apenas el servidor vuelva a levantar normal.
