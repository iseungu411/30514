import streamlit as st
import random

# 페이지 설정
st.set_page_config(page_title="Clash Royale Streamlit", layout="centered")

# --- 카드 데이터 ---
CARDS = {
    "기사": {"cost": 3, "hp": 12, "atk": 3, "icon": "🛡️"},
    "아처": {"cost": 3, "hp": 6, "atk": 4, "icon": "🏹"},
    "자이언트": {"cost": 5, "hp": 25, "atk": 2, "icon": "🧔"},
    "미니언": {"cost": 3, "hp": 5, "atk": 5, "icon": "🦇"},
    "화염구": {"cost": 4, "hp": 0, "atk": 10, "icon": "🔥"},
}

# --- 게임 초기화 ---
def init_game():
    st.session_state.elixir = 5
    st.session_state.king_hp = 30
    st.session_state.enemy_king_hp = 30
    st.session_state.my_units = []
    st.session_state.enemy_units = []
    
    deck = list(CARDS.keys())
    random.shuffle(deck)
    st.session_state.deck = deck
    st.session_state.hand = [st.session_state.deck.pop() for _ in range(3)]
    st.session_state.log = []
    st.session_state.game_over = False

# 버전 호환성을 보장하는 안전한 rerun 함수
def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

# 최초 실행 시 세션 초기화
if "elixir" not in st.session_state:
    init_game()

# --- 게임 주요 로직 ---
def draw_card():
    if st.session_state.deck and len(st.session_state.hand) < 3:
        st.session_state.hand.append(st.session_state.deck.pop(0))

def play_card(card_name):
    card = CARDS[card_name]
    if st.session_state.elixir < card["cost"]:
        st.toast("⚠️ 엘릭서가 부족합니다!")
        return

    st.session_state.elixir -= card["cost"]
    st.session_state.hand.remove(card_name)
    st.session_state.deck.append(card_name)
    draw_card()

    # 유닛 생성 및 타워 직접 공격 구분
    if card["hp"] > 0:
        st.session_state.my_units.append({
            "name": card_name, "hp": card["hp"], "atk": card["atk"], "icon": card["icon"]
        })
        icon = card['icon']
        st.session_state.log.append(f"🔵 플레이어가 {card_name}{icon}을(를) 소환했습니다.")
    else:
        st.session_state.enemy_king_hp -= card["atk"]
        st.session_state.log.append(f"🔥 화염구! 적 타워에 {card['atk']} 데미지!")

    run_turn()

def enemy_ai_turn():
    if random.random() < 0.6:
        possible_cards = [k for k, v in CARDS.items() if v["hp"] > 0]
        chosen = random.choice(possible_cards)
        card = CARDS[chosen]
        st.session_state.enemy_units.append({
            "name": chosen, "hp": card["hp"], "atk": card["atk"], "icon": card["icon"]
        })
        icon = card['icon']
        st.session_state.log.append(f"🔴 적이 {chosen}{icon}을(를) 소환했습니다.")

def run_turn():
    # 1. 엘릭서 충전
    st.session_state.elixir = min(10, st.session_state.elixir + 2)

    # 2. 적 AI 행동
    enemy_ai_turn()

    # 3. 아군 유닛 공격
    for unit in list(st.session_state.my_units):
        if st.session_state.enemy_units:
            target = st.session_state.enemy_units[0]
            target["hp"] -= unit["atk"]
            if target["hp"] <= 0:
                st.session_state.enemy_units.pop(0)
                u_name = unit['name']
                t_name = target['name']
                st.session_state.log.append(f"⚔️ {u_name}이(가) 적 {t_name}을(를) 처치했습니다!")
        else:
            st.session_state.enemy_king_hp -= unit["atk"]
            u_name = unit['name']
            u_atk = unit['atk']
            st.session_state.log.append(f"🏰 {u_name}이(가) 적 타워를 공격했습니다! (-{u_atk})")

    # 4. 적 유닛 공격
    for unit in list(st.session_state.enemy_units):
        if st.session_state.my_units:
            target = st.session_state.my_units[0]
            target["hp"] -= unit["atk"]
            if target["hp"] <= 0:
                st.session_state.my_units.pop(0)
                u_name = unit['name']
                t_name = target['name']
                st.session_state.log.append(f"💥 적 {u_name}이(가) 내 {t_name}을(를) 처치했습니다!")
        else:
            st.session_state.king_hp -= unit["atk"]
            u_name = unit['name']
            u_atk = unit['atk']
            st.session_state.log.append(f"💥 적 {u_name}이(가) 내 타워를 공격했습니다! (-{u_atk})")

    # 승패 체크
    if st.session_state.enemy_king_hp <= 0:
        st.session_state.game_over = True
    elif st.session_state.king_hp <= 0:
        st.session_state.game_over = True

    safe_rerun()

# --- 화면 구성 (UI) ---
st.title("👑 클래시로얄 Streamlit")

# 상태 표시
col1, col2 = st.columns(2)
col1.metric("🔴 적 타워 HP", f"{max(0, st.session_state.enemy_king_hp)} / 30")
col2.metric("🔵 내 타워 HP", f"{max(0, st.session_state.king_hp)} / 30")

st.progress(st.session_state.elixir / 10, text=f"🧪 엘릭서: {st.session_state.elixir} / 10")

st.markdown("---")

# 전장 상황
f_col1, f_col2 = st.columns(2)
with f_col1:
    st.subheader("🔴 적 아레나")
    if not st.session_state.enemy_units:
        st.caption("배치된 적 유닛이 없습니다.")
    for u in st.session_state.enemy_units:
        st.error(f"{u['icon']} **{u['name']}** (HP: {u['hp']} | ATK: {u['atk']})")

with f_col2:
    st.subheader("🔵 아군 아레나")
    if not st.session_state.my_units:
        st.caption("배치된 아군 유닛이 없습니다.")
    for u in st.session_state.my_units:
        st.info(f"{u['icon']} **{u['name']}** (HP: {u['hp']} | ATK: {u['atk']})")

st.markdown("---")

# 게임 오버 화면 처리
if st.session_state.game_over:
    if st.session_state.enemy_king_hp <= 0:
        st.balloons()
        st.success("👑 적 타워를 파괴하고 승리했습니다!")
    else:
        st.error("💀 내 타워가 파괴되었습니다...")
    if st.button("🔄 새 게임 시작"):
        init_game()
        safe_rerun()
else:
    # 핸드 및 카드 소환
    st.subheader("🃏 카드 내기")
    card_cols = st.columns(3)
    for idx, card_name in enumerate(st.session_state.hand):
        card = CARDS[card_name]
        with card_cols[idx]:
            btn_label = f"{card['icon']} {card_name}\n(🧪{card['cost']})"
            if st.button(btn_label, key=f"hand_{idx}"):
                play_card(card_name)

# 전투 로그
with st.expander("📜 전투 기록", expanded=True):
    for log in reversed(st.session_state.log[-5:]):
        st.write(log)
