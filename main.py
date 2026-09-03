import streamlit as st
import random
import time

st.set_page_config(page_title="NEON RPG: EXPANDED WORLD", page_icon="⚔️", layout="centered")

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
        width: 100%; height: 140px;
        display: flex; justify-content: center; align-items: center;
        background: rgba(0, 0, 0, 0.4); border-radius: 12px; margin-bottom: 10px;
    }
    .monster-container {
        width: 100%; height: 160px;
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
    '''<svg width="100" height="100" viewBox="0 0 100 100"><path d="M 46 15 L 50 5 L 54 15 L 53 65 L 47 65 Z" fill="#B0BEC5" stroke="#37474F" stroke-width="2"/><rect x="35" y="65" width="30" height="6" fill="#455A64"/></svg>''',
    '''<svg width="100" height="100" viewBox="0 0 100 100"><path d="M 45 15 L 50 5 L 55 15 L 53 65 L 47 65 Z" fill="#7E57C2" stroke="#00f0ff" stroke-width="2"/><circle cx="50" cy="40" r="4" fill="#00f0ff"/></svg>''',
    '''<svg width="100" height="100" viewBox="0 0 100 100"><path d="M 46 10 L 50 2 L 54 10 L 53 65 L 47 65 Z" fill="#66BB6A" stroke="#2E7D32" stroke-width="2"/><polygon points="40,65 60,65 50,72" fill="#A5D6A7"/></svg>''',
    '''<svg width="100" height="100" viewBox="0 0 100 100"><path d="M 46 15 L 50 5 L 54 15 L 53 65 L 47 65 Z" fill="#ECEFF1" stroke="#FFD700" stroke-width="2"/><path d="M 30 65 L 70 65 L 50 72 Z" fill="#FFD700"/></svg>''',
    '''<svg width="100" height="100" viewBox="0 0 100 100"><path d="M 40 10 L 50 0 L 60 10 L 56 65 L 44 65 Z" fill="#FF5722" stroke="#BF360C" stroke-width="2"/><rect x="30" y="65" width="40" height="8" fill="#D84315"/></svg>''',
    '''<svg width="100" height="100" viewBox="0 0 100 100"><path d="M 45 10 L 50 0 L 55 10 L 54 60 L 46 60 Z" fill="#00f0ff" filter="drop-shadow(0 0 8px #00f0ff)"/><path d="M 25 60 L 75 60 L 50 70 Z" fill="#ff007f"/></svg>''',
    '''<svg width="100" height="100" viewBox="0 0 100 100"><path d="M 42 5 L 50 -5 L 58 5 L 55 65 L 45 65 Z" fill="#FF007F" filter="drop-shadow(0 0 12px #FF007F)"/><polygon points="30,65 70,65 50,75" fill="#FFD700"/></svg>'''
]

MONSTER_SVGS = [
    '''<svg width="120" height="120" viewBox="0 0 100 100"><path d="M 20 80 Q 10 40 50 30 Q 90 40 80 80 Q 50 95 20 80 Z" fill="#00E676"/><circle cx="40" cy="55" r="5" fill="#fff"/><circle cx="60" cy="55" r="5" fill="#fff"/></svg>''',
    '''<svg width="120" height="120" viewBox="0 0 100 100"><circle cx="50" cy="50" r="35" fill="#8D6E63"/><polygon points="30,20 40,35 20,35" fill="#5D4037"/><polygon points="70,20 80,35 60,35" fill="#5D4037"/></svg>''',
    '''<svg width="120" height="120" viewBox="0 0 100 100"><path d="M 25 30 L 75 30 L 70 85 L 30 85 Z" fill="#78909C"/><ellipse cx="50" cy="45" rx="15" ry="8" fill="#FF1744"/></svg>''',
    '''<svg width="120" height="120" viewBox="0 0 100 100"><path d="M 20 20 L 80 20 L 70 90 L 30 90 Z" fill="#3E2723"/><line x1="30" y1="40" x2="70" y2="40" stroke="#FFD54F" stroke-width="4"/></svg>''',
    '''<svg width="120" height="120" viewBox="0 0 100 100"><path d="M 30 30 L 70 30 L 85 60 L 50 90 L 15 60 Z" fill="#D50000"/><polygon points="50,10 35,30 65,30" fill="#FF6D00"/></svg>''',
    '''<svg width="120" height="120" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="#29B6F6"/><path d="M 20 50 Q 50 20 80 50 Q 50 80 20 50 Z" fill="#0288D1"/></svg>''',
    '''<svg width="120" height="120" viewBox="0 0 100 100"><path d="M 20 30 L 50 10 L 80 30 L 90 85 L 50 95 L 10 85 Z" fill="#311B92" stroke="#ff007f" stroke-width="2"/><ellipse cx="50" cy="50" rx="15" ry="8" fill="#ff007f"/></svg>''',
    '''<svg width="120" height="120" viewBox="0 0 100 100"><polygon points="50,5 90,30 80,85 20,85 10,30" fill="#1A237E" stroke="#00f0ff" stroke-width="3"/><circle cx="50" cy="50" r="15" fill="#FF007F"/></svg>'''
]

# --- ⚔️ Data Definitions (확장된 무기 & 몬스터) ---
HERO_TIERS = [
    {"title": "초보 모험가", "svg": HERO_SVGS[0]},
    {"title": "영웅 기사", "svg": HERO_SVGS[1]},
    {"title": "신화의 오버로드", "svg": HERO_SVGS[2]}
]

# 🗡️ 확장된 검 데이터 (총 8종)
WEAPON_TIERS = [
    {"name": "낡은 수련검", "base": 25, "svg": WEAPON_SVGS[0]},
    {"name": "강철 장검", "base": 60, "svg": WEAPON_SVGS[1]},
    {"name": "룬 각인 검", "base": 110, "svg": WEAPON_SVGS[2]},
    {"name": "엘프의 명검", "base": 180, "svg": WEAPON_SVGS[3]},
    {"name": "영웅의 성검", "base": 280, "svg": WEAPON_SVGS[4]},
    {"name": "용살자의 대검", "base": 420, "svg": WEAPON_SVGS[5]},
    {"name": "차원 파괴검", "base": 600, "svg": WEAPON_SVGS[6]},
    {"name": "신화의 오버로드 블레이드", "base": 1000, "svg": WEAPON_SVGS[7]}
]

# 👹 확장된 몬스터 데이터 (총 8종)
MONSTERS = [
    {"name": "말랑 슬라임", "hp": 150, "atk": 15, "skill": "💦 액체 체벌", "reward": 200, "svg": MONSTER_SVGS[0]},
    {"name": "고블린 족장", "hp": 300, "atk": 35, "skill": "🪓 몽둥이 난타", "reward": 500, "svg": MONSTER_SVGS[1]},
    {"name": "저주받은 골렘", "hp": 650, "atk": 60, "skill": "🪨 암석 내려찍기", "reward": 1200, "svg": MONSTER_SVGS[2]},
    {"name": "지옥의 미노타우로스", "hp": 1200, "atk": 110, "skill": "🐂 붉은 뿔 돌진", "reward": 2500, "svg": MONSTER_SVGS[3]},
    {"name": "지옥 화염 드래곤", "hp": 2200, "atk": 180, "skill": "🔥 브레스 대폭발", "reward": 5000, "svg": MONSTER_SVGS[4]},
    {"name": "심연의 크라켄", "hp": 3800, "atk": 260, "skill": "🐙 해일 해저 조르기", "reward": 9000, "svg": MONSTER_SVGS[5]},
    {"name": "세계뱀 요르문간드", "hp": 6500, "atk": 380, "skill": "🐍 맹독 차원 수용돌이", "reward": 18000, "svg": MONSTER_SVGS[6]},
    {"name": "종말의 신 파괴자", "hp": 12000, "atk": 600, "skill": "⚡ 우주 멸망 일격", "reward": 40000, "svg": MONSTER_SVGS[7]}
]

# --- 🎮 Session Initialization ---
if "gold" not in st.session_state:
    st.session_state.hero_name = "용사님"
    st.session_state.hero_level = 1
    st.session_state.gold = 3000
    st.session_state.weapon_lvl = 0
    st.session_state.protection_scrolls = 1
    st.session_state.log = ["✨ 광활한 대륙의 새로운 모험이 시작되었습니다!"]

def get_hero_tier_idx(): 
    return 2 if st.session_state.hero_level >= 15 else (1 if st.session_state.hero_level >= 7 else 0)

def get_weapon_tier_idx():
    idx = st.session_state.weapon_lvl // 3
    return min(idx, len(WEAPON_TIERS) - 1)

def get_hero_atk(): return st.session_state.hero_level * 35
def get_weapon_atk(): return WEAPON_TIERS[get_weapon_tier_idx()]["base"] + (st.session_state.weapon_lvl * 30)
def get_total_atk(): return get_hero_atk() + get_weapon_atk()
def get_max_hp(): return 250 + (st.session_state.hero_level * 90)
def get_w_cost(): return (st.session_state.weapon_lvl + 1) * 350
def get_h_cost(): return st.session_state.hero_level * 400
def get_w_rate(): return max(10, 100 - (st.session_state.weapon_lvl * 4))

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
            st.toast("🛡️ 파괴 방지권 사용으로 등급 유지!", icon="🛡️")
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
m4.metric("🛡️ 무기 등급", f"+{st.session_state.weapon_lvl}")

st.markdown("---")

col_hero, col_weapon = st.columns(2)
hero_info = HERO_TIERS[get_hero_tier_idx()]
weapon_info = WEAPON_TIERS[get_weapon_tier_idx()]

with col_hero:
    st.markdown(f"<div class='profile-card'><div class='svg-container'>{hero_info['svg']}</div><b>[{hero_info['title']}] {st.session_state.hero_name}</b><br>HP: {get_max_hp():,} | ATK: {get_hero_atk():,}</div>", unsafe_allow_html=True)
    st.write("")
    if st.button("💪 히어로 스탯 단련"): enhance_hero()

with col_weapon:
    st.markdown(f"<div class='weapon-card-glow'><div class='svg-container'>{weapon_info['svg']}</div><b>+{st.session_state.weapon_lvl} {weapon_info['name']}</b><br>ATK: {get_weapon_atk():,} | 성공률: {get_w_rate()}%</div>", unsafe_allow_html=True)
    st.write("")
    if st.button("🔨 명검 초월 연마"): enhance_weapon()

st.markdown("---")

# --- 👹 대폭 확장된 몬스터 실시간 전투 시스템 ---
st.subheader("👹 광활한 대륙의 사냥터")

skip_battle = st.checkbox("⏩ 전투 연출 SKIP (즉시 결과만 보기)", value=False)

m_idx = st.selectbox(
    "🎯 도전할 괴물 선택", 
    range(len(MONSTERS)), 
    format_func=lambda x: f"[{x+1}단계] {MONSTERS[x]['name']} (권장 ATK: {MONSTERS[x]['hp']//3})"
)
monster = MONSTERS[m_idx]

st.markdown(f"<div class='monster-container'>{monster['svg']}</div>", unsafe_allow_html=True)
st.caption(f"👹 **{monster['name']}** | 체력: {monster['hp']:,} HP | 공격력: {monster['atk']:,} ATK | 필살기: {monster['skill']} | 보상: {monster['reward']:,} G")

skill_choice = st.radio("⚔️ 공격 전략 선택", ["기본 베기", "🔥 필살 차원참 (공격력 2.2배)"], horizontal=True)

if st.button("🚀 전투 시작!", use_container_width=True):
    hero_hp = get_max_hp()
    monster_hp = monster["hp"]
    atk_mult = 2.2 if "차원참" in skill_choice else 1.0
    hero_atk = int(get_total_atk() * atk_mult)
    
    st.markdown("<div class='battle-box'>", unsafe_allow_html=True)
    st.markdown("### 💥 치열한 격전 진행 중...")
    
    hero_bar = st.progress(1.0, text=f"🦸 용사 HP: {hero_hp:,}/{get_max_hp():,}")
    monster_bar = st.progress(1.0, text=f"👹 {monster['name']} HP: {monster_hp:,}/{monster['hp']:,}")
    log_area = st.empty()
    
    battle_logs = []
    turn = 1
    
    while hero_hp > 0 and monster_hp > 0:
        # 1. 용사 공격
        is_crit = random.random() < 0.25
        damage_to_monster = int(hero_atk * (1.6 if is_crit else random.uniform(0.9, 1.1)))
        monster_hp = max(0, monster_hp - damage_to_monster)
        
        crit_str = "💥 **크리티컬 회심의 일격!!** " if is_crit else ""
        battle_logs.append(f"🗡️ [Turn {turn}] 용사의 공격! {crit_str}몬스터에게 {damage_to_monster:,} 피해!")
        
        if not skip_battle:
            monster_bar.progress(monster_hp / monster['hp'], text=f"👹 {monster['name']} HP: {monster_hp:,}/{monster['hp']:,}")
            log_area.markdown("<br>".join(battle_logs[-4:]), unsafe_allow_html=True)
            time.sleep(0.35)
            
        if monster_hp <= 0:
            break
            
        # 2. 몬스터 공격
        is_monster_skill = random.random() < 0.35
        m_atk = monster["atk"] * (1.7 if is_monster_skill else random.uniform(0.8, 1.1))
        damage_to_hero = int(m_atk)
        hero_hp = max(0, hero_hp - damage_to_hero)
        
        m_str = f"☠️ **{monster['skill']} 발동!** " if is_monster_skill else "🐾 Monster의 반격! "
        battle_logs.append(f"👹 [Turn {turn}] {m_str} 용사에게 {damage_to_hero:,} 피해!")
        
        if not skip_battle:
            hero_bar.progress(hero_hp / get_max_hp(), text=f"🦸 용사 HP: {hero_hp:,}/{get_max_hp():,}")
            log_area.markdown("<br>".join(battle_logs[-4:]), unsafe_allow_html=True)
            time.sleep(0.35)
            
        turn += 1

    # SKIP 모드일 경우 즉시 반영
    if skip_battle:
        hero_bar.progress(hero_hp / get_max_hp(), text=f"🦸 용사 HP: {hero_hp:,}/{get_max_hp():,}")
        monster_bar.progress(monster_hp / monster['hp'], text=f"👹 {monster['name']} HP: {monster_hp:,}/{monster['hp']:,}")
        log_area.markdown("<br>".join(battle_logs[-5:]), unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # 승패 결과
    if monster_hp <= 0:
        reward = monster['reward'] + random.randint(100, 1000)
        st.session_state.gold += reward
        st.success(f"🎉 **토벌 성공!** [{monster['name']}]을(를) 물리치고 {reward:,} Gold를 획득했습니다!")
        st.session_state.log.append(f"🏆 [{monster['name']}] 토벌 (+{reward:,} G)")
    else:
        penalty = random.randint(400, 1500)
        st.session_state.gold = max(0, st.session_state.gold - penalty)
        st.error(f"☠️ **사망...** 괴물의 강력한 일격에 부상을 입고 {penalty:,} Gold 치료비를 지불했습니다.")
        st.session_state.log.append(f"💀 [{monster['name']}] 전투 패배 (-{penalty:,} G)")

st.markdown("---")
with st.expander("📜 최근 모험 기록"):
    for log in reversed(st.session_state.log[-5:]):
        st.write(log)
