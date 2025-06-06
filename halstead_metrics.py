import matplotlib.pyplot as plt

# Метрики Django
django_metrics = {
    "n1": 43,
    "n2": 305,
    "N1": 1537,
    "N2": 921,
    "Vocabulary": 348,
    "Length": 2458,
    "Volume": 20752.755112796174,
    "Difficulty": 64.92295081967214,
    "Effort": 1347330.0995607655,
    "Quality Level": 0.01540287351968285
}

# Метрики BlockSet
blockset_metrics = {
    "n1": 25,
    "n2": 57,
    "N1": 243,
    "N2": 148,
    "Vocabulary": 82,
    "Length": 391,
    "Volume": 2485.80,
    "Difficulty": 32.46,
    "Effort": 80679.57,
    "Quality Level": 0.03
}

# Список метрик
metrics = list(django_metrics.keys())

# Создаем подграфики: 5 строк x 2 столбца
fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(12, 18))
axes = axes.flatten()

# Функция для подписи значений
def add_value_labels(ax, bars):
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f'{height:.2f}' if height < 1000 else f'{height:.0f}',
            ha='center', va='bottom',
            fontsize=9
        )

# Отрисовка графиков
for i, metric in enumerate(metrics):
    ax = axes[i]
    values = [django_metrics[metric], blockset_metrics[metric]]
    bars = ax.bar(["Django", "BlockSet"], values, color=["steelblue", "orange"])
    ax.set_title(metric)
    ax.set_ylabel("Значение")
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    add_value_labels(ax, bars)

# Удаление лишних осей
for j in range(len(metrics), len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.show()
