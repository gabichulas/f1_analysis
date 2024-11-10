import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.options.display.width = 0

df = pd.read_csv(r"data\qualifying.csv")

# Parsear los tiempos de vueltas, que vienen como strings
def time_to_milliseconds(time_str):
    if pd.isna(time_str):
        return None
    try:
        minutes, seconds = time_str.split(':')
        seconds, milliseconds = seconds.split('.')
        total_milliseconds = (int(minutes) * 60 * 1000) + (int(seconds) * 1000) + int(milliseconds)
        return total_milliseconds
    except ValueError:
        return None

df['q1_ms'] = df['q1'].apply(time_to_milliseconds)
df['q2_ms'] = df['q2'].apply(time_to_milliseconds)
df['q3_ms'] = df['q3'].apply(time_to_milliseconds)

#print(df[['q1_ms', 'q2_ms', 'q3_ms']].head(10))

# Eliminar valores atípicos en q1_ms ya que hay un dato muy grande
Q1 = df['q1_ms'].quantile(0.25)
Q3 = df['q1_ms'].quantile(0.75)
RI = Q3 - Q1
filter = (df['q1_ms'] >= (Q1 - 1.5 * RI)) & (df['q1_ms'] <= (Q3 + 1.5 * RI))
df_filtered = df.loc[filter]

# Hacer un boxplot de los tiempos de vuelta en milisegundos
plt.figure(figsize=(10,6))
sns.boxplot(data=df_filtered[['q1_ms', 'q2_ms', 'q3_ms']])
plt.xlabel('Sesión de Clasificación')
plt.ylabel('Tiempo en Milisegundos')
plt.savefig(r'images\laptimes_boxplot.png')
plt.close()

# A modo de experimentación, veremos los tiempos de vuelta del piloto con driverId = 4, o sea, Fernando Alonso
df_alonso = df[df['driverId'] == 4]

#print(df_hamilton.describe())

# Importamos races, ya que necesitamos filtrar por alguna carrera para que los tiempos sean consistentes, ya que no todos los circuitos son iguales.
# En este caso, buscaremos los id de las carreras que se corrieron en Silverstone.
df_races = pd.read_csv(r"data\races.csv")
df_races_filtered = df_races[df_races['name'] == "British Grand Prix"]['raceId'].values


# A partir de este análisis, descubrimos que las carreras que se corrieron en Silverston fueron:
df_alonso_silverstone = df_alonso[df_alonso['raceId'].isin(df_races_filtered)]
print(df_alonso_silverstone)



plt.figure(figsize=(10,6))
sns.scatterplot(data=df_alonso_silverstone, x='position', y='q1_ms')
sns.regplot(data=df_alonso_silverstone, x='position', y='q1_ms', scatter=False, color='red')
plt.ylabel('Tiempo de Q1 en milisegundos')
plt.xlabel('Posición final en la clasificación')
plt.title("Relación entre Q1 y posición para Alonso en Silverstone")
plt.savefig(r'images\Q1_position_alonso_silverstone.png')
plt.close()