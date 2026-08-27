import streamlit as st
import random

st.set_page_config(page_title="Legendary Hero RPG", layout="centered")

# --- 사이버펑크 RPG CSS 스타일 ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0e14;
        color: #e6e6e6;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .main-title {
        text-align: center;
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ff007f 0%, #7928ca 50%, #00f0ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }
    .card-box {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid #00f0ff;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.2);
        margin-bottom: 15px;
    }
    .card-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #ff007f;
        text-shadow: 0 0 8px #ff007f;
    }
    .art-display {
        font-size: 3rem;
        margin: 10px 0;
    }
    div.stButton > button {
        width: 100% !important;
        height: 50px !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        font-size: 1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# 안전한 rerun 함수
def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

# --- 칼 아트 & 단계 ---
WEAPON_DATA = [
    {"name": "녹슨 단검", "art": "🗡️", "base": 10},
    {"name": "강철 장검", "art": "⚔️", "base": 25},
    {"name": "빛나는 성검", "art": "🗡️✨", "base": 50},
    {"name": "드래곤 슬레이어", "art": "⚔️🔥", "base": 90},
    {"name": "신을 찌르는 창", "art": "🔱⚡", "base": 150}
]

# --- 몬스터 아트 ---
MONSTERS = [
    {"name": "슬라임", "art": "🟢", "hp": 30},
    {"name": "고블린", "art": "👺", "hp": 60},
    {"name": "오크 족장", "art": "👹", "hp": 120},
    {"name": "화염 드래곤", "art": "🐉🔥", "hp": 250},
    {"name": "심연의 마왕", "art": "👾⚡", "hp": 500}
]

# --- 게임 초기화 ---
def init_game():
    st.session_state.hero_name = "용사님"
    st.session_state.hero_level = 1
    st.session_state.gold = 1000
    st.session_state.weapon_lvl = 0
    st.session_state.weapon_tier = 0
    st.session_state.log = ["⚒️ 전설의 시작! 모험을 준비하세요."]

if "gold" not in st.session_state:
    init_game()

# --- 수치 계산 ---
def get_hero_atk():
    return st.session_state.hero_level * 15

def get_weapon_atk():
    w = WEAPON_DATA[st.session_state.weapon_tier]
    return w["base"] + (st.session_state.weapon_lvl * 10)

def get_total_atk():
    return get_hero_atk() + get_weapon_atk()

def get_w_cost():
    return (st.session_state.weapon_lvl + 1) * 120

def get_h_cost():
    return st.session_state.hero_level * 150

def get_w_rate():
    return max(20, 100 - (st.session_state.weapon_lvl * 7))

# --- 행동 로직 ---
def enhance_weapon():
    cost = get_w_cost()
    if st.session_state.gold < cost:
        st.toast("⚠️ 골드가 부족합니다!", icon="💰")
        return
    st.session_state.gold -= cost

    if random.randint(1, 100) <= get_w_rate():
        st.session_state.weapon_lvl += 1
        if st.session_state.weapon_lvl % 4 == 0 and st.session_state.weapon_tier < len(WEAPON_DATA) - 1:
            st.session_state.weapon_tier += 1
            st.toast("🎉 무기가 멋진 형태로 진화했습니다!", icon="✨")
        st.session_state.log.append(f"⚔️ 무기 강화 성공! (+{st.session_state.weapon_lvl})")
    else:
        st.session_state.weapon_lvl = max(0, st.session_state.weapon_lvl - 1)
        st.session_state.log.append("❌ 무기 강화 실패! 단계 하락")
    safe_rerun()

def enhance_hero():
    cost = get_h_cost()
    if st.session_state.gold < cost:
        st.toast("⚠️ 골드가 부족합니다!", icon="💰")
        return
    st.session_state.gold -= cost
    st.session_state.hero_level += 1
    st.session_state.log.append(f"🦸 {st.session_state.hero_name} 훈련 성공! (Lv.{st.session_state.hero_level})")
    safe_rerun()

def hunt_monster():
    monster = random.choice(MONSTERS)
    atk = get_total_atk()
    reward = random.randint(atk * 2, atk * 4)
    st.session_state.gold += reward
    st.session_state.log.append(f"⚔️ {monster['art']} [{monster['name']}] 처치! +{reward:,} G")
    safe_rerun()

# --- UI 레이아웃 ---
st.markdown("<h1 class='main-title'>⚔️ HERO & SWORD RPG ⚔️</h1>", unsafe_allow_html=True)

# 히어로 이름 설정
with st.sidebar:
    st.header("⚙️ 히어로 설정")
    new_name = st.text_input("히어로 이름 변경", value=st.session_state.hero_name)
    if new_name != st.session_state.hero_name:
        st.session_state.hero_name = new_name
        safe_rerun()

# 상단 상태바
c1, c2, c3 = st.columns(3)
c1.metric("💰 골드", f"{st.session_state.gold:,} G")
c2.metric("⚔️ 총 공격력", f"{get_total_atk():,} ATK")
c3.metric("🦸 히어로 레벨", f"Lv.{st.session_state.hero_level}")

st.markdown("---")

# 카드 영역 (히어로 & 칼 디스플레이)
w_info = WEAPON_DATA[st.session_state.weapon_tier]

col_hero, col_weapon = st.columns(2)

with col_hero:
    st.markdown(f"""
        <div class='card-box'>
            <div style='color:#a0a0a0; font-size:0.9rem;'>MY HERO</div>
            <div class='art-display'>🦸‍♂️</div>
            <div class='card-title'>{st.session_state.hero_name}</div>
            <div>기본 공격력: <b>{get_hero_atk()}</b></div>
            <div style='color:#00f0ff; margin-top:5px;'>훈련 비용: <b>{get_h_cost():,} G</b></div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("💪 히어로 레벨업 (100% 성공)"):
        enhance_hero()

with col_weapon:
    st.markdown(f"""
        <div class='card-box'>
            <div style='color:#a0a0a0; font-size:0.9rem;'>EQUIPPED WEAPON</div>
            <div class='art-display'>{w_info['art']}</div>
            <div class='card-title'>+{st.session_state.weapon_lvl} {w_info['name']}</div>
            <div>무기 공격력: <b>{get_weapon_atk()}</b></div>
            <div style='color:#ff007f; margin-top:5px;'>성공률: <b>{get_w_rate()}%</b> | 비용: <b>{get_w_cost():,} G</b></div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🔨 무기 강화하기"):
        enhance_weapon()

st.markdown("---")

# 던전 탐험 (몬스터 전투)
st.subheader("👹 던전 탐험")
if st.button("⚔️ 몬스터 사냥하러 가기!", use_container_width=True):
    hunt_monster()

# 게임 초기화
if st.button("🔄 게임 처음부터 다시하기"):
    init_game()
    safe_rerun()

# 로그
with st.expander("📜 모험 기록", expanded=True):
    for log in reversed(st.session_state.log[-5:]):
        st.write(log)
