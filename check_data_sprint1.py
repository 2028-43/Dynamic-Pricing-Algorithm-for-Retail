"""
СПРИНТ 1: Проверка данных и построение графиков
"""

import pandas as pd
import matplotlib.pyplot as plt

# Загружаем данные
df = pd.read_csv('sprint1_sales_data.csv')
df['date'] = pd.to_datetime(df['date'])

# Создаем графики для демонстрации
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('СПРИНТ 1: Анализ сгенерированных данных', fontsize=16)

# График 1: Зависимость продаж от цены (все товары)
axes[0, 0].scatter(df['price'], df['sales'], alpha=0.3, c='blue')
axes[0, 0].set_xlabel('Цена')
axes[0, 0].set_ylabel('Продажи')
axes[0, 0].set_title('Зависимость продаж от цены')
axes[0, 0].grid(True, alpha=0.3)

# График 2: Динамика для товара 1
product1 = df[df['product_id'] == 1].sort_values('date')
axes[0, 1].plot(product1['date'], product1['price'], label='Цена', color='red', linewidth=1)
axes[0, 1].plot(product1['date'], product1['sales'], label='Продажи', color='blue', linewidth=1)
axes[0, 1].set_xlabel('Дата')
axes[0, 1].set_ylabel('Значение')
axes[0, 1].set_title('Динамика для Товара 1')
axes[0, 1].legend()
axes[0, 1].tick_params(axis='x', rotation=45)

# График 3: Распределение продаж
axes[1, 0].hist(df['sales'], bins=20, color='green', alpha=0.7)
axes[1, 0].set_xlabel('Продажи')
axes[1, 0].set_ylabel('Частота')
axes[1, 0].set_title('Распределение продаж')

# График 4: Средние продажи по товарам
avg_sales = df.groupby('product_id')['sales'].mean()
avg_sales.plot(kind='bar', ax=axes[1, 1], color='orange')
axes[1, 1].set_xlabel('Товар')
axes[1, 1].set_ylabel('Средние продажи')
axes[1, 1].set_title('Средние продажи по товарам')

plt.tight_layout()
plt.show()

# Проверка эластичности
print("\n" + "="*50)
print("ПРОВЕРКА ЭЛАСТИЧНОСТИ")
print("="*50)
correlation = df['price'].corr(df['sales'])
print(f"Корреляция между ценой и продажами: {correlation:.3f}")

if correlation < 0:
    print("Данные правдоподобны: при росте цены продажи падают")
else:
    print("Ошибка: зависимость не соответствует эластичности")

print("\nПример данных для товара 1 (первые 5 дней):")
print(product1[['date', 'price', 'sales']].head())