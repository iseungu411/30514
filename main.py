import streamlit as st
import streamlit.components.v1 as components
import random
import time

st.set_page_config(page_title="NEON RPG: REBIRTH OVERDRIVE", page_icon="🌌", layout="centered")

# --- 🎨 Cyberpunk & High-End Neon Design CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=Noto+Sans+KR:wght@500;700;900&display=swap');

    .stApp {
        background: 
            radial-gradient(circle at 50% 20%, rgba(255, 0, 127, 0.35) 0%, transparent 60%),
            radial-gradient(circle at 80% 80%, rgba(0, 240, 255, 0.3) 0%, transparent 60%),
            linear-gradient(180deg, #050010 0%, #010003 100%);
        color: #ffffff;
        font-family: 'Noto Sans KR', sans-serif;
    }

    .game-title {
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        font-size: 2.8rem;
        font-weight: 900;
        letter-spacing: 5px;
        background: linear-gradient(180deg, #fff 0%, #ffd700 30%, #00f0ff 70%, #ff007f 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 35px rgba(0, 240, 255, 0.9), 0 0 20px rgba(255, 0, 127, 0.8);
        margin-bottom: 25px;
    }

    .profile-card, .weapon-card-glow {
        background: rgba(10, 2, 22, 0.88);
        backdrop-filter: blur(16px);
        border: 2px solid rgba(0, 240, 255, 0.8);
        border-radius: 20px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.4), inset 0 0 20px rgba(0, 240, 255, 0.2);
    }
    .weapon-card-glow { 
        border-color: rgba(255, 0, 127, 0.9); 
        box-shadow: 0 0 35px rgba(255, 0, 127, 0.5), inset 0 0 20px rgba(255, 0, 127, 0.25);
    }

    .svg-container {
        width: 100%; height: 140px;
        display: flex; justify-content: center; align-items: center;
        background: radial-gradient(circle, rgba(0, 240, 255, 0.2) 0%, rgba(0,0,0,0.95) 100%);
        border-radius: 14px; margin-bottom: 12px;
        border: 1px solid rgba(255, 215, 0, 0.4);
    }
    
    .battle-arena {
        background: radial-gradient(circle at center, rgba(50, 5, 80, 0.95) 0%, rgba(2, 0, 8, 0.99) 100%);
        border: 2px solid #ffd700;
        box-shadow: 0 0 50px rgba(255, 0, 127, 0.7), inset 0 0 30px rgba(0, 240, 255, 0.35);
        border-radius: 24px;
        padding: 22px;
        margin-top: 15px;
    }

    .battle-log-text {
        font-family: 'Orbitron', 'Noto Sans KR', sans-serif;
        font-size: 0.9rem;
        line-height: 1.6;
        background: rgba(0, 0, 0, 0.85);
        padding: 12px;
        border-radius: 10px;
        border: 1px solid rgba(255, 215, 0, 0.3);
    }

    .rebirth-box {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.35) 0%, rgba(255, 0, 127, 0.45) 100%);
        border: 3px solid #ffd700;
        box-shadow: 0 0 70px rgba(255, 215, 0, 0.9);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        margin-top: 20px;
    }
    
    div.stButton > button {
        width: 100% !important; height: 50px !important; border-radius: 14px !important;
        font-weight: 900 !important; font-size: 1.1rem !important;
        background: linear-gradient(135deg, #ff007f 0%, #7928ca 50%, #00f0ff 100%) !important;
        color: #ffffff !important; border: none !important;
        box-shadow: 0 0 25px rgba(255, 0, 127, 0.6) !important;
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 0 40px rgba(0, 240, 255, 1) !important;
    }
    </style>
""", unsafe_allow_html=True)

def safe_rerun():
    if hasattr(st, "rerun"): st.rerun()
    elif hasattr(st, "experimental_rerun"): st.experimental_rerun()

# --- ⚔️ 무기 SVG 라이브러리 ---
WEAPON_SVGS = [
    # 0. 단검
    '''<svg width="120" height="120" viewBox="0 0 100 100">
        <defs><linearGradient id="g0" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#b0bec5"/><stop offset="100%" stop-color="#37474f"/></linearGradient></defs>
        <path d="M50 15 L56 60 L50 65 L44 60 Z" fill="url(#g0)" stroke="#102027" stroke-width="1.5"/>
        <rect x="42" y="65" width="16" height="4" fill="#546e7a" rx="1"/>
        <rect x="47" y="69" width="6" height="18" fill="#37474f"/>
        <circle cx="50" cy="89" r="4" fill="#78909c"/>
    </svg>''',
    # 1. 장검
    '''<svg width="120" height="120" viewBox="0 0 100 100">
        <defs><linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#e0e0e0"/><stop offset="50%" stop-color="#9e9e9e"/><stop offset="100%" stop-color="#424242"/></linearGradient></defs>
        <path d="M50 8 L57 65 L50 72 L43 65 Z" fill="url(#g1)" stroke="#212121" stroke-width="1.5"/>
        <line x1="50" y1="12" x2="50" y2="65" stroke="#ffffff" stroke-width="1"/>
        <path d="M35 72 L65 72 L50 78 Z" fill="#757575"/>
        <rect x="47" y="78" width="6" height="16" fill="#212121"/>
    </svg>''',
    # 2. 룬 각인검
    '''<svg width="120" height="120" viewBox="0 0 100 100">
        <defs>
            <linearGradient id="g2" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#00e5ff"/><stop offset="100%" stop-color="#1a237e"/></linearGradient>
            <filter id="f2"><feGaussianBlur stdDeviation="2" result="coloredBlur"/><feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
        </defs>
        <path d="M50 5 L58 65 L50 72 L42 65 Z" fill="url(#g2)" stroke="#00b0ff" stroke-width="1.5"/>
        <path d="M50 15 L50 55" stroke="#ffffff" stroke-width="2" filter="url(#f2)"/>
        <polygon points="32,70 68,70 50,78" fill="#00b0ff" filter="url(#f2)"/>
        <circle cx="50" cy="40" r="4" fill="#ffffff" filter="url(#f2)"/>
    </svg>''',
    # 3. 엘프의 명검
    '''<svg width="120" height="120" viewBox="0 0 100 100">
        <defs>
            <linearGradient id="g3" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#b9f6ca"/><stop offset="50%" stop-color="#00e676"/><stop offset="100%" stop-color="#1b5e20"/></linearGradient>
            <filter id="f3"><feDropShadow dx="0" dy="0" stdDeviation="3" flood-color="#69f0ae"/></filter>
        </defs>
        <path d="M50 5 Q58 35 56 65 L50 72 Q42 35 44 65 Z" fill="url(#g3)" stroke="#00c853" stroke-width="1.5" filter="url(#f3)"/>
        <path d="M35 68 C45 68 45 78 50 82 C55 78 55 68 65 68 C55 74 45 74 35 68 Z" fill="#00e676"/>
        <rect x="47" y="82" width="6" height="14" fill="#2e7d32" rx="2"/>
    </svg>''',
    # 4. 영웅의 성검
    '''<svg width="120" height="120" viewBox="0 0 100 100">
        <defs>
            <linearGradient id="g4" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#fff59d"/><stop offset="50%" stop-color="#ffd700"/><stop offset="100%" stop-color="#ff6f00"/></linearGradient>
            <filter id="f4"><feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="#ffea00"/></filter>
        </defs>
        <path d="M50 2 L60 62 L50 70 L40 62 Z" fill="url(#g4)" stroke="#ffab00" stroke-width="1.5" filter="url(#f4)"/>
        <line x1="50" y1="8" x2="50" y2="60" stroke="#ffffff" stroke-width="2.5"/>
        <path d="M25 66 L75 66 L50 76 Z" fill="#ffc107" filter="url(#f4)"/>
        <polygon points="50,60 55,68 50,74 45,68" fill="#ffffff"/>
    </svg>''',
    # 5. 용살자의 대검
    '''<svg width="120" height="120" viewBox="0 0 100 100">
        <defs>
            <linearGradient id="g5" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#ff3d00"/><stop offset="50%" stop-color="#dd2c00"/><stop offset="100%" stop-color="#3e2723"/></linearGradient>
            <filter id="f5"><feDropShadow dx="0" dy="0" stdDeviation="5" flood-color="#ff3d00"/></filter>
        </defs>
        <path d="M46 2 L54 2 L62 60 L50 72 L38 60 Z" fill="url(#g5)" stroke="#bf360c" stroke-width="2" filter="url(#f5)"/>
        <path d="M48 10 L52 10 L55 55 L50 60 L45 55 Z" fill="#ff9e80"/>
        <path d="M22 62 L78 62 L50 75 Z" fill="#d50000" filter="url(#f5)"/>
        <circle cx="50" cy="68" r="5" fill="#ffeb3b"/>
    </svg>''',
    # 6. 차원 파괴검
    '''<svg width="120" height="120" viewBox="0 0 100 100">
        <defs>
            <linearGradient id="g6" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#00f0ff"/><stop offset="50%" stop-color="#7000ff"/><stop offset="100%" stop-color="#ff007f"/></linearGradient>
            <filter id="f6"><feGaussianBlur stdDeviation="3" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
        </defs>
        <path d="M50 0 L63 58 L50 68 L37 58 Z" fill="url(#g6)" stroke="#00f0ff" stroke-width="2" filter="url(#f6)"/>
        <polygon points="50,5 55,25 50,45 45,25" fill="#ffffff" filter="url(#f6)"/>
        <path d="M20 62 L80 62 L50 76 Z" fill="#7000ff" stroke="#00f0ff" stroke-width="1.5"/>
        <circle cx="50" cy="69" r="6" fill="#00f0ff" filter="url(#f6)"/>
    </svg>''',
    # 7. 🌌 신멸의 절망검
    '''<svg width="120" height="120" viewBox="0 0 100 100">
        <defs>
            <linearGradient id="g7" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#ffffff"/><stop offset="30%" stop-color="#ff007f"/><stop offset="70%" stop-color="#7000ff"/><stop offset="100%" stop-color="#00f0ff"/></linearGradient>
            <filter id="f7"><feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="#ff007f"/><feDropShadow dx="0" dy="0" stdDeviation="10" flood-color="#00f0ff"/></filter>
        </defs>
        <path d="M50 -5 L65 58 L50 70 L35 58 Z" fill="url(#g7)" filter="url(#f7)"/>
        <path d="M48 5 L52 5 L56 50 L50 58 L44 50 Z" fill="#ffffff"/>
        <polygon points="15,60 85,60 50,80" fill="#110022" stroke="#ffd700" stroke-width="2.5" filter="url(#f7)"/>
        <circle cx="50" cy="70" r="7" fill="#ffd700" filter="url(#f7)"/>
        <polygon points="50,20 54,28 50,36 46,28" fill="#00f0ff"/>
    </svg>'''
]

# --- 🦸 레벨별 용사 SVG 외형 (단계적 성장형) ---
def get_hero_svg(lvl):
    if lvl < 10:
        # 1. 초보 모험가 (소박한 천 옷 + 작은 투구)
        return '''<svg width="115" height="115" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="40" fill="none" stroke="#78909c" stroke-width="1.5"/>
            <path d="M30 85 L50 45 L70 85 Z" fill="#455a64"/>
            <circle cx="50" cy="38" r="16" fill="#ffe0b2"/>
            <path d="M36 28 C36 18 64 18 64 28 Z" fill="#78909c"/>
            <circle cx="44" cy="38" r="2" fill="#212121"/>
            <circle cx="56" cy="38" r="2" fill="#212121"/>
        </svg>'''
    elif lvl < 25:
        # 2. 숙련된 기사 (강철 갑옷 + 푸른 오라)
        return '''<svg width="115" height="115" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="42" fill="none" stroke="#00f0ff" stroke-width="2" stroke-dasharray="4 3"/>
            <path d="M25 85 L50 40 L75 85 Z" fill="#263238" stroke="#00b0ff" stroke-width="1.5"/>
            <circle cx="50" cy="36" r="18" fill="#eceff1"/>
            <polygon points="32,22 50,8 68,22" fill="#00e5ff"/>
            <rect x="42" y="32" width="16" height="4" fill="#00b0ff"/>
        </svg>'''
    elif lvl < 40:
        # 3. 전설의 챔피언 (황금 날개 + 붉은 성광)
        return '''<svg width="115" height="115" viewBox="0 0 100 100">
            <defs><filter id="hf1"><feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="#ffd700"/></filter></defs>
            <path d="M 10 50 Q -5 10 40 25 Z" fill="#ffd700" filter="url(#hf1)"/>
            <path d="M 90 50 Q 105 10 60 25 Z" fill="#ffd700" filter="url(#hf1)"/>
            <path d="M22 88 L50 35 L78 88 Z" fill="#37474f" stroke="#ffd700" stroke-width="2"/>
            <circle cx="50" cy="34" r="20" fill="#ffffff" filter="url(#hf1)"/>
            <polygon points="20,20 35,2 50,15 65,2 80,20" fill="#ffab00"/>
        </svg>'''
    else:
        # 4. 차원 절대신 (네온 후광 + 천상 빛나는 오라)
        return '''<svg width="115" height="115" viewBox="0 0 100 100">
            <defs>
                <filter id="hf2"><feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="#ff007f"/><feDropShadow dx="0" dy="0" stdDeviation="10" flood-color="#00f0ff"/></filter>
            </defs>
            <circle cx="50" cy="50" r="45" fill="none" stroke="#ffd700" stroke-width="2.5" filter="url(#hf2)"/>
            <path d="M 0 50 Q -20 -10 45 15 Z" fill="rgba(255,0,127,0.8)" filter="url(#hf2)"/>
            <path d="M 100 50 Q 120 -10 55 15 Z" fill="rgba(0,240,255,0.8)" filter="url(#hf2)"/>
            <path d="M18 90 L50 28 L82 90 Z" fill="#110022" stroke="#ff007f" stroke-width="2.5"/>
            <circle cx="50" cy="30" r="22" fill="#ffffff" filter="url(#hf2)"/>
            <polygon points="15,15 32,-5 50,10 68,-5 85,15" fill="#ffd700" filter="url(#hf2)"/>
        </svg>'''

def get_hero_title(lvl):
    if lvl < 10: return "초보 모험가"
    elif lvl < 20: return "숙련된 기사"
    elif lvl < 30: return "영웅 챔피언"
    elif lvl < 40: return "전설의 마스터"
    elif lvl < 50: return "신화의 오버로드"
    else: return "🌌 차원 절대신"

def get_weapon_info(lvl):
    names = [
        "녹슨 단검", "강철 장검", "룬 각인 검", "엘프의 명검", 
        "영웅의 성검", "용살자의 대검", "차원 파괴검", "🌌 신멸의 절망검"
    ]
    idx = min(lvl // 7, len(names) - 1)
    return {"name": names[idx], "svg": WEAPON_SVGS[idx]}

# 🔥 몬스터 스탯 난이도 대폭 강화
def get_monster_info(step):
    prefix = ["말랑", "흉폭한", "저주받은", "심연의", "지옥의", "우주의", "멸망의", "절대"]
    base_names = ["슬라임", "고블린", "골렘", "미노타우로스", "드래곤", "크라켄", "요르문간드", "파괴자"]
    
    if step == 50:
        return {
            "name": "👑 [FINAL BOSS] 종말의 창조신 파괴자",
            "hp": 8500000,   # 체력 상향
            "atk": 12000,    # 공격력 상향
            "skill": "⚡ 우주 멸망 소멸 포격",
            "reward": 3000000
        }
    
    p_idx = min((step - 1) // 7, len(prefix) - 1)
    b_idx = min((step - 1) // 7, len(base_names) - 1)
    
    name = f"{prefix[p_idx]} {base_names[b_idx]} (Lv.{step})"
    # 🔥 배율을 1.20 -> 1.28 로 높여 몬스터 체력 및 공격력 대폭 상향
    hp = int(450 * (1.28 ** step))
    atk = int(35 * (1.16 ** step))
    reward = int(500 * (1.25 ** step))
    
    return {"name": name, "hp": hp, "atk": atk, "skill": "💥 강격 파동", "reward": reward}

# --- 💾 Session State 초기화 ---
if "gold" not in st.session_state:
    st.session_state.hero_name = "용사님"
    st.session_state.hero_level = 1
    st.session_state.gold = 10000
    st.session_state.weapon_lvl = 0
    st.session_state.rebirth_count = 0
    st.session_state.selected_step = 1
    st.session_state.log = ["✨ 50단계 신화 모험이 시작되었습니다!"]

# --- 🌟 환생 스탯 계산식 ---
def get_gold_multiplier():
    return 1.0 + (st.session_state.rebirth_count * 0.10)

def get_rebirth_atk_bonus():
    return 1.0 + (st.session_state.rebirth_count * 0.20)

def get_hero_atk(): 
    base = st.session_state.hero_level * 1000
    return int(base * get_rebirth_atk_bonus())

def get_weapon_atk(): 
    if st.session_state.weapon_lvl == 0: return 0
    base = int(800 * (1.123 ** st.session_state.weapon_lvl))
    return int(base * get_rebirth_atk_bonus())

def get_total_atk(): return get_hero_atk() + get_weapon_atk()
def get_max_hp(): return 800 + (st.session_state.hero_level * 344)

def get_w_cost(): return int(350 * (1.18 ** st.session_state.weapon_lvl))
def get_h_cost(): return int(400 * (1.15 ** st.session_state.hero_level))

def get_w_rate(): 
    if st.session_state.weapon_lvl >= 49:
        return 1.0
    return max(5.0, 100.0 - (st.session_state.weapon_lvl * 1.95))

# 🎯 레벨 및 스탯 맞춤형 몬스터 추천 알고리즘
def recommend_monster_step():
    total_atk = get_total_atk()
    max_hp = get_max_hp()
    
    recommended = 1
    for s in range(1, 51):
        m = get_monster_info(s)
        # 몬스터를 4~6턴 안에 처치할 수 있는 수준이 가장 알맞은 도전 단계
        turns_to_kill = m["hp"] / (total_atk * 1.2)
        turns_to_die = max_hp / max(1, m["atk"])
        
        if turns_to_kill <= 6 and turns_to_die >= 3:
            recommended = s
        else:
            break
            
    st.session_state.selected_step = recommended
    st.toast(f"🎯 AI 추천: Lv.{recommended} 몬스터가 현재 스탯에 가장 적합합니다!", icon="🤖")

# 🔄 환생 수행
def do_rebirth():
    st.session_state.rebirth_count += 1
    st.session_state.hero_level = 1
    st.session_state.weapon_lvl = 0
    st.session_state.gold = 10000
    st.session_state.selected_step = 1
    
    relic_names = [
        "🔮 태초의 차원 구슬 (골드 +10%, ATK +20%)",
        "🔱 차원의 왕관 (골드 +20%, ATK +40%)",
        "💎 신멸의 성 결정 (골드 +30%, ATK +60%)",
        "👑 오버로드 절대 룬 (골드 +40%, ATK +80%)"
    ]
    current_relic = relic_names[min(st.session_state.rebirth_count - 1, len(relic_names) - 1)]
    
    st.session_state.log.append(f"🔄 [{st.session_state.rebirth_count}회차 환생] 차원 초월 완료! {current_relic} 해금!")
    st.toast(f"🔄 환생 완료! {st.session_state.rebirth_count}회차 초월 스탯이 영구 적용됩니다.", icon="✨")
    safe_rerun()

def enhance_weapon():
    if st.session_state.weapon_lvl >= 50:
        st.toast("👑 검이 이미 최고 단계(50단계)에 도달했습니다!", icon="⭐")
        return
    if st.session_state.gold < get_w_cost():
        st.toast("⚠️ 골드가 부족합니다!", icon="💰")
        return
    
    st.session_state.gold -= get_w_cost()
    rate = get_w_rate()
    
    if random.uniform(0, 100) <= rate:
        st.session_state.weapon_lvl += 1
        st.toast(f"⚔️ 무기 강화 성공! (+{st.session_state.weapon_lvl})", icon="✨")
    else:
        if st.session_state.weapon_lvl >= 10:
            st.session_state.weapon_lvl -= 1
            st.toast("💥 강화 실패! 무기 등급이 -1 하락했습니다!", icon="⚠️")
        else:
            st.toast("❌ 강화 실패! (등급 유지)", icon="🛡️")
    safe_rerun()

def enhance_hero():
    if st.session_state.hero_level >= 50:
        st.toast("👑 용사가 이미 최고 레벨(50단계)에 도달했습니다!", icon="⭐")
        return
    if st.session_state.gold < get_h_cost():
        st.toast("⚠️ 골드가 부족합니다!", icon="💰")
        return
    st.session_state.gold -= get_h_cost()
    st.session_state.hero_level += 1
    st.toast(f"🦸 레벨 업! (Lv.{st.session_state.hero_level})", icon="💪")
    safe_rerun()

# --- 🎨 2D Canvas Battle Engine ---
def render_canvas_battle(hero_name, monster_name, monster_step, is_ultimate, damage, is_hero_turn, hero_level, render_id):
    is_final_boss = (monster_step == 50)
    
    html_code = f"""
    <div style="text-align: center;">
        <canvas id="battleCanvas_{render_id}" width="600" height="230" style="border-radius:15px; border:2px solid { "#ffd700" if is_final_boss else "#00f0ff" }; background: linear-gradient(180deg, #090017 0%, #010005 100%); box-shadow: 0 0 35px { "rgba(255, 215, 0, 0.9)" if is_final_boss else "rgba(0, 240, 255, 0.5)" };"></canvas>
    </div>
    <script>
    (function() {{
        const canvas = document.getElementById('battleCanvas_{render_id}');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        let frame = 0;
        
        let heroX = 90;
        let monsterX = 470;
        let isFinalBoss = { 'true' if is_final_boss else 'false' };
        let mStep = {monster_step};
        let isUlt = { 'true' if is_ultimate else 'false' };
        let isHeroTurn = { 'true' if is_hero_turn else 'false' };
        let hLvl = {hero_level};

        function animate() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            if (isUlt && isHeroTurn && frame >= 10 && frame <= 20) {{
                let shakeX = (Math.random() - 0.5) * 16;
                let shakeY = (Math.random() - 0.5) * 16;
                ctx.setTransform(1, 0, 0, 1, shakeX, shakeY);
            }} else {{
                ctx.setTransform(1, 0, 0, 1, 0, 0);
            }}

            ctx.strokeStyle = isFinalBoss ? 'rgba(255, 215, 0, 0.2)' : 'rgba(0, 240, 255, 0.1)';
            ctx.lineWidth = 1;
            for(let x=0; x<canvas.width; x+=30) {{ ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,canvas.height); ctx.stroke(); }}
            for(let y=0; y<canvas.height; y+=30) {{ ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(canvas.width,y); ctx.stroke(); }}
            
            let hX = heroX;
            let mX = monsterX;
            let strike = false;
            
            if (isHeroTurn) {{
                if (frame < 10) hX += frame * 18;
                else if (frame < 20) {{ hX = 370; strike = true; mX += Math.sin(frame)*14; }}
                else hX -= (frame - 20) * 18;
            }} else {{
                if (frame < 10) mX -= frame * 18;
                else if (frame < 20) {{ mX = 190; strike = true; hX += Math.sin(frame)*14; }}
                else mX += (frame - 20) * 18;
            }}
            
            // 용사 외형 (레벨에 따라 진화)
            ctx.save();
            if (hLvl >= 25) {{
                ctx.save();
                ctx.translate(hX, 115);
                ctx.rotate(frame * 0.04);
                ctx.strokeStyle = hLvl >= 40 ? 'rgba(255, 0, 127, 0.7)' : 'rgba(0, 240, 255, 0.5)';
                ctx.lineWidth = 2;
                ctx.beginPath(); ctx.arc(0, 0, 42, 0, Math.PI*2); ctx.stroke();
                ctx.restore();
            }}

            // 레벨별 날개/오라 이펙트
            if (hLvl >= 10) {{
                ctx.fillStyle = hLvl >= 40 ? 'rgba(255, 0, 127, 0.6)' : 'rgba(0, 240, 255, 0.4)';
                ctx.beginPath();
                ctx.moveTo(hX, 115); ctx.lineTo(hX - 55, 60); ctx.lineTo(hX - 25, 110);
                ctx.moveTo(hX, 115); ctx.lineTo(hX + 55, 60); ctx.lineTo(hX + 25, 110);
                ctx.fill();
            }}

            ctx.shadowColor = hLvl >= 40 ? '#ff007f' : '#00f0ff';
            ctx.shadowBlur = 20 + hLvl;
            ctx.fillStyle = '#ffffff';
            ctx.beginPath(); ctx.arc(hX, 115, 20 + (hLvl > 30 ? 6 : 0), 0, Math.PI*2); ctx.fill();
            
            // 왕관/투구
            if (hLvl >= 20) {{
                ctx.fillStyle = '#ffd700'; ctx.shadowColor = '#ffd700'; ctx.shadowBlur = 15;
                ctx.beginPath();
                ctx.moveTo(hX - 20, 95); ctx.lineTo(hX - 10, 72); ctx.lineTo(hX, 86); ctx.lineTo(hX + 10, 72); ctx.lineTo(hX + 20, 95);
                ctx.closePath(); ctx.fill();
            }}
            
            ctx.fillStyle = '#fff'; ctx.font = 'bold 12px Orbitron'; ctx.fillText('{hero_name}', hX - 25, 162);
            ctx.restore();
            
            // 몬스터
            ctx.save();
            if (isFinalBoss) {{
                let size = 58 + Math.sin(frame*0.2)*8;
                ctx.strokeStyle = '#ffd700'; ctx.lineWidth = 5; ctx.shadowColor = '#ff0055'; ctx.shadowBlur = 50;
                ctx.beginPath(); ctx.arc(mX, 115, size, 0, Math.PI*2); ctx.stroke();
                ctx.fillStyle = '#110022'; ctx.fillRect(mX - 35, 115 - 35, 70, 70);
                ctx.fillStyle = '#ff0055'; ctx.beginPath(); ctx.arc(mX, 115, 20, 0, Math.PI*2); ctx.fill();
            }} else {{
                ctx.fillStyle = mStep >= 25 ? '#ff007f' : '#a100ff';
                ctx.shadowColor = '#a100ff'; ctx.shadowBlur = 15;
                let boxSize = 38 + Math.min(mStep, 50) * 0.5;
                ctx.fillRect(mX - boxSize/2, 115 - boxSize/2, boxSize, boxSize);
            }}
            ctx.fillStyle = '#fff'; ctx.font = 'bold 12px Orbitron'; ctx.fillText('{monster_name}', mX - 40, 165);
            ctx.restore();
            
            // 타격 이펙트
            if (strike) {{
                ctx.save();
                if (isHeroTurn) {{
                    if (isUlt) {{
                        ctx.strokeStyle = '#ffd700'; ctx.shadowColor = '#ffd700'; ctx.shadowBlur = 45; ctx.lineWidth = 14;
                        ctx.beginPath(); ctx.moveTo(mX - 70, 45); ctx.lineTo(mX + 70, 185); ctx.stroke();
                        ctx.beginPath(); ctx.moveTo(mX + 70, 45); ctx.lineTo(mX - 70, 185); ctx.stroke();
                    }} else {{
                        ctx.strokeStyle = '#00f0ff'; ctx.shadowColor = '#00f0ff'; ctx.shadowBlur = 25; ctx.lineWidth = 8;
                        ctx.beginPath(); ctx.moveTo(mX - 45, 65); ctx.lineTo(mX + 45, 165); ctx.stroke();
                    }}
                }} else {{
                    ctx.strokeStyle = '#ff007f'; ctx.shadowColor = '#ff007f'; ctx.shadowBlur = 20; ctx.lineWidth = 7;
                    ctx.beginPath(); ctx.moveTo(hX + 35, 65); ctx.lineTo(hX - 35, 165); ctx.stroke();
                }}
                
                ctx.fillStyle = isUlt ? '#ffd700' : '#ffff00';
                ctx.font = '900 30px Orbitron';
                let txtX = isHeroTurn ? mX : hX;
                ctx.fillText('-' + damage.toLocaleString(), txtX - 35, 40);
                ctx.restore();
            }}
            
            frame++;
            if (frame < 28) requestAnimationFrame(animate);
        }}
        animate();
    }})();
    </script>
    """
    return html_code

# --- 🖥️ UI Layout ---
st.markdown("<h1 class='game-title'>🌌 REBIRTH OVERDRIVE 🌌</h1>", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
m1.metric("💰 골드", f"{st.session_state.gold:,} G", f"버프 +{int((get_gold_multiplier()-1)*100)}%")
m2.metric("⚡ 총 공격력", f"{get_total_atk():,} ATK", f"환생 +{int((get_rebirth_atk_bonus()-1)*100)}%")
m3.metric("🦸 용사 단계", f"Lv.{st.session_state.hero_level} / 50")
m4.metric("🔄 환생 횟수", f"{st.session_state.rebirth_count} 회차")

st.markdown("---")

col_hero, col_weapon = st.columns(2)
w_info = get_weapon_info(st.session_state.weapon_lvl)

with col_hero:
    st.markdown(f"""
    <div class='profile-card'>
        <div class='svg-container'>
            {get_hero_svg(st.session_state.hero_level)}
        </div>
        <b>[{get_hero_title(st.session_state.hero_level)}] {st.session_state.hero_name}</b><br>
        HP: {get_max_hp():,} | ATK: {get_hero_atk():,}
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button(f"💪 용사 훈련 (비용: {get_h_cost():,}G)"): enhance_hero()

with col_weapon:
    st.markdown(f"""
    <div class='weapon-card-glow'>
        <div class='svg-container'>
            {w_info['svg']}
        </div>
        <b>+{st.session_state.weapon_lvl} {w_info['name']}</b><br>
        ATK: {get_weapon_atk():,} | 성공률: {get_w_rate():.1f}%
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button(f"🔨 검 강화 (비용: {get_w_cost():,}G)"): enhance_weapon()

st.markdown("---")

# --- 👹 전투 아레나 ---
st.subheader("⚔️ 50단계 실시간 격투 아레나")

skip_battle = st.checkbox("⏩ 전투 연출 SKIP (즉시 계산)", value=False)

# 몬스터 단계 선택 및 AI 추천
c_step1, c_step2 = st.columns([3, 1])
with c_step1:
    m_step = st.slider("🎯 사냥할 괴물 단계 선택 (1 ~ 50단계)", 1, 50, key="selected_step")
with c_step2:
    st.write("")
    if st.button("🤖 AI 추천 도전"):
        recommend_monster_step()
        safe_rerun()

monster = get_monster_info(m_step)

st.markdown(f"**상대 Monster**: <span style='color:#ff007f; font-weight:bold;'>{monster['name']}</span> | HP: {monster['hp']:,} | ATK: {monster['atk']:,}", unsafe_allow_html=True)

if st.button("⚡ 전투 개시!", use_container_width=True):
    hero_hp = get_max_hp()
    monster_hp = monster["hp"]
    base_atk = get_total_atk()
    
    st.markdown("<div class='battle-arena'>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"<h4 style='color:#00f0ff; text-align:center;'>🦸 {st.session_state.hero_name}</h4>", unsafe_allow_html=True)
        hero_bar = st.progress(1.0, text=f"HP: {hero_hp:,} / {get_max_hp():,}")
    with col_b:
        st.markdown(f"<h4 style='color:#ff007f; text-align:center;'>👹 {monster['name']}</h4>", unsafe_allow_html=True)
        monster_bar = st.progress(1.0, text=f"HP: {monster_hp:,} / {monster['hp']:,}")
    
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin:10px 0;'>", unsafe_allow_html=True)
    
    canvas_box = st.empty()
    status_display = st.empty()
    battle_log_box = st.empty()
    
    battle_logs = []
    turn = 1
    
    while hero_hp > 0 and monster_hp > 0:
        is_ultimate = (turn % 4 == 0)
        
        # 1. 용사 공격
        if is_ultimate:
            atk_mult = 3.0
            skill_name = "💥 **[필살 차원 종말참]**"
            if not skip_battle: status_display.markdown("<h3 style='text-align:center; color:#ffd700;'>🔥 [4번째 턴] 필살 차원 참격 대폭발!!</h3>", unsafe_allow_html=True)
        else:
            atk_mult = 1.0
            skill_name = "🗡️ **[기본 검격]**"
            if not skip_battle: status_display.markdown(f"<h4 style='text-align:center; color:#00f0ff;'>🗡️ [{turn % 4}/3번째 턴] 용사의 검격!</h4>", unsafe_allow_html=True)
        
        is_crit = random.random() < 0.25
        crit_mult = 1.5 if is_crit else 1.0
        damage_to_monster = int(base_atk * atk_mult * crit_mult * random.uniform(0.9, 1.1))
        monster_hp = max(0, monster_hp - damage_to_monster)
        
        crit_text = "✨ **CRITICAL!** " if is_crit else ""
        battle_logs.append(f"<span style='color:#00f0ff;'>[Turn {turn}] 용사의 {skill_name}! {crit_text}<b>{damage_to_monster:,}</b> 피해!</span>")
        
        if not skip_battle:
            monster_bar.progress(monster_hp / monster['hp'], text=f"HP: {monster_hp:,} / {monster['hp']:,}")
            with canvas_box:
                components.html(render_canvas_battle(st.session_state.hero_name, monster['name'], m_step, is_ultimate, damage_to_monster, True, st.session_state.hero_level, f"h_{turn}_{time.time()}"), height=240)
            battle_log_box.markdown("<div class='battle-log-text'>" + "<br>".join(battle_logs[-4:]) + "</div>", unsafe_allow_html=True)
            time.sleep(0.7)
            
        if monster_hp <= 0:
            break
            
        # 2. 몬스터 공격
        is_m_skill = random.random() < 0.35
        m_atk_mult = 1.8 if is_m_skill else random.uniform(0.9, 1.2)
        damage_to_hero = int(monster["atk"] * m_atk_mult)
        hero_hp = max(0, hero_hp - damage_to_hero)
        
        m_skill_text = f"☠️ <b>[{monster['skill']}]</b>" if is_m_skill else "🐾 <b>[일반 반격]</b>"
        battle_logs.append(f"<span style='color:#ff007f;'>[Turn {turn}] {monster['name']}의 {m_skill_text}! 용사에게 <b>{damage_to_hero:,}</b> 피해!</span>")
        
        if not skip_battle:
            hero_bar.progress(hero_hp / get_max_hp(), text=f"HP: {hero_hp:,} / {get_max_hp():,}")
            with canvas_box:
                components.html(render_canvas_battle(st.session_state.hero_name, monster['name'], m_step, False, damage_to_hero, False, st.session_state.hero_level, f"m_{turn}_{time.time()}"), height=240)
            battle_log_box.markdown("<div class='battle-log-text'>" + "<br>".join(battle_logs[-4:]) + "</div>", unsafe_allow_html=True)
            time.sleep(0.7)
            
        turn += 1

    if skip_battle:
        hero_bar.progress(hero_hp / get_max_hp(), text=f"HP: {hero_hp:,} / {get_max_hp():,}")
        monster_bar.progress(monster_hp / monster['hp'], text=f"HP: {monster_hp:,} / {monster['hp']:,}")
        status_display.markdown("<h3 style='text-align:center; color:#ff007f;'>⚡ 전투 즉시 완료!</h3>", unsafe_allow_html=True)
        battle_log_box.markdown("<div class='battle-log-text'>" + "<br>".join(battle_logs[-5:]) + "</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # 전투 결과
    if monster_hp <= 0:
        raw_reward = monster['reward']
        final_reward = int(raw_reward * get_gold_multiplier())
        st.session_state.gold += final_reward
        st.balloons()
        
        if m_step == 50:
            st.markdown(f"""
            <div class='rebirth-box'>
                <h1 style='color:#ffd700; font-size: 2.3rem;'>🏆 FINAL BOSS CLEAR! 🏆</h1>
                <p style='font-size: 1.2rem; color:#fff;'>세계관 최종 50단계 [종말의 창조신]을 격파했습니다!</p>
                <hr style='border-color: #ffd700;'>
                <p style='color:#00f0ff;'>지금 환생하면 <b>영구 골드 버프 +10%</b> 및 <b>기본 공격력 +20%</b> 증가 패시브가 부여됩니다.</p>
            </div>
            """, unsafe_allow_html=True)
            st.write("")
            if st.button("🌌 차원 환생 수행하기 (스탯 영구 보너스 획득)", use_container_width=True):
                do_rebirth()
        else:
            st.success(f"🎉 **토벌 완료!** [{monster['name']}]을(를) 물리치고 **{final_reward:,} Gold** (환생 보너스 포함)를 획득했습니다!")
            st.session_state.log.append(f"🏆 [{monster['name']}] 토벌 성공 (+{final_reward:,} G)")
    else:
        penalty = int(monster['reward'] * 0.1)
        st.session_state.gold = max(0, st.session_state.gold - penalty)
        st.error(f"☠️ **전투 패배...** 괴물의 막강한 공격에 패배하여 {penalty:,} Gold를 잃었습니다.")
        st.session_state.log.append(f"💀 [{monster['name']}] 사냥 실패 (-{penalty:,} G)")

st.markdown("---")
with st.expander("📜 최근 모험 및 환생 기록"):
    for log in reversed(st.session_state.log[-5:]):
        st.write(log)
