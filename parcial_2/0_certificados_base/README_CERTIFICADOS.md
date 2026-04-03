Coloca aqui los certificados OpenSSL generados en clase.

Nombres esperados por los scripts:

- `ca.crt`: certificado de la CA que firma al servidor.
- `server.crt`: certificado publico del servidor FTPS.
- `server.key`: clave privada del servidor FTPS.

Si tus archivos tienen otros nombres, puedes:

1. Renombrarlos a esos nombres.
2. O exportar variables antes de ejecutar el script del servidor:

```bash
export CERT_DIR=/vagrant/parcial1_entrega/parcial_2/0_certificados_base
export CA_CERT=/vagrant/parcial1_entrega/parcial_2/0_certificados_base/mi-ca.crt
export SERVER_CERT=/vagrant/parcial1_entrega/parcial_2/0_certificados_base/mi-servidor.crt
export SERVER_KEY=/vagrant/parcial1_entrega/parcial_2/0_certificados_base/mi-servidor.key
```

Si el certificado del servidor fue emitido para un nombre DNS y no para una IP, agrega ese nombre a `/etc/hosts` en el cliente o usa ese hostname en FileZilla para que la validacion sea coherente durante la sustentacion.

## Generacion rapida de respaldo

Si no encuentras los certificados de clase, genera un juego funcional asi:

```bash
bash /vagrant/parcial1_entrega/parcial_2/0_certificados_base/generate_lab_certs.sh /vagrant/parcial1_entrega/parcial_2/0_certificados_base
```
