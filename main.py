import streamlit as st
import random
import time

st.set_page_config(page_title="Legendary Smith RPG", layout="centered")

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
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ff007f 0%, #7928ca 50%, #00f0ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }
    .weapon-card {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid #00f0ff;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.3);
        margin-bottom: 20px;
    }
    .weapon-name {
        font-size: 1.8rem;
        font-weight: bold;
        color: #ff007f;
        text-shadow: 0 0 10px #ff007f;
    }
    div.stButton > button {
        width: 100% !important;
        height: 50px !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# 안전한 rerun 함수
def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

# --- 게임 데이터 & 상태 초기화 ---
WEAPON_NAMES = ["녹슨 단검", "초보자의 검", "강철 장검", "빛나는 성검", "드래곤 슬레이어", "신을 찌르는 창"]

def init_game():
    st.session_state.gold = 1000
    st.session_state.enhance_level = 0
    st.session_state.weapon_idx = 0
    st.session_state.max_level_reached = 0
    st.session_state.log = ["⚒️ 대장간에 입장했습니다."]

if "gold" not in st.session_state:
    init_game()

# --- 게임 수치 계산 함수 ---
def get_weapon_name():
    idx = min(st.session_state.weapon_idx, len(WEAPON_NAMES) - 1)
    return f"+{st.session_state.enhance_level} {WEAPON_NAMES[idx]}"

def get_weapon_atk():
    return (st.session_state.weapon_idx + 1) * 15 + (st.session_state.enhance_level * 12)

def get_enhance_cost():
    return (st.session_state.enhance_level + 1) * 150

def get_success_rate():
    # 강철 단계 이후 확률 하락 (최저 15%)
    rate = max(15, 100 - (st.session_state.enhance_level * 8))
    return rate

# --- 게임 행동 로직 ---
def enhance_weapon():
    cost = get_enhance_cost()
    if st.session_state.gold < cost:
        st.toast("⚠️ 골드가 부족합니다!", icon="💰")
        return

    st.session_state.gold -= cost
    rate = get_success_rate()
    rand = random.randint(1, 100)

    if rand <= rate:
        st.session_state.enhance_level += 1
        
        # 5강마다 무기 외형 승급
        if st.session_state.enhance_level % 5 == 0 and st.session_state.weapon_idx < len(WEAPON_NAMES) - 1:
            st.session_state.weapon_idx += 1
            st.toast("🎉 무기가 더 강력한 외형으로 진화했습니다!", icon="✨")
            
        st.session_state.log.append(f"✅ 강화 성공! ({get_weapon_name()})")
        if st.session_state.enhance_level > st.session_state.max_level_reached:
            st.session_state.max_level_reached = st.session_state.enhance_level
    else:
        # 실패 시 처리
        if st.session_state.enhance_level >= 7:
            # 7강 이상 실패 시 파괴 방지 (강화 단계만 1 감소)
            st.session_state.enhance_level = max(0, st.session_state.enhance_level - 1)
            st.session_state.log.append("💥 강화 실패! 단계가 1 하락했습니다.")
        else:
            st.session_state.log.append("❌ 강화 실패!")

    safe_rerun()

def explore_dungeon():
    atk = get_weapon_atk()
    # 공격력 기반 보상 계산
    gained_gold = random.randint(atk * 2, atk * 4)
    st.session_state.gold += gained_gold
    
    monsters = ["슬라임", "고블린", "오크", "골렘", "드래곤"]
    monster = random.choice(monsters)
    
    st.session_state.log.append(f"⚔️ 던전 탐험 성공! [{monster}]을(를) 처치하고 {gained_gold:,} G 획득!")
    safe_rerun()

# --- UI 레이아웃 ---
st.markdown("<h1 class='main-title'>⚔️ LEGENDARY SMITH RPG ⚔️</h1>", unsafe_allow_html=True)

# 상단 유저 상태창
col1, col2, col3 = st.columns(3)
col1.metric("💰 보유 골드", f"{st.session_state.gold:,} G")
col2.metric("⚔️ 공격력", f"{get_weapon_atk():,} ATK")
col3.metric("🏆 최고 기록", f"+{st.session_state.max_level_reached} 강")

st.markdown("---")

# 무기 디스플레이
st.markdown(f"""
    <div class='weapon-card'>
        <div style='font-size: 0.9rem; color: #a0a0a0;'>CURRENT WEAPON</div>
        <div class='weapon-name'>{get_weapon_name()}</div>
        <div style='margin-top: 10px; font-size: 1.1rem; color: #00f0ff;'>
            강화 성공 확률: <b>{get_success_rate()}%</b> | 비용: <b>{get_enhance_cost():,} G</b>
        </div>
    </div>
""", unsafe_allow_html=True)

# 조작 버튼
btn_col1, btn_col2 = st.columns(2)

with btn_col1:
    if st.button("🔨 무기 강화하기"):
        enhance_weapon()

with btn_col2:
    if st.button("🗡️ 던전 탐험하기 (골드 벌기)"):
        explore_dungeon()

st.write("")

# 리셋 버튼
if st.button("🔄 게임 초기화", use_container_width=True):
    init_game()
    safe_rerun()

# 로그 화면
with st.expander("📜 게임 활동 기록", expanded=True):
    for log in reversed(st.session_state.log[-6:]):
        st.write(log)
