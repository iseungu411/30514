import streamlit as st
import random
import time

st.set_page_config(page_title="NEON RPG: BATTLE REVOLUTION", page_icon="⚔️", layout="centered")

# --- 🎨 Visual CSS ---
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
    }
    .profile-card, .weapon-card-glow {
        background: rgba(25, 15, 45, 0.85);
        border: 2px solid #00f0ff;
        border-radius: 20px;
        padding: 15px;
        text-align: center;
    }
    .weapon-card-glow { border-color: #ff007f; }
    .svg-container {
        width: 100%; height: 150px;
        display: flex; justify-content: center; align-items: center;
        background: rgba(0, 0, 0, 0.4); border-radius: 12px; margin-bottom: 10px;
    }
    .monster-container {
        width: 100%; height: 180px;
        display: flex; justify-content: center; align-items: center;
        background: radial-gradient(circle, rgba(255,0,127,0.2) 0%, rgba(10,0,20,0.8) 100%);
        border-radius: 15px; border: 2px solid #ff007f; margin-bottom: 10px;
    }
    .battle-box {
        background: rgba(10, 0, 20, 0.9);
        border: 2px solid #ff007f;
        border-radius: 15px;
        padding: 15px;
        margin-top: 10px;
    }
    div.stButton > button {
        width: 100% !important; height: 50px !important; border-radius: 12px !important;
        font-weight: 800 !important; background: linear-gradient(135deg, #2b1055 0%, #15082a 100%) !important;
        color: #00f0ff !important; border: 2px solid #00f0ff !important;
    }
    </style>
""", unsafe_allow_html=True)

def safe_rerun():
    if hasattr(st, "rerun"): st.rerun()
    elif hasattr(st, "experimental_rerun"): st.experimental_rerun()

# --- 🎨 SVG Graphic Resources ---
HERO_SVGS = [
    '''<svg width="100" height="100" viewBox="0 0 100 100"><circle cx="50" cy="35" r="20" fill="#ffcc99"/><path d="M 20 90 Q 50 50 80 90" fill="#78909C"/><circle cx="43" cy="32" r="3" fill="#000"/><circle cx="57" cy="32" r="3" fill="#000"/></svg>''',
    '''<svg width="100" height="100" viewBox="0 0 100 100"><path d="M 25 20 L 75 20 L 70 85 L 50 95 L 30 85 Z" fill="#37474F" stroke="#00f0ff" stroke-width="2"/><rect x="35" y="35" width="30" height="8" fill="#00f0ff"/></svg>''',
    '''<svg width="100" height="100" viewBox="0 0 100 100"><circle cx="50" cy="50" r="45" fill="none" stroke="#ff007f" stroke-width="3"/><path d="M 20 25 L 80 25 L 75 85 L 50 100 L 25 85 Z" fill="#1A237E" stroke="#00f0ff" stroke-width="3"/><polygon points="50,15 60,35 40,35" fill="#ffd700"/></svg>'''
]

WEAPON_SVGS = [
    '''<svg width="100" height="100" viewBox="0 0 100 100"><rect x="47" y="20" width="6" height="50" fill="#8D6E63"/><rect x="35" y="70" width="30" height="6" fill="#5D4037"/><rect x="47" y="76" width="6" height="15" fill="#3E2723"/></svg>''',
    '''<svg width="100" height="100" viewBox="0 0 100 100"><path d="M 46 15 L 50 5 L 54 15 L 53 65 L 47 65 Z" fill="#ECEFF1" stroke="#FFD700" stroke-width="2"/><path d="M 30 65 L 70 65 L 50 72 Z" fill="#FFD700"/></svg>''',
    '''<svg width="100" height="100" viewBox="0 0 100 100"><path d="M 45 10 L 50 0 L 55 10 L 54 60 L 46 60 Z" fill="#00f0ff" filter="drop-shadow(0 0 8px #00f0ff)"/><path d="M 25 60 L 75 60 L 50 70 Z" fill="#ff007f"/></svg>'''
]

MONSTER_SVGS = [
    '''<svg width="120" height="120" viewBox="0 0 100 100"><path d="M 20 80 Q 10 40 50 30 Q 90 40 80 80 Q 50 95 20 80 Z" fill="#00E676"/><circle cx="40" cy="55" r="5" fill="#fff"/><circle cx="60" cy="55" r="5" fill="#fff"/><circle cx="40" cy="55" r="2" fill="#000"/><circle cx="60" cy="55" r="2" fill="#000"/></svg>''',
    '''<svg width="120" height="120" viewBox="0 0 100 100"><path d="M 30 30 L 70 30 L 85 60 L 50 90 L 15 60 Z" fill="#D50000"/><polygon points="50,10 35,30 65,30" fill="#FF6D00"/><circle cx="40" cy="45" r="4" fill="#FFD600"/><circle cx="60" cy="45" r="4" fill="#FFD600"/></svg>''',
    '''<svg width="120" height="120" viewBox="0 0 100 100"><path d="M 20 30 L 50 10 L 80 30 L 90 85 L 50 95 L 10 85 Z" fill="#311B92" stroke="#ff007f" stroke-width="2"/><polygon points="20,30 5,5 30,20" fill="#AA00FF"/><polygon points="80,30 95,5 70,20" fill="#AA00FF"/><ellipse cx="50" cy="50" rx="15" ry="8" fill="#ff007f"/></svg>'''
]

# --- ⚔️ Data Definitions ---
HERO_TIERS = [{"title": "초보 모험가", "svg": HERO_SVGS[0]}, {"title": "영웅 기사", "svg": HERO_SVGS[1]}, {"title": "신화의 오버로드", "svg": HERO_SVGS[2]}]
WEAPON_TIERS = [{"name": "낡은 수련검", "base": 25, "svg": WEAPON_SVGS[0]}, {"name": "영웅의 성검", "base": 100, "svg": WEAPON_SVGS[1]}, {"name": "신화의 차원검", "base": 300, "svg": WEAPON_SVGS[2]}]

MONSTERS = [
    {"name": "심연의 점액 몬스터", "hp": 300, "atk": 35, "skill": "🤮 맹독 액체 분사", "reward": 600, "svg": MONSTER_SVGS[0]},
    {"name": "지옥 화염 드래곤", "hp": 800, "atk": 90, "skill": "🔥 브레스 대폭발", "reward": 3000, "svg": MONSTER_SVGS[1]},
    {"name": "멸망의 마왕 파괴신", "hp": 2000, "atk": 220, "skill": "⚡ 차원 붕괴 일격", "reward": 12000, "svg": MONSTER_SVGS[2]}
]

# --- 🎮 Session Initialization ---
if "gold" not in st.session_state:
    st.session_state.hero_name = "용사님"
    st.session_state.hero_level = 1
    st.session_state.gold = 3000
    st.session_state.weapon_lvl = 0
    st.session_state.protection_scrolls = 1
    st.session_state.log = ["✨ 새로운 모험이 시작되었습니다!"]

def get_hero_tier_idx(): return 2 if st.session_state.hero_level >= 10 else (1 if st.session_state.hero_level >= 5 else 0)
def get_weapon_tier_idx(): return 2 if st.session_state.weapon_lvl >= 10 else (1 if st.session_state.weapon_lvl >= 5 else 0)
def get_hero_atk(): return st.session_state.hero_level * 30
def get_weapon_atk(): return WEAPON_TIERS[get_weapon_tier_idx()]["base"] + (st.session_state.weapon_lvl * 25)
def get_total_atk(): return get_hero_atk() + get_weapon_atk()
def get_max_hp(): return 200 + (st.session_state.hero_level * 80)
def get_w_cost(): return (st.session_state.weapon_lvl + 1) * 300
def get_h_cost(): return st.session_state.hero_level * 350
def get_w_rate(): return max(15, 100 - (st.session_state.weapon_lvl * 5))

def enhance_weapon():
    if st.session_state.gold < get_w_cost():
        st.toast("⚠️ 골드가 부족합니다!", icon="💰")
        return
    st.session_state.gold -= get_w_cost()
    if random.randint(1, 100) <= get_w_rate():
        st.session_state.weapon_lvl += 1
        st.toast(f"⚔️ 무기 강화 성공! (+{st.session_state.weapon_lvl})", icon="✨")
    else:
        if st.session_state.protection_scrolls > 0 and st.session_state.weapon_lvl >= 5:
            st.session_state.protection_scrolls -= 1
            st.toast("🛡️ 방지권 사용으로 등급 유지!", icon="🛡️")
        else:
            st.session_state.weapon_lvl = max(0, st.session_state.weapon_lvl - 1)
            st.toast("❌ 강화 실패...", icon="💀")
    safe_rerun()

def enhance_hero():
    if st.session_state.gold < get_h_cost():
        st.toast("⚠️ 골드가 부족합니다!", icon="💰")
        return
    st.session_state.gold -= get_h_cost()
    st.session_state.hero_level += 1
    st.toast(f"🦸 레벨 업! (Lv.{st.session_state.hero_level})", icon="💪")
    safe_rerun()

# --- 🖥️ UI Layout ---
st.markdown("<h1 class='game-title'>⚔️ BATTLE REVOLUTION ⚔️</h1>", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
m1.metric("💰 골드", f"{st.session_state.gold:,} G")
m2.metric("⚡ 총 공격력", f"{get_total_atk():,} ATK")
m3.metric("🦸 히어로", f"Lv.{st.session_state.hero_level}")
m4.metric("🛡️ 검 강화", f"+{st.session_state.weapon_lvl}")

st.markdown("---")

col_hero, col_weapon = st.columns(2)
hero_info, weapon_info = HERO_TIERS[get_hero_tier_idx()], WEAPON_TIERS[get_weapon_tier_idx()]

with col_hero:
    st.markdown(f"<div class='profile-card'><div class='svg-container'>{hero_info['svg']}</div><b>[{hero_info['title']}] {st.session_state.hero_name}</b><br>HP: {get_max_hp()} | ATK: {get_hero_atk()}</div>", unsafe_allow_html=True)
    st.write("")
    if st.button("💪 히어로 훈련"): enhance_hero()

with col_weapon:
    st.markdown(f"<div class='weapon-card-glow'><div class='svg-container'>{weapon_info['svg']}</div><b>+{st.session_state.weapon_lvl} {weapon_info['name']}</b><br>ATK: {get_weapon_atk()} | 성공률: {get_w_rate()}%</div>", unsafe_allow_html=True)
    st.write("")
    if st.button("🔨 검 초월 연마"): enhance_weapon()

st.markdown("---")

# --- 👹 개선된 몬스터 실시간 전투 시스템 ---
st.subheader("👹 괴물 사냥터 (실시간 전투)")

skip_battle = st.checkbox("⏩ 전투 연출 SKIP (즉시 결과만 보기)", value=False)

if "selected_monster_idx" not in st.session_state:
    st.session_state.selected_monster_idx = 0

m_idx = st.selectbox("🎯 사냥할 괴물 선택", range(len(MONSTERS)), format_func=lambda x: MONSTERS[x]["name"])
monster = MONSTERS[m_idx]

st.markdown(f"<div class='monster-container'>{monster['svg']}</div>", unsafe_allow_html=True)
st.caption(f"👹 {monster['name']} | 체력: {monster['hp']} HP | 공격력: {monster['atk']} ATK | 필살기: {monster['skill']}")

skill_choice = st.radio("⚔️ 공격 기술 선택", ["기본 베기", "🔥 필살 차원참 (공격력 2배)"], horizontal=True)

if st.button("🚀 전투 개시!", use_container_width=True):
    hero_hp = get_max_hp()
    monster_hp = monster["hp"]
    atk_mult = 2.0 if "차원참" in skill_choice else 1.0
    hero_atk = int(get_total_atk() * atk_mult)
    
    st.markdown("<div class='battle-box'>", unsafe_allow_html=True)
    st.markdown("### 💥 전투 시뮬레이션 진행 중...")
    
    hero_bar = st.progress(1.0, text=f"🦸 용사 HP: {hero_hp}/{get_max_hp()}")
    monster_bar = st.progress(1.0, text=f"👹 {monster['name']} HP: {monster_hp}/{monster['hp']}")
    log_area = st.empty()
    
    battle_logs = []
    turn = 1
    
    while hero_hp > 0 and monster_hp > 0:
        # 1. 용사 공격
        is_crit = random.random() < 0.25
        damage_to_monster = int(hero_atk * (1.5 if is_crit else random.uniform(0.9, 1.1)))
        monster_hp = max(0, monster_hp - damage_to_monster)
        
        crit_str = "💥 **크리티컬 히트!!** " if is_crit else ""
        battle_logs.append(f"🗡️ [Turn {turn}] 용사의 일격! {crit_str}몬스터에게 {damage_to_monster} 피해!")
        
        if not skip_battle:
            monster_bar.progress(monster_hp / monster['hp'], text=f"👹 {monster['name']} HP: {monster_hp}/{monster['hp']}")
            log_area.markdown("<br>".join(battle_logs[-4:]), unsafe_allow_html=True)
            time.sleep(0.4)
            
        if monster_hp <= 0:
            break
            
        # 2. 몬스터 공격
        is_monster_skill = random.random() < 0.35
        m_atk = monster["atk"] * (1.6 if is_monster_skill else random.uniform(0.8, 1.1))
        damage_to_hero = int(m_atk)
        hero_hp = max(0, hero_hp - damage_to_hero)
        
        m_str = f"☠️ **{monster['skill']} 사용!** " if is_monster_skill else "🐾 Monster 공격! "
        battle_logs.append(f"👹 [Turn {turn}] {m_str} 용사에게 {damage_to_hero} 피해!")
        
        if not skip_battle:
            hero_bar.progress(hero_hp / get_max_hp(), text=f"🦸 용사 HP: {hero_hp}/{get_max_hp()}")
            log_area.markdown("<br>".join(battle_logs[-4:]), unsafe_allow_html=True)
            time.sleep(0.4)
            
        turn += 1

    # SKIP 모드일 경우 게이지 한 번에 갱신
    if skip_battle:
        hero_bar.progress(hero_hp / get_max_hp(), text=f"🦸 용사 HP: {hero_hp}/{get_max_hp()}")
        monster_bar.progress(monster_hp / monster['hp'], text=f"👹 {monster['name']} HP: {monster_hp}/{monster['hp']}")
        log_area.markdown("<br>".join(battle_logs[-5:]), unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # 승패 판정
    if monster_hp <= 0:
        reward = monster['reward'] + random.randint(100, 500)
        st.session_state.gold += reward
        st.success(f"🎉 **승리!** [{monster['name']}]을(를) 토벌하고 {reward:,} Gold를 획득했습니다!")
        st.session_state.log.append(f"🏆 [{monster['name']}] 토벌 성공 (+{reward:,} G)")
    else:
        penalty = random.randint(300, 600)
        st.session_state.gold = max(0, st.session_state.gold - penalty)
        st.error(f"☠️ **패배...** 괴물의 강렬한 공격에 패배하여 {penalty:,} Gold를 잃었습니다.")
        st.session_state.log.append(f"💀 [{monster['name']}] 사냥 실패 (-{penalty:,} G)")

st.markdown("---")
with st.expander("📜 최근 모험 일지"):
    for log in reversed(st.session_state.log[-5:]):
        st.write(log)
