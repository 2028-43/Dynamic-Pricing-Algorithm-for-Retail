"""
СПРИНТ 2: Демонстрация результатов
Показывает, какие цены изменились и по каким правилам
"""

import pandas as pd
import matplotlib.pyplot as plt

# Загружаем результаты
df = pd.read_csv('sprint2_data_with_recommendations.csv')
df['date'] = pd.to_datetime(df['date'])

print("="*60)
print("СПРИНТ 2: ДЕМОНСТРАЦИЯ РАБОТЫ АЛГОРИТМА")
print("="*60)

# Показываем примеры для каждого правила
print("\nПРИМЕРЫ ПРИМЕНЕНИЯ ПРАВИЛ:")

# Пример правила 1
rule1_examples = df[df['rule_applied'].str.contains('Правило 1', na=False)].head(3)
if not rule1_examples.empty:
    print("\n Правило 1 (конкурент дешевле на 10%):")
    for _, row in rule1_examples.iterrows():
        print(f"  Товар {row['product_id']} | {row['date'].strftime('%Y-%m-%d')}")
        print(f"    Наша цена: {row['price']} руб. | Конкурент: {row['competitor_price']} руб.")
        print(f"    Рекомендация: {row['recommended_price']} руб. (снижение на {abs(row['price_change_percent']):.1f}%)")

# Пример правила 2
rule2_examples = df[df['rule_applied'].str.contains('Правило 2', na=False)].head(3)
if not rule2_examples.empty:
    print("\n🔹 Правило 2 (не было продаж вчера):")
    for _, row in rule2_examples.iterrows():
        print(f"  Товар {row['product_id']} | {row['date'].strftime('%Y-%m-%d')}")
        print(f"    Продажи: {row['sales']} | Цена: {row['price']} руб.")
        print(f"    Рекомендация: {row['recommended_price']} руб. (снижение на 1 рубль)")

# Визуализация
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# График 1: Сравнение цен для товара 1
product1 = df[df['product_id'] == 1].sort_values('date').head(30)
axes[0].plot(product1['date'], product1['price'], 'o-', label='Текущая цена', linewidth=1)
axes[0].plot(product1['date'], product1['recommended_price'], 's-', label='Рекомендуемая цена', linewidth=1)
axes[0].set_xlabel('Дата')
axes[0].set_ylabel('Цена')
axes[0].set_title('Товар 1: Сравнение текущей и рекомендуемой цены')
axes[0].legend()
axes[0].tick_params(axis='x', rotation=45)

# График 2: Количество применений правил
rule_counts = df['rule_applied'].value_counts()
rule_counts.plot(kind='bar', ax=axes[1], color=['blue', 'orange', 'gray'])
axes[1].set_xlabel('Правило')
axes[1].set_ylabel('Количество применений')
axes[1].set_title('Статистика применения правил')
axes[1].tick_params(axis='x', rotation=15)

plt.tight_layout()
plt.show()

print("\n" + "="*60)
print("Готово для Показа 2")
print("="*60)