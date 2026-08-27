import streamlit as st
import random

# 페이지 레이아웃 설정
st.set_page_config(page_title="Clash Royale Streamlit Edition", layout="centered", initial_sidebar_state="collapsed")

# --- 클래시로얄 스타일 CSS 적용 ---
st.markdown("""
    <style>
    /* 전체 배경을 아레나 분위기의 어두운 톤으로 설정 */
    .stApp {
        background-color: #0b131e;
        color: #ffffff;
        font-family: 'Supercell-Magic', 'Segoe UI', Tahoma, sans-serif;
    }
    
    /* 클래시로얄 스타일 타이틀 */
    .cr-header {
        text-align: center;
        background: linear-gradient(180deg, #ffd700 0%, #ff8800 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.2rem;
        font-weight: 900;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        margin-bottom: 10px;
    }

    /* 전장 (아레나) 보드 배경 스타일링 */
    .arena-board {
        background: linear-gradient(to bottom, #2b4c20 0%, #3e6b2e 50%, #2b4c20 100%);
        border: 4px solid #5a3d28;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.7);
        position: relative;
    }

    /* 강가 & 다리 그래픽 구현 */
    .river-line {
        background: linear-gradient(90deg, #1c4966, #2d739e, #1c4966);
        height: 25px;
        margin: 15px 0;
        border-top: 3px solid #8b5a2b;
        border-bottom: 3px solid #8b5a2b;
        display: flex;
        justify-content: space-around;
        align-items: center;
    }
    
    .bridge {
        width: 50px;
        height: 29px;
        background-color: #a0522d;
        border: 2px solid #5c2c10;
        box-shadow: inset 0 0 5px #000;
    }

    /* 타워 UI 스타일 */
    .tower-card {
        background: rgba(0, 0, 0, 0.4);
        border-radius: 10px;
        padding: 8px;
        text-align: center;
        border: 2px solid #e1b12c;
    }

    /* 엘릭서 바 커스텀 */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #e056fd 0%, #be2edd 100%) !important;
        box-shadow: 0 0 10px #e056fd;
    }

    /* 클래시로얄 버튼 스타일 */
    div.stButton > button {
        background: linear-gradient(180deg, #4cd137 0%, #44bd32 100%) !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        border: 2px solid #2ed573 !important;
        box-shadow: 0 4px 0 #20bf6b !important;
        height: 60px !important;
    }
    div.stButton > button:active {
        box-shadow: none !important;
        transform: translateY(4px) !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 카드 데이터 ---
CARDS = {
    "기사": {"cost": 3, "hp": 12, "atk": 3, "icon": "⚔️"},
    "아처": {"cost": 3, "hp": 6, "atk": 4, "icon": "🏹"},
    "자이언트": {"cost": 5, "hp": 25, "atk": 2, "icon": "🧔"},
    "미니언": {"cost": 3, "hp": 5, "atk": 5, "icon": "🦇"},
    "화염구": {"cost": 4, "hp": 0, "atk": 10, "icon": "🔥"},
}

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

def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

if "elixir" not in st.session_state:
    init_game()

# --- 게임 시스템 로직 ---
def draw_card():
    if st.session_state.deck and len(st.session_state.hand) < 3:
        st.session_state.hand.append(st.session_state.deck.pop(0))

def play_card(card_name):
    card = CARDS[card_name]
    if st.session_state.elixir < card["cost"]:
        st.toast("⚠️ 엘릭서 부족!", icon="🧪")
        return

    st.session_state.elixir -= card["cost"]
    st.session_state.hand.remove(card_name)
    st.session_state.deck.append(card_name)
    draw_card()

    if card["hp"] > 0:
        st.session_state.my_units.append({
            "name": card_name, "hp": card["hp"], "atk": card["atk"], "icon": card["icon"]
        })
        icon = card['icon']
        st.session_state.log.append(f"🔵 {card_name}{icon} 소환!")
    else:
        st.session_state.enemy_king_hp -= card["atk"]
        st.session_state.log.append(f"🔥 화염구! 적 타워 -{card['atk']}")

    run_turn()

def enemy_ai_turn():
    if random.random() < 0.65:
        possible = [k for k, v in CARDS.items() if v["hp"] > 0]
        chosen = random.choice(possible)
        card = CARDS[chosen]
        st.session_state.enemy_units.append({
            "name": chosen, "hp": card["hp"], "atk": card["atk"], "icon": card["icon"]
        })
        icon = card['icon']
        st.session_state.log.append(f"🔴 적 {chosen}{icon} 소환!")

def run_turn():
    st.session_state.elixir = min(10, st.session_state.elixir + 2)
    enemy_ai_turn()

    # 교전 로직 (아군)
    for unit in list(st.session_state.my_units):
        if st.session_state.enemy_units:
            target = st.session_state.enemy_units[0]
            target["hp"] -= unit["atk"]
            if target["hp"] <= 0:
                st.session_state.enemy_units.pop(0)
                st.session_state.log.append(f"⚔️ {unit['name']}이(가) 적 {target['name']} 격파!")
        else:
            st.session_state.enemy_king_hp -= unit["atk"]
            st.session_state.log.append(f"🏰 {unit['name']} 적 타워 공격! (-{unit['atk']})")

    # 교전 로직 (적군)
    for unit in list(st.session_state.enemy_units):
        if st.session_state.my_units:
            target = st.session_state.my_units[0]
            target["hp"] -= unit["atk"]
            if target["hp"] <= 0:
                st.session_state.my_units.pop(0)
                st.session_state.log.append(f"💥 적 {unit['name']}에게 아군 {target['name']} 처치당함")
        else:
            st.session_state.king_hp -= unit["atk"]
            st.session_state.log.append(f"💥 적 {unit['name']} 내 타워 공격! (-{unit['atk']})")

    if st.session_state.enemy_king_hp <= 0 or st.session_state.king_hp <= 0:
        st.session_state.game_over = True

    safe_rerun()

# --- 클래시로얄 아레나 메인 UI ---
st.markdown("<h1 class='cr-header'>⚔️ CLASH ROYALE ⚔️</h1>", unsafe_allow_html=True)

# 전장 (아레나) 스타트
st.markdown("<div class='arena-board'>", unsafe_allow_html=True)

# 1. 적진 (King Tower + Arena Units)
st.markdown("### 🔴 RED ARENA")
col_e_tower1, col_e_tower2 = st.columns([1, 1])
with col_e_tower1:
    st.markdown(f"<div class='tower-card'>👑 적 킹타워<br><b>HP: {max(0, st.session_state.enemy_king_hp)} / 30</b></div>", unsafe_allow_html=True)

st.write("")
if not st.session_state.enemy_units:
    st.caption("배치된 적 유닛 없음")
else:
    for u in st.session_state.enemy_units:
        st.error(f"{u['icon']} **{u['name']}** | HP: {u['hp']} | ATK: {u['atk']}")

# 2. 강가 및 다리 섹션 (클래시로얄 지형 시각화)
st.markdown("""
    <div class='river-line'>
        <div class='bridge'></div>
        <div class='bridge'></div>
    </div>
""", unsafe_allow_html=True)

# 3. 아군 진영 (King Tower + Arena Units)
st.markdown("### 🔵 BLUE ARENA")
if not st.session_state.my_units:
    st.caption("배치된 아군 유닛 없음")
else:
    for u in st.session_state.my_units:
        st.info(f"{u['icon']} **{u['name']}** | HP: {u['hp']} | ATK: {u['atk']}")

st.write("")
col_m_tower1, col_m_tower2 = st.columns([1, 1])
with col_m_tower1:
    st.markdown(f"<div class='tower-card'>👑 아군 킹타워<br><b>HP: {max(0, st.session_state.king_hp)} / 30</b></div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True) # 전장 태그 끝

# 하단 엘릭서 게이지
st.write("")
st.progress(st.session_state.elixir / 10, text=f"🧪 Elixir: {st.session_state.elixir} / 10")

# 승패 처리 또는 카드 조작 UI
if st.session_state.game_over:
    if st.session_state.enemy_king_hp <= 0:
        st.balloons()
        st.success("🏆 THREE CROWN VICTORY! 승리했습니다!")
    else:
        st.error("💀 DEFEAT! 타워가 파괴되었습니다.")
    if st.button("🔄 다시 경기하기", use_container_width=True):
        init_game()
        safe_rerun()
else:
    # 덱/핸드 영역
    st.subheader("🃏 카드 소환")
    card_cols = st.columns(3)
    for idx, card_name in enumerate(st.session_state.hand):
        card = CARDS[card_name]
        with card_cols[idx]:
            btn_text = f"{card['icon']} {card_name}\n(🧪 {card['cost']})"
            if st.button(btn_text, key=f"btn_{idx}", use_container_width=True):
                play_card(card_name)

# 전투 로그
with st.expander("📜 Live Battle Log"):
    for log in reversed(st.session_state.log[-5:]):
        st.write(log)
