import streamlit as st
import streamlit.components.v1 as components
import random
import time

# -------------------------------------------------------------------
# 1. 페이지 및 Cyberpunk Neon Style 설정
# -------------------------------------------------------------------
st.set_page_config(page_title="NEON RPG: CELESTIAL OVERDRIVE", page_icon="🌌", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=Noto+Sans+KR:wght@500;700;900&display=swap');

    .stApp {
        background: 
            radial-gradient(circle at 50% 15%, rgba(255, 0, 127, 0.4) 0%, transparent 60%),
            radial-gradient(circle at 80% 80%, rgba(0, 240, 255, 0.35) 0%, transparent 60%),
            linear-gradient(180deg, #050010 0%, #010003 100%);
        color: #ffffff;
        font-family: 'Noto Sans KR', sans-serif;
    }

    .game-title {
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        font-size: 2.6rem;
        font-weight: 900;
        letter-spacing: 4px;
        background: linear-gradient(180deg, #fff 0%, #ffd700 30%, #00f0ff 70%, #ff007f 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 35px rgba(0, 240, 255, 0.9), 0 0 20px rgba(255, 0, 127, 0.8);
        margin-bottom: 20px;
    }

    .profile-card, .weapon-card-glow {
        background: rgba(10, 2, 22, 0.9);
        backdrop-filter: blur(16px);
        border: 2px solid rgba(0, 240, 255, 0.8);
        border-radius: 20px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 0 35px rgba(0, 240, 255, 0.4), inset 0 0 20px rgba(0, 240, 255, 0.2);
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
        padding: 20px;
        margin-top: 15px;
    }

    .battle-log-text {
        font-family: 'Orbitron', 'Noto Sans KR', sans-serif;
        font-size: 0.88rem;
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
        width: 100% !important; height: 48px !important; border-radius: 12px !important;
        font-weight: 900 !important; font-size: 1rem !important;
        background: linear-gradient(135deg, #ff007f 0%, #7928ca 50%, #00f0ff 100%) !important;
        color: #ffffff !important; border: none !important;
        box-shadow: 0 0 20px rgba(255, 0, 127, 0.5) !important;
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 0 35px rgba(0, 240, 255, 1) !important;
    }
    </style>
""", unsafe_allow_html=True)

def safe_rerun():
    if hasattr(st, "rerun"): st.rerun()
    elif hasattr(st, "experimental_rerun"): st.experimental_rerun()

# -------------------------------------------------------------------
# 2. 무기 및 10단계 초간지 용사 SVG 리소스
# -------------------------------------------------------------------
WEAPON_SVGS = [
    '''<svg width="110" height="110" viewBox="0 0 100 100"><defs><linearGradient id="g0" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#b0bec5"/><stop offset="100%" stop-color="#37474f"/></linearGradient></defs><path d="M50 15 L56 60 L50 65 L44 60 Z" fill="url(#g0)" stroke="#102027" stroke-width="1.5"/><rect x="42" y="65" width="16" height="4" fill="#546e7a" rx="1"/><rect x="47" y="69" width="6" height="18" fill="#37474f"/><circle cx="50" cy="89" r="4" fill="#78909c"/></svg>''',
    '''<svg width="110" height="110" viewBox="0 0 100 100"><defs><linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#e0e0e0"/><stop offset="50%" stop-color="#9e9e9e"/><stop offset="100%" stop-color="#424242"/></linearGradient></defs><path d="M50 8 L57 65 L50 72 L43 65 Z" fill="url(#g1)" stroke="#212121" stroke-width="1.5"/><line x1="50" y1="12" x2="50" y2="65" stroke="#ffffff" stroke-width="1"/><path d="M35 72 L65 72 L50 78 Z" fill="#757575"/><rect x="47" y="78" width="6" height="16" fill="#212121"/></svg>''',
    '''<svg width="110" height="110" viewBox="0 0 100 100"><defs><linearGradient id="g2" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#00e5ff"/><stop offset="100%" stop-color="#1a237e"/></linearGradient><filter id="f2"><feGaussianBlur stdDeviation="2" result="coloredBlur"/><feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><path d="M50 5 L58 65 L50 72 L42 65 Z" fill="url(#g2)" stroke="#00b0ff" stroke-width="1.5"/><path d="M50 15 L50 55" stroke="#ffffff" stroke-width="2" filter="url(#f2)"/><polygon points="32,70 68,70 50,78" fill="#00b0ff" filter="url(#f2)"/><circle cx="50" cy="40" r="4" fill="#ffffff" filter="url(#f2)"/></svg>''',
    '''<svg width="110" height="110" viewBox="0 0 100 100"><defs><linearGradient id="g3" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#b9f6ca"/><stop offset="50%" stop-color="#00e676"/><stop offset="100%" stop-color="#1b5e20"/></linearGradient><filter id="f3"><feDropShadow dx="0" dy="0" stdDeviation="3" flood-color="#69f0ae"/></filter></defs><path d="M50 5 Q58 35 56 65 L50 72 Q42 35 44 65 Z" fill="url(#g3)" stroke="#00c853" stroke-width="1.5" filter="url(#f3)"/><path d="M35 68 C45 68 45 78 50 82 C55 78 55 68 65 68 C55 74 45 74 35 68 Z" fill="#00e676"/><rect x="47" y="82" width="6" height="14" fill="#2e7d32" rx="2"/></svg>''',
    '''<svg width="110" height="110" viewBox="0 0 100 100"><defs><linearGradient id="g4_1" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#ff9100"/><stop offset="100%" stop-color="#ff3d00"/></linearGradient><filter id="f4_1"><feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="#ff3d00"/></filter></defs><path d="M50 2 C65 30 55 55 56 68 L50 74 L44 68 C45 55 35 30 50 2 Z" fill="url(#g4_1)" filter="url(#f4_1)"/><rect x="40" y="74" width="20" height="5" fill="#d50000"/><rect x="47" y="79" width="6" height="16" fill="#3e2723"/></svg>''',
    '''<svg width="110" height="110" viewBox="0 0 100 100"><defs><linearGradient id="g4" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#fff59d"/><stop offset="50%" stop-color="#ffd700"/><stop offset="100%" stop-color="#ff6f00"/></linearGradient><filter id="f4"><feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="#ffea00"/></filter></defs><path d="M50 2 L60 62 L50 70 L40 62 Z" fill="url(#g4)" stroke="#ffab00" stroke-width="1.5" filter="url(#f4)"/><line x1="50" y1="8" x2="50" y2="60" stroke="#ffffff" stroke-width="2.5"/><path d="M25 66 L75 66 L50 76 Z" fill="#ffc107" filter="url(#f4)"/><polygon points="50,60 55,68 50,74 45,68" fill="#ffffff"/></svg>''',
    '''<svg width="110" height="110" viewBox="0 0 100 100"><defs><linearGradient id="g5" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#ff3d00"/><stop offset="50%" stop-color="#dd2c00"/><stop offset="100%" stop-color="#3e2723"/></linearGradient><filter id="f5"><feDropShadow dx="0" dy="0" stdDeviation="5" flood-color="#ff3d00"/></filter></defs><path d="M46 2 L54 2 L62 60 L50 72 L38 60 Z" fill="url(#g5)" stroke="#bf360c" stroke-width="2" filter="url(#f5)"/><path d="M48 10 L52 10 L55 55 L50 60 L45 55 Z" fill="#ff9e80"/><path d="M22 62 L78 62 L50 75 Z" fill="#d50000" filter="url(#f5)"/><circle cx="50" cy="68" r="5" fill="#ffeb3b"/></svg>''',
    '''<svg width="110" height="110" viewBox="0 0 100 100"><defs><linearGradient id="g7_1" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#00f0ff"/><stop offset="100%" stop-color="#7000ff"/></linearGradient><filter id="f7_1"><feDropShadow dx="0" dy="0" stdDeviation="5" flood-color="#00f0ff"/></filter></defs><path d="M49 0 L51 0 L53 65 L50 72 L47 65 Z" fill="url(#g7_1)" filter="url(#f7_1)"/><circle cx="50" cy="74" r="12" fill="none" stroke="#00f0ff" stroke-width="3"/><rect x="48" y="80" width="4" height="15" fill="#ffffff"/></svg>''',
    '''<svg width="110" height="110" viewBox="0 0 100 100"><defs><linearGradient id="g6" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#00f0ff"/><stop offset="50%" stop-color="#7000ff"/><stop offset="100%" stop-color="#ff007f"/></linearGradient><filter id="f6"><feGaussianBlur stdDeviation="3" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><path d="M50 0 L63 58 L50 68 L37 58 Z" fill="url(#g6)" stroke="#00f0ff" stroke-width="2" filter="url(#f6)"/><polygon points="50,5 55,25 50,45 45,25" fill="#ffffff" filter="url(#f6)"/><path d="M20 62 L80 62 L50 76 Z" fill="#7000ff" stroke="#00f0ff" stroke-width="1.5"/><circle cx="50" cy="69" r="6" fill="#00f0ff" filter="url(#f6)"/></svg>''',
    '''<svg width="110" height="110" viewBox="0 0 100 100"><defs><filter id="f9"><feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="#ff007f"/></filter></defs><path d="M48 10 L52 10 L50 90 Z" fill="#333"/><path d="M50 12 C75 -5 90 20 85 40 C70 25 55 20 50 25 Z" fill="#ff007f" filter="url(#f9)"/></svg>''',
    '''<svg width="110" height="110" viewBox="0 0 100 100"><defs><linearGradient id="g10" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#ffffff"/><stop offset="50%" stop-color="#00f0ff"/><stop offset="100%" stop-color="#ff007f"/></linearGradient><filter id="f10"><feDropShadow dx="0" dy="0" stdDeviation="8" flood-color="#00f0ff"/></filter></defs><polygon points="50,-5 60,60 50,68 40,60" fill="url(#g10)" filter="url(#f10)"/><circle cx="50" cy="74" r="8" fill="#ffd700"/></svg>''',
    '''<svg width="110" height="110" viewBox="0 0 100 100"><defs><linearGradient id="g7" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#ffffff"/><stop offset="30%" stop-color="#ff007f"/><stop offset="70%" stop-color="#7000ff"/><stop offset="100%" stop-color="#00f0ff"/></linearGradient><filter id="f7"><feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="#ff007f"/><feDropShadow dx="0" dy="0" stdDeviation="10" flood-color="#00f0ff"/></filter></defs><path d="M50 -5 L65 58 L50 70 L35 58 Z" fill="url(#g7)" filter="url(#f7)"/><path d="M48 5 L52 5 L56 50 L50 58 L44 50 Z" fill="#ffffff"/><polygon points="15,60 85,60 50,80" fill="#110022" stroke="#ffd700" stroke-width="2.5" filter="url(#f7)"/><circle cx="50" cy="70" r="7" fill="#ffd700" filter="url(#f7)"/><polygon points="50,20 54,28 50,36 46,28" fill="#00f0ff"/></svg>'''
]

# --- 10단계 초간지 용사 SVG 연출 ---
def get_hero_svg(lvl):
    if lvl <= 5: # 1단계: 사이버 비기너
        return '''<svg width="120" height="120" viewBox="0 0 100 100"><polygon points="30,85 50,45 70,85" fill="#37474f" stroke="#78909c" stroke-width="2"/><circle cx="50" cy="35" r="16" fill="#eceff1"/><path d="M38 25 L62 25 L50 12 Z" fill="#546e7a"/><circle cx="45" cy="35" r="3" fill="#00f0ff"/><circle cx="55" cy="35" r="3" fill="#00f0ff"/></svg>'''
    elif lvl <= 10: # 2단계: 네온 가디언
        return '''<svg width="120" height="120" viewBox="0 0 100 100"><defs><filter id="h_g2"><feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="#00f0ff"/></filter></defs><path d="M25 88 L50 40 L75 88 Z" fill="#1a237e" stroke="#00f0ff" stroke-width="2" filter="url(#h_g2)"/><circle cx="50" cy="32" r="17" fill="#263238"/><path d="M34 28 C34 10 66 10 66 28 Z" fill="#00b0ff" filter="url(#h_g2)"/><rect x="40" y="30" width="20" height="4" fill="#ffffff" filter="url(#h_g2)"/></svg>'''
    elif lvl <= 15: # 3단계: 플라즈마 스트라이커
        return '''<svg width="120" height="120" viewBox="0 0 100 100"><defs><filter id="h_g3"><feDropShadow dx="0" dy="0" stdDeviation="5" flood-color="#7000ff"/></filter></defs><path d="M15 70 L35 45 L20 30 Z" fill="#7000ff"/><path d="M85 70 L65 45 L80 30 Z" fill="#7000ff"/><polygon points="25,88 50,35 75,88" fill="#0d47a1" stroke="#7000ff" stroke-width="2" filter="url(#h_g3)"/><circle cx="50" cy="30" r="18" fill="#ffffff"/><polygon points="32,20 50,2 68,20" fill="#7000ff" filter="url(#h_g3)"/></svg>'''
    elif lvl <= 20: # 4단계: 네온 스페셜리스트
        return '''<svg width="120" height="120" viewBox="0 0 100 100"><defs><filter id="h_g4"><feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="#ff007f"/></filter></defs><path d="M10 80 Q 20 20 45 35 Z" fill="#ff007f" filter="url(#h_g4)"/><path d="M90 80 Q 80 20 55 35 Z" fill="#ff007f" filter="url(#h_g4)"/><polygon points="22,90 50,30 78,90" fill="#212121" stroke="#ff007f" stroke-width="2.5"/><circle cx="50" cy="28" r="19" fill="#00f0ff" filter="url(#h_g4)"/><line x1="32" y1="28" x2="68" y2="28" stroke="#ffffff" stroke-width="3"/></svg>'''
    elif lvl <= 25: # 5단계: 영웅 챔피언
        return '''<svg width="120" height="120" viewBox="0 0 100 100"><defs><filter id="h_g5"><feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="#ffd700"/></filter></defs><path d="M5 85 L35 45 L20 20 Z" fill="#ffd700" filter="url(#h_g5)"/><path d="M95 85 L65 45 L80 20 Z" fill="#ffd700" filter="url(#h_g5)"/><polygon points="20,90 50,28 80,90" fill="#1b003a" stroke="#ffd700" stroke-width="2.5"/><circle cx="50" cy="26" r="20" fill="#ffffff" filter="url(#h_g5)"/><polygon points="28,14 50,-2 72,14" fill="#ffd700"/></svg>'''
    elif lvl <= 30: # 6단계: 전설의 네온 마스터
        return '''<svg width="120" height="120" viewBox="0 0 100 100"><defs><filter id="h_g6"><feDropShadow dx="0" dy="0" stdDeviation="8" flood-color="#00f0ff"/></filter></defs><path d="M 0 50 C 10 10 40 20 45 30 C 20 40 10 70 0 50 Z" fill="#00f0ff" filter="url(#h_g6)"/><path d="M 100 50 C 90 10 60 20 55 30 C 80 40 90 70 100 50 Z" fill="#00f0ff" filter="url(#h_g6)"/><polygon points="20,92 50,25 80,92" fill="#000511" stroke="#00f0ff" stroke-width="3"/><circle cx="50" cy="25" r="21" fill="#ff007f" filter="url(#h_g6)"/><polygon points="30,8 50,-6 70,8" fill="#ffffff" filter="url(#h_g6)"/></svg>'''
    elif lvl <= 35: # 7단계: 신화의 오버로드
        return '''<svg width="120" height="120" viewBox="0 0 100 100"><defs><filter id="h_g7"><feDropShadow dx="0" dy="0" stdDeviation="8" flood-color="#ff007f"/><feDropShadow dx="0" dy="0" stdDeviation="12" flood-color="#7000ff"/></filter></defs><path d="M -5 80 L 35 40 L 15 10 Z" fill="#ff007f" filter="url(#h_g7)"/><path d="M 105 80 L 65 40 L 85 10 Z" fill="#ff007f" filter="url(#h_g7)"/><polygon points="18,92 50,22 82,92" fill="#0a0014" stroke="#ff007f" stroke-width="3"/><circle cx="50" cy="22" r="22" fill="#ffffff" filter="url(#h_g7)"/><polygon points="22,8 50,-8 78,8" fill="#7000ff" filter="url(#h_g7)"/></svg>'''
    elif lvl <= 40: # 8단계: 차원 초월자
        return '''<svg width="120" height="120" viewBox="0 0 100 100"><defs><filter id="h_g8"><feDropShadow dx="0" dy="0" stdDeviation="10" flood-color="#00f0ff"/><feDropShadow dx="0" dy="0" stdDeviation="15" flood-color="#ffd700"/></filter></defs><circle cx="50" cy="50" r="46" fill="none" stroke="#00f0ff" stroke-width="2" stroke-dasharray="8 4" filter="url(#h_g8)"/><path d="M -10 60 Q 15 -10 45 20 Z" fill="#ffd700" filter="url(#h_g8)"/><path d="M 110 60 Q 85 -10 55 20 Z" fill="#ffd700" filter="url(#h_g8)"/><polygon points="16,92 50,18 84,92" fill="#000" stroke="#ffd700" stroke-width="3"/><circle cx="50" cy="20" r="23" fill="#00f0ff" filter="url(#h_g8)"/><polygon points="20,2 50,-12 80,2" fill="#ff007f" filter="url(#h_g8)"/></svg>'''
    elif lvl <= 45: # 9단계: 시공간 파괴자
        return '''<svg width="120" height="120" viewBox="0 0 100 100"><defs><filter id="h_g9"><feDropShadow dx="0" dy="0" stdDeviation="12" flood-color="#ff0055"/><feDropShadow dx="0" dy="0" stdDeviation="18" flood-color="#00f0ff"/></filter></defs><path d="M -15 90 C -5 -20 40 10 48 20 C 15 30 0 80 -15 90 Z" fill="#ff0055" filter="url(#h_g9)"/><path d="M 115 90 C 105 -20 60 10 52 20 C 85 30 100 80 115 90 Z" fill="#ff0055" filter="url(#h_g9)"/><polygon points="15,95 50,15 85,95" fill="#030008" stroke="#00f0ff" stroke-width="3.5" filter="url(#h_g9)"/><circle cx="50" cy="18" r="24" fill="#ffffff" filter="url(#h_g9)"/><polygon points="15,-2 50,-16 85,-2" fill="#ffd700" filter="url(#h_g9)"/></svg>'''
    else: # 10단계: 🌌 차원 절대신
        return '''<svg width="120" height="120" viewBox="0 0 100 100"><defs><filter id="h_g10"><feDropShadow dx="0" dy="0" stdDeviation="10" flood-color="#ffd700"/><feDropShadow dx="0" dy="0" stdDeviation="20" flood-color="#ff007f"/><feDropShadow dx="0" dy="0" stdDeviation="30" flood-color="#00f0ff"/></filter></defs><circle cx="50" cy="50" r="48" fill="none" stroke="#ffd700" stroke-width="3" filter="url(#h_g10)"/><path d="M -20 70 Q -10 -30 45 10 Z" fill="rgba(0, 240, 255, 0.9)" filter="url(#h_g10)"/><path d="M 120 70 Q 110 -30 55 10 Z" fill="rgba(255, 0, 127, 0.9)" filter="url(#h_g10)"/><polygon points="12,95 50,10 88,95" fill="#000000" stroke="#ffffff" stroke-width="4" filter="url(#h_g10)"/><circle cx="50" cy="15" r="25" fill="#ffffff" filter="url(#h_g10)"/><polygon points="10,-5 50,-22 90,-5" fill="#ffd700" filter="url(#h_g10)"/></svg>'''

def get_hero_title(lvl):
    titles = [
        "사이버 비기너", "네온 가디언", "플라즈마 스트라이커", 
        "네온 스페셜리스트", "영웅 챔피언", "전설의 네온 마스터", 
        "신화의 오버로드", "차원 초월자", "⚡ 시공간 파괴자", "🌌 차원 절대신"
    ]
    idx = min((lvl - 1) // 5, len(titles) - 1)
    return titles[idx]

def get_weapon_info(lvl):
    names = [
        "녹슨 단검", "강철 장검", "룬 각인 검", "엘프의 명검", 
        "화염 블레이드", "영웅의 성검", "용살자의 대검", "플라즈마 레이피어", 
        "차원 파괴검", "아포칼립스 낫", "갤럭시 세이버", "🌌 신멸의 절망검"
    ]
    idx = min(lvl // 4, len(names) - 1)
    return {"name": names[idx], "svg": WEAPON_SVGS[idx]}

def get_monster_info(step):
    prefix = ["말랑", "흉폭한", "저주받은", "심연의", "지옥의", "우주의", "멸망의", "절대"]
    base_names = ["슬라임", "고블린", "골렘", "미노타우로스", "드래곤", "크라켄", "요르문간드", "파괴자"]
    
    if step == 50:
        return {"name": "👑 [FINAL BOSS] 종말의 창조신 파괴자", "hp": 8500000, "atk": 12000, "skill": "⚡ 우주 멸망 소멸 포격", "reward": 3000000}
    
    p_idx = min((step - 1) // 7, len(prefix) - 1)
    b_idx = min((step - 1) // 7, len(base_names) - 1)
    
    name = f"{prefix[p_idx]} {base_names[b_idx]} (Lv.{step})"
    hp = int(450 * (1.28 ** step))
    atk = int(35 * (1.16 ** step))
    reward = int(500 * (1.25 ** step))
    return {"name": name, "hp": hp, "atk": atk, "skill": "💥 강격 파동", "reward": reward}

# -------------------------------------------------------------------
# 3. Session State 초기화 및 계산 함수
# -------------------------------------------------------------------
if "gold" not in st.session_state:
    st.session_state.hero_name = "용사님"
    st.session_state.hero_level = 1
    st.session_state.gold = 10000
    st.session_state.weapon_lvl = 0
    st.session_state.rebirth_count = 0
    st.session_state.selected_step = 1
    st.session_state.log = ["✨ 50단계 신화 모험이 시작되었습니다!"]

def get_gold_multiplier(): return 1.0 + (st.session_state.rebirth_count * 0.10)
def get_rebirth_atk_bonus(): return 1.0 + (st.session_state.rebirth_count * 0.20)

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
    if st.session_state.weapon_lvl >= 49: return 1.0
    return max(5.0, 100.0 - (st.session_state.weapon_lvl * 1.95))

# -------------------------------------------------------------------
# 4. 상호작용 액션 함수
# -------------------------------------------------------------------
def recommend_monster_step():
    total_atk = get_total_atk()
    max_hp = get_max_hp()
    recommended = 1
    for s in range(1, 51):
        m = get_monster_info(s)
        turns_to_kill = m["hp"] / (total_atk * 1.2)
        turns_to_die = max_hp / max(1, m["atk"])
        if turns_to_kill <= 6 and turns_to_die >= 3:
            recommended = s
        else:
            break
    st.session_state.selected_step = recommended
    st.toast(f"🎯 AI 추천: Lv.{recommended} 몬스터가 가장 적합합니다!", icon="🤖")

def do_rebirth():
    st.session_state.rebirth_count += 1
    st.session_state.hero_level = 1
    st.session_state.weapon_lvl = 0
    st.session_state.gold = 10000
    st.session_state.selected_step = 1
    st.session_state.log.append(f"🔄 [{st.session_state.rebirth_count}회차 환생] 차원 초월 완료! 영구 버프 부여!")
    st.toast(f"🔄 환생 완료! {st.session_state.rebirth_count}회차 스탯 보너스가 적용됩니다.", icon="✨")
    safe_rerun()

def enhance_weapon():
    if st.session_state.weapon_lvl >= 50:
        st.toast("👑 검이 최고 단계에 도달했습니다!", icon="⭐")
        return
    if st.session_state.gold < get_w_cost():
        st.toast("⚠️ 골드가 부족합니다!", icon="💰")
        return
    st.session_state.gold -= get_w_cost()
    if random.uniform(0, 100) <= get_w_rate():
        st.session_state.weapon_lvl += 1
        st.toast(f"⚔️ 무기 강화 성공! (+{st.session_state.weapon_lvl})", icon="✨")
    else:
        if st.session_state.weapon_lvl >= 10:
            st.session_state.weapon_lvl -= 1
            st.toast("💥 강화 실패! 무기 등급 하락!", icon="⚠️")
        else:
            st.toast("❌ 강화 실패! (등급 유지)", icon="🛡️")
    safe_rerun()

def enhance_hero():
    if st.session_state.hero_level >= 50:
        st.toast("👑 용사가 최고 레벨에 도달했습니다!", icon="⭐")
        return
    if st.session_state.gold < get_h_cost():
        st.toast("⚠️ 골드가 부족합니다!", icon="💰")
        return
    st.session_state.gold -= get_h_cost()
    st.session_state.hero_level += 1
    st.toast(f"🦸 레벨 업! (Lv.{st.session_state.hero_level})", icon="💪")
    safe_rerun()

# -------------------------------------------------------------------
# HTML5 Canvas 하이테크 전투 연출 (필살기 및 용사 아우라 극대화)
# -------------------------------------------------------------------
def render_canvas_battle(hero_name, monster_name, monster_step, is_ultimate, damage, is_hero_turn, hero_level, render_id):
    is_final_boss = (monster_step == 50)
    html_code = f"""
    <div style="text-align: center;">
        <canvas id="battleCanvas_{render_id}" width="600" height="220" style="border-radius:15px; border:2px solid { "#ffd700" if is_final_boss else "#00f0ff" }; background: linear-gradient(180deg, #090017 0%, #010005 100%); box-shadow: 0 0 35px { "rgba(255, 215, 0, 0.9)" if is_final_boss else "rgba(0, 240, 255, 0.5)" };"></canvas>
    </div>
    <script>
    (function() {{
        const canvas = document.getElementById('battleCanvas_{render_id}');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        let frame = 0;
        let heroX = 90, monsterX = 470;
        let isFinalBoss = { 'true' if is_final_boss else 'false' };
        let mStep = {monster_step}, isUlt = { 'true' if is_ultimate else 'false' }, isHeroTurn = { 'true' if is_hero_turn else 'false' }, hLvl = {hero_level};

        function animate() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            if (isUlt && isHeroTurn && frame >= 8 && frame <= 22) {{
                ctx.setTransform(1, 0, 0, 1, (Math.random() - 0.5) * 22, (Math.random() - 0.5) * 22);
            }} else {{ ctx.setTransform(1, 0, 0, 1, 0, 0); }}

            // 배경 격자
            ctx.strokeStyle = isFinalBoss ? 'rgba(255, 215, 0, 0.2)' : 'rgba(0, 240, 255, 0.1)';
            ctx.lineWidth = 1;
            for(let x=0; x<canvas.width; x+=30) {{ ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,canvas.height); ctx.stroke(); }}
            for(let y=0; y<canvas.height; y+=30) {{ ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(canvas.width,y); ctx.stroke(); }}
            
            let hX = heroX, mX = monsterX, strike = false;
            if (isHeroTurn) {{
                if (frame < 10) hX += frame * 18;
                else if (frame < 20) {{ hX = 370; strike = true; mX += Math.sin(frame)*14; }}
                else hX -= (frame - 20) * 18;
            }} else {{
                if (frame < 10) mX -= frame * 18;
                else if (frame < 20) {{ mX = 190; strike = true; hX += Math.sin(frame)*14; }}
                else mX += (frame - 20) * 18;
            }}
            
            // 용사 연출 (레벨별 삼각 아우라)
            ctx.save();
            let auraColor = hLvl >= 40 ? '#ffd700' : (hLvl >= 20 ? '#ff007f' : '#00f0ff');
            ctx.shadowColor = auraColor;
            ctx.shadowBlur = 20 + hLvl;
            
            // 용사 아바타 (화려한 차원 다각형)
            ctx.fillStyle = auraColor;
            ctx.beginPath();
            ctx.moveTo(hX, 110 - (20 + hLvl*0.2));
            ctx.lineTo(hX - (18 + hLvl*0.2), 110 + (20 + hLvl*0.2));
            ctx.lineTo(hX + (18 + hLvl*0.2), 110 + (20 + hLvl*0.2));
            ctx.closePath();
            ctx.fill();

            ctx.fillStyle = '#fff';
            ctx.font = 'bold 12px Orbitron';
            ctx.fillText('{hero_name}', hX - 25, 160);
            ctx.restore();
            
            // 몬스터 연출
            ctx.save();
            if (isFinalBoss) {{
                let size = 55 + Math.sin(frame*0.2)*8;
                ctx.strokeStyle = '#ffd700'; ctx.lineWidth = 5; ctx.shadowColor = '#ff0055'; ctx.shadowBlur = 40;
                ctx.beginPath(); ctx.arc(mX, 110, size, 0, Math.PI*2); ctx.stroke();
                ctx.fillStyle = '#ff0055'; ctx.beginPath(); ctx.arc(mX, 110, 18, 0, Math.PI*2); ctx.fill();
            }} else {{
                ctx.fillStyle = mStep >= 25 ? '#ff007f' : '#a100ff'; ctx.shadowColor = '#a100ff'; ctx.shadowBlur = 15;
                let boxSize = 36 + Math.min(mStep, 50) * 0.5;
                ctx.fillRect(mX - boxSize/2, 110 - boxSize/2, boxSize, boxSize);
            }}
            ctx.fillStyle = '#fff'; ctx.font = 'bold 12px Orbitron'; ctx.fillText('{monster_name}', mX - 40, 165);
            ctx.restore();
            
            // 타격 이펙트 & 데미지 텍스트
            if (strike) {{
                ctx.save();
                ctx.strokeStyle = isHeroTurn ? (isUlt ? '#ffd700' : '#00f0ff') : '#ff007f';
                ctx.shadowBlur = 30; ctx.lineWidth = isUlt ? 15 : 7;
                ctx.beginPath(); ctx.moveTo(mX - 50, 40); ctx.lineTo(mX + 50, 170); ctx.stroke();
                
                if(isUlt) {{
                    ctx.beginPath(); ctx.moveTo(mX + 50, 40); ctx.lineTo(mX - 50, 170); ctx.stroke();
                }}

                ctx.fillStyle = isUlt ? '#ffd700' : '#ffff00'; ctx.font = '900 30px Orbitron';
                ctx.fillText('-' + damage.toLocaleString(), (isHeroTurn ? mX : hX) - 35, 35);
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

# -------------------------------------------------------------------
# 5. UI 메인 레이아웃
# -------------------------------------------------------------------
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
        <div class='svg-container'>{get_hero_svg(st.session_state.hero_level)}</div>
        <b>[{get_hero_title(st.session_state.hero_level)}] {st.session_state.hero_name}</b><br>
        HP: {get_max_hp():,} | ATK: {get_hero_atk():,}
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button(f"💪 용사 각성 ({get_h_cost():,}G)"): enhance_hero()

with col_weapon:
    st.markdown(f"""
    <div class='weapon-card-glow'>
        <div class='svg-container'>{w_info['svg']}</div>
        <b>+{st.session_state.weapon_lvl} {w_info['name']}</b><br>
        ATK: {get_weapon_atk():,} | 성공률: {get_w_rate():.1f}%
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button(f"🔨 검 강화 ({get_w_cost():,}G)"): enhance_weapon()

st.markdown("---")

# --- 👹 전투 아레나 ---
st.subheader("⚔️ 50단계 실시간 격투 아레나")

skip_battle = st.checkbox("⏩ 전투 연출 SKIP (즉시 결과 계산)", value=False)

c_step1, c_step2 = st.columns([3, 1])
with c_step1:
    m_step = st.slider("🎯 괴물 단계 선택 (1 ~ 50단계)", 1, 50, value=st.session_state.selected_step)
    st.session_state.selected_step = m_step
with c_step2:
    st.write("")
    if st.button("🤖 AI 추천"):
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
    
    canvas_box = st.empty()
    status_display = st.empty()
    battle_log_box = st.empty()
    battle_logs = []
    turn = 1
    
    while hero_hp > 0 and monster_hp > 0:
        is_ultimate = (turn % 4 == 0)
        if is_ultimate:
            atk_mult = 3.0
            skill_name = "💥 **[초월적 차원 붕괴참]**"
            if not skip_battle: status_display.markdown("<h3 style='text-align:center; color:#ffd700;'>🔥 [4번째 턴] 초월적 차원 붕괴참 폭발!!</h3>", unsafe_allow_html=True)
        else:
            atk_mult = 1.0
            skill_name = "🗡️ **[네온 플라즈마 참격]**"
            if not skip_battle: status_display.markdown(f"<h4 style='text-align:center; color:#00f0ff;'>🗡️ [{turn % 4}/3번째 턴] 용사의 검격!</h4>", unsafe_allow_html=True)
        
        is_crit = random.random() < 0.25
        damage_to_monster = int(base_atk * atk_mult * (1.5 if is_crit else 1.0) * random.uniform(0.9, 1.1))
        monster_hp = max(0, monster_hp - damage_to_monster)
        
        battle_logs.append(f"<span style='color:#00f0ff;'>[Turn {turn}] 용사의 {skill_name}! <b>{damage_to_monster:,}</b> 피해!</span>")
        
        if not skip_battle:
            monster_bar.progress(monster_hp / monster['hp'], text=f"HP: {monster_hp:,} / {monster['hp']:,}")
            with canvas_box:
                components.html(render_canvas_battle(st.session_state.hero_name, monster['name'], m_step, is_ultimate, damage_to_monster, True, st.session_state.hero_level, f"h_{turn}_{time.time()}"), height=230)
            battle_log_box.markdown("<div class='battle-log-text'>" + "<br>".join(battle_logs[-4:]) + "</div>", unsafe_allow_html=True)
            time.sleep(0.6)
            
        if monster_hp <= 0: break
            
        is_m_skill = random.random() < 0.35
        damage_to_hero = int(monster["atk"] * (1.8 if is_m_skill else random.uniform(0.9, 1.2)))
        hero_hp = max(0, hero_hp - damage_to_hero)
        
        battle_logs.append(f"<span style='color:#ff007f;'>[Turn {turn}] {monster['name']}의 공격! <b>{damage_to_hero:,}</b> 피해!</span>")
        
        if not skip_battle:
            hero_bar.progress(hero_hp / get_max_hp(), text=f"HP: {hero_hp:,} / {get_max_hp():,}")
            with canvas_box:
                components.html(render_canvas_battle(st.session_state.hero_name, monster['name'], m_step, False, damage_to_hero, False, st.session_state.hero_level, f"m_{turn}_{time.time()}"), height=230)
            battle_log_box.markdown("<div class='battle-log-text'>" + "<br>".join(battle_logs[-4:]) + "</div>", unsafe_allow_html=True)
            time.sleep(0.6)
            
        turn += 1

    if skip_battle:
        hero_bar.progress(hero_hp / get_max_hp(), text=f"HP: {hero_hp:,} / {get_max_hp():,}")
        monster_bar.progress(monster_hp / monster['hp'], text=f"HP: {monster_hp:,} / {monster['hp']:,}")
        battle_log_box.markdown("<div class='battle-log-text'>" + "<br>".join(battle_logs[-4:]) + "</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    if monster_hp <= 0:
        final_reward = int(monster['reward'] * get_gold_multiplier())
        st.session_state.gold += final_reward
        st.balloons()
        
        if m_step == 50:
            st.markdown("""
            <div class='rebirth-box'>
                <h1 style='color:#ffd700;'>🏆 FINAL BOSS CLEAR! 🏆</h1>
                <p>최종 50단계 종말의 창조신을 격파했습니다!</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🌌 차원 환생 수행하기 (영구 버프 획득)", use_container_width=True):
                do_rebirth()
        else:
            st.success(f"🎉 **토벌 완료!** 보상으로 **{final_reward:,} Gold**를 획득했습니다!")
            st.session_state.log.append(f"🏆 [{monster['name']}] 토벌 성공 (+{final_reward:,} G)")
    else:
        penalty = int(monster['reward'] * 0.1)
        st.session_state.gold = max(0, st.session_state.gold - penalty)
        st.error(f"☠️ **전투 패배...** {penalty:,} Gold를 잃었습니다.")
        st.session_state.log.append(f"💀 [{monster['name']}] 사냥 실패 (-{penalty:,} G)")

st.markdown("---")
with st.expander("📜 최근 모험 및 환생 기록"):
    for log in reversed(st.session_state.log[-5:]):
        st.write(log)
