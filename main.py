import streamlit as st
import random
import time

# 웹 페이지 레이아웃 & 아이콘 설정
st.set_page_config(page_title="Legendary Hero RPG: OVERLOAD", page_icon="⚔️", layout="centered")

# --- 🎨 극강의 사이버펑크 & 그래픽 CSS 스타일 ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;800;900&display=swap');

    .stApp {
        background: radial-gradient(circle at center, #121624 0%, #080911 100%);
        color: #ffffff;
        font-family: 'Segoe UI', Roboto, sans-serif;
    }
    
    .game-title {
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        font-size: 2.6rem;
        font-weight: 900;
        background: linear-gradient(180deg, #00f0ff 0%, #ff007f 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(0, 240, 255, 0.6);
        margin-bottom: 5px;
    }

    /* 네온 카드 패널 */
    .hero-card {
        background: rgba(18, 22, 36, 0.7);
        border: 2px solid #00f0ff;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.2), inset 0 0 15px rgba(0, 240, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .weapon-card {
        background: rgba(18, 22, 36, 0.7);
        border: 2px solid #ff007f;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 20px rgba(255, 0, 127, 0.2), inset 0 0 15px rgba(255, 0, 127, 0.1);
        backdrop-filter: blur(10px);
    }

    .art-avatar {
        font-size: 4rem;
        filter: drop-shadow(0 0 15px rgba(255,255,255,0.4));
        transition: transform 0.2s;
    }

    /* 전장 애니메이션 무대 */
    .battle-arena {
        background: linear-gradient(180deg, #1f082b 0%, #0a0212 100%);
        border: 3px solid #ff007f;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 0 30px rgba(255, 0, 127, 0.4);
    }

    /* 커스텀 버튼 커스터마이징 */
    div.stButton > button {
        width: 100% !important;
        height: 52px !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
        background: linear-gradient(135deg, #1e2640 0%, #111525 100%) !important;
        color: #00f0ff !important;
        border: 1px solid #00f0ff !important;
        transition: all 0.2s ease-in-out !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.6) !important;
        background: linear-gradient(135deg, #00f0ff 0%, #7928ca 100%) !important;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# 안전한 Rerun 지원
def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

# --- 🔊 브라우저 효과음 시스템 ---
def play_sfx(sfx_type):
    sfx_urls = {
        "slash": "https://assets.mixkit.co/active_storage/sfx/212/212-preview.mp3",
        "upgrade": "https://assets.mixkit.co/active_storage/sfx/1435/1435-preview.mp3",
        "defeat": "https://assets.mixkit.co/active_storage/sfx/2658/2658-preview.mp3"
    }
    if sfx_type in sfx_urls:
        st.components.v1.html(
            f'<audio autoplay style="display:none;"><source src="{sfx_urls[sfx_type]}" type="audio/mpeg"></audio>',
            height=0
        )

# --- ⚔️ 무기 데이터 ---
WEAPON_DATA = [
    {"name": "수련용 나무검", "art": "🗡️", "base": 15},
    {"name": "기사의 강철검", "art": "⚔️", "base": 40},
    {"name": "플라즈마 세이버", "art": "🗡️⚡", "base": 85},
    {"name": "드래곤 슬레이어", "art": "⚔️🔥", "base": 160},
    {"name": "신멸의 차원창", "art": "🔱🌌", "base": 300}
]

# --- 👹 몬스터 데이터 (패턴 및 보스 포함) ---
MONSTERS = [
    {"name": "하급 슬라임", "art": "🟢", "hp": 100, "req_atk": 25, "reward": 250, "boss": False},
    {"name": "변종 고블린", "art": "👺", "hp": 220, "req_atk": 60, "reward": 700, "boss": False},
    {"name": "강철 오크", "art": "👹", "hp": 500, "req_atk": 130, "reward": 1800, "boss": False},
    {"name": "화염 군주 드래곤", "art": "🐉🔥", "hp": 1200, "req_atk": 280, "reward": 5000, "boss": True},
    {"name": "심연의 멸망자 마왕", "art": "👾⚡", "hp": 3000, "req_atk": 500, "reward": 15000, "boss": True}
]

# --- 🎮 데이터 세션 초기화 ---
def init_game():
    st.session_state.hero_name = "아스날"
    st.session_state.hero_level = 1
    st.session_state.gold = 1500
    st.session_state.weapon_lvl = 0
    st.session_state.weapon_tier = 0
    st.session_state.protection_scrolls = 1  # 파괴 방지권
    st.session_state.ring_lvl = 0             # 보조 장신구
    st.session_state.log = ["✨ 전설의 모험가여, 아레나에 오신 것을 환영합니다!"]

if "gold" not in st.session_state:
    init_game()

# --- 📊 스탯 및 비용 계산 ---
def get_hero_atk():
    return st.session_state.hero_level * 20

def get_weapon_atk():
    w = WEAPON_DATA[st.session_state.weapon_tier]
    return w["base"] + (st.session_state.weapon_lvl * 15)

def get_ring_atk():
    return st.session_state.ring_lvl * 35

def get_total_atk():
    return get_hero_atk() + get_weapon_atk() + get_ring_atk()

def get_w_cost():
    return (st.session_state.weapon_lvl + 1) * 200

def get_h_cost():
    return st.session_state.hero_level * 250

def get_w_rate():
    return max(15, 100 - (st.session_state.weapon_lvl * 6))

# --- 🔨 강화/육성 행동 로직 ---
def enhance_weapon():
    cost = get_w_cost()
    if st.session_state.gold < cost:
        st.toast("⚠️ 골드가 부족합니다!", icon="💰")
        return
    st.session_state.gold -= cost

    rate = get_w_rate()
    if random.randint(1, 100) <= rate:
        st.session_state.weapon_lvl += 1
        play_sfx("upgrade")
        if st.session_state.weapon_lvl % 4 == 0 and st.session_state.weapon_tier < len(WEAPON_DATA) - 1:
            st.session_state.weapon_tier += 1
            st.toast("🌟 무기 외형과 등급이 초월 진화했습니다!", icon="💎")
        st.session_state.log.append(f"⚔️ 무기 강화 성공! (+{st.session_state.weapon_lvl})")
    else:
        # 방지권이 있는 경우
        if st.session_state.protection_scrolls > 0 and st.session_state.weapon_lvl >= 5:
            st.session_state.protection_scrolls -= 1
            st.toast("🛡️ 파괴 방지권이 소모되어 강화 단계가 유지되었습니다!", icon="🛡️")
            st.session_state.log.append("🛡️ 강화 실패 (방지권으로 단계 보존)")
        else:
            st.session_state.weapon_lvl = max(0, st.session_state.weapon_lvl - 1)
            play_sfx("defeat")
            st.session_state.log.append("❌ 무기 강화 실패! 단계 하락")
    safe_rerun()

def enhance_hero():
    cost = get_h_cost()
    if st.session_state.gold < cost:
        st.toast("⚠️ 골드가 부족합니다!", icon="💰")
        return
    st.session_state.gold -= cost
    st.session_state.hero_level += 1
    play_sfx("upgrade")
    st.session_state.log.append(f"🦸 {st.session_state.hero_name} 훈련 완료 (Lv.{st.session_state.hero_level})")
    safe_rerun()

def buy_protection():
    if st.session_state.gold >= 3000:
        st.session_state.gold -= 3000
        st.session_state.protection_scrolls += 1
        st.toast("📜 파괴 방지권을 구입했습니다!", icon="📜")
        safe_rerun()
    else:
        st.toast("⚠️ 골드가 부족합니다 (3,000 G 필요)", icon="💰")

# --- ⚔️ 실시간 연출 전투 모달 ---
@st.dialog("⚔️ BATTLE ARENA ⚔️")
def start_battle_modal():
    monster = random.choice(MONSTERS)
    w_art = WEAPON_DATA[st.session_state.weapon_tier]["art"]
    total_atk = get_total_atk()
    
    boss_tag = "🔥 [BOSS] " if monster["boss"] else ""
    st.markdown(f"### {boss_tag}**{monster['name']}** 과(와) 대치 중!")
    
    # HP 바 및 캐릭터 연출
    hp_progress = st.progress(1.0)
    battle_display = st.empty()
    status_msg = st.empty()
    
    # 1. 대치 화면
    battle_display.markdown(f"""
        <div class='battle-arena'>
            <span class='art-avatar'>🦸‍♂️{w_art}</span>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ⚔️ VS ⚔️ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <span class='art-avatar'>{monster['art']}</span>
        </div>
    """, unsafe_allow_html=True)
    status_msg.info("⚡ 전투 태세를 갖추고 있습니다...")
    time.sleep(0.8)
    
    # 2. 실시간 연타 공격 모션 (3회 타격 애니메이션)
    current_hp = monster["hp"]
    play_sfx("slash")
    
    for attack_round in range(1, 4):
        damage = int(total_atk * random.uniform(0.3, 0.5))
        current_hp = max(0, current_hp - damage)
        hp_ratio = current_hp / monster["hp"]
        
        hp_progress.progress(hp_ratio)
        battle_display.markdown(f"""
            <div class='battle-arena'>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                <span class='art-avatar' style='transform: translateX(30px);'>🦸‍♂️{w_art}</span>
                <span style='font-size:3rem;'>💥</span>
                <span class='art-avatar'>{monster['art']}</span>
            </div>
        """, unsafe_allow_html=True)
        status_msg.warning(f"💥 {attack_round}차 연타 공격! -{damage} DMG!")
        time.sleep(0.5)

    # 3. 승패 최종 결정
    win_rate = min(95, max(15, int((total_atk / monster["req_atk"]) * 70)))
    
    if random.randint(1, 100) <= win_rate:
        # 승리
        hp_progress.progress(0.0)
        battle_display.markdown(f"""
            <div class='battle-arena'>
                <span class='art-avatar'>🦸‍♂️{w_art}</span> 👑
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                <span style='font-size:3rem;'>💥💀</span>
            </div>
        """, unsafe_allow_html=True)
        
        reward = monster["reward"] + random.randint(100, 500)
        st.session_state.gold += reward
        play_sfx("upgrade")
        st.session_state.log.append(f"🎉 [{monster['name']}] 처치 완료! (+{reward:,} G)")
        status_msg.success(f"🏆 승리! [{monster['name']}]을 처치하고 {reward:,} Gold를 획득했습니다!")
    else:
        # 패배
        battle_display.markdown(f"""
            <div class='battle-arena'>
                <span style='font-size:3rem;'>💥💫🏃‍♂️</span>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                <span class='art-avatar'>{monster['art']}</span>😈
            </div>
        """, unsafe_allow_html=True)
        
        penalty = random.randint(200, 500)
        st.session_state.gold = max(0, st.session_state.gold - penalty)
        play_sfx("defeat")
        st.session_state.log.append(f"☠️ [{monster['name']}] 사냥 실패... (-{penalty:,} G)")
        status_msg.error(f"💀 패배... 몬스터의 반격에 부상을 입고 후퇴했습니다. (-{penalty:,} G)")

    if st.button("돌아가기", use_container_width=True):
        safe_rerun()

# --- 🖥️ 메인 대시보드 UI ---
st.markdown("<h1 class='game-title'>⚔️ HERO RPG: OVERLOAD ⚔️</h1>", unsafe_allow_html=True)

# 사이드바: 옵션 & 상점
with st.sidebar:
    st.header("⚙️ 히어로 프로필")
    new_name = st.text_input("히어로 이름", value=st.session_state.hero_name)
    if new_name != st.session_state.hero_name:
        st.session_state.hero_name = new_name
        safe_rerun()
        
    st.markdown("---")
    st.header("🛒 상점 & 소모품")
    st.write(f"📜 파괴 방지권: **{st.session_state.protection_scrolls}개**")
    if st.button("📜 방지권 구매 (3,000G)"):
        buy_protection()

# 최상단 메트릭 스탯
m1, m2, m3, m4 = st.columns(4)
m1.metric("💰 보유 골드", f"{st.session_state.gold:,} G")
m2.metric("⚔️ 총 공격력", f"{get_total_atk():,} ATK")
m3.metric("🦸 히어로", f"Lv.{st.session_state.hero_level}")
m4.metric("🛡️ 무기 강화", f"+{st.session_state.weapon_lvl}")

st.markdown("---")

# 히어로 & 무기 쇼케이스 카드
col_hero, col_weapon = st.columns(2)

with col_hero:
    st.markdown(f"""
        <div class='hero-card'>
            <div style='color:#00f0ff; font-weight:bold; font-size:0.85rem;'>HERO STATS</div>
            <div class='art-avatar'>🦸‍♂️</div>
            <div style='font-size:1.4rem; font-weight:bold; color:#fff;'>{st.session_state.hero_name}</div>
            <div style='margin:8px 0;'>순수 공격력: <b>{get_hero_atk()}</b></div>
            <div style='color:#00f0ff; font-size:0.95rem;'>훈련 비용: <b>{get_h_cost():,} G</b></div>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("💪 히어로 스탯 훈련"):
        enhance_hero()

with col_weapon:
    w_info = WEAPON_DATA[st.session_state.weapon_tier]
    st.markdown(f"""
        <div class='weapon-card'>
            <div style='color:#ff007f; font-weight:bold; font-size:0.85rem;'>EQUIPPED WEAPON</div>
            <div class='art-avatar'>{w_info['art']}</div>
            <div style='font-size:1.4rem; font-weight:bold; color:#fff;'>+{st.session_state.weapon_lvl} {w_info['name']}</div>
            <div style='margin:8px 0;'>무기 공격력: <b>{get_weapon_atk()}</b></div>
            <div style='color:#ff007f; font-size:0.95rem;'>성공률: <b>{get_w_rate()}%</b> | 비용: <b>{get_w_cost():,} G</b></div>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("🔨 무기 초월 강화"):
        enhance_weapon()

st.markdown("---")

# 👹 사냥터 및 액션 파트
st.subheader("👹 아레나 던전 탐험")
act_col1, act_col2 = st.columns(2)

with act_col1:
    if st.button("⚔️ 던전 사냥 입장", use_container_width=True):
        start_battle_modal()

with act_col2:
    if st.button("🔄 게임 데이터 리셋", use_container_width=True):
        init_game()
        safe_rerun()

# 활동 기록 로그
with st.expander("📜 모험 기록 일지", expanded=True):
    for log in reversed(st.session_state.log[-6:]):
        st.write(log)
