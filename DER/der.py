"""Analisis de datos Proyecto Final
Energias renovables"""

#Librerias necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#cargar archivo CSV
file_path = "data/complete_renewable_energy_dataset.csv"
df=pd.read_csv(file_path)
#print(df.head())

#Exploración inicial
#print("Dimensiones del dataset: ", df.shape)

#tipo
#print("Tipos de datos categoricos o numericos", df.dtypes)

#datos nulos
#print("Datos nulos por columna:\n", df.isnull().sum())

#Eliminar duplicados
#print("Cantidad de filas duplicadas: ", df.duplicated().sum())
df = df.drop_duplicates()
#print("Dimensiones del dataset: ", df.shape)

# Limpieza de datos
num_cols = df.select_dtypes(include=['int64', 'float64']).columns
df_clean = df.copy()
for col in num_cols:
   if df_clean[col].isnull().sum()>0:
       df_clean[col] = df_clean[col].fillna(df_clean[col].mean())
#print("Dimensiones del dataset limpio: ", df_clean.shape)

#identificacion de outiliers
#calcular los cuartiles Q1(25%) y Q3(75%) de las columnas numéricas
q1 = df_clean[num_cols].quantile(0.25)
q3 = df_clean[num_cols].quantile(0.75)
#calcular el rango intercuartil (IQR)
irq = q3 - q1
#identificar outliers (mascara booleana=oum)
oum = (df_clean[num_cols] < (q1 - 1.5 * irq)) | (df_clean[num_cols] > (q3 + 1.5 * irq))
#contar valores outliers
outliers_count = oum.sum()
#print("Cantidad de outliers:\n", outliers_count)

#datasets sin outliers
df_coul = df_clean.copy()
for col in num_cols:
    lower = q1[col] - 1.5 * irq[col]
    upper = q3[col] + 1.5 * irq[col]
    df_coul = df_coul[(df_coul[col] >= lower) & (df_coul[col] <= upper)]
#print("outliers del dataset limpio",df_coul.shape)

print(df_coul['EnergyTypeSource'].unique())

#sumar biomasa y biogas
df=df_coul.copy()
df.loc[df['EnergyTypeSource'] == 'Biomass', 'EnergyTypeSource'] +=df.loc[df['EnergyTypeSource']=='Biogas','EnergyTypeSource'].sum()