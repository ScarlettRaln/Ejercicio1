from ping import ping
from Reporte import reporte

ip_ = input("Ingrese la dirección IP:")
mascara = input("Ingrese mascara de subred:")

new_param = ""
ip_split = ip_.split(".")

if mascara == "255.255.255.255":
    print("\n Número de nodos en la red: 1")

elif mascara == "255.255.255.0":
    print("\n Número de Nodos en la Lista: 256")
    for oct in range(3):  # 0 1 2
        new_param = new_param + ip_split[oct] # 10.0.0
        if oct != 2:
            new_param = new_param + "."   #10.0.

    ping(new_param, 1)
    new_param = ""

elif mascara == "255.255.0.0": #ip original = 10.0.0.13
    print("\n Número de nodos en la Red: ",256*256)
    for oct in range(2):  # 0 1
        new_param = new_param + ip_split[oct] #10.0
        if oct != 1:
            new_param = new_param + "." #10.

    ping(new_param, 2)
    new_param = ""

elif mascara == "255.0.0.0":
    print("\nNúmero de Nodos en la Lista: ",256*256*256)
    ping(ip_split[0], 3)

print("\n    >>> Generando Reporte :3")
reporte(ip_)