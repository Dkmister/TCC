import csv
import pandas as pd

df = pd.read_csv('Quest.csv')

series = []

for i in range(len(df['Semestre de Ingresso'])):
	if df['Etapa do Ordenamento '].iloc[i] != 9 and df['Semestre de Ingresso'].iloc[i] == 1:
		x = (2020 - df['Ano de Ingresso do Curso'].iloc[i]) * 2 - (df['Etapa do Ordenamento '].iloc[i])
		print(x)
		series.append(int(x))
	elif df['Etapa do Ordenamento '].iloc[i] != 9 and df['Semestre de Ingresso'].iloc[i] != 1:
		x = (2020 - df['Ano de Ingresso do Curso'].iloc[i]) * 2 - (df['Etapa do Ordenamento '].iloc[i]) - 1
		print(x)
		series.append(int(x))
	else:
		series.append(" ")

df['Tempo Atraso'] =  pd.Series(series)

