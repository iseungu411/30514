import streamlit as st
import random
import time

# 웹 페이지 기본 설정
st.set_page_config(page_title="NEON RPG: TRUE EVOLUTION", page_icon="⚔️", layout="centered")

# --- 🎨 Ultra Visual & Custom Graphics CSS ---
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
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(180deg, #ff007f 0%, #00f0ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(255, 0, 127, 0.7);
        margin-bottom: 10px;
    }

    .profile-card {
        background: rgba(25, 15, 45, 0.85);
        border: 2px solid #00f0ff;
        border-radius: 20px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.3);
    }
    
    .weapon-card-glow {
        background: rgba(25, 15, 45, 0.85);
        border: 2px solid #ff007f;
        border-radius: 20px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 0 20px rgba(255, 0, 127, 0.3);
    }

    .svg-container {
        width: 100%;
        height: 180px;
        display: flex;
        justify-content: center;
        align-items: center;
        background: rgba(0, 0, 0, 0.4);
        border-radius: 12px;
        margin-bottom: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .monster-container {
        width: 100%;
        height: 200px;
        display: flex;
        justify-content: center;
        align-items: center;
        background: radial-gradient(circle, rgba(255,0,127,0.2) 0%, rgba(10,0,20,0.8) 100%);
        border-radius: 15px;
        border: 2px solid #ff007f;
        margin-bottom: 10px;
    }

    div.stButton > button {
        width: 100% !important;
        height: 50px !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #2b1055 0%, #15082a 100%) !important;
        color: #00f0ff !important;
        border: 2px solid #00f0ff !important;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #00f0ff 0%, #ff007f 100%) !important;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

# --- 🎨 SVG 자원 (이미지 깨짐 방지 100% 자체 그래픽) ---
HERO_SVGS = [
    # 1단계: 초보 모험가
    '''<svg width="120" height="120" viewBox="0 0 100 100">
        <circle cx="50" cy="35" r="20" fill="#ffcc99"/>
        <path d="M 20 90 Q 50 50 80 90" fill="#78909C"/>
        <circle cx="43" cy="32" r="3" fill="#000"/><circle cx="57" cy="32" r="3" fill="#000"/>
        <path d="M 45 42 Q 50 45 55 42" stroke="#000" stroke-width="2" fill="none"/>
    </svg>''',
    # 2단계: 영웅 기사
    '''<svg width="120" height="120" viewBox="0 0 100 100">
        <path d="M 25 20 L 75 20 L 70 85 L 50 95 L 30 85 Z" fill="#37474F" stroke="#00f0ff" stroke-width="2"/>
        <rect x="35" y="35" width="30" height="8" fill="#00f0ff"/>
        <path d="M 15 40 L 30 25 L 30 75 Z" fill="#455A64"/>
        <path d="M 85 40 L 70 25 L 70 75 Z" fill="#455A64"/>
    </svg>''',
    # 3단계: 신화 오버로드
    '''<svg width="120" height="120" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="45" fill="none" stroke="#ff007f" stroke-width="3" stroke-dasharray="6,6"/>
        <path d="M 20 25 L 80 25 L 75 85 L 50 100 L 25 85 Z" fill="#1A237E" stroke="#00f0ff" stroke-width="3"/>
        <polygon points="50,15 60,35 40,35" fill="#ffd700"/>
        <circle cx="50" cy="55" r="12" fill="#ff007f"/>
    </svg>'''
]

WEAPON_SVGS = [
    # 1단계: 낡은 수련검
    '''<svg width="120" height="120" viewBox="0 0 100 100">
        <rect x="47" y="20" width="6" height="50" fill="#8D6E63"/>
        <rect x="35" y="70" width="30" height="6" fill="#5D4037"/>
        <rect x="47" y="76" width="6" height="15" fill="#3E2723"/>
        <path d="M 47 20 L 50 10 L 53 20 Z" fill="#795548"/>
    </svg>''',
    # 2단계: 영웅의 성검
    '''<svg width="120" height="120" viewBox="0 0 100 100">
        <path d="M 46 15 L 50 5 L 54 15 L 53 65 L 47 65 Z" fill="#ECEFF1" stroke="#FFD700" stroke-width="2"/>
        <path d="M 30 65 L 70 65 L 50 72 Z" fill="#FFD700"/>
        <rect x="46" y="72" width="8" height="18" fill="#37474F"/>
        <circle cx="50" cy="93" r="5" fill="#FFD700"/>
    </svg>''',
    # 3단계: 신화의 차원검
    '''<svg width="120" height="120" viewBox="0 0 100 100">
        <path d="M 45 10 L 50 0 L 55 10 L 54 60 L 46 60 Z" fill="#00f0ff" filter="drop-shadow(0 0 8px #00f0ff)"/>
        <path d="M 25 60 L 75 60 L 50 70 Z" fill="#ff007f"/>
        <rect x="46" y="70" width="8" height="20" fill="#1A237E"/>
        <circle cx="50" cy="50" r="25" fill="none" stroke="#ff007f" stroke-width="2"/>
    </svg>'''
]

MONSTER_SVGS = [
    # 심연의 슬라임
    '''<svg width="140" height="140" viewBox="0 0 100 100">
        <path d="M 20 80 Q 10 40 50 30 Q 90 40 80 80 Q 50 95 20 80 Z" fill="#00E676"/>
        <circle cx="40" cy="55" r="6" fill="#fff"/><circle cx="60" cy="55" r="6" fill="#fff"/>
        <circle cx="40" cy="55" r="3" fill="#000"/><circle cx="60" cy="55" r="3" fill="#000"/>
    </svg>''',
    # 화염 드래곤
    '''<svg width="140" height="140" viewBox="0 0 100 100">
        <path d="M 30 30 L 70 30 L 85 60 L 50 90 L 15 60 Z" fill="#D50000"/>
        <polygon points="50,10 35,30 65,30" fill="#FF6D00"/>
        <polygon points="20,20 10,50 30,40" fill="#FFD600"/>
        <polygon points="80,20 90,50 70,40" fill="#FFD600"/>
        <circle cx="40" cy="45" r="4" fill="#FFD600"/><circle cx="60" cy="45" r="4" fill="#FFD600"/>
    </svg>''',
    # 멸망의 마왕
    '''<svg width="140" height="140" viewBox="0 0 100 100">
        <path d="M 20 30 L 50 10 L 80 30 L 90 85 L 50 95 L 10 85 Z" fill="#311B92" stroke="#ff007f" stroke-width="2"/>
        <polygon points="20,30 5,5 30,20" fill="#AA00FF"/>
        <polygon points="80,30 95,5 70,20" fill="#AA00FF"/>
        <ellipse cx="50" cy="50" rx="15" ry="8" fill="#ff007f"/>
    </svg>'''
]

# --- ⚔️ 데이터 구조 정의 ---
HERO_TIERS = [
    {"title": "초보 모험가", "svg": HERO_SVGS[0]},
    {"title": "영웅 기사", "svg": HERO_SVGS[1]},
    {"title": "신화의 오버로드", "svg": HERO_SVGS[2]}
]

WEAPON_TIERS = [
    {"name": "낡은 수련검", "base": 25, "svg": WEAPON_SVGS[0]},
    {"name": "영웅의 성검", "base": 100, "svg": WEAPON_SVGS[1]},
    {"name": "신화의 차원검", "base": 300, "svg": WEAPON_SVGS[2]}
]

MONSTERS = [
    {"name": "심연의 슬라임", "req_atk": 40, "reward": 500, "svg": MONSTER_SVGS[0]},
    {"name": "지옥 화염 드래곤", "req_atk": 150, "reward": 2500, "svg": MONSTER_SVGS[1]},
    {"name": "멸망의 마왕 파괴신", "req_atk": 400, "reward": 10000, "svg": MONSTER_SVGS[2]}
]

# --- 🎮 세션 초기화 ---
if "gold" not in st.session_state:
    st.session_state.hero_name = "용사님"
    st.session_state.hero_level = 1
    st.session_state.gold = 3000
    st.session_state.weapon_lvl = 0
    st.session_state.protection_scrolls = 1
    st.session_state.log = ["✨ 차원의 문이 열렸습니다. 검과 영웅을 진화시켜 보세요!"]

# --- 📊 단계 및 스탯 계산 ---
def get_hero_tier_idx():
    if st.session_state.hero_level >= 10:
        return 2
    elif st.session_state.hero_level >= 5:
        return 1
    return 0

def get_weapon_tier_idx():
    if st.session_state.weapon_lvl >= 10:
        return 2
    elif st.session_state.weapon_lvl >= 5:
        return 1
    return 0

def get_hero_atk():
    return st.session_state.hero_level * 30

def get_weapon_atk():
    w_idx = get_weapon_tier_idx()
    return WEAPON_TIERS[w_idx]["base"] + (st.session_state.weapon_lvl * 25)

def get_total_atk():
    return get_hero_atk() + get_weapon_atk()

def get_w_cost():
    return (st.session_state.weapon_lvl + 1) * 300

def get_h_cost():
    return st.session_state.hero_level * 350

def get_w_rate():
    return max(15, 100 - (st.session_state.weapon_lvl * 5))

# --- 🔨 로직 ---
def enhance_weapon():
    cost = get_w_cost()
    if st.session_state.gold < cost:
        st.toast("⚠️ 골드가 부족합니다!", icon="💰")
        return
    st.session_state.gold -= cost

    if random.randint(1, 100) <= get_w_rate():
        st.session_state.weapon_lvl += 1
        st.toast(f"⚔️ 무기 강화 성공! (+{st.session_state.weapon_lvl})", icon="✨")
        st.session_state.log.append(f"⚔️ 무기 강화 성공! (+{st.session_state.weapon_lvl})")
    else:
        if st.session_state.protection_scrolls > 0 and st.session_state.weapon_lvl >= 5:
            st.session_state.protection_scrolls -= 1
            st.toast("🛡️ 방지권 사용으로 등급 유지!", icon="🛡️")
            st.session_state.log.append("🛡️ 강화 실패 (방지권 사용)")
        else:
            st.session_state.weapon_lvl = max(0, st.session_state.weapon_lvl - 1)
            st.toast("❌ 강화 실패...", icon="💀")
            st.session_state.log.append("❌ 무기 강화 실패! 단계 하락")
    safe_rerun()

def enhance_hero():
    cost = get_h_cost()
    if st.session_state.gold < cost:
        st.toast("⚠️ 골드가 부족합니다!", icon="💰")
        return
    st.session_state.gold -= cost
    st.session_state.hero_level += 1
    st.toast(f"🦸 레벨 업! (Lv.{st.session_state.hero_level})", icon="💪")
    st.session_state.log.append(f"🦸 {st.session_state.hero_name} 레벨 업 (Lv.{st.session_state.hero_level})")
    safe_rerun()

# --- 🎧 사이드바 ---
with st.sidebar:
    st.header("🎵 BGM 설정")
    bgm_on = st.toggle("배경음악 재생", value=True)
    if bgm_on:
        st.components.v1.html("""
            <audio autoplay loop style="width: 100%; height: 30px;">
                <source src="https://assets.mixkit.co/music/preview/mixkit-game-level-music-689.mp3" type="audio/mpeg">
            </audio>
        """, height=40)
    
    st.markdown("---")
    st.header("⚙️ 캐릭터 설정")
    new_name = st.text_input("용사 이름", value=st.session_state.hero_name)
    if new_name != st.session_state.hero_name:
        st.session_state.hero_name = new_name
        safe_rerun()

    st.markdown("---")
    st.header("🛒 상점")
    st.write(f"📜 파괴 방지권: **{st.session_state.protection_scrolls}개**")
    if st.button("📜 방지권 구매 (4,000G)"):
        if st.session_state.gold >= 4000:
            st.session_state.gold -= 4000
            st.session_state.protection_scrolls += 1
            st.toast("구매 완료!", icon="📜")
            safe_rerun()

# --- 🖥️ 메인 UI ---
st.markdown("<h1 class='game-title'>⚔️ HERO EVOLUTION ⚔️</h1>", unsafe_allow_html=True)

# 메트릭 대시보드
m1, m2, m3, m4 = st.columns(4)
m1.metric("💰 골드", f"{st.session_state.gold:,} G")
m2.metric("⚡ 총 공격력", f"{get_total_atk():,} ATK")
m3.metric("🦸 레벨", f"Lv.{st.session_state.hero_level}")
m4.metric("🛡️ 무기 연마", f"+{st.session_state.weapon_lvl}")

st.markdown("---")

# 진화 프로필
col_hero, col_weapon = st.columns(2)

hero_info = HERO_TIERS[get_hero_tier_idx()]
weapon_info = WEAPON_TIERS[get_weapon_tier_idx()]

with col_hero:
    st.markdown(f"""
        <div class='profile-card'>
            <div class='svg-container'>{hero_info['svg']}</div>
            <div style='color:#00f0ff; font-weight:bold;'>[{hero_info['title']}]</div>
            <div style='font-size:1.2rem; font-weight:bold;'>{st.session_state.hero_name}</div>
            <div style='margin:4px 0;'>히어로 ATK: <b>{get_hero_atk()}</b></div>
            <div style='color:#00f0ff;'>육성 비용: <b>{get_h_cost():,} G</b></div>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("💪 히어로 훈련"):
        enhance_hero()

with col_weapon:
    st.markdown(f"""
        <div class='weapon-card-glow'>
            <div class='svg-container'>{weapon_info['svg']}</div>
            <div style='color:#ff007f; font-weight:bold;'>EQUIPPED WEAPON</div>
            <div style='font-size:1.2rem; font-weight:bold;'>+{st.session_state.weapon_lvl} {weapon_info['name']}</div>
            <div style='margin:4px 0;'>무기 ATK: <b>{get_weapon_atk()}</b></div>
            <div style='color:#ff007f;'>성공률: <b>{get_w_rate()}%</b> | 비용: <b>{get_w_cost():,} G</b></div>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("🔨 무기 연마"):
        enhance_weapon()

st.markdown("---")

# --- 👹 던전 전투 시스템 (100% 그래픽 + SKIP) ---
st.subheader("👹 괴물 전장 탐험")

skip_battle = st.checkbox("⏩ 전투 연출 SKIP (빠른 진행)", value=False)

with st.expander("⚔️ 사냥터 입장", expanded=True):
    monster = random.choice(MONSTERS)
    
    st.markdown(f"#### 👹 출현 괴물: **[{monster['name']}]**")
    st.caption(f"권장 공격력: {monster['req_atk']} ATK | 내 공격력: {get_total_atk()} ATK")
    
    # 몬스터 자체 SVG 그래픽 출력
    st.markdown(f"<div class='monster-container'>{monster['svg']}</div>", unsafe_allow_html=True)
    
    skill = st.radio("⚔️ 스킬 선택", ["기본 공격", "🔥 엑스칼리버 (공격력 2.5배)"], horizontal=True)
    
    if st.button("🚀 전투 개시!", use_container_width=True):
        multiplier = 2.5 if "엑스칼리버" in skill else 1.0
        
        if not skip_battle:
            status_box = st.empty()
            status_box.info("⚔️ 몬스터와 격렬히 교전 중...")
            time.sleep(0.5)
            status_box.empty()
        
        # 승패 판정
        win_rate = min(95, max(10, int((get_total_atk() * multiplier / monster['req_atk']) * 70)))
        
        if random.randint(1, 100) <= win_rate:
            reward = monster['reward'] + random.randint(100, 500)
            st.session_state.gold += reward
            st.success(f"🎉 **VICTORY!** [{monster['name']}]을(를) 물리치고 {reward:,} Gold를 획득했습니다!")
            st.session_state.log.append(f"🏆 [{monster['name']}] 처치! (+{reward:,} G)")
        else:
            penalty = random.randint(300, 700)
            st.session_state.gold = max(0, st.session_state.gold - penalty)
            st.error(f"☠️ **DEFEAT...** 괴물의 반격으로 {penalty:,} Gold를 잃었습니다.")
            st.session_state.log.append(f"💀 [{monster['name']}] 사냥 실패... (-{penalty:,} G)")

# 게임 초기화
st.markdown("---")
if st.button("🔄 게임 데이터 초기화", use_container_width=True):
    st.session_state.clear()
    safe_rerun()

# 로그
with st.expander("📜 모험 기록 일지", expanded=True):
    for log in reversed(st.session_state.log[-5:]):
        st.write(log)
