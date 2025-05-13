import streamlit as st
import random

SUITS = ['♠️', '♥️', '♦️', '♣️']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

def get_deck():
    return [f"{r}{s}" for r in RANKS for s in SUITS]

def draw_cards(deck, n):
    return random.sample(deck, n)

def evaluate_hand(hand):
    # 아주 간단한 족보 판단기 (추후 개선 가능)
    ranks = [card[:-1] for card in hand]
    unique_ranks = set(ranks)
    if len(unique_ranks) == 2:
        return "Two Pair or Three of a Kind"
    elif len(unique_ranks) == 3:
        return "One Pair"
    elif len(unique_ranks) == 5:
        return "High Card"
    else:
        return "Unknown"

def hand_guide(hand):
    score = evaluate_hand(hand)
    if "Pair" in score:
        return "✔️ 승산 있어요! 배팅해볼까요?"
    else:
        return "⚠️ 조심하세요. 체크가 나을 수도 있어요."

# 초기 상태 설정
if 'money' not in st.session_state:
    st.session_state.money = 1000
    st.session_state.pot = 0
    st.session_state.deck = get_deck()
    st.session_state.player_hand = []
    st.session_state.computer_hand = []
    st.session_state.game_started = False

st.title("♠️ 1인용 포커 게임")
st.write(f"💰 현재 자금: {st.session_state.money} 원")
st.write(f"🪙 현재 판돈: {st.session_state.pot} 원")

# 게임 시작
if st.button("🎲 게임 시작"):
    st.session_state.deck = get_deck()
    cards = draw_cards(st.session_state.deck, 10)
    st.session_state.player_hand = cards[:5]
    st.session_state.computer_hand = cards[5:]
    st.session_state.pot += 100
    st.session_state.money -= 100
    st.session_state.game_started = True

# 게임 진행 중
if st.session_state.game_started:
    st.subheader("🧑‍💼 당신의 패:")
    st.write(" ".join(st.session_state.player_hand))
    
    st.info(f"📊 족보 분석: **{evaluate_hand(st.session_state.player_hand)}**")
    st.warning(hand_guide(st.session_state.player_hand))
    
    if st.button("👀 결과 보기"):
        player_score = evaluate_hand(st.session_state.player_hand)
        computer_score = evaluate_hand(st.session_state.computer_hand)

        st.write("🤖 컴퓨터의 패:")
        st.write(" ".join(st.session_state.computer_hand))
        st.write(f"📊 컴퓨터 족보: **{computer_score}**")

        # 간단한 승패 판별 (추후 족보 비교 함수로 정밀화)
        if "Pair" in player_score and "Pair" not in computer_score:
            st.success("🎉 당신이 이겼습니다!")
            st.session_state.money += st.session_state.pot * 2
        else:
            st.error("😢 당신이 졌습니다...")

        st.session_state.pot = 0
        st.session_state.game_started = False
