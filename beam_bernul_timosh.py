import numpy as np
import plotly.graph_objects as go
import streamlit as st

# Функция для расчета напряжений и прогибов
def calculate_stresses_and_deflections(L, q, b, h, E, G):
    I = (b * h**3) / 12  # Момент инерции
    M_max = q * L**2 / 8  # Максимальный изгибающий момент
    V_max = q * L / 2  # Максимальная поперечная сила
    # Распределение напряжений по теории Бернулли
    y = np.linspace(-h / 2, h / 2, 100)
    sigma_x_bernoulli = -M_max * y / I  # Нормальные напряжения
    tau_xy_bernoulli = np.zeros_like(y)  # Касательные напряжения не учитываются
    # Распределение напряжений по теории Тимошенко
    Q = (b * (h**2 / 4 - y**2)) / 2  # Статический момент отсеченной части
    tau_xy_timoshenko = V_max * Q / (I * b)  # Касательные напряжения
    sigma_x_timoshenko = sigma_x_bernoulli  # Нормальные напряжения (как у Бернулли)
    # Прогибы
    x = np.linspace(0, L, 100)
    w_bernoulli = -(q * x * (L**3 - 2 * L * x**2 + x**3)) / (24 * E * I)  # Прогиб по Бернулли
    w_timoshenko = w_bernoulli + (q * L**2 * x / (2 * k * G * b * h)) * (x - L) / L  # Прогиб по Тимошенко
    return y, sigma_x_bernoulli, tau_xy_bernoulli, sigma_x_timoshenko, tau_xy_timoshenko, x, w_bernoulli, w_timoshenko

# Параметры балки
L_init = 5.0  # Пролет балки (м)
q_init = 10.0  # Распределенная нагрузка (кН/м)
b_init = 0.2  # Ширина сечения (м)
h_init = 0.4  # Высота сечения (м)
E_init = 210e6  # Модуль упругости (кПа)
G_init = 84e6  # Модуль сдвига (кПа)
k = 5 / 6  # Коэффициент сдвига для прямоугольного сечения

# Создание интерфейса Streamlit
st.title("Анализ балки: Теория Бернулли vs Теория Тимошенко")

# Слайдеры для управления параметрами
L = st.slider("Пролет балки (м)", 1.0, 10.0, L_init, step=0.1)
q = st.slider("Нагрузка на балку (кН/м)", 1.0, 20.0, q_init, step=0.1)
b = st.slider("Ширина балки (м)", 0.1, 0.5, b_init, step=0.01)
h = st.slider("Высота балки (м)", 0.1, 0.5, h_init, step=0.01)

# Отображение отношения h/L
st.write(f"Отношение h/L = {h / L:.4f}")

# Рассчитываем данные
y, sigma_x_bernoulli, tau_xy_bernoulli, sigma_x_timoshenko, tau_xy_timoshenko, x, w_bernoulli, w_timoshenko = calculate_stresses_and_deflections(
    L, q, b, h, E_init, G_init
)

# График 1: Теория Бернулли
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=sigma_x_bernoulli, y=y, mode='lines', name="σ_x (Бернулли)", line=dict(color="blue")))
fig1.add_trace(go.Scatter(x=tau_xy_bernoulli, y=y, mode='lines', name="τ_xy (Бернулли)", line=dict(color="orange", dash="dash")))
fig1.update_layout(title="Теория Бернулли", xaxis_title="Напряжения (кПа)", yaxis_title="Высота сечения балки (м)")

# График 2: Теория Тимошенко
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=sigma_x_timoshenko, y=y, mode='lines', name="σ_x (Тимошенко)", line=dict(color="green")))
fig2.add_trace(go.Scatter(x=tau_xy_timoshenko, y=y, mode='lines', name="τ_xy (Тимошенко)", line=dict(color="red", dash="dash")))
fig2.update_layout(title="Теория Тимошенко", xaxis_title="Напряжения (кПа)", yaxis_title="Высота сечения балки (м)")

# График 3: Сравнение прогибов
fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=x, y=w_bernoulli, mode='lines', name="Прогиб (Бернулли)", line=dict(color="blue")))
fig3.add_trace(go.Scatter(x=x, y=w_timoshenko, mode='lines', name="Прогиб (Тимошенко)", line=dict(color="green")))
fig3.update_layout(title="Сравнение прогибов", xaxis_title="Длина балки (м)", yaxis_title="Прогиб балки (м)")

# Отображение графиков
st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)
st.plotly_chart(fig3, use_container_width=True)
