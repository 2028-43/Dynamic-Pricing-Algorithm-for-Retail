"""
СПРИНТ 3: Веб-интерфейс на Streamlit
Позволяет выбрать товар и увидеть график "Текущая цена" vs "Оптимальная цена"

Запуск: streamlit run sprint3_ui.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os

# Настройка страницы
st.set_page_config(
    page_title="Спринт 3: Оптимальная цена",
    page_icon="📊",
    layout="wide"
)

# Заголовок
st.title("Спринт 3: Расчет оптимальной цены")
st.markdown("Максимизация выручки: Цена × (A - B × Цена)")

# Загрузка данных
@st.cache_data
def load_data():
    df = pd.read_csv('sprint1_sales_data.csv')
    return df

# Загрузка моделей
@st.cache_resource
def load_models():
    models = {}
    coefficients = {}
    
    if os.path.exists('models/coefficients.csv'):
        coeff_df = pd.read_csv('models/coefficients.csv')
        for _, row in coeff_df.iterrows():
            pid = int(row['product_id'])
            coefficients[pid] = {'A': row['A'], 'B': row['B']}
    
    return coefficients

# Загружаем
df = load_data()
coefficients = load_models()

# Боковая панель с выбором товара
st.sidebar.header("Настройки")

# Список товаров
products = sorted(df['product_id'].unique())
product_names = {pid: f"Товар {pid}" for pid in products}

selected_product = st.sidebar.selectbox(
    "Выберите товар:",
    options=products,
    format_func=lambda x: product_names[x]
)

# Параметры отображения
show_all_data = st.sidebar.checkbox("Показать все точки данных", value=True)
show_regression = st.sidebar.checkbox("Показать линию регрессии", value=True)

# Основной контент
st.header(f"Анализ для Товара {selected_product}")

# Фильтруем данные для выбранного товара
product_df = df[df['product_id'] == selected_product].copy()

# Получаем коэффициенты для этого товара
if selected_product in coefficients:
    A = coefficients[selected_product]['A']
    B = coefficients[selected_product]['B']
    
    # Оптимальная цена
    optimal_price = A / (2 * B) if B > 0 else 0
    
    # Текущая средняя цена
    current_avg_price = product_df['price'].mean()
    
    # Колонки с метриками
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Текущая средняя цена",
            value=f"{current_avg_price:.2f} руб."
        )
    
    with col2:
        st.metric(
            label="Оптимальная цена",
            value=f"{optimal_price:.2f} руб.",
            delta=f"{optimal_price - current_avg_price:.2f} руб."
        )
    
    with col3:
        st.metric(
            label="Коэффициент A (спрос при цене 0)",
            value=f"{A:.2f}"
        )
    
    with col4:
        st.metric(
            label="Коэффициент B (чувствительность)",
            value=f"{B:.2f}"
        )
    
    # График
    st.subheader("Зависимость спроса от цены")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # График 1: Точки данных и регрессия
    ax1.scatter(product_df['price'], product_df['sales'], alpha=0.5, label='Данные')
    
    if show_regression:
        # Линия регрессии
        price_range = np.linspace(
            product_df['price'].min() * 0.8,
            product_df['price'].max() * 1.2,
            100
        )
        demand_range = A - B * price_range
        ax1.plot(price_range, demand_range, 'r-', label=f'Спрос = {A:.1f} - {B:.1f}×Цена')
        
        # Отмечаем оптимальную цену
        opt_demand = A - B * optimal_price
        ax1.plot(optimal_price, opt_demand, 'ro', markersize=10, label=f'Оптимум: {optimal_price:.1f} руб.')
    
    ax1.set_xlabel('Цена (руб.)')
    ax1.set_ylabel('Продажи')
    ax1.set_title('Зависимость продаж от цены')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # График 2: Функция выручки
    price_range = np.linspace(
        max(10, product_df['price'].min() * 0.5),
        product_df['price'].max() * 1.5,
        100
    )
    
    # Выручка = Цена × Спрос = Цена × (A - B×Цена)
    revenue = price_range * (A - B * price_range)
    
    ax2.plot(price_range, revenue, 'g-', linewidth=2)
    ax2.axvline(x=optimal_price, color='r', linestyle='--', label=f'Оптимум: {optimal_price:.1f} руб.')
    ax2.axvline(x=current_avg_price, color='b', linestyle='--', label=f'Текущая средняя: {current_avg_price:.1f} руб.')
    
    # Точка текущей выручки
    current_revenue = current_avg_price * (A - B * current_avg_price)
    ax2.plot(current_avg_price, current_revenue, 'bo', markersize=8)
    
    # Точка оптимальной выручки
    opt_revenue = optimal_price * (A - B * optimal_price)
    ax2.plot(optimal_price, opt_revenue, 'ro', markersize=8)
    
    ax2.set_xlabel('Цена (руб.)')
    ax2.set_ylabel('Выручка (руб.)')
    ax2.set_title('Функция выручки: Цена × (A - B×Цена)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Вывод формулы
    st.markdown(f"""
    ### Математическая модель
    
    **Спрос:** `Продажи = {A:.2f} - {B:.2f} × Цена`
    
    **Выручка:** `Выручка = Цена × ({A:.2f} - {B:.2f} × Цена) = {A:.2f}×Цена - {B:.2f}×Цена²`
    
    **Оптимальная цена:** `Цена_опт = A / (2B) = {A:.2f} / (2 × {B:.2f}) = {optimal_price:.2f} руб.`
    
    **Выручка при текущей цене:** {current_avg_price:.2f} × ({A:.2f} - {B:.2f}×{current_avg_price:.2f}) = **{current_revenue:.2f} руб.**
    
    **Выручка при оптимальной цене:** {optimal_price:.2f} × ({A:.2f} - {B:.2f}×{optimal_price:.2f}) = **{opt_revenue:.2f} руб.**
    
    **Потенциальный рост:** **{((opt_revenue - current_revenue)/current_revenue*100):.1f}%**
    """)
    
else:
    st.warning(f"Для Товара {selected_product} нет обученной модели. Запустите sprint3_train_model.py сначала.")

# Инструкция по запуску
st.sidebar.markdown("---")
st.sidebar.markdown("### Инструкция")
st.sidebar.markdown("""
    1. Сначала обучите модели:
    2. Затем запустите интерфейс:
""")

# Информация о данных
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Всего записей:** {len(df)}")
st.sidebar.markdown(f"**Товаров:** {df['product_id'].nunique()}")
st.sidebar.markdown(f"**Период:** {df['date'].min()} - {df['date'].max()}")