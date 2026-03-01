"""
СПРИНТ 1: Генерация синтетических данных
Задание: 100 дней, 5 товаров
Формула: Продажи = 100 - 2 * Цена + Случайный_Шум
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Параметры
np.random.seed(42)
products = [1, 2, 3, 4, 5]
start_date = datetime(2024, 1, 1)
days = 100

# Генерация данных
data = []

for product_id in products:
    # Базовая цена для каждого товара (разная)
    base_price = 50 + product_id * 10  # 60, 70, 80, 90, 100
    
    for day in range(days):
        current_date = start_date + timedelta(days=day)
        
        # Цена с небольшими колебаниями
        price = base_price + np.random.normal(0, 5)
        price = max(round(price, 2), 10)
        
        # Формула из задания: Продажи = 100 - 2 * Цена + Случайный_Шум
        sales = 100 - 2 * price + np.random.normal(0, 5)
        sales = max(int(round(sales)), 0)
        
        data.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'product_id': product_id,
            'price': price,
            'sales': sales
        })

# Создаем DataFrame и сохраняем
df = pd.DataFrame(data)
df.to_csv('sprint1_sales_data.csv', index=False)

print("="*50)
print("СПРИНТ 1: Генерация данных завершена")
print("="*50)
print(f"Файл: sprint1_sales_data.csv")
print(f"Записей: {len(df)}")
print(f"Товаров: {len(df['product_id'].unique())}")
print(f"Дней: {df['date'].nunique()}")
print(f"Период: {df['date'].min()} - {df['date'].max()}")
print("\nПервые 5 строк:")
print(df.head())
print("\nСтатистика:")
print(f"Средняя цена: {df['price'].mean():.2f}")
print(f"Средние продажи: {df['sales'].mean():.2f}")
print(f"Мин продажи: {df['sales'].min()}")
print(f"Макс продажи: {df['sales'].max()}")