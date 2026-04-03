# Tabla Comparativa FTPS vs SFTP

| Criterio | FTPS | SFTP |
| --- | --- | --- |
| Protocolo base | FTP + TLS | SSH |
| Numero de puertos utilizados | 21 para control y rango pasivo para datos | 22 unico |
| Tipo de certificado requerido | Certificado X.509 del servidor y CA de confianza | Claves o certificados SSH |
| Modo de cifrado | TLS explicito para canal de control y datos | Todo el trafico va dentro del canal SSH |
| Compatibilidad con firewalls | Mas delicada por el canal de datos pasivo | Mejor en entornos con reglas estrictas |
| Facilidad de configuracion | Requiere alinear `vsftpd`, TLS y rango pasivo en UFW | Mas simple porque todo va por SSH |

## Conclusión

En un entorno con firewall estricto, SFTP suele ser la opcion mas conveniente porque usa un solo puerto, reduce reglas en UFW y evita problemas de NAT o de puertos pasivos. FTPS sigue siendo seguro, pero operativamente es mas sensible a errores de configuracion en red y firewall.
