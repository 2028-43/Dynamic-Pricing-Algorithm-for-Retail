"""
СПРИНТ 3: Сравнение текущих и оптимальных цен для всех товаров
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Загружаем данные
df = pd.read_csv('sprint1_sales_data.csv')
coeff_df = pd.read_csv('models/coefficients.csv')

# Рассчитываем оптимальные цены
comparison = []

for _, row in coeff_df.iterrows():
    pid = row['product_id']
    A = row['A']
    B = row['B']
    
    # Оптимальная цена
    optimal_price = A / (2 * B) if B > 0 else 0
    
    # Текущая средняя цена
    current_avg = df[df['product_id'] == pid]['price'].mean()
    
    # Текущая средняя выручка
    current_revenue = current_avg * (A - B * current_avg)
    
    # Оптимальная выручка
    optimal_revenue = optimal_price * (A - B * optimal_price)
    
    comparison.append({
        'Товар': pid,
        'Текущая цена': round(current_avg, 2),
        'Оптимальная цена': round(optimal_price, 2),
        'Изменение цены': round(optimal_price - current_avg, 2),
        'Изменение %': round((optimal_price - current_avg) / current_avg * 100, 1),
        'Текущая выручка': round(current_revenue, 2),
        'Оптимальная выручка': round(optimal_revenue, 2),
        'Рост выручки %': round((optimal_revenue - current_revenue) / current_revenue * 100, 1)
    })

# Создаем DataFrame
comp_df = pd.DataFrame(comparison)

print("="*70)
print("СРАВНЕНИЕ ТЕКУЩИХ И ОПТИМАЛЬНЫХ ЦЕН")
print("="*70)
print(comp_df.to_string(index=False))

# Визуализация
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# График 1: Сравнение цен
x = np.arange(len(comp_df))
width = 0.35

ax1.bar(x - width/2, comp_df['Текущая цена'], width, label='Текущая цена', color='blue', alpha=0.7)
ax1.bar(x + width/2, comp_df['Оптимальная цена'], width, label='Оптимальная цена', color='green', alpha=0.7)
ax1.set_xlabel('Товар')
ax1.set_ylabel('Цена (руб.)')
ax1.set_title('Сравнение текущей и оптимальной цены')
ax1.set_xticks(x)
ax1.set_xticklabels([f'Товар {p}' for p in comp_df['Товар']])
ax1.legend()
ax1.grid(True, alpha=0.3)

# График 2: Рост выручки
colors = ['green' if x > 0 else 'red' for x in comp_df['Рост выручки %']]
ax2.bar(comp_df['Товар'], comp_df['Рост выручки %'], color=colors, alpha=0.7)
ax2.set_xlabel('Товар')
ax2.set_ylabel('Рост выручки (%)')
ax2.set_title('Потенциальный рост выручки при оптимальной цене')
ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Сохраняем сравнение
comp_df.to_csv('models/price_comparison.csv', index=False)
print("\nРезультаты сохранены в models/price_comparison.csv")