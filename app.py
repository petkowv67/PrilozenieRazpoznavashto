import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import re

st.set_page_config(page_title="OCR Съставки Checker", layout="centered")

st.title("📷 Проверка на съставки от снимка")
st.write("Качи снимка на етикет и ще открия потенциално вредни съставки (напр. E621).")

uploaded_file = st.file_uploader("Качи изображение", type=["jpg", "jpeg", "png"])

# Примерен списък с добавки за търсене
harmful_ingredients = [
    "E621", "E622", "E623", "E624", "E625",  # глутамати
    "E102", "E110", "E122", "E124", "E129",  # оцветители
    "E211", "E212", "E213"                  # консерванти
]

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Качено изображение", use_column_width=True)

    with st.spinner("🔍 Разпознаване на текст..."):
        reader = easyocr.Reader(['en', 'bg'])
        img_array = np.array(image)
        results = reader.readtext(img_array, detail=0)

        extracted_text = " ".join(results)

    st.subheader("📄 Разпознат текст:")
    st.write(extracted_text)

    st.subheader("⚠️ Намерени потенциално вредни съставки:")

    found = []
    for ingredient in harmful_ingredients:
        if re.search(rf"\b{ingredient}\b", extracted_text, re.IGNORECASE):
            found.append(ingredient)

    if found:
        st.error(f"Открити са: {', '.join(found)}")
    else:
        st.success("Не са открити вредни съставки от списъка ✅")

    st.subheader("ℹ️ Бележка:")
    st.write("Това е базова проверка. За по-точни резултати може да се разшири списъкът със съставки.")
