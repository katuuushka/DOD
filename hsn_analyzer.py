import streamlit as st
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model

# Загрузка обученной модели
try:
    model = load_model('hsn_model.h5')
except FileNotFoundError:
    st.error("Модель 'hsn_model.h5' не найдена. Пожалуйста, убедитесь, что файл находится в правильном каталоге.")
    st.stop()

# Функция для предсказания ХСН
def predict_hsn(sad, glucose, creatinine):
    """
    Предсказывает наличие ХСН на основе введенных данных.

    Args:
        sad (float): Показатель САД.
        glucose (float): Уровень глюкозы.
        creatinine (float): Уровень креатинина.

    Returns:
        int: 1, если есть ХСН, 0, если нет.
    """
    input_data = pd.DataFrame([[sad, glucose, creatinine]], columns=['САД', 'Глюкоза', 'Креатинин'])
    prediction = model.predict(input_data)
    return int(np.round(prediction[0][0]))  # Возвращаем 0 или 1

# Настройка Streamlit
st.title("Чат с Анализатором ХСН")

# Инициализация истории чата в Session State (если еще не существует)
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Функция для отображения истории чата
def display_chat_history():
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Отображаем историю чата при каждом обновлении страницы
display_chat_history()


# Функция для получения ответа от Анализатора
def get_analyzer_response(sad, glucose, creatinine):
    try:
        prediction = predict_hsn(sad, glucose, creatinine)
        if prediction == 1:
            response = "Похоже, что у вас есть признаки ХСН.  Рекомендуется обратиться к врачу для дальнейшей диагностики и лечения."
        else:
            response = "Судя по введенным данным, признаков ХСН не выявлено.  Однако, для полной уверенности рекомендуется проконсультироваться с врачом."
        return response
    except Exception as e:
        return f"Произошла ошибка при анализе данных: {e}. Пожалуйста, убедитесь, что введены корректные числовые значения."


# Ввод данных пользователем
with st.sidebar:
    st.header("Введите данные пациента")
    sad = st.number_input("САД (систолическое артериальное давление):", min_value=0.0, value=120.0)
    glucose = st.number_input("Уровень глюкозы:", min_value=0.0, value=80.0)
    creatinine = st.number_input("Уровень креатинина:", min_value=0.0, value=1.0)

# Логика чата
if prompt := st.chat_input("Введите 'Анализировать' для получения результата"):
    # Добавляем сообщение пользователя в историю чата
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Проверяем, что пользователь хочет проанализировать данные
    if prompt.lower() == "анализировать":
        # Получаем ответ от Анализатора
        analyzer_response = get_analyzer_response(sad, glucose, creatinine)

        # Добавляем сообщение Анализатора в историю чата
        st.session_state.chat_history.append({"role": "assistant", "content": analyzer_response})
        with st.chat_message("assistant"):
            st.markdown(analyzer_response)
    else:
        # Если пользователь ввел что-то другое, предлагаем ввести "Анализировать"
        response_text = "Пожалуйста, введите 'Анализировать' для получения результата."
        st.session_state.chat_history.append({"role": "assistant", "content": response_text})
        with st.chat_message("assistant"):
            st.markdown(response_text)


# Дополнительные инструкции и дисклеймер
st.markdown("---")
st.markdown("⚠️ **Внимание:** Этот инструмент предназначен только для информационных целей и не является заменой консультации с квалифицированным врачом. Результаты анализа не являются диагнозом и не должны использоваться для самостоятельного лечения. Всегда обращайтесь к врачу для получения профессиональной медицинской помощи.")
