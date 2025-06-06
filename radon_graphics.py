"""
Рисует график с результатами
"""
import matplotlib.pyplot as plt


# Данные из анализа
labels = ['LOC', 'LLOC', 'SLOC']
values = [527, 282, 334]
# values = [129, 113, 68]

# Построение графика
plt.figure(figsize=(10, 6))
bars = plt.bar(labels, values, color=['#4CAF50', '#2196F3', '#FF9800', '#9C27B0'])

# Подписи значений
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 2, int(yval), ha='center', fontsize=10)

# Настройки графика
plt.title('Обзор структуры кода')
plt.ylabel('Количество строк')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
