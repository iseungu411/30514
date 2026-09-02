import streamlit as st
import random
import time

# 웹 페이지 설정
st.set_page_config(page_title="Legendary Hero RPG: BEYOND", page_icon="⚔️", layout="centered")

# --- 🎨 극강의 사이버펑크 Visual & 애니메이션 CSS ---
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

    /* 카드 네온 스타일 */
    .hero-card {
        background: rgba(25, 15, 45, 0.7);
        border: 2px solid #00f0ff;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.3), inset 0 0 15px rgba(0, 240, 255, 0.15);
    }
    
    .weapon-card {
        background: rgba(25, 15, 45, 0.7);
        border: 2px solid #ff007f;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 25px rgba(255, 0, 127, 0.3), inset 0 0 15px rgba(255, 0, 127, 0.15);
    }

    .art-avatar {
        font-size: 4.5rem;
        filter: drop-shadow(0 0 20px rgba(255,255,255,0.5));
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

    /* 버튼 스타일링 */
    div.stButton > button {
        width: 100% !important;
        height: 55px !important;
        border-radius: 14px !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        background: linear-gradient(135deg, #2b1055 0%, #15082a 100%) !important;
        color: #00f0ff !important;
        border: 2px solid #00f0ff !important;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.3) !important;
        transition: all 0.2s ease-in-out !important;
    }
    div.stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.8) !important;
        background: linear-gradient(135deg, #00f0ff 0%, #ff007f 100%) !important;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# 안전한 Rerun
def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

# --- 🎶 웹 BGM & SFX 사운드 시스템 ---
def render_audio_player():
    st.sidebar.header("🎧 음향 시스템")
    bgm_on = st.sidebar.toggle("🎵 판타지 BGM 재생", value=True)
    
    if bgm_on:
        # 판타지 모험 루프 BGM
        bgm_url = "https://assets.mixkit.co/music/preview/mixkit-game-level-music-689.mp3"
        st.sidebar.components.v1.html(f"""
            <audio autoplay loop style="width: 100%; height: 30px;">
                <source src="{bgm_url}" type="audio/mpeg">
            </audio>
        """, height=40)

def play_sfx(sfx_type):
    sfx_urls = {
        "slash": "https://assets.mixkit.co/active_storage/sfx/212/212-preview.mp3",
        "skill": "https://assets.mixkit.co/active_storage/sfx/2019/2019-preview.mp3",
        "upgrade": "https://assets.mixkit.co/active_storage/sfx/1435/1435-preview.mp3",
        "defeat": "https://assets.mixkit.co/active_storage/sfx/2658/2658-preview.mp3"
    }
    if sfx_type in sfx_urls:
        st.components.v1.html(
            f'<audio autoplay style="display:none;"><source src="{sfx_urls[sfx_type]}" type="audio/mpeg"></audio>',
            height=0
        )

# --- ⚔️ 데이터 정의 ---
WEAPON_DATA = [
    {"name": "수련용 목검", "art": "🗡️", "base": 20},
    {"name": "기사의 강철검", "art": "⚔️", "base": 50},
    {"name": "플라즈마 세이버", "art": "🗡️⚡", "base": 100},
    {"name": "드래곤 슬레이어", "art": "⚔️🔥", "base": 200},
    {"name": "신멸의 차원창", "art": "🔱🌌", "base": 400}
]

MONSTERS = [
    {"name": "하급 슬라임", "art": "🟢", "hp": 120, "req_atk": 30, "reward": 300, "boss": False},
    {"name": "변종 고블린", "art": "👺", "hp": 280, "req_atk": 70, "reward": 800, "boss": False},
    {"name": "강철 오크", "art": "👹", "hp": 650, "req_atk": 150, "reward": 2200, "boss": False},
    {"name": "화염 군주 드래곤", "art": "🐉🔥", "hp": 1500, "req_atk": 320, "reward": 6000, "boss": True},
    {"name": "심연의 멸망자 마왕", "art": "👾⚡", "hp": 4000, "req_atk": 600, "reward": 20000, "boss": True}
]

# --- 🎮 데이터 초기화 ---
def init_game():
    st.session_state.hero_name = "아스날"
    st.session_state.hero_level = 1
    st.session_state.gold = 2000
    st.session_state.weapon_lvl = 0
    st.session_state.weapon_tier = 0
    st.session_state.protection_scrolls = 1
    st.session_state.log = ["✨ 차원의 문이 열렸습니다. 무기를 연마하세요!"]

if "gold" not in st.session_state:
    init_game()

# --- 📊 스탯 계산 ---
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

# --- 🔨 행동 로직 ---
def enhance_weapon():
    cost = get_w_cost()
    if st.session_state.gold < cost:
        st.toast("⚠️ 골드가 부족합니다!", icon="💰")
        return
    st.session_state.gold -= cost

    if random.randint(1, 100) <= get_w_rate():
        st.session_state.weapon_lvl += 1
        play_sfx("upgrade")
        if st.session_state.weapon_lvl % 4 == 0 and st.session_state.weapon_tier < len(WEAPON_DATA) - 1:
            st.session_state.weapon_tier += 1
            st.toast("🌟 무기가 신화 등급으로 진화했습니다!", icon="💎")
        st.session_state.log.append(f"⚔️ 무기 강화 성공! (+{st.session_state.weapon_lvl})")
    else:
        if st.session_state.protection_scrolls > 0 and st.session_state.weapon_lvl >= 5:
            st.session_state.protection_scrolls -= 1
            st.toast("🛡️ 파괴 방지권 발동! 단계 유지", icon="🛡️")
            st.session_state.log.append("🛡️ 강화 실패 (방지권 사용)")
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
    if st.session_state.gold >= 4000:
        st.session_state.gold -= 4000
        st.session_state.protection_scrolls += 1
        st.toast("📜 방지권 구매 완료!", icon="📜")
        safe_rerun()
    else:
        st.toast("⚠️ 골드가 부족합니다 (4,000 G 필요)", icon="💰")

# --- ⚔️ 스킬 선택 전투 모달 ---
@st.dialog("⚔️ BATTLE ARENA ⚔️")
def start_battle_modal():
    monster = random.choice(MONSTERS)
    w_art = WEAPON_DATA[st.session_state.weapon_tier]["art"]
    
    st.markdown(f"### 👹 **[{monster['name']}]** 등판!")
    st.caption(f"권장 공격력: {monster['req_atk']} | 내 공격력: {get_total_atk()}")
    
    # 공격 스킬 선택
    skill = st.radio("⚔️ 사용할 전투 스킬 선택", ["기본 공격 (안정적)", "🔥 엑스칼리버 (공격력 2.5배, 성공률 -15%)"], horizontal=True)
    
    hp_progress = st.progress(1.0)
    battle_display = st.empty()
    status_msg = st.empty()
    
    battle_display.markdown(f"""
        <div class='battle-arena'>
            <span class='art-avatar'>🦸‍♂️{w_art}</span>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ⚔️ VS ⚔️ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <span class='art-avatar'>{monster['art']}</span>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 공격 개시!", use_container_width=True):
        multiplier = 2.5 if "엑스칼리버" in skill else 1.0
        sfx_name = "skill" if "엑스칼리버" in skill else "slash"
        play_sfx(sfx_name)
        
        # 전투 연출
        for i in range(1, 4):
            damage = int(get_total_atk() * multiplier * random.uniform(0.3, 0.5))
            rem_hp = max(0, monster['hp'] - (damage * i))
            hp_progress.progress(rem_hp / monster['hp'])
            
            battle_display.markdown(f"""
                <div class='battle-arena'>
                    <span class='art-avatar' style='transform: scale(1.2);'>🦸‍♂️{w_art}</span>
                    <span style='font-size:3.5rem;'>💥⚡</span>
                    <span class='art-avatar'>{monster['art']}</span>
                </div>
            """, unsafe_allow_html=True)
            status_msg.warning(f"💥 {i}타 강격! {damage} 데미지 부여!")
            time.sleep(0.4)

        # 승패 판정
        penalty_rate = 15 if "엑스칼리버" in skill else 0
        win_rate = min(95, max(10, int((get_total_atk() * multiplier / monster['req_atk']) * 70) - penalty_rate))
        
        if random.randint(1, 100) <= win_rate:
            hp_progress.progress(0.0)
            reward = monster['reward'] + random.randint(100, 600)
            st.session_state.gold += reward
            play_sfx("upgrade")
            st.session_state.log.append(f"🏆 [{monster['name']}] 처치! (+{reward:,} G)")
            status_msg.success(f"🎉 승리! [{monster['name']}]을 격파하고 {reward:,} Gold를 획득했습니다!")
        else:
            penalty = random.randint(300, 700)
            st.session_state.gold = max(0, st.session_state.gold - penalty)
            play_sfx("defeat")
            st.session_state.log.append(f"💀 [{monster['name']}] 사냥 실패... (-{penalty:,} G)")
            status_msg.error(f"☠️ 패배! 몬스터의 치명타를 맞아 후퇴했습니다. (-{penalty:,} G)")

        time.sleep(1)
        safe_rerun()

# --- 🖥️ UI 레이아웃 ---
render_audio_player()

st.markdown("<h1 class='game-title'>⚔️ HERO RPG: BEYOND ⚔️</h1>", unsafe_allow_html=True)

# 사이드바
with st.sidebar:
    st.header("⚙️ 캐릭터 설정")
    new_name = st.text_input("히어로 이름", value=st.session_state.hero_name)
    if new_name != st.session_state.hero_name:
        st.session_state.hero_name = new_name
        safe_rerun()
        
    st.markdown("---")
    st.header("🛒 소모품 상점")
    st.write(f"📜 파괴 방지권: **{st.session_state.protection_scrolls}개**")
    if st.button("📜 방지권 구매 (4,000G)"):
        buy_protection()

# 스탯 메트릭
m1, m2, m3, m4 = st.columns(4)
m1.metric("💰 보유 골드", f"{st.session_state.gold:,} G")
m2.metric("⚔️ 총 공격력", f"{get_total_atk():,} ATK")
m3.metric("🦸 히어로", f"Lv.{st.session_state.hero_level}")
m4.metric("🛡️ 무기 연마", f"+{st.session_state.weapon_lvl}")

st.markdown("---")

# 카드 디스플레이
col_hero, col_weapon = st.columns(2)

with col_hero:
    st.markdown(f"""
        <div class='hero-card'>
            <div style='color:#00f0ff; font-weight:bold;'>HERO PROFILE</div>
            <div class='art-avatar'>🦸‍♂️</div>
            <div style='font-size:1.5rem; font-weight:bold;'>{st.session_state.hero_name}</div>
            <div style='margin:8px 0;'>히어로 ATK: <b>{get_hero_atk()}</b></div>
            <div style='color:#00f0ff;'>육성 비용: <b>{get_h_cost():,} G</b></div>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("💪 히어로 스탯 육성"):
        enhance_hero()

with col_weapon:
    w_info = WEAPON_DATA[st.session_state.weapon_tier]
    st.markdown(f"""
        <div class='weapon-card'>
            <div style='color:#ff007f; font-weight:bold;'>EQUIPPED WEAPON</div>
            <div class='art-avatar'>{w_info['art']}</div>
            <div style='font-size:1.5rem; font-weight:bold;'>+{st.session_state.weapon_lvl} {w_info['name']}</div>
            <div style='margin:8px 0;'>무기 ATK: <b>{get_weapon_atk()}</b></div>
            <div style='color:#ff007f;'>성공률: <b>{get_w_rate()}%</b> | 비용: <b>{get_w_cost():,} G</b></div>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("🔨 무기 초월 연마"):
        enhance_weapon()

st.markdown("---")

# 액션
st.subheader("👹 차원의 던전 탐험")
act_col1, act_col2 = st.columns(2)

with act_col1:
    if st.button("⚔️ 던전 사냥 입장", use_container_width=True):
        start_battle_modal()

with act_col2:
    if st.button("🔄 게임 데이터 리셋", use_container_width=True):
        init_game()
        safe_rerun()

# 로그
with st.expander("📜 모험 기록 일지", expanded=True):
    for log in reversed(st.session_state.log[-6:]):
        st.write(log)
