import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import re

st.set_page_config(page_title="Съставки Analyzer", layout="centered")

st.title("📦 Анализ на съставки от етикети")
st.write("Качи снимка, използвай камера или въведи текст за анализ.")

# -----------------------------
# РЕЖИМ
# -----------------------------
mode = st.radio("Избери метод:", ["📷 Снимка", "✍️ Текст", "🎥 Камера"])

# -----------------------------
# БАЗА ДАННИ
# -----------------------------
harmful_ingredients = {
    "E621": "Мононатриев глутамат – може да предизвика чувствителност при някои хора.",
    "E102": "Тартразин – изкуствен оцветител, свързан с хиперактивност.",
    "E110": "Оцветител – може да предизвика алергии.",
    "E124": "Червен оцветител – спорен за здравето.",
    "E211": "Натриев бензоат – консервант, който може да образува вредни съединения."
}

good_ingredients = {
    "витамин C": "Подсилва имунната система.",
    "витамин D": "Подпомага костите и имунитета.",
    "фибри": "Подобряват храносмилането.",
    "протеин": "Важно за мускулите.",
    "калций": "Здрави кости и зъби."
}

# -----------------------------
# АНАЛИЗ ФУНКЦИЯ
# -----------------------------
def analyze_text(text):
    found_bad = []
    found_good = []

    for ing, desc in harmful_ingredients.items():
        if re.search(rf"\b{re.escape(ing)}\b", text, re.IGNORECASE):
            found_bad.append((ing, desc))

    for ing, desc in good_ingredients.items():
        if re.search(rf"\b{re.escape(ing)}\b", text, re.IGNORECASE):
            found_good.append((ing, desc))

    return found_good, found_bad

def display_results(text):
    st.subheader("📄 Разпознат текст")
    st.write(text)

    good, bad = analyze_text(text)

    if good:
        st.subheader("✅ Полезни съставки")
        for g, d in good:
            st.success(f"{g} → {d}")

    if bad:
        st.subheader("⚠️ Вредни съставки")
        for b, d in bad:
            st.error(f"{b} → {d}")

    if not good and not bad:
        st.info("Няма разпознати съставки от базата данни.")

# -----------------------------
# OCR INIT (само веднъж)
# -----------------------------
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en', 'bg'])

reader = load_reader()

# -----------------------------
# 📷 СНИМКА
# -----------------------------
if mode == "📷 Снимка":
    uploaded_file = st.file_uploader("Качи снимка на етикет", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Качена снимка", use_column_width=True)

        with st.spinner("🔍 Анализ..."):
            img_array = np.array(image)
            results = reader.readtext(img_array, detail=0)
            text = " ".join(results)

        display_results(text)

# -----------------------------
# ✍️ ТЕКСТ
# -----------------------------
elif mode == "✍️ Текст":
    user_text = st.text_area("Въведи съставки:")

    if st.button("Провери"):
        if user_text.strip():
            display_results(user_text)
        else:
            st.warning("Моля въведи текст.")

# -----------------------------
# 🎥 КАМЕРА
# -----------------------------
elif mode == "🎥 Камера":
    camera_image = st.camera_input("Сканирай етикет")

    if camera_image:
        image = Image.open(camera_image)
        st.image(image, caption="Снимка от камера", use_column_width=True)

        with st.spinner("🔍 Анализ..."):
            img_array = np.array(image)
            results = reader.readtext(img_array, detail=0)
            text = " ".join(results)

        display_results(text)

# -----------------------------
# INFO
# -----------------------------
st.markdown("---")
st.caption("⚠️ Анализът е информативен и не е медицински съвет.")









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
        time.sleep(0.5)
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
