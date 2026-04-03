# Guia Rapida de Sustentacion - Parcial 2

Estudiante: Juan Camilo Ballesteros Sierra  
Codigo: 2230721  
Profesor: Oscar Hernan Mondragon Martinez

## 1) Preparacion

1. Abrir tres terminales:
- `CMD 1 (Host)` en `C:\Users\USUARIO\Desktop\UAO 2026 SEMESTRE 1\Servicios telematicos\prueba`
- `CMD 2 (Servidor)` para `vagrant ssh servidor`
- `CMD 3 (Cliente)` para `vagrant ssh cliente`

2. Verificar que los certificados de OpenSSL esten en:
- `/vagrant/parcial1_entrega/parcial_2/0_certificados_base/ca.crt`
- `/vagrant/parcial1_entrega/parcial_2/0_certificados_base/server.crt`
- `/vagrant/parcial1_entrega/parcial_2/0_certificados_base/server.key`

3. Levantar VMs:
```bash
vagrant up
```

## 2) Punto 1 - FTPS protegido con UFW

En `CMD 2 (servidor)` configurar servicio:
```bash
bash /vagrant/parcial1_entrega/parcial_2/1_ftps_ufw/scripts/setup_ftps_ufw.sh
sudo ufw status verbose
```

Demostracion de firewall:
```bash
bash /vagrant/parcial1_entrega/parcial_2/1_ftps_ufw/scripts/toggle_port21_demo.sh close
```

En `CMD 3 (cliente)` probar y mostrar que falla:
```bash
openssl s_client -connect 192.168.50.3:21 -starttls ftp -CAfile /vagrant/parcial1_entrega/parcial_2/0_certificados_base/ca.crt < /dev/null
```

Habilitar otra vez el puerto 21:
```bash
# servidor
bash /vagrant/parcial1_entrega/parcial_2/1_ftps_ufw/scripts/toggle_port21_demo.sh open
```

Validacion completa desde cliente:
```bash
bash /vagrant/parcial1_entrega/parcial_2/1_ftps_ufw/scripts/verify_ftps_ufw.sh
```

Que debes explicar:
- `21/tcp`: canal de control FTP y negociacion TLS explicita.
- `50000:50010/tcp`: rango pasivo para canal de datos FTPS.
- `22/tcp`: administracion SSH y luego SFTP.
- Si UFW no permite el rango pasivo, la conexion puede autenticar pero la transferencia/listado falla.

## 3) Punto 2 - DNS over TLS

En `CMD 3 (cliente)`:
```bash
bash /vagrant/parcial1_entrega/parcial_2/2_dot/scripts/setup_dot_client.sh
bash /vagrant/parcial1_entrega/parcial_2/2_dot/scripts/verify_dot.sh
```

Que debes mostrar:
- El contenido final de `/etc/systemd/resolved.conf`
- `resolvectl status` con `DNSOverTLS=yes`
- Tres consultas exitosas
- Pcap en `853/tcp`
- Pcap en `53` con nombres DNS visibles

Si el profesor exige desactivar DoT de forma explicita para comparar:
```bash
sudo resolvectl dnsovertls eth0 no
dig @8.8.8.8 example.org
sudo resolvectl dnsovertls eth0 yes
```

## 4) Punto 3 - SFTP protegido con UFW

En `CMD 2 (servidor)`:
```bash
bash /vagrant/parcial1_entrega/parcial_2/3_sftp_ufw/scripts/setup_sftp_server.sh
bash /vagrant/parcial1_entrega/parcial_2/3_sftp_ufw/scripts/toggle_port22_demo.sh close
```

En `CMD 3 (cliente)` demostrar que falla con 22 bloqueado:
```bash
sshpass -p 'Telemat1cos!' sftp -o PreferredAuthentications=password -o PubkeyAuthentication=no -o StrictHostKeyChecking=no telematico@192.168.50.3
```

Volver a abrir `22/tcp`:
```bash
# servidor
bash /vagrant/parcial1_entrega/parcial_2/3_sftp_ufw/scripts/toggle_port22_demo.sh open
```

Validacion completa:
```bash
bash /vagrant/parcial1_entrega/parcial_2/3_sftp_ufw/scripts/verify_sftp_ufw.sh
```

## 5) Tabla comparativa FTPS vs SFTP

| Criterio | FTPS | SFTP |
| --- | --- | --- |
| Protocolo base | FTP + TLS | SSH |
| Numero de puertos | 21 + rango pasivo de datos | 22 unico |
| Certificado requerido | Certificado X.509 del servidor y CA de confianza | No requiere PKI X.509; usa claves/certificados SSH |
| Modo de cifrado | TLS para control y datos | Cifrado completo dentro del canal SSH |
| Compatibilidad con firewalls | Mas delicado por canal de datos pasivo | Mejor en entornos restrictivos |
| Facilidad de configuracion | Mas pasos y sincronizacion con firewall | Mas simple y directa |

Conclusion sugerida:

SFTP es mas adecuado para un entorno con firewall estricto porque concentra autenticacion y transferencia en un unico puerto, reduce reglas de red y baja la probabilidad de errores en NAT o modo pasivo. FTPS es valido, pero operativamente exige mas coordinacion entre servicio y firewall.

## 6) Archivos a mostrar si preguntan

- `parcial_2/0_enunciado/2026-01 Segundo_Parcial_ServiciosTelematicos.pdf`
- `parcial_2/README_PARCIAL2.md`
- `parcial_2/4_comandos_sustentacion/comandos_rapidos.txt`
- Los `.pcapng` generados en `/tmp` dentro del cliente
- Las capturas que guardes en `parcial_2/5_evidencia_visual/`
