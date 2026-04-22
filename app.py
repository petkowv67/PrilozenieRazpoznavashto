
import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import re

st.set_page_config(page_title="OCR Съставки Checker", layout="centered")

st.title("📷 Проверка на съставки")
st.write("Качи снимка или въведи текст, за да анализирам съставките.")

mode = st.radio("Избери метод:", ["📷 Снимка", "✍️ Текст"])

# ❌ Вредни съставки + описание
harmful_ingredients = {
    "E621": "Мононатриев глутамат – може да предизвика главоболие и чувствителност при някои хора.",
    "E102": "Тартразин – изкуствен оцветител, свързан с хиперактивност.",
    "E110": "Жълт залез – може да причини алергични реакции.",
    "E124": "Понсо 4R – потенциално вреден оцветител.",
    "E211": "Натриев бензоат – консервант, който при определени условия може да образува бензен."
}

# ✅ Полезни съставки + описание
good_ingredients = {
    "витамин C": "Подсилва имунната система.",
    "витамин D": "Подпомага здравето на костите.",
    "фибри": "Подобряват храносмилането.",
    "протеин": "Помага за изграждане на мускули.",
    "калций": "Важен за костите и зъбите."
}

def analyze_text(text):
    found_bad = []
    found_good = []

    # търси вредни
    for ingredient, desc in harmful_ingredients.items():
        if re.search(rf"\b{ingredient}\b", text, re.IGNORECASE):
            found_bad.append((ingredient, desc))

    # търси полезни
    for ingredient, desc in good_ingredients.items():
        if re.search(rf"\b{ingredient}\b", text, re.IGNORECASE):
            found_good.append((ingredient, desc))

    return found_good, found_bad

def display_results(text):
    st.subheader("📄 Текст:")
    st.write(text)

    good, bad = analyze_text(text)

    if good:
        st.subheader("✅ Полезни съставки:")
        for ing, desc in good:
            st.success(f"{ing} → {desc}")

    if bad:
        st.subheader("⚠️ Потенциално вредни съставки:")
        for ing, desc in bad:
            st.error(f"{ing} → {desc}")

    if not good and not bad:
        st.info("Не са открити разпознати съставки от списъка.")

# --- СНИМКА ---
if mode == "📷 Снимка":
    uploaded_file = st.file_uploader("Качи изображение", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Качено изображение", use_column_width=True)

        with st.spinner("🔍 Разпознаване на текст..."):
            reader = easyocr.Reader(['en', 'bg'])
            img_array = np.array(image)
            results = reader.readtext(img_array, detail=0)
            extracted_text = " ".join(results)

        display_results(extracted_text)

# --- ТЕКСТ ---
elif mode == "✍️ Текст":
    user_text = st.text_area("Въведи текст със съставки:")

    if st.button("Провери"):
        if user_text.strip():
            display_results(user_text)
        else:
            st.warning("Моля, въведи текст.")

st.subheader("ℹ️ Бележка:")
st.write("Анализът е базиран на предварително зададени списъци и не е медицински съвет.")
