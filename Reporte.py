from getSNMP import consultaSNMP
from decimal import Decimal
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus.tables import Table

def reporte(ip):

    descripcion = str(consultaSNMP("CarlaDanielaGonzalezLedesma", ip, '1.3.6.1.2.1.1.1.0'))

    name = descripcion.split()[2]
    if name.lower() != 'linux':
        name = "Windows"

    nombre_documento = "Reporte_"+name.capitalize()+".pdf"

    #  Empezamos para crear el Documento
    doc = SimpleDocTemplate(nombre_documento, pagesize=letter,
                            rightMargin=50, leftMargin=50,
                            topMargin=20, bottomMargin=18)

    Story = []

    estilos = getSampleStyleSheet()
    estilos.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    Story.append(Paragraph("Reporte Generado", estilos["Title"]))
    Story.append(Spacer(1, 4))

    texto = "Sistema Operativo del Agente: "+name.capitalize()
    Story.append(Paragraph(texto, estilos["Heading4"]))

    Story.append(Spacer(1, 8))

    texto = "Descripción del Agente:        "+descripcion.replace("SNMPv2-MIB::sysDescr.0 = ", "")
    Story.append(Paragraph(texto, estilos["BodyText"]))

    Story.append(Spacer(1, 4))

    texto = "OID del Sistema: " + str(consultaSNMP("CarlaDanielaGonzalezLedesma", ip, '1.3.6.1.2.1.1.2.0')).split()[2]
    Story.append(Paragraph(texto, estilos["BodyText"]))

    Story.append(Spacer(1, 4))

    timesys = str(consultaSNMP("CarlaDanielaGonzalezLedesma", ip, '1.3.6.1.2.1.1.3.0')).split()[2]
    seg = Decimal(timesys)/100
    texto = "Agente activo desde hace: " + str(seg) + " segundos"
    Story.append(Paragraph(texto, estilos["BodyText"]))

    Story.append(Spacer(1, 4))
    try:
        texto = "Contacto: " + str(consultaSNMP("CarlaDanielaGonzalezLedesma", ip, '1.3.6.1.2.1.1.4.0')).split()[2]
    except:
        texto = "Contacto: Sin registrar"

    Story.append(Paragraph(texto, estilos["BodyText"]))

    Story.append(Spacer(1, 4))

    texto = "Nombre del Agente: " + str(consultaSNMP("CarlaDanielaGonzalezLedesma", ip, '1.3.6.1.2.1.1.5.0')).split()[2]
    Story.append(Paragraph(texto, estilos["BodyText"]))

    Story.append(Spacer(1, 4))

    texto = "Localización del Agente: " + str(consultaSNMP("CarlaDanielaGonzalezLedesma", ip, '1.3.6.1.2.1.1.6.0')).replace("SNMPv2-MIB::sysLocation.0 = ", "")
    if texto == "Localización del Agente: ":
        texto = texto + "Sin registrar"

    Story.append(Paragraph(texto, estilos["BodyText"]))

    Story.append(Spacer(1, 4))

    texto = "**********************************************************************************************************************************************"
    Story.append(Paragraph(texto, estilos["Heading5"]))

    interfaces = str(consultaSNMP("CarlaDanielaGonzalezLedesma", ip, '1.3.6.1.2.1.2.1.0')).split()[2]
    texto = "Numero de interfaces: " + interfaces
    Story.append(Paragraph(texto, estilos["Heading4"]))

    Story.append(Spacer(1, 4))

    if name == "Windows":
        for num_interfaz in range(int(interfaces)+1):
            if num_interfaz != 0:
                OID = "1.3.6.1.2.1.2.2.1.2."+str(num_interfaz)
                nombre_interfaz_hex = str(consultaSNMP("CarlaDanielaGonzalezLedesma", ip, OID)).split()[2]
                aux_nombre_interfax = nombre_interfaz_hex[2:len(nombre_interfaz_hex)]
                texto = "> Nombre Interfaz " + str(num_interfaz) + ":  " + str(bytearray.fromhex(aux_nombre_interfax).decode('unicode_escape').encode('utf-8'))
                Story.append(Paragraph(texto, estilos["BodyText"]))

                OID_in = "1.3.6.1.2.1.2.2.1.10."+str(num_interfaz)
                trafico_entrada = str(consultaSNMP("CarlaDanielaGonzalezLedesma", ip, OID_in)).split()[2]
                texto = ("Tráfico de entrada: " + trafico_entrada + " Bytes")
                Story.append(Paragraph(texto, estilos["BodyText"]))

                OID_out = "1.3.6.1.2.1.2.2.1.16." + str(num_interfaz)
                trafico_salida = str(consultaSNMP("CarlaDanielaGonzalezLedesma", ip, OID_out)).split()[2]
                texto = ("Tráfico de salida: " + trafico_salida + " Bytes")
                Story.append(Paragraph(texto, estilos["BodyText"]))

                Story.append(Spacer(1, 8))
    else: #Linux
        for num_interfaz in range(int(interfaces)+1):
            if num_interfaz != 0:
                OID = "1.3.6.1.2.1.2.2.1.2."+str(num_interfaz)
                nombre_interfaz = str(consultaSNMP("CarlaDanielaGonzalezLedesma", ip, OID))
                txt_remp = "SNMPv2-SMI::mib-2.2.2.1.2."+str(num_interfaz)+" = "
                nombre_interfaz_limpia = nombre_interfaz.replace(txt_remp,"")
                texto = "> Nombre Interfaz " + str(num_interfaz) + ":  " + nombre_interfaz_limpia
                Story.append(Paragraph(texto, estilos["BodyText"]))

                OID_in = "1.3.6.1.2.1.2.2.1.10."+str(num_interfaz)
                trafico_entrada = str(consultaSNMP("CarlaDanielaGonzalezLedesma", ip, OID_in)).split()[2]
                texto = ("Tráfico de entrada: " + trafico_entrada + " Bytes")
                Story.append(Paragraph(texto, estilos["BodyText"]))

                OID_out = "1.3.6.1.2.1.2.2.1.16." + str(num_interfaz)
                trafico_salida = str(consultaSNMP("CarlaDanielaGonzalezLedesma", ip, OID_out)).split()[2]
                texto = ("Tráfico de salida: " + trafico_salida + " Bytes")
                Story.append(Paragraph(texto, estilos["BodyText"]))

                Story.append(Spacer(1, 8))

    Story.append(Spacer(1, 4))

    texto = "**********************************************************************************************************************************************"
    Story.append(Paragraph(texto, estilos["Heading5"]))

    if name == 'Linux':
        i = 1
        bandera = True
        espacio = []
        disco = []
        while bandera:
            OID_name_disk = "1.3.6.1.4.1.2021.9.1.2." + str(i)
            discos = str(consultaSNMP("CarlaDanielaGonzalezLedesma", ip, OID_name_disk))
            name_disks = discos.replace("SNMPv2-SMI::enterprises.2021.9.1.2."+str(i)+" = ","")

            if(name_disks != "No Such Instance currently exists at this OID"):

                texto = "> Nombre de la Partición " + str(i) + ":  " + name_disks
                disco.append(texto)

                OID_espacio_disk = "1.3.6.1.4.1.2021.9.1.7." + str(i)
                espacio_ = str(consultaSNMP("CarlaDanielaGonzalezLedesma", ip, OID_espacio_disk).split()[2])
                disponible_ = "Espacio Disponible: " + espacio_ + " Bytes"
                espacio.append(disponible_)

            else:
                Title = "Numero de particiones del Disco: " + str(i-1)
                Story.append(Paragraph(Title, estilos["Heading4"]))
                Story.append(Spacer(1, 8))

                for n in range(i-1):
                    Story.append(Paragraph(disco[n], estilos["BodyText"]))
                    Story.append(Paragraph(espacio[n], estilos["BodyText"]))
                    Story.append(Spacer(1, 8))

                bandera = False

            i=i+1
    elif name == "Windows":

        i = 1
        bandera = True
        espacio = []
        disco = []
        while bandera:
            try:
                OID_name_disk = "1.3.6.1.2.1.25.2.3.1.3." + str(i)
                discos = str(consultaSNMP("CarlaDanielaGonzalezLedesma", ip, OID_name_disk))
                name_disks = discos.replace("SNMPv2-SMI::mib-2.25.2.3.1.3." + str(i) + " = ", "")

                texto = "> Nombre de la Partición " + str(i) + ":  " + name_disks
                disco.append(texto)

            except:
                Title = "Dispositivos de Almacenamiento: " + str(i - 1)
                Story.append(Paragraph(Title, estilos["Heading4"]))
                Story.append(Spacer(1, 8))

                for x in range(i-1):
                    OID_espacio_disk = "1.3.6.1.2.1.25.2.3.1.5." + str(x+1)
                    espacio_ = str(consultaSNMP("CarlaDanielaGonzalezLedesma", ip, OID_espacio_disk).split()[2])

                    OID_disk_usado = "1.3.6.1.2.1.25.2.3.1.6." + str(x+1)
                    usado_ = str(consultaSNMP("CarlaDanielaGonzalezLedesma", ip, OID_disk_usado).split()[2])

                    disponible_disk = int(espacio_) - int(usado_)
                    disponible_ = "Espacio disponible: " + str(disponible_disk) + " Bytes"
                    espacio.append(disponible_)

                for n in range(i - 1):
                    Story.append(Paragraph(disco[n], estilos["BodyText"]))
                    Story.append(Paragraph(espacio[n], estilos["BodyText"]))
                    Story.append(Spacer(1, 8))

                bandera = False

            i = i + 1


    texto = "**********************************************************************************************************************************************"
    Story.append(Paragraph(texto, estilos["Heading5"]))

    Story.append(Paragraph("Carga de los CPU", estilos["Heading4"]))

    Story.append(Spacer(1, 4))

    if name == "Linux":

        cargaCPU =str(consultaSNMP("CarlaDanielaGonzalezLedesma", ip, "1.3.6.1.2.1.25.3.3.1.2.196608"))
        texto = "Carga del CPU 1: " + cargaCPU.replace("SNMPv2-SMI::mib-2.25.3.3.1.2.196608 = ","") + " %"
        Story.append(Paragraph(texto, estilos["BodyText"]))

        cargaCPU = str(consultaSNMP("CarlaDanielaGonzalezLedesma", ip, "1.3.6.1.2.1.25.3.3.1.2.196609"))

        texto = "Carga del CPU 2: " + cargaCPU.replace("SNMPv2-SMI::mib-2.25.3.3.1.2.196609 = ","") + " %"
        Story.append(Paragraph(texto, estilos["BodyText"]))

        Story.append(Spacer(1, 4))

        # Memoria Ram

        Total_RAM = int(consultaSNMP("CarlaDanielaGonzalezLedesma", ip, '1.3.6.1.2.1.25.2.3.1.5.1').split()[2])
        used_RAM = int(consultaSNMP("CarlaDanielaGonzalezLedesma", ip, '1.3.6.1.2.1.25.2.3.1.6.1').split()[2])
        porcentaje_Libre = float(((Total_RAM - used_RAM) * 100) / Total_RAM)

        texto = "Memoria RAM disponible: " + "{0:.2f}".format(porcentaje_Libre) + "%"
        Story.append(Paragraph(texto, estilos["Heading4"]))

    else: # Windows
        cargaCPU = str(consultaSNMP("CarlaDanielaGonzalezLedesma", ip, "1.3.6.1.2.1.25.3.3.1.2.3"))
        texto = "Carga del CPU 1: " + cargaCPU.replace("SNMPv2-SMI::mib-2.25.3.3.1.2.3 = ","") + " %"
        Story.append(Paragraph(texto, estilos["BodyText"]))

        Total_RAM = int(consultaSNMP("CarlaDanielaGonzalezLedesma", ip, '1.3.6.1.2.1.25.2.3.1.5.4').split()[2])
        physical_used = int(consultaSNMP("CarlaDanielaGonzalezLedesma", ip, '1.3.6.1.2.1.25.2.3.1.6.4').split()[2])
        porcent_used = float((Total_RAM - physical_used) * 100 / Total_RAM)
        texto = "Memoria RAM disponible: " + "{0:.2f}".format(porcent_used) + "%"
        Story.append(Paragraph(texto, estilos["Heading4"]))

    Story.append(Spacer(1, 4))

    doc.build(Story)

    print("       > Su reporte ha sido generado exitosamente! :D ")
