import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import re

st.set_page_config(page_title="OCR Съставки Checker", layout="centered")

st.title("📷 Проверка на съставки")
st.write("Качи снимка или въведи текст, за да открия потенциално вредни съставки (напр. E621).")

# избор на режим
mode = st.radio("Избери метод:", ["📷 Снимка", "✍️ Текст"])

# Примерен списък с добавки за търсене
harmful_ingredients = [
    "E621", "E622", "E623", "E624", "E625",
    "E102", "E110", "E122", "E124", "E129",
    "E211", "E212", "E213"
]

def check_ingredients(text):
    found = []
    for ingredient in harmful_ingredients:
        if re.search(rf"\b{ingredient}\b", text, re.IGNORECASE):
            found.append(ingredient)
    return found

# --- РЕЖИМ 1: СНИМКА ---
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

        st.subheader("📄 Разпознат текст:")
        st.write(extracted_text)

        found = check_ingredients(extracted_text)

        st.subheader("⚠️ Намерени потенциално вредни съставки:")
        if found:
            st.error(f"Открити са: {', '.join(found)}")
        else:
            st.success("Не са открити вредни съставки от списъка ✅")

# --- РЕЖИМ 2: ТЕКСТ ---
elif mode == "✍️ Текст":
    user_text = st.text_area("Въведи текст със съставки:")

    if st.button("Провери"):
        if user_text.strip():
            st.subheader("📄 Въведен текст:")
            st.write(user_text)

            found = check_ingredients(user_text)

            st.subheader("⚠️ Намерени потенциално вредни съставки:")
            if found:
                st.error(f"Открити са: {', '.join(found)}")
            else:
                st.success("Не са открити вредни съставки от списъка ✅")
        else:
            st.warning("Моля, въведи текст.")

st.subheader("ℹ️ Бележка:")
st.write("Това е базова проверка. За по-точни резултати може да се разшири списъкът със съставки.")










import time
import random

st.sidebar.markdown("---")
st.sidebar.title("🎮 Tic Tac Toe")

# init
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
if "player_turn" not in st.session_state:
    st.session_state.player_turn = True
if "winner" not in st.session_state:
    st.session_state.winner = None

def check_winner(board):
    wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for w in wins:
        if board[w[0]] == board[w[1]] == board[w[2]] != "":
            return board[w[0]]
    if "" not in board:
        return "Draw"
    return None

def ai_move():
     empty = [i for i, x in enumerate(st.session_state.board) if x == ""]
    if empty:
        time.sleep(0.5)  # максимум 0.5 сек (можеш 0.2 ако искаш още по-бързо)
        move = random.choice(empty)
        st.session_state.board[move] = "O"
def reset_game():
    st.session_state.board = [""] * 9
    st.session_state.player_turn = True
    st.session_state.winner = None

# 🎯 ПОКАЗВАНЕ НА РЕДА
if st.session_state.winner is None:
    if st.session_state.player_turn:
        st.sidebar.info("👉 Ти си на ход (X)")
    else:
        st.sidebar.warning("🤖 AI мисли...")
else:
    if st.session_state.winner == "Draw":
        st.sidebar.info("Равенство 🤝")
    else:
        st.sidebar.success(f"Победител: {st.session_state.winner}")

# UI
cols = st.sidebar.columns(3)
for i in range(9):
    if cols[i % 3].button(st.session_state.board[i] or " ", key=f"btn_{i}"):
        if (
            st.session_state.board[i] == "" 
            and st.session_state.winner is None 
            and st.session_state.player_turn
        ):
            st.session_state.board[i] = "X"
            st.session_state.player_turn = False

            st.session_state.winner = check_winner(st.session_state.board)

            if st.session_state.winner is None:
                ai_move()
                st.session_state.winner = check_winner(st.session_state.board)
                st.session_state.player_turn = True

st.sidebar.button("🔄 Нова игра", on_click=reset_game)
