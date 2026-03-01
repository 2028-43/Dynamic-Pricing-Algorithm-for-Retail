"""
СПРИНТ 3: Обучение модели для каждого товара
Находит коэффициенты A и B в формуле Спрос = A - B * Цена
Для максимизации выручки Цена * (A - B * Цена)
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import pickle
import os

# Создаем папку для моделей
os.makedirs('models', exist_ok=True)

# Загружаем данные из Спринта 1
print("="*50)
print("СПРИНТ 3: Обучение моделей")
print("="*50)

df = pd.read_csv('sprint1_sales_data.csv')
print(f"Загружено {len(df)} записей")

# Для каждого товара обучаем отдельную модель
products = df['product_id'].unique()
models = {}
coefficients = {}

for product_id in products:
    # Данные для конкретного товара
    product_df = df[df['product_id'] == product_id].copy()
    
    # Подготовка данных для регрессии
    X = product_df[['price']].values  # Цена
    y = product_df['sales'].values     # Спрос
    
    # Линейная регрессия: sales = A - B * price
    # В sklearn: y = coef_ * X + intercept_
    # Значит: B = -coef_, A = intercept_
    model = LinearRegression()
    model.fit(X, y)
    
    # Извлекаем коэффициенты
    B = -model.coef_[0]  # Чтобы было A - B*price
    A = model.intercept_
    
    # Сохраняем
    models[product_id] = model
    coefficients[product_id] = {'A': A, 'B': B}
    
    # Оптимальная цена: A/(2B)
    optimal_price = A / (2 * B) if B > 0 else 0
    
    print(f"\nТовар {product_id}:")
    print(f"  Спрос = {A:.2f} - {B:.2f} * Цена")
    print(f"  R² = {model.score(X, y):.3f}")
    print(f"  Оптимальная цена: {optimal_price:.2f} руб.")
    
    # Сохраняем модель
    with open(f'models/product_{product_id}_model.pkl', 'wb') as f:
        pickle.dump(model, f)

# Сохраняем коэффициенты в CSV
coeff_df = pd.DataFrame([
    {'product_id': pid, 'A': coeff['A'], 'B': coeff['B']}
    for pid, coeff in coefficients.items()
])
coeff_df.to_csv('models/coefficients.csv', index=False)

print("\n" + "="*50)
print("Модели сохранены в папке /models")
print("="*50)