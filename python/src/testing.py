import warnings
import serial
import serial.tools.list_ports
import csv


# print(dir(serial))

isArduino = False
baud = 9600

ports = list(serial.tools.list_ports.comports())

# Procura o primeiro arduino disponível na lista de dispositivos
for p in ports:
    print(p)
    if 'CH340' in p.description:
        portName = str(p)
        print("Arduino Nano encontrado!")
        tmp = portName.split(" ")
        port = tmp[0]
        isArduino = True
        break;
    elif 'USB' in p.description:
        print("Arduino encontrado!")
        portName = str(p)
        tmp = portName.split(" ")
        port = tmp[0]
        isArduino = True
        break;


if isArduino: # Se encontrar o arduino
    print(f'Conexão: {port}:{baud}')
    ser = serial.Serial(port, baud)
    # ser = serial.Serial('COM6', 9600)
    # f = open('dataFile.txt','a')
    print("aaaaaa")
    while 1 :
        line = ser.readline().decode().strip()
        print(line)
        data = list(line.split(","))
        # print(data)
        if line != "Setup":
            x = data[0]
            y = data[1]
            z = data[2]
            # print(x, y, z)
            data = [x, y, z]
        # data = (f"{data[0]}")
            with open('movement_graph.csv', 'a+') as file:
                reader = csv.reader(file)
                dataWriter = csv.writer(file, lineterminator='\n')
                dataWriter.writerow(data)
        # f.write(line)
        # f.close()
        # f = open('dataFile.txt','a')


else: # Se não encontrar
    print("Arduino não conectado!")




    