import warnings
import serial
import serial.tools.list_ports
import csv
import game as g

class Arduino:

    def __init__(self):
        self.baudRate = 115200
        self.isArduino = False
        self.port = None


    # Check for available arduino device
    def check_ports(self):
        
        # Lists all connected ports
        self.ports = list(serial.tools.list_ports.comports())


        # Look for the first arduino available
        for p in self.ports:
            # print(p)
            if 'CH340' in p.description:
                self.portName = str(p)
                print("Arduino Nano Encontrado!")
                self.tmp = self.portName.split(" ")
                self.port = self.tmp[0]
                self.isArduino = True
                break;
            elif 'Arduino' in p.description:
                print("Arduino encontrado!")
                self.portName = str(p)
                self.tmp = self.portName.split(" ")
                self.port = self.tmp[0]
                self.isArduino = True
                break;
    
    def connect(self):
        self.ser = serial.Serial(self.port, self.baudRate)
        print(f'Conexão: {self.port}, {self.baudRate}')
    

    def get_data(self):

        if self.isArduino:
            self.line = self.ser.readline().decode().strip()
            self.data = list(self.line.split(","))
            print(self.data)

            # if self.line != "teste":
            #     self.x = self.data[0][7:10]
            #     self.y = self.data[1][7:10]
            #     self.z = self.data[2][7:10]
            #     print(self.x, self.y, self.z)
            #     self.data = [self.x, self.y, self.z]
            # self.data = (f"{self.data[0]}")
            # with open('movement_graph.csv', 'a+') as file:
            #     reader = csv.reader(file)
            #     dataWriter = csv.writer(file, lineterminator='\n')
            #     dataWriter.writerow(self.data)
        
        else:
            print("Arduino não encontrado!")