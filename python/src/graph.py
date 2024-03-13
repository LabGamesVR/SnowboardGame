import matplotlib.pyplot as plt
import csv
# Fazer uma func para criar vários .csv a partir do csv principal, separando por nome (row[0])
# Criando um csv para cada nome, salvando o nome do file com o nome do paciente

'''
Ideias para plotar o gráfico:
  * Fazer uma média da pontuação e tempo jogado do paciente em cada sessão, plotar o gráfico mostrando essas medias e plotar tbm os dados de cada sessão
'''

x = []
y = []
  
with open('teste_2023-04-24-1.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter = ',')
      
    for row in plots:
        x.append(row[0])
        y.append(float(row[1]))
  
plt.bar(x, y, color = 'g', width = 0.72, label = "Points")
plt.xlabel('Name')
plt.ylabel('Points')
plt.title('Scoreboard')
plt.legend()
plt.show()