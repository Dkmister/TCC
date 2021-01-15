# Commented out IPython magic to ensure Python compatibility.
# %cd TCC

import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

df = pd.read_csv("Quest.csv")
df.head(10)

def get_tempo_atraso(aluno):
  if (aluno['Etapa do Ordenamento '] != 9 and aluno['Semestre de Ingresso'] == 1):
	  tempo_atraso = (2020 - aluno['Ano de Ingresso do Curso']) * 2 - (aluno['Etapa do Ordenamento '])
  elif (aluno['Etapa do Ordenamento '] != 9 and aluno['Semestre de Ingresso'] != 1):
	  tempo_atraso = (2020 - aluno['Ano de Ingresso do Curso']) * 2 - (aluno['Etapa do Ordenamento ']) - 1
  else:
	  tempo_atraso = np.NaN

  return  tempo_atraso

df['Tempo Atraso'] = df.apply(get_tempo_atraso, axis=1)


rep = df.copy()

disc = []
for i in range(len(rep)):
  cont = 0
  for column in rep:
    if "reprovei com D ou FF" in str(rep.iloc[i][column]):
      cont += 1 
  disc.append(cont)


df['Disciplinas Reprovadas'] = disc


#sns.displot(df['Disciplinas Reprovadas'])


pos_rep = []


array_c = []


pos = 0

dic = {}
for i,c in enumerate(rep):
  if "disciplina?" in str(c):
    dic[c] = i
  pos += 1

# pos_rep mostra todas posições que contém o campo perguntando se o aluno já aprovou na disciplina



colunas = {i:coluna for i,coluna in enumerate(rep.columns)}



n_repro = []

for i in range(len(rep)):
  qtd = 0
  for column in dic:
    if "Não aprovei" in str(rep[column].iloc[i]):
      qtd += float(rep.iloc[i][colunas[dic[column] - 1]]) + 1 # soma um porque alguns colocaram 0 (mas e se colocaram 2?)
    elif str(rep[column].iloc[i]) != 'nan':
      if str(rep.iloc[i][colunas[dic[column] - 1]]) != 'nan':
        qtd += float(rep.iloc[i][colunas[dic[column] - 1]])      
      else:
        qtd += 1                                              # considera que reprovou pelo menos 1 vez (mas pode ter sido mais)
  n_repro.append(qtd)

not_rep = 0

for el in n_repro:
  if el == 0:
    not_rep+=1

df['Quantidade de Reprovações'] = n_repro

# bins ajusta o tamanho dos intervalos 
# inverter colunas vs linhas!? 
# count é a quantidade de alunos ou a quantidade de reprovações, por aluno? deixar claro...

def nota_to_number(frase):
  if "com A" in frase:
    return 10
  elif "com B" in frase:
    return 8
  elif "com C" in frase:
    return 6
  elif "reprovei" in frase:
    return 4

# calculo de media de disciplinas
lista_notas = []

flag_rep = 0

for line in range(len(rep)):
  notas = []
  for column in rep:
    if "Cursei" in str(rep.iloc[line][column]):
      notas.append(str(rep.iloc[line][column]))
    elif "Cursei, reprovei com conceito D ou" in str(rep.iloc[line][column]):
      notas.append(str(rep.iloc[line][column]))

  lista_notas.append(notas)




# razão entre aprovações e reprovações, por aluno e global?
aprovacoes = []
for i in range(len(rep)):
  c = 0
  for column in rep:
    if "aprovei" in str(rep.iloc[i][column]):
      c += 1
  aprovacoes.append(c)



df['Aprovações'] = aprovacoes

def TaxaRep(aluno):
  taxa_rep = aluno['Quantidade de Reprovações']/(aluno['Aprovações'] + aluno['Quantidade de Reprovações'])
  return taxa_rep

df['Taxa de Reprovação'] = df.apply(TaxaRep,axis=1)


def TaxaAprov(aluno):
  taxa_ap = aluno['Aprovações']/(aluno['Aprovações'] + aluno['Quantidade de Reprovações'])
  return taxa_ap

df['Taxa de Aprovação'] = df.apply(TaxaAprov,axis=1)

df.to_csv('TesteFinal.csv')
