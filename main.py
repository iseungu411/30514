import streamlit as st
import random
import time

# 웹 페이지 기본 설정
st.set_page_config(page_title="Legendary Hero RPG", page_icon="⚔️", layout="centered")

# --- 🎨 사이버펑크 Visual CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Noto+Sans+KR:wght@500;700;900&display=swap');

    .stApp {
        background: radial-gradient(circle at center, #180b2a 0%, #080311 100%);
        color: #ffffff;
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    .game-title {
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        font-size: 2.2rem;
        font-weight: 900;
        background: linear-gradient(180deg, #ff007f 0%, #00f0ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 15px;
    }

    .hero-card {
        background: rgba(25, 15, 45, 0.7);
        border: 2px solid #00f0ff;
        border-radius: 16px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.3);
    }
    
    .weapon-card {
        background: rgba(25, 15, 45, 0.7);
        border: 2px solid #ff007f;
        border-radius: 16px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 0 15px rgba(255, 0, 127, 0.3);
    }

    .art-avatar {
        font-size: 3.5rem;
    }

    .battle-arena {
        background: linear-gradient(180deg, #320340 0%, #0c0114 100%);
        border: 2px solid #ff007f;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin-top: 10px;
    }

    div.stButton > button {
        width: 100% !important;
        height: 48px !important;
        border-radius: 10px !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #2b1055 0%, #15082a 100%) !important;
        color: #00f0ff !important;
        border: 1px solid #00f0ff !important;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #00f0ff 0%, #ff007f 100%) !important;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# 안전한 페이지 새로고침
def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

# --- ⚔️ 데이터 세팅 ---
WEAPON_DATA = [
    {"name": "수련용 목검", "art": "🗡️", "base": 20},
    {"name": "기사의 강철검", "art": "⚔️", "base": 50},
    {"name": "플라즈마 세이버", "art": "🗡️⚡", "base": 100},
    {"name": "드래곤 슬레이어", "art": "⚔️🔥", "base": 200},
    {"name": "신멸의 차원창", "art": "🔱🌌", "base": 400}
]

MONSTERS = [
    {"name": "하급 슬라임", "art": "🟢", "req_atk": 30, "reward": 300},
    {"name": "변종 고블린", "art": "👺", "req_atk": 70, "reward": 800},
    {"name": "강철 오크", "art": "👹", "req_atk": 150, "reward": 2200},
    {"name": "화염 군주 드래곤", "art": "🐉🔥", "req_atk": 320, "reward": 6000},
    {"name": "심연의 멸망자 마왕", "art": "👾⚡", "req_atk": 600, "reward": 20000}
]

# --- 🎮 세션 데이터 상태 초기화 ---
if "gold" not in st.session_state:
    st.session_state.hero_name = "용사님"
    st.session_state.hero_level = 1
    st.session_state.gold = 2000
    st.session_state.weapon_lvl = 0
    st.session_state.weapon_tier = 0
    st.session_state.protection_scrolls = 1
    st.session_state.log = ["✨ 차원의 문이 열렸습니다. 모험을 시작하세요!"]

# --- 📊 계산 스탯 ---
def get_hero_atk():
    return st.session_state.hero_level * 25

def get_weapon_atk():
    w = WEAPON_DATA[st.session_state.weapon_tier]
    return w["base"] + (st.session_state.weapon_lvl * 20)

def get_total_atk():
    return get_hero_atk() + get_weapon_atk()

def get_w_cost():
    return (st.session_state.weapon_lvl + 1) * 250

def get_h_cost():
    return st.session_state.hero_level * 300

def get_w_rate():
    return max(15, 100 - (st.session_state.weapon_lvl * 6))

# --- 🔨 게임 로직 ---
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
            st.toast("🌟 무기가 한 단계 진화했습니다!", icon="💎")
        st.session_state.log.append(f"⚔️ 무기 강화 성공! (+{st.session_state.weapon_lvl})")
    else:
        if st.session_state.protection_scrolls > 0 and st.session_state.weapon_lvl >= 5:
            st.session_state.protection_scrolls -= 1
            st.toast("🛡️ 방지권 사용으로 무기 파괴 방지!", icon="🛡️")
            st.session_state.log.append("🛡️ 강화 실패 (방지권 사용)")
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
    st.session_state.log.append(f"🦸 {st.session_state.hero_name} 훈련 완료 (Lv.{st.session_state.hero_level})")
    safe_rerun()

def buy_protection():
    if st.session_state.gold >= 4000:
        st.session_state.gold -= 4000
        st.session_state.protection_scrolls += 1
        st.toast("📜 방지권 구매 완료!", icon="📜")
        safe_rerun()
    else:
        st.toast("⚠️ 골드가 부족합니다 (4,000 G 필요)", icon="💰")

# --- 🎧 BGM 시스템 ---
with st.sidebar:
    st.header("🎵 배경음악")
    bgm_on = st.toggle("BGM 켜기/끄기", value=True)
    if bgm_on:
        st.components.v1.html("""
            <audio autoplay loop style="width: 100%; height: 30px;">
                <source src="https://assets.mixkit.co/music/preview/mixkit-game-level-music-689.mp3" type="audio/mpeg">
            </audio>
        """, height=40)
        
    st.markdown("---")
    st.header("⚙️ 캐릭터 설정")
    new_name = st.text_input("히어로 이름", value=st.session_state.hero_name)
    if new_name != st.session_state.hero_name:
        st.session_state.hero_name = new_name
        safe_rerun()
        
    st.markdown("---")
    st.header("🛒 상점")
    st.write(f"📜 파괴 방지권: **{st.session_state.protection_scrolls}개**")
    if st.button("📜 방지권 구매 (4,000G)"):
        buy_protection()

# --- 🖥️ 메인 화면 ---
st.markdown("<h1 class='game-title'>⚔️ HERO RPG: OVERLOAD ⚔️</h1>", unsafe_allow_html=True)

# 상단 메트릭
m1, m2, m3, m4 = st.columns(4)
m1.metric("💰 골드", f"{st.session_state.gold:,} G")
m2.metric("⚔️ 공격력", f"{get_total_atk():,} ATK")
m3.metric("🦸 레벨", f"Lv.{st.session_state.hero_level}")
m4.metric("🛡️ 무기 연마", f"+{st.session_state.weapon_lvl}")

st.markdown("---")

# 캐릭터 & 무기 정보
col_hero, col_weapon = st.columns(2)

with col_hero:
    st.markdown(f"""
        <div class='hero-card'>
            <div style='color:#00f0ff; font-weight:bold;'>HERO PROFILE</div>
            <div class='art-avatar'>🦸‍♂️</div>
            <div style='font-size:1.3rem; font-weight:bold;'>{st.session_state.hero_name}</div>
            <div style='margin:5px 0;'>히어로 ATK: <b>{get_hero_atk()}</b></div>
            <div style='color:#00f0ff;'>육성 비용: <b>{get_h_cost():,} G</b></div>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("💪 히어로 훈련"):
        enhance_hero()

with col_weapon:
    w_info = WEAPON_DATA[st.session_state.weapon_tier]
    st.markdown(f"""
        <div class='weapon-card'>
            <div style='color:#ff007f; font-weight:bold;'>EQUIPPED WEAPON</div>
            <div class='art-avatar'>{w_info['art']}</div>
            <div style='font-size:1.3rem; font-weight:bold;'>+{st.session_state.weapon_lvl} {w_info['name']}</div>
            <div style='margin:5px 0;'>무기 ATK: <b>{get_weapon_atk()}</b></div>
            <div style='color:#ff007f;'>성공률: <b>{get_w_rate()}%</b> | 비용: <b>{get_w_cost():,} G</b></div>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("🔨 무기 연마"):
        enhance_weapon()

st.markdown("---")

# 전투 구역
st.subheader("👹 던전 전투")

with st.expander("⚔️ 몬스터 사냥터 열기", expanded=True):
    monster = random.choice(MONSTERS)
    w_art = WEAPON_DATA[st.session_state.weapon_tier]["art"]
    
    st.markdown(f"#### 👹 출현 몬스터: **[{monster['name']}]** {monster['art']}")
    st.caption(f"권장 공격력: {monster['req_atk']} | 내 공격력: {get_total_atk()}")
    
    skill = st.radio("⚔️ 전투 스킬 선택", ["기본 공격", "🔥 엑스칼리버 (공격력 2.5배)"], horizontal=True)
    
    if st.button("🚀 전투 개시!", use_container_width=True):
        multiplier = 2.5 if "엑스칼리버" in skill else 1.0
        
        # 애니메이션 연출
        arena = st.empty()
        arena.markdown(f"""
            <div class='battle-arena'>
                <span class='art-avatar'>🦸‍♂️{w_art}</span>
                <span style='font-size:2rem;'> 💥 </span>
                <span class='art-avatar'>{monster['art']}</span>
            </div>
        """, unsafe_allow_html=True)
        
        time.sleep(0.5)
        
        # 승패 판정
        win_rate = min(95, max(10, int((get_total_atk() * multiplier / monster['req_atk']) * 70)))
        
        if random.randint(1, 100) <= win_rate:
            reward = monster['reward'] + random.randint(100, 500)
            st.session_state.gold += reward
            st.success(f"🎉 승리! [{monster['name']}]을(를) 격파하고 {reward:,} Gold를 획득했습니다!")
            st.session_state.log.append(f"🏆 [{monster['name']}] 처치! (+{reward:,} G)")
        else:
            penalty = random.randint(200, 500)
            st.session_state.gold = max(0, st.session_state.gold - penalty)
            st.error(f"☠️ 패배... 몬스터의 반격으로 {penalty:,} Gold를 잃었습니다.")
            st.session_state.log.append(f"💀 [{monster['name']}] 사냥 실패... (-{penalty:,} G)")

# 초기화 버튼
if st.button("🔄 게임 처음부터 다시하기", use_container_width=True):
    st.session_state.clear()
    safe_rerun()

# 기록 일지
with st.expander("📜 모험 기록 일지", expanded=True):
    for log in reversed(st.session_state.log[-5:]):
        st.write(log)
