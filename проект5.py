import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Завантаження даних
df = pd.read_csv('Space_Corrected.csv')

# Перевірка наявності пропусків
print("Пропущені значення в кожному стовпчику:")
print(df.isnull().sum())

# Заповнення пропусків (можливий варіант - заповнити пропуски порожніми рядками)
df.fillna('', inplace=True)

# Додати стовпець для ранкового часу (наприклад, з 6:00 до 12:00)
df['LaunchTime'] = pd.to_datetime(df['Datum'], errors='coerce').dt.hour
df['MorningLaunch'] = df['LaunchTime'].between(6, 12)

# Визначення приватних компаній
private_companies = ['SpaceX', 'Rocket Lab', 'Virgin Orbit', 'Blue Origin', 'OneSpace']

# Додати стовпець для позначення приватних компаній
df['PrivateCompany'] = df['Company Name'].apply(lambda x: x in private_companies)

# Аналіз запусків
# Всі запуски приватних та державних компаній
total_private_launches = df[df['PrivateCompany']]
total_public_launches = df[~df['PrivateCompany']]

# Успішні запуски
private_success = total_private_launches[total_private_launches['Status Mission'] == 'Success']
public_success = total_public_launches[total_public_launches['Status Mission'] == 'Success']

# Всі ранкові запуски
private_morning_launches = total_private_launches[total_private_launches['MorningLaunch']]
public_morning_launches = total_public_launches[total_public_launches['MorningLaunch']]

# Успішні ранкові запуски
private_morning_success = private_success[private_success['MorningLaunch']]
public_morning_success = public_success[public_success['MorningLaunch']]

# Результати
print("Загальна кількість запусків приватних компаній:", len(total_private_launches))
print("Загальна кількість запусків державних компаній:", len(total_public_launches))
print("Успішні запуски приватних компаній:", len(private_success))
print("Успішні запуски державних компаній:", len(public_success))
print("Ранкові запуски приватних компаній:", len(private_morning_launches))
print("Ранкові запуски державних компаній:", len(public_morning_launches))
print("Успішні ранкові запуски приватних компаній:", len(private_morning_success))
print("Успішні ранкові запуски державних компаній:", len(public_morning_success))

# Візуалізація
labels = ['Всі запуски', 'Успішні запуски', 'Ранкові запуски', 'Ранкові успішні запуски']
private_counts = [len(total_private_launches), len(private_success), len(private_morning_launches), len(private_morning_success)]
public_counts = [len(total_public_launches), len(public_success), len(public_morning_launches), len(public_morning_success)]

x = np.arange(len(labels)) 
width = 0.35  

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

# Перша діаграма
rects1 = ax1.bar(x - width/2, private_counts, width, label='Приватні')
rects2 = ax1.bar(x + width/2, public_counts, width, label='Державні')

ax1.set_ylabel('Кількість')
ax1.set_title('Порівняння запусків приватних та державних компаній')
ax1.set_xticks(x)
ax1.set_xticklabels(labels)
ax1.legend()

def autolabel(rects, ax):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(rects1, ax1)
autolabel(rects2, ax1)

# Друге вікно для тексту
fig.text(0.5, 0.4, 'Загальна успішність запусків державних компаній:89%', 
         ha='center', va='center', fontsize=12)

fig.text(0.5, 0.3, 'Загальна успішність запусків приватних компаній:92%', 
         ha='center', va='center', fontsize=12)

fig.text(0.5, 0.2, 'Успішні ранкові запуски державних компаній:89%', 
         ha='center', va='center', fontsize=12)

fig.text(0.5, 0.1, 'Успішні ранкові запуски приватних компаній:99%', 
         ha='center', va='center', fontsize=12)

fig.tight_layout()
plt.show()
