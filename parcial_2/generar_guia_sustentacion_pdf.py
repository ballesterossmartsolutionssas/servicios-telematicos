#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parent
OUT_PDF = ROOT / "GUIA_SUSTENTACION_PARCIAL2_COMPLETA.pdf"


def add_page_number(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawRightString(19.2 * cm, 0.8 * cm, f"Pagina {doc.page}")
    canvas.restoreState()


def add_command(story, text: str, mono) -> None:
    safe = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br/>")
    )
    story.append(Paragraph(safe, mono))
    story.append(Spacer(1, 0.12 * cm))


def add_bullets(story, lines: list[str], bullet) -> None:
    for line in lines:
        safe = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        story.append(Paragraph(f"- {safe}", bullet))
    story.append(Spacer(1, 0.12 * cm))


def main() -> None:
    doc = SimpleDocTemplate(
        str(OUT_PDF),
        pagesize=A4,
        leftMargin=1.6 * cm,
        rightMargin=1.6 * cm,
        topMargin=1.4 * cm,
        bottomMargin=1.3 * cm,
        title="Guia Completa de Sustentacion Parcial 2",
        author="Juan Camilo Ballesteros Sierra",
    )

    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "TitleX",
        parent=styles["Title"],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0b2e59"),
        spaceAfter=8,
    )
    subtitle = ParagraphStyle(
        "SubtitleX",
        parent=styles["Normal"],
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#444444"),
        spaceAfter=4,
    )
    h1 = ParagraphStyle(
        "H1",
        parent=styles["Heading1"],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#0b2e59"),
        spaceBefore=8,
        spaceAfter=6,
    )
    h2 = ParagraphStyle(
        "H2",
        parent=styles["Heading2"],
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#184c8c"),
        spaceBefore=6,
        spaceAfter=4,
    )
    p = ParagraphStyle(
        "P",
        parent=styles["Normal"],
        fontSize=9.5,
        leading=12.5,
        spaceAfter=3,
    )
    bullet = ParagraphStyle(
        "BulletX",
        parent=p,
        leftIndent=0.25 * cm,
    )
    mono = ParagraphStyle(
        "Mono",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=8,
        leading=9.8,
        textColor=colors.HexColor("#202020"),
        backColor=colors.HexColor("#f3f6fa"),
        borderPadding=4,
        borderColor=colors.HexColor("#d9e2f0"),
        borderWidth=0.4,
        borderRadius=2,
    )

    story = []
    story.append(Paragraph("Guia Completa de Sustentacion - Parcial 2", title))
    story.append(Paragraph("Servicios Telematicos", subtitle))
    story.append(Paragraph("Estudiante: Juan Camilo Ballesteros Sierra", subtitle))
    story.append(Paragraph("Codigo: 2230721", subtitle))
    story.append(Paragraph("Topologia usada: cliente 192.168.50.2 | servidor 192.168.50.3", subtitle))
    story.append(Paragraph("Branch listo: codex/parcial-2-ready", subtitle))
    story.append(Spacer(1, 0.18 * cm))
    story.append(
        Paragraph(
            "Esta guia esta hecha para hablar durante la sustentacion. Incluye el orden recomendado, "
            "los comandos que debes ejecutar y frases cortas para explicar que esta pasando.",
            p,
        )
    )

    story.append(Paragraph("1. Preparacion Antes De Entrar", h1))
    add_bullets(
        story,
        [
            "Abre tres terminales: Host, Servidor y Cliente.",
            "Deja abierta la carpeta del repo en parcial_2 y la guia markdown por si te preguntan rutas.",
            "Si vas a mostrar GUI, abre VirtualBox, Wireshark y FileZilla antes de entrar a Webex.",
            "El servidor y el cliente ya quedaron preparados; en principio solo necesitas prender las VMs.",
        ],
        bullet,
    )
    story.append(Paragraph("Host:", h2))
    add_command(story, r"cd C:\Users\USUARIO\Desktop\UAO 2026 SEMESTRE 1\Servicios telematicos\prueba", mono)
    add_command(story, "vagrant up", mono)
    add_command(story, "vagrant status", mono)
    story.append(Paragraph("Servidor:", h2))
    add_command(story, "vagrant ssh servidor", mono)
    story.append(Paragraph("Cliente:", h2))
    add_command(story, "vagrant ssh cliente", mono)

    story.append(Paragraph("2. Orden Recomendado De Exposicion", h1))
    add_bullets(
        story,
        [
            "Empieza por FTPS + UFW porque muestra seguridad de red, TLS y transferencia real.",
            "Luego DNS over TLS porque es corto y deja claro el puerto 853 frente al 53.",
            "Termina con SFTP porque es la comparacion perfecta con FTPS y te da la conclusion final.",
            "Si el profesor te interrumpe con conceptos, responde corto y vuelve al flujo.",
        ],
        bullet,
    )

    story.append(Paragraph("3. Punto 1 - FTPS Protegido Con UFW", h1))
    story.append(
        Paragraph(
            "Idea que debes decir: FTPS usa FTP con TLS explicito. El firewall permite solo 21 para control, "
            "50000 al 50010 para datos pasivos y 22 para administracion. Si cierras 21, la sesion ni siquiera inicia.",
            p,
        )
    )
    story.append(Paragraph("Configuracion inicial en servidor:", h2))
    add_command(story, "bash /vagrant/parcial1_entrega/parcial_2/1_ftps_ufw/scripts/setup_ftps_ufw.sh", mono)
    add_command(story, "sudo ufw status verbose", mono)
    story.append(Paragraph("Que explicar mientras sale:", h2))
    add_bullets(
        story,
        [
            "La politica por defecto de UFW es deny incoming.",
            "21/tcp es el canal de control FTP.",
            "50000:50010/tcp es el rango pasivo para el canal de datos.",
            "22/tcp queda para administracion SSH y para el punto de SFTP.",
        ],
        bullet,
    )
    story.append(Paragraph("Demostracion de bloqueo del puerto 21:", h2))
    add_command(story, "bash /vagrant/parcial1_entrega/parcial_2/1_ftps_ufw/scripts/toggle_port21_demo.sh close", mono)
    add_command(
        story,
        "openssl s_client -connect 192.168.50.3:21 -starttls ftp -CAfile /vagrant/parcial1_entrega/parcial_2/0_certificados_base/ca.crt < /dev/null",
        mono,
    )
    story.append(
        Paragraph(
            "Frase sugerida: con UFW activo y sin la regla 21/tcp, el cliente no puede negociar el canal de control, "
            "por eso la conexion falla antes de autenticarse.",
            p,
        )
    )
    story.append(Paragraph("Reabrir 21 y validar FTPS completo:", h2))
    add_command(story, "bash /vagrant/parcial1_entrega/parcial_2/1_ftps_ufw/scripts/toggle_port21_demo.sh open", mono)
    add_command(story, "bash /vagrant/parcial1_entrega/parcial_2/1_ftps_ufw/scripts/verify_ftps_ufw.sh", mono)
    story.append(Paragraph("Que mostrar en la salida:", h2))
    add_bullets(
        story,
        [
            "En OpenSSL debe salir Verify return code: 0.",
            "En lftp deben verse ls, put y get.",
            "Los sha256 del archivo original y descargado deben ser iguales.",
            "La captura FTPS no muestra el contenido del archivo en texto plano.",
        ],
        bullet,
    )
    story.append(Paragraph("Pregunta conceptual tipica:", h2))
    story.append(
        Paragraph(
            "Por que deben coincidir UFW y vsftpd en puertos pasivos? Porque el servidor anuncia ese rango al cliente; "
            "si el firewall no lo permite, autenticas pero no puedes listar ni transferir.",
            p,
        )
    )

    story.append(PageBreak())
    story.append(Paragraph("4. Punto 2 - DNS Over TLS", h1))
    story.append(
        Paragraph(
            "Idea que debes decir: DNS over TLS cifra las consultas DNS usando TLS sobre el puerto 853. "
            "Asi se evita que cualquiera en la red vea en texto plano los dominios consultados.",
            p,
        )
    )
    story.append(Paragraph("Configuracion y verificacion en cliente:", h2))
    add_command(story, "bash /vagrant/parcial1_entrega/parcial_2/2_dot/scripts/setup_dot_client.sh", mono)
    add_command(story, "bash /vagrant/parcial1_entrega/parcial_2/2_dot/scripts/verify_dot.sh", mono)
    story.append(Paragraph("Que debes ir diciendo:", h2))
    add_bullets(
        story,
        [
            "En resolved.conf quedaron DNS y FallbackDNS con servidores que soportan DoT.",
            "resolvectl status debe mostrar DNSOverTLS=yes.",
            "Las consultas de openai.com, uao.edu.co y github.com deben resolver bien.",
            "El pcap del puerto 853 demuestra transporte cifrado.",
            "El pcap del puerto 53 deja ver consultas DNS sin cifrar.",
        ],
        bullet,
    )
    story.append(Paragraph("Comando corto por si piden comparar desactivando DoT:", h2))
    add_command(story, "sudo resolvectl dnsovertls eth0 no", mono)
    add_command(story, "dig @8.8.8.8 example.org", mono)
    add_command(story, "sudo resolvectl dnsovertls eth0 yes", mono)
    story.append(Paragraph("Pregunta conceptual tipica:", h2))
    story.append(
        Paragraph(
            "Que se expone en DNS sin cifrar? El nombre consultado, el tipo de consulta y parte del contexto de navegacion. "
            "Con DoT eso ya no viaja visible para un observador de red.",
            p,
        )
    )

    story.append(Paragraph("5. Punto 3 - SFTP Protegido Con UFW", h1))
    story.append(
        Paragraph(
            "Idea que debes decir: SFTP no es FTP con TLS. Es un subsistema de SSH, por eso toda la comunicacion viaja "
            "cifrada dentro del puerto 22 y no necesita rango pasivo.",
            p,
        )
    )
    story.append(Paragraph("Configuracion en servidor:", h2))
    add_command(story, "bash /vagrant/parcial1_entrega/parcial_2/3_sftp_ufw/scripts/setup_sftp_server.sh", mono)
    add_command(story, "bash /vagrant/parcial1_entrega/parcial_2/3_sftp_ufw/scripts/toggle_port22_demo.sh close", mono)
    story.append(Paragraph("Demostracion de bloqueo:", h2))
    add_command(
        story,
        "sshpass -p 'Telemat1cos!' sftp -o PreferredAuthentications=password -o PubkeyAuthentication=no -o StrictHostKeyChecking=no telematico@192.168.50.3",
        mono,
    )
    story.append(
        Paragraph(
            "Frase sugerida: al cerrar 22/tcp en UFW, SFTP falla porque todo depende del canal SSH. "
            "A diferencia de FTPS, aqui un solo puerto controla todo.",
            p,
        )
    )
    story.append(Paragraph("Reabrir 22 y validar SFTP completo:", h2))
    add_command(story, "bash /vagrant/parcial1_entrega/parcial_2/3_sftp_ufw/scripts/toggle_port22_demo.sh open", mono)
    add_command(story, "bash /vagrant/parcial1_entrega/parcial_2/3_sftp_ufw/scripts/verify_sftp_ufw.sh", mono)
    story.append(Paragraph("Que mostrar en la salida:", h2))
    add_bullets(
        story,
        [
            "La sesion sftp debe listar el directorio remoto.",
            "Debe verse put y get del archivo de prueba.",
            "Los hashes deben coincidir.",
            "La captura de puerto 22 no muestra el contenido en texto plano.",
        ],
        bullet,
    )

    story.append(PageBreak())
    story.append(Paragraph("6. Comparacion FTPS Vs SFTP", h1))
    story.append(Paragraph("Respuesta corta lista para decir:", h2))
    add_bullets(
        story,
        [
            "FTPS se basa en FTP + TLS; SFTP se basa en SSH.",
            "FTPS usa 21 mas un rango pasivo; SFTP usa solo 22.",
            "FTPS necesita certificado X.509 y confianza en CA; SFTP usa mecanismos de SSH.",
            "Con firewalls estrictos, SFTP es mas facil de operar.",
            "FTPS es seguro, pero exige mejor coordinacion entre servicio y firewall.",
        ],
        bullet,
    )
    story.append(
        Paragraph(
            "Conclusion recomendada: en un entorno con reglas estrictas de firewall, SFTP suele ser mas adecuado "
            "porque reduce superficie de red y complejidad operativa. FTPS sigue siendo seguro, pero es mas delicado "
            "por el uso de multiples puertos.",
            p,
        )
    )

    story.append(Paragraph("7. Comandos Flash De Emergencia", h1))
    add_command(story, "vagrant status", mono)
    add_command(story, "vagrant reload servidor", mono)
    add_command(story, "vagrant reload cliente", mono)
    add_command(story, "sudo ufw status verbose", mono)
    add_command(story, "resolvectl status | sed -n '1,80p'", mono)
    story.append(
        Paragraph(
            "Si algo raro pasa el martes, lo primero es verificar que ambas VMs esten arriba y luego reintentar "
            "con reload de la maquina puntual.",
            p,
        )
    )

    story.append(Paragraph("8. Archivos Que Debes Tener Abiertos", h1))
    add_bullets(
        story,
        [
            "parcial_2/GUIA_SUSTENTACION_PARCIAL2.md",
            "parcial_2/4_comandos_sustentacion/comandos_rapidos.txt",
            "parcial_2/1_ftps_ufw/evidencia_ftps_funcional.txt",
            "parcial_2/2_dot/evidencia_dot.txt",
            "parcial_2/3_sftp_ufw/evidencia_sftp_funcional.txt",
            "parcial_2/5_evidencia_visual/06_dot_853.pcapng",
            "parcial_2/5_evidencia_visual/07_dns_53.pcapng",
            "parcial_2/5_evidencia_visual/08_ftps_tls.pcapng",
            "parcial_2/5_evidencia_visual/09_sftp_22.pcapng",
        ],
        bullet,
    )

    story.append(Paragraph("9. Cierre De 20 Segundos", h1))
    story.append(
        Paragraph(
            "Con esta practica demostre tres cosas: FTPS con TLS y UFW, DNS over TLS con systemd-resolved y SFTP sobre "
            "OpenSSH. En los tres casos valide funcionamiento real, control de firewall y evidencia de trafico cifrado. "
            "Ademas compare FTPS contra SFTP y concluí que SFTP es mas practico en entornos con restricciones estrictas.",
            p,
        )
    )

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"PDF generado: {OUT_PDF}")


if __name__ == "__main__":
    main()
