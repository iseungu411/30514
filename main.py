import streamlit as st
import random
import time

# 웹 페이지 설정
st.set_page_config(page_title="NEON OVERLORD: BEYOND", page_icon="⚔️", layout="centered")

# --- 🎨 Ultra Visual & CSS Effects ---
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
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(180deg, #ff007f 0%, #00f0ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 25px rgba(255, 0, 127, 0.7);
        margin-bottom: 5px;
    }

    /* 카드 네온 애니메이션 효과 */
    @keyframes pulse-glow {
        0% { box-shadow: 0 0 15px rgba(0, 240, 255, 0.4); }
        50% { box-shadow: 0 0 30px rgba(0, 240, 255, 0.8); }
        100% { box-shadow: 0 0 15px rgba(0, 240, 255, 0.4); }
    }
    
    @keyframes weapon-pulse {
        0% { box-shadow: 0 0 15px rgba(255, 0, 127, 0.4); }
        50% { box-shadow: 0 0 30px rgba(255, 0, 127, 0.8); }
        100% { box-shadow: 0 0 15px rgba(255, 0, 127, 0.4); }
    }

    .hero-card {
        background: rgba(25, 15, 45, 0.7);
        border: 2px solid #00f0ff;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        animation: pulse-glow 3s infinite ease-in-out;
    }
    
    .weapon-card {
        background: rgba(25, 15, 45, 0.7);
        border: 2px solid #ff007f;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        animation: weapon-pulse 3s infinite ease-in-out;
    }

    .art-avatar {
        font-size: 4rem;
        filter: drop-shadow(0 0 15px rgba(255,255,255,0.6));
    }

    /* 전장 애니메이션 무대 */
    .battle-arena {
        background: linear-gradient(180deg, #320340 0%, #0c0114 100%);
        border: 3px solid #ff007f;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 0 35px rgba(255, 0, 127, 0.5);
    }

    /* 네온 버튼 스타일 */
    div.stButton > button {
        width: 100% !important;
        height: 52px !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
        background: linear-gradient(135deg, #2b1055 0%, #15082a 100%) !important;
        color: #00f0ff !important;
        border: 2px solid #00f0ff !important;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.3) !important;
        transition: all 0.2s ease-in-out !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.8) !important;
        background: linear-gradient(135deg, #00f0ff 0%, #ff007f 100%) !important;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# 페이지 안전 새로고침
def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

# --- ⚔️ 데이터 세팅 ---
WEAPON_DATA = [
    {"name": "수련용 목검", "art": "🗡️", "base": 25},
    {"name": "기사의 강철검", "art": "⚔️", "base": 65},
    {"name": "플라즈마 세이버", "art": "🗡️⚡", "base": 130},
    {"name": "드래곤 슬레이어", "art": "⚔️🔥", "base": 260},
    {"name": "신멸의 차원창", "art": "🔱🌌", "base": 550}
]

MONSTERS = [
    {"name": "하급 슬라임", "art": "🟢", "req_atk": 30, "reward": 350},
    {"name": "변종 고블린", "art": "👺", "req_atk": 80, "reward": 950},
    {"name": "강철 오크", "art": "👹", "req_atk": 180, "reward": 2500},
    {"name": "화염 군주 드래곤", "art": "🐉🔥", "req_atk": 400, "reward": 7500},
    {"name": "심연의 멸망자 마왕", "art": "👾⚡", "req_atk": 800, "reward": 25000}
]

ARTIFACTS = [
    {"name": "기사의 반지", "art": "💍", "bonus_atk": 30},
    {"name": "폭풍의 날개", "art": "🪽", "bonus_atk": 80},
    {"name": "차원의 마도서", "art": "📜", "bonus_atk": 180},
    {"name": "신화의 여의주", "art": "🔮", "bonus_atk": 400}
]

# --- 🎮 세션 초기화 ---
if "gold" not in st.session_state:
    st.session_state.hero_name = "네온 용사"
    st.session_state.hero_level = 1
    st.session_state.gold = 3000
    st.session_state.weapon_lvl = 0
    st.session_state.weapon_tier = 0
    st.session_state.protection_scrolls = 1
    st.session_state.my_artifacts = []
    st.session_state.log = ["✨ 시공의 균열이 열렸습니다. 네온 전장에 입장하세요!"]

# --- 📊 스탯 계산 ---
def get_hero_atk():
    return st.session_state.hero_level * 30

def get_weapon_atk():
    w = WEAPON_DATA[st.session_state.weapon_tier]
    return w["base"] + (st.session_state.weapon_lvl * 25)

def get_artifact_atk():
    return sum(a["bonus_atk"] for a in st.session_state.my_artifacts)

def get_total_atk():
    return get_hero_atk() + get_weapon_atk() + get_artifact_atk()

def get_w_cost():
    return (st.session_state.weapon_lvl + 1) * 280

def get_h_cost():
    return st.session_state.hero_level * 350

def get_w_rate():
    return max(15, 100 - (st.session_state.weapon_lvl * 6))

# --- 🔨 주요 기능 로직 ---
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
            st.toast("🌟 무기가 차원을 넘어 진화했습니다!", icon="💎")
        st.session_state.log.append(f"⚔️ 무기 강화 성공! (+{st.session_state.weapon_lvl})")
    else:
        if st.session_state.protection_scrolls > 0 and st.session_state.weapon_lvl >= 5:
            st.session_state.protection_scrolls -= 1
            st.toast("🛡️ 방지권 사용으로 강화 등급 유지!", icon="🛡️")
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
    st.session_state.log.append(f"🦸 {st.session_state.hero_name} 한계 돌파 (Lv.{st.session_state.hero_level})")
    safe_rerun()

def draw_artifact():
    cost = 5000
    if st.session_state.gold < cost:
        st.toast("⚠️ 유물 소환에는 5,000 G가 필요합니다!", icon="💰")
        return
    st.session_state.gold -= cost
    item = random.choice(ARTIFACTS)
    st.session_state.my_artifacts.append(item)
    st.toast(f"🔮 유물 획득: {item['name']} (+{item['bonus_atk']} ATK)", icon="✨")
    st.session_state.log.append(f"🔮 [유물 소환] {item['name']} 획득!")
    safe_rerun()

# --- 🎧 BGM 음향 시스템 ---
with st.sidebar:
    st.header("🎵 사운드 시스템")
    bgm_on = st.toggle("판타지 BGM 재생", value=True)
    if bgm_on:
        st.components.v1.html("""
            <audio autoplay loop style="width: 100%; height: 30px;">
                <source src="https://assets.mixkit.co/music/preview/mixkit-game-level-music-689.mp3" type="audio/mpeg">
            </audio>
        """, height=40)
        
    st.markdown("---")
    st.header("⚙️ 캐릭터 설정")
    new_name = st.text_input("용사 이름 변경", value=st.session_state.hero_name)
    if new_name != st.session_state.hero_name:
        st.session_state.hero_name = new_name
        safe_rerun()

    st.markdown("---")
    st.header("🎁 보물 상점")
    if st.button("🔮 유물 보물상자 뽑기 (5,000G)"):
        draw_artifact()
    st.write(f"📜 파괴 방지권: **{st.session_state.protection_scrolls}개**")

# --- 🖥️ 메인 UI ---
st.markdown("<h1 class='game-title'>⚔️ NEON OVERLORD: BEYOND ⚔️</h1>", unsafe_allow_html=True)

# 메트릭 대시보드
m1, m2, m3, m4 = st.columns(4)
m1.metric("💰 보유 골드", f"{st.session_state.gold:,} G")
m2.metric("⚡ 총 공격력", f"{get_total_atk():,} ATK")
m3.metric("🦸 히어로", f"Lv.{st.session_state.hero_level}")
m4.metric("🛡️ 무기 등급", f"+{st.session_state.weapon_lvl}")

st.markdown("---")

# 캐릭터 & 무기 프로필
col_hero, col_weapon = st.columns(2)

with col_hero:
    st.markdown(f"""
        <div class='hero-card'>
            <div style='color:#00f0ff; font-weight:bold; font-size:0.9rem;'>HERO OVERLORD</div>
            <div class='art-avatar'>🦸‍♂️</div>
            <div style='font-size:1.3rem; font-weight:bold;'>{st.session_state.hero_name}</div>
            <div style='margin:6px 0; font-size:0.95rem;'>기본 ATK: <b>{get_hero_atk()}</b></div>
            <div style='color:#00f0ff; font-size:0.9rem;'>육성 비용: <b>{get_h_cost():,} G</b></div>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("💪 히어로 스탯 육성"):
        enhance_hero()

with col_weapon:
    w_info = WEAPON_DATA[st.session_state.weapon_tier]
    st.markdown(f"""
        <div class='weapon-card'>
            <div style='color:#ff007f; font-weight:bold; font-size:0.9rem;'>ULTIMATE WEAPON</div>
            <div class='art-avatar'>{w_info['art']}</div>
            <div style='font-size:1.3rem; font-weight:bold;'>+{st.session_state.weapon_lvl} {w_info['name']}</div>
            <div style='margin:6px 0; font-size:0.95rem;'>무기 ATK: <b>{get_weapon_atk()}</b></div>
            <div style='color:#ff007f; font-size:0.9rem;'>성공률: <b>{get_w_rate()}%</b> | 비용: <b>{get_w_cost():,} G</b></div>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("🔨 무기 초월 연마"):
        enhance_weapon()

st.markdown("---")

# 액션 던전 전장
st.subheader("👹 차원의 던전 탐험")

with st.expander("⚔️ 보스 및 몬스터 전투 개시", expanded=True):
    monster = random.choice(MONSTERS)
    w_art = WEAPON_DATA[st.session_state.weapon_tier]["art"]
    
    st.markdown(f"#### 👹 출현 몬스터: **[{monster['name']}]** {monster['art']}")
    st.caption(f"권장 공격력: {monster['req_atk']} ATK | 내 공격력: {get_total_atk()} ATK")
    
    skill = st.radio("⚔️ 전투 스킬 선택", ["기본 필살격", "🔥 엑스칼리버 (치명타 연타)"], horizontal=True)
    
    if st.button("🚀 공격 개시!", use_container_width=True):
        multiplier = 2.5 if "엑스칼리버" in skill else 1.0
        
        arena = st.empty()
        
        # 연속타 연출
        for phase in ["💥", "⚡", "🔥"]:
            arena.markdown(f"""
                <div class='battle-arena'>
                    <span class='art-avatar'>🦸‍♂️{w_art}</span>
                    <span style='font-size:2.8rem;'> {phase} </span>
                    <span class='art-avatar'>{monster['art']}</span>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(0.2)
        
        # 승패 결과 계산
        win_rate = min(95, max(10, int((get_total_atk() * multiplier / monster['req_atk']) * 70)))
        
        if random.randint(1, 100) <= win_rate:
            reward = monster['reward'] + random.randint(200, 800)
            st.session_state.gold += reward
            st.success(f"🎉 **CRITICAL VICTORY!** [{monster['name']}]을(를) 격파하고 {reward:,} Gold를 토벌했습니다!")
            st.session_state.log.append(f"🏆 [{monster['name']}] 처치! (+{reward:,} G)")
        else:
            penalty = random.randint(300, 800)
            st.session_state.gold = max(0, st.session_state.gold - penalty)
            st.error(f"☠️ **DEFEAT...** 몬스터의 치명타를 맞아 {penalty:,} Gold를 잃었습니다.")
            st.session_state.log.append(f"💀 [{monster['name']}] 사냥 실패... (-{penalty:,} G)")

# 보유 유물 디스플레이
if st.session_state.my_artifacts:
    st.markdown("---")
    st.subheader("🔮 장착 중인 유물 목록")
    art_cols = st.columns(len(st.session_state.my_artifacts))
    for idx, item in enumerate(st.session_state.my_artifacts):
        art_cols[idx % 4].info(f"{item['art']} {item['name']}\n(+{item['bonus_atk']} ATK)")

# 게임 데이터 관리
st.markdown("---")
if st.button("🔄 게임 데이터 리셋", use_container_width=True):
    st.session_state.clear()
    safe_rerun()

# 모험 로그
with st.expander("📜 모험 기록 일지", expanded=True):
    for log in reversed(st.session_state.log[-5:]):
        st.write(log)
