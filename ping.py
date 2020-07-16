import os

def ping(ip,opc):
    hostname = ""

    if opc == 1:

        f = open('Discovery.txt', 'a')  # Abrimos el archivo

        for num in range(20): #Vamos a variar los valores del último octeto for(num=0; num<256)
            hostname = ip + "." + str(num)  #concatenamos num
            response = os.system("ping -c 1 " + hostname) #mandamos la solicitud

            if response == 0:
                f.write(str(hostname))
                f.write("\n")
        f.close()

    elif opc == 2: #10.0

        f = open('Discovery.txt', 'a')  # Abrimos el archivo

        for num in range(256):  # Vamos a variar los valores del tercer octeto
            hostname = ip + "." + str(num)  # concatenamos num
            #10.0.0
            for num2 in range(256):
                aux = hostname + "." + str(num2)  # concatenamos num2
                #print(aux) #10.0.0.1
                aux = ""
                response = os.system("ping -c 1 " + hostname)  # mandamos la solicitud

                if response == 0:
                    f.write(str(hostname))
                    f.write("\n")
        f.close()

    elif opc == 3: #10
        f = open('Discovery.txt', 'a')  # Abrimos el archivo

        for num in range(256):  # Vamos a variar los valores del segundo octeto
            hostname = ip + "." + str(num)  # concatenamos num
            #10.0
            for num2 in range(256):  # Vamos a variar los valores del tercer octeto
                aux = hostname + "." + str(num2)  # concatenamos num2
                # 10.0.0
                for num3 in range(256):  # Vamos a variar los valores del ultimo octeto
                    aux2 = aux + "." + str(num3)  # concatenamos num3
                    # 10.0.0.0
                    #print(aux2)
                    response = os.system("ping -c 1 " + hostname)  # mandamos la solicitud
                    if response == 0:
                        f.write(str(hostname))
                        f.write("\n")

                    aux2 = ""
                aux = ""
        f.close()

