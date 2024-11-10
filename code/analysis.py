import matplotlib.pyplot as plt
import seaborn as sns
from functions import *

pd.options.display.width = 0

df = pd.read_csv(r"data\qualifying.csv")

# Parsear los tiempos de vueltas, que vienen como strings

df['q1_ms'] = df['q1'].apply(time_to_milliseconds)
df['q2_ms'] = df['q2'].apply(time_to_milliseconds)
df['q3_ms'] = df['q3'].apply(time_to_milliseconds)

# Eliminar valores atípicos en q1_ms para evitar valores excesivamente grandes (previamente revisados)
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

# Importamos races, ya que necesitamos filtrar por alguna carrera para que los tiempos sean consistentes, ya que no todos los circuitos son iguales.
# En este caso, buscaremos los id de las carreras que se corrieron en Silverstone.
df_races = pd.read_csv(r"data\races.csv")
df_races_filtered = df_races[df_races['name'] == "British Grand Prix"]['raceId'].values


# A partir de este análisis, descubrimos que las carreras que se corrieron en Silverston fueron:
df_alonso_silverstone = df_alonso[df_alonso['raceId'].isin(df_races_filtered)]

plt.figure(figsize=(10,6))
sns.scatterplot(data=df_alonso_silverstone, x='position', y='q1_ms')
sns.regplot(data=df_alonso_silverstone, x='position', y='q1_ms', scatter=False, color='red')
plt.ylabel('Tiempo de Q1 en milisegundos')
plt.xlabel('Posición final en la clasificación')
plt.title("Relación entre Q1 y posición para Alonso en Silverstone")
plt.savefig(r'images\Q1_position_alonso_silverstone.png')
plt.close()

# Ahora, veremos como se distribuyen las pole positions según las escuderías:
# Filtrar las pole positions
pole_positions = df[df['position'] == 1]

# Contar las pole positions por escudería
pole_positions_by_team = pole_positions['constructorId'].value_counts()

# Crear un DataFrame para facilitar la visualización
df_pole_positions_by_team = pd.DataFrame({
    'constructorId': pole_positions_by_team.index,
    'pole_positions': pole_positions_by_team.values
})

# Cargar los datos de los constructores para obtener los nombres de las escuderías
df_constructors = pd.read_csv(r"data/constructors.csv")

# Unir los datos de pole positions con los nombres de las escuderías
df_pole_positions_by_team = df_pole_positions_by_team.merge(df_constructors, left_on='constructorId', right_on='constructorId')

# Crear el histograma
plt.figure(figsize=(12, 8))
sns.barplot(x='name', y='pole_positions', data=df_pole_positions_by_team, palette='pastel')
plt.xlabel('Escudería')
plt.ylabel('Número de Pole Positions')
plt.title('Histograma de Pole Positions por Escudería')
plt.xticks(rotation=90)
plt.savefig(r'images\pole_positions_by_team.png')
plt.close()

# Como una actividad similar, compararemos las medias de las posiciones obtenidas por cada escudería
df_mean = df.groupby('constructorId')['position'].mean().reset_index()
df_mean = df_mean.merge(df_constructors, left_on='constructorId', right_on='constructorId')

plt.figure(figsize=(16,14))
sns.barplot(x='name', y='position', data=df_mean.sort_values('position'), palette='pastel')
plt.xlabel('Escuderías')
plt.ylabel('Media de Posiciones')
plt.xticks(rotation=90)
plt.savefig(r'images/mean_positions_by_team.png')
plt.close()

# Ahora, veremos la proporción de pole positions convertidas en victorias por pilotos
df_results = pd.read_csv(r"data\results.csv")
df_drivers = pd.read_csv(r"data\drivers.csv")

df_race_winners_with_pole = df_results[(df_results['position'] == "1") & (df_results['grid'] == 1)]['driverId'].value_counts().reset_index()
df_race_winners_with_pole.columns = ['driverId', 'wins_from_pole']
df_pole_count = df_results[df_results['grid'] == 1]['driverId'].value_counts().reset_index()
df_pole_count.columns = ['driverId', 'pole_positions']

df_pole_to_victory = df_pole_count.merge(df_race_winners_with_pole, on='driverId', how='left').fillna(0)

# Calcular la proporción de pole positions convertidas en victorias
df_pole_to_victory['proportion'] = df_pole_to_victory['wins_from_pole'] / df_pole_to_victory['pole_positions']

df_pole_to_victory = df_pole_to_victory.merge(df_drivers[['driverId', 'surname']], on='driverId')

# Crear un gráfico de barras para visualizar las pole positions y victorias por piloto
plt.figure(figsize=(16, 13))
sns.barplot(x='surname', y='pole_positions', data=df_pole_to_victory.head(35), color='blue', label='Pole Positions')
sns.barplot(x='surname', y='wins_from_pole', data=df_pole_to_victory.head(35), color='red', label='Victorias desde Pole', alpha=0.6)
plt.xlabel('Piloto')
plt.ylabel('Número de Pole Positions y Victorias desde Pole')
plt.title('Comparativa entre Pole Positions y Victorias desde Pole por Piloto')
plt.xticks(rotation=90)
plt.legend()
plt.savefig(r'images/pole_positions_vs_victories_by_driver.png')
plt.close()

plt.figure(figsize=(16, 13))
sns.barplot(x='surname', y='proportion', data=df_pole_to_victory.head(35).sort_values('proportion', ascending=False), palette='pastel')
plt.xlabel('Piloto')
plt.ylabel('Proporción entre Pole Positions y Victorias')
plt.title('Proporción de Poles entre Victorias por Piloto')
plt.xticks(rotation=90)
plt.savefig(r'images/pole_positions_vs_victories_by_driver_proportion.png')
plt.close()