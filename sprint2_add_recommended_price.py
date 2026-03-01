"""
СПРИНТ 2: Добавление колонки "Рекомендованная цена"
Берет CSV из Спринта 1 и добавляет колонку на основе правил:

Правила из задания:
1. Если цена конкурента ниже нашей на 10% -> снижаем нашу на 5%
2. Если продаж вчера не было -> снижаем цену на 1 рубль

Входной файл: sprint1_sales_data.csv (из Спринта 1)
Выходной файл: sprint2_data_with_recommendations.csv
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Шаг 1: Загружаем данные из Спринта 1
print("="*50)
print("СПРИНТ 2: Загрузка данных из Спринта 1")
print("="*50)

df = pd.read_csv('sprint1_sales_data.csv')
df['date'] = pd.to_datetime(df['date'])
print(f"Загружено {len(df)} записей")

# Шаг 2: Добавляем цену конкурента (для правила 1)
# В задании нет генерации цены конкурента, поэтому добавим её сейчас
np.random.seed(100)  # Для воспроизводимости
df['competitor_price'] = df.apply(
    lambda row: round(row['price'] * np.random.uniform(0.8, 1.2), 2), 
    axis=1
)

# Шаг 3: Сортируем для корректного поиска предыдущего дня
df = df.sort_values(['product_id', 'date'])

# Шаг 4: Функция применения правил
def calculate_recommended_price(row, df_full):
    """
    Применяет два правила из задания к одной строке
    """
    current_price = row['price']
    competitor_price = row['competitor_price']
    product_id = row['product_id']
    current_date = row['date']
    
    # Находим продажи за предыдущий день для этого товара
    prev_day = current_date - timedelta(days=1)
    prev_sales_row = df_full[
        (df_full['product_id'] == product_id) & 
        (df_full['date'] == prev_day)
    ]
    
    prev_sales = prev_sales_row['sales'].values[0] if not prev_sales_row.empty else None
    
    # Применяем правила
    recommended_price = current_price
    rule_applied = "Нет"
    
    # Правило 1: Если цена конкурента ниже нашей на 10%
    if competitor_price <= current_price * 0.9:
        recommended_price = round(current_price * 0.95, 2)  # снижаем на 5%
        rule_applied = "Правило 1: конкурент дешевле на 10%"
    
    # Правило 2: Если продаж вчера не было
    elif prev_sales == 0:
        recommended_price = round(current_price - 1, 2)  # снижаем на 1 рубль
        rule_applied = "Правило 2: не было продаж вчера"
    
    return recommended_price, rule_applied

# Шаг 5: Применяем правила к каждой строке
print("\nПрименяем правила ценообразования...")

recommended_prices = []
rules_applied = []

for idx, row in df.iterrows():
    rec_price, rule = calculate_recommended_price(row, df)
    recommended_prices.append(rec_price)
    rules_applied.append(rule)

# Шаг 6: Добавляем новые колонки
df['recommended_price'] = recommended_prices
df['rule_applied'] = rules_applied
df['price_change'] = df['recommended_price'] - df['price']
df['price_change_percent'] = round((df['price_change'] / df['price'] * 100), 1)

# Шаг 7: Сохраняем результат
output_file = 'sprint2_data_with_recommendations.csv'
df.to_csv(output_file, index=False)

print("\n" + "="*50)
print("СПРИНТ 2: Результаты")
print("="*50)
print(f"Сохранено в файл: {output_file}")

# Статистика по примененным правилам
rule_counts = df['rule_applied'].value_counts()
print("\nПримененные правила:")
for rule, count in rule_counts.items():
    print(f"  {rule}: {count} раз ({count/len(df)*100:.1f}%)")

# Пример результатов
print("\nПример результатов (первые 10 строк):")
cols = ['date', 'product_id', 'price', 'competitor_price', 'sales', 'recommended_price', 'rule_applied']
print(df[cols].head(10).to_string())

print("\nСтатистика изменений цен:")
print(f"Среднее изменение: {df['price_change'].mean():.2f} руб.")
print(f"Макс снижение: {df['price_change'].min():.2f} руб.")
print(f"Макс повышение: {df['price_change'].max():.2f} руб.")
print(f"Количество изменений: {(df['price_change'] != 0).sum()} из {len(df)}")