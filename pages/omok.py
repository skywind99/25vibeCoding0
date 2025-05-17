
import streamlit as st
import numpy as np

st.set_page_config(page_title="🎮 오목 게임", page_icon="⚫")

st.title("🎯 오목 게임 - Five in a Row")
st.write("🧠 사람이 두는 오목! 5개를 먼저 연결하세요!")

# 보드 설정
BOARD_SIZE = 10
if 'board' not in st.session_state:
    st.session_state.board = np.full((BOARD_SIZE, BOARD_SIZE), '⬜')
    st.session_state.turn = '⚫'  # 시작 플레이어
    st.session_state.winner = None

# 승리 조건 검사
def check_winner(board, player):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if j <= BOARD_SIZE - 5 and all(board[i, j + k] == player for k in range(5)):
                return True
            if i <= BOARD_SIZE - 5 and all(board[i + k, j] == player for k in range(5)):
                return True
            if i <= BOARD_SIZE - 5 and j <= BOARD_SIZE - 5 and all(board[i + k, j + k] == player for k in range(5)):
                return True
            if i <= BOARD_SIZE - 5 and j >= 4 and all(board[i + k, j - k] == player for k in range(5)):
                return True
    return False

# 게임판 출력
def render_board():
    for i in range(BOARD_SIZE):
        cols = st.columns(BOARD_SIZE)
        for j in range(BOARD_SIZE):
            if st.session_state.board[i, j] == '⬜' and st.session_state.winner is None:
                if cols[j].button(" ", key=f"{i}-{j}"):
                    st.session_state.board[i, j] = st.session_state.turn
                    if check_winner(st.session_state.board, st.session_state.turn):
                        st.session_state.winner = st.session_state.turn
                    st.session_state.turn = '⚪' if st.session_state.turn == '⚫' else '⚫'
            else:
                cols[j].markdown(f"<h3 style='text-align: center;'>{st.session_state.board[i, j]}</h3>", unsafe_allow_html=True)

render_board()

# 승리 메시지
if st.session_state.winner:
    st.markdown(f"## 🏆 {st.session_state.winner} 승리!")
    if st.session_state.winner == '⚫':
        st.balloons()
    else:
        st.snow()

# 초기화 버튼
if st.button("🔄 게임 다시 시작"):
    st.session_state.board = np.full((BOARD_SIZE, BOARD_SIZE), '⬜')
    st.session_state.turn = '⚫'
    st.session_state.winner = None
