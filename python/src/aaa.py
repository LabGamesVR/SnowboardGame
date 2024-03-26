import matplotlib.pyplot as plt
import csv
import numpy as np
# Fazer uma func para criar vários .csv a partir do csv principal, separando por nome (row[0])
# Criando um csv para cada nome, salvando o nome do file com o nome do paciente

'''
Ideias para plotar o gráfico:
  * Fazer uma média da pontuação e tempo jogado do paciente em cada sessão, plotar o gráfico mostrando essas medias e plotar tbm os dados de cada sessão
'''
x = []
y = []
xAcc = []
yAcc = []
currTime = []
  
with open('./results/teste43_2023-10-18-1.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter = ',')
      
    for row in plots:
      x.append(float(row[0])) # Mede a inclinação lateral
      y.append(float(row[1])) # Mede a inclinação frontal
      xAcc.append(float(row[2])*10) # Aceleração X
      yAcc.append(float(row[3])*10) # Aceleração Y
      currTime.append(float(row[5])) # Tempo total

      


# plt.bar(z, y, color = 'g', width = 0.72, label = "Points")
# plt.plot(x)
# plt.plot(y)
# plt.ylabel("Movimento")
# plt.show()
plt.plot(currTime, x)
plt.ylabel("Inclinação lateral")
plt.show()

plt.plot(currTime, y)
plt.ylabel("Inclinação frontal")
plt.show()

plt.plot(currTime, xAcc)
plt.ylabel("Aceleração de X")
plt.show()

plt.plot(currTime, yAcc)
plt.ylabel("Aceleração de Y")
plt.show()

# plt.plot(z)
# plt.ylabel("Inclinação frontal")
# plt.show()

plt.plot(currTime, x)
plt.plot(currTime, y)
plt.title("Junção dos graficos de inclinação")
plt.legend(['xAng','yAng'])
plt.show()


plt.plot(currTime, x)
plt.plot(currTime, yAcc)
plt.title("Junção dos graficos de inclinação X e acc Y")
plt.legend(['xAng','yAcc'])
plt.show()


plt.plot(currTime, y)
plt.plot(currTime, xAcc)
plt.legend(['yAng','xAcc'])
plt.title("Junção dos graficos de inclinação Y e acc X")
plt.show()