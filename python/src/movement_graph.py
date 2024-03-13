import matplotlib.pyplot as plt
import csv
import numpy as np
import glob
import os
# Fazer uma func para criar vários .csv a partir do csv principal, separando por nome (row[0])
# Criando um csv para cada nome, salvando o nome do file com o nome do paciente

'''
Ideias para plotar o gráfico:
  * Fazer uma média da pontuação e tempo jogado do paciente em cada sessão, plotar o gráfico mostrando essas medias e plotar tbm os dados de cada sessão
'''
x = []
y = []
z = []
time = []
xAcc = []
yAcc = []
zAcc = []

run = True

def menu():
  print("=" * 20)

  print("[1] - Imprimir um grafico")
  print("[2] - Sair")

  print("=" * 20)

# userTxt = input("Digite o nome: ").lower()



# dir_path = f'.\\{userTxt.lower()}*.csv'
# files_found = glob.glob(dir_path)

# index = 0
# files_dict = {}
# for file in files_found:
#   files_dict[index] = {file}
#   print(f"[{index}] {file}")
#   index += 1
# dict_values = files_dict.values()
# print(files_found)
# os.rename('movement_graph.csv', f'{userTxt.lower()}_{today}-{len(files_found)+1}.csv')
# with open('results.csv', 'a+') as file:
#   reader = csv.reader(file)
#   scoreWriter = csv.writer(file, lineterminator='\n')
#   scoreWriter.writerow(results)

# opc = int(input("Digite o número do arquivo desejado:"))
# tmp = str(files_dict[opc])
# tmp = tmp[5:-2]
# print(tmp)

# with open(f'{str(files_dict[opc])[5:-1]}','r') as csvfile:
with open(f'anormal_2023-08-12-5.csv','r') as csvfile:

    plots = csv.reader(csvfile, delimiter = ',')
      
    for row in plots:
      x.append(float(row[0]))
      y.append(float(row[1])-275) # Mede a inclinação lateral
      # y.append(float(row[1])) # Mede a inclinação lateral
      z.append(float(row[2])-180) # Mede a inclinação frontal
      # z.append(float(row[2])) # Mede a inclinação frontal
      # Os valores subtraídos são para manter o 0 como valor "correto", sem nenhuma inclinação
      # xAcc.append(float(row[3]))
      # yAcc.append(float(row[4]))
      # zAcc.append(float(row[5]))
      time.append(float(row[3]))

# plt.bar(z, y, color = 'g', width = 0.72, label = "Points")
# plt.plot(x)
# plt.plot(y)
# plt.ylabel("Movimento")
# plt.show()
# plt.plot(time,x)
# # plt.ylabel("Movimento")
# plt.show()
# plt.plot(time,y)
# plt.ylabel("Inclinação lateral")
# plt.show()
plt.plot(time,z)
plt.ylabel("Inclinação")
plt.xlabel("Tempo(s)")
plt.show()

'''
plt.plot(yAcc)
plt.ylabel("yAcc")
plt.show()

plt.plot(zAcc)
plt.ylabel("zAcc")
plt.show()

plt.plot(y)
plt.plot(yAcc)
plt.title("Y e YAcc")
plt.show()

plt.plot(y)
plt.plot(zAcc)
plt.title("Y e zAcc")
plt.show()

plt.plot(z)
plt.plot(zAcc)
plt.title("z e zAcc")
plt.show()

plt.plot(z)
plt.plot(yAcc)
plt.title("Z e YAcc")
plt.show()

'''
