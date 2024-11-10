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

print(df[['q1_ms', 'q2_ms', 'q3_ms']].head(10))

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
