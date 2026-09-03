import streamlit as st
import random
import time

# 웹 페이지 설정
st.set_page_config(page_title="NEON RPG: EVOLUTION", page_icon="⚔️", layout="centered")

# --- 🎨 Ultra Visual & CSS ---
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
        font-size: 2.6rem;
        font-weight: 900;
        background: linear-gradient(180deg, #ff007f 0%, #00f0ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(255, 0, 127, 0.7);
        margin-bottom: 5px;
    }

    /* 프로필 카드 디자인 */
    .profile-card {
        background: rgba(25, 15, 45, 0.8);
        border: 2px solid #00f0ff;
        border-radius: 20px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.3);
    }
    
    .weapon-card-glow {
        background: rgba(25, 15, 45, 0.8);
        border: 2px solid #ff007f;
        border-radius: 20px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 0 20px rgba(255, 0, 127, 0.3);
    }

    /* 이미지 스타일 */
    .art-img {
        width: 100%;
        height: 180px;
        object-fit: cover;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.2);
        margin-bottom: 10px;
    }

    .monster-img {
        width: 100%;
        height: 220px;
        object-fit: cover;
        border-radius: 15px;
        border: 2px solid #ff007f;
        box-shadow: 0 0 15px rgba(255,0,127,0.5);
    }

    /* 버튼 디자인 */
    div.stButton > button {
        width: 100% !important;
        height: 50px !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        font-size: 1rem !important;
        background: linear-gradient(135deg, #2b1055 0%, #15082a 100%) !important;
        color: #00f0ff !important;
        border: 2px solid #00f0ff !important;
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.3) !important;
    }
    div.stButton > button:hover {
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

# --- ⚔️ 진화형 데이터 정의 (이미지 포함) ---
HERO_TIERS = [
    {"title": "견습 모험가", "img": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=400"},
    {"title": "숙련된 기사", "img": "https://images.unsplash.com/photo-1578632767115-351597cf2477?w=400"},
    {"title": "성기사 오버로드", "img": "https://images.unsplash.com/photo-1563089145-599997674d42?w=400"}
]

WEAPON_TIERS = [
    {"name": "수련용 낡은 목검", "base": 25, "img": "https://images.unsplash.com/photo-1595590424283-b8f17842773f?w=400"},
    {"name": "플라즈마 레이저 세이버", "base": 100, "img": "https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=400"},
    {"name": "신멸의 은하 차원검", "base": 300, "img": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=400"}
]

MONSTERS = [
    {"name": "심연의 맹독 고블린", "req_atk": 40, "reward": 500, "img": "https://images.unsplash.com/photo-1563089145-599997674d42?w=500"},
    {"name": "지옥 화염 드래곤", "req_atk": 150, "reward": 2500, "img": "https://images.unsplash.com/photo-1579783902614-a3fb3927b675?w=500"},
    {"name": "멸망의 마왕 파괴신", "req_atk": 400, "reward": 10000, "img": "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=500"}
]

# --- 🎮 세션 데이터 초기화 ---
if "gold" not in st.session_state:
    st.session_state.hero_name = "네온 용사"
    st.session_state.hero_level = 1
    st.session_state.gold = 3000
    st.session_state.weapon_lvl = 0
    st.session_state.protection_scrolls = 1
    st.session_state.log = ["✨ 차원의 문이 열렸습니다. 무기와 영웅을 진화시키세요!"]

# --- 📊 스탯 및 진화 등급 계산 ---
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

# --- 🔨 로직 처리 ---
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
    st.header("🎧 음향 & 설정")
    bgm_on = st.toggle("🎵 BGM 재생", value=True)
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
m3.metric("🦸 히어로", f"Lv.{st.session_state.hero_level}")
m4.metric("🛡️ 무기 연마", f"+{st.session_state.weapon_lvl}")

st.markdown("---")

# 진화형 프로필 및 무기 정보
col_hero, col_weapon = st.columns(2)

hero_info = HERO_TIERS[get_hero_tier_idx()]
weapon_info = WEAPON_TIERS[get_weapon_tier_idx()]

with col_hero:
    st.markdown(f"""
        <div class='profile-card'>
            <img src='{hero_info['img']}' class='art-img'>
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
            <img src='{weapon_info['img']}' class='art-img'>
            <div style='color:#ff007f; font-weight:bold;'>EQUIPPED WEAPON</div>
            <div style='font-size:1.2rem; font-weight:bold;'>+{st.session_state.weapon_lvl} {weapon_info['name']}</div>
            <div style='margin:4px 0;'>무기 ATK: <b>{get_weapon_atk()}</b></div>
            <div style='color:#ff007f;'>성공률: <b>{get_w_rate()}%</b> | 비용: <b>{get_w_cost():,} G</b></div>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("🔨 무기 초월 연마"):
        enhance_weapon()

st.markdown("---")

# --- 👹 던전 전투 시스템 (이미지 & SKIP 기능 추가) ---
st.subheader("👹 괴물 전장 탐험")

# SKIP 토글 옵션
skip_battle = st.checkbox("⏩ 전투 애니메이션 연출 SKIP (빠른 진행)", value=False)

with st.expander("⚔️ 보스 및 몬스터 사냥터 열기", expanded=True):
    monster = random.choice(MONSTERS)
    
    st.markdown(f"#### 👹 출현 괴물: **[{monster['name']}]**")
    st.caption(f"권장 공격력: {monster['req_atk']} ATK | 내 공격력: {get_total_atk()} ATK")
    
    # 괴물 이미지 출력
    st.markdown(f"<img src='{monster['img']}' class='monster-img'>", unsafe_allow_html=True)
    st.write("")
    
    skill = st.radio("⚔️ 스킬 선택", ["기본 공격", "🔥 엑스칼리버 (공격력 2.5배)"], horizontal=True)
    
    if st.button("🚀 전투 개시!", use_container_width=True):
        multiplier = 2.5 if "엑스칼리버" in skill else 1.0
        
        # SKIP 옵션이 꺼져있을 때만 연출 출력
        if not skip_battle:
            status_box = st.empty()
            status_box.info("⚔️ 몬스터에게 돌진하는 중...")
            time.sleep(0.4)
            status_box.warning("💥 격렬한 전투가 펼쳐집니다!")
            time.sleep(0.4)
            status_box.empty()
        
        # 승패 판정
        win_rate = min(95, max(10, int((get_total_atk() * multiplier / monster['req_atk']) * 70)))
        
        if random.randint(1, 100) <= win_rate:
            reward = monster['reward'] + random.randint(100, 500)
            st.session_state.gold += reward
            st.success(f"🎉 **VICTORY!** [{monster['name']}]을(를) 처단하고 {reward:,} Gold를 토벌했습니다!")
            st.session_state.log.append(f"🏆 [{monster['name']}] 처치! (+{reward:,} G)")
        else:
            penalty = random.randint(300, 700)
            st.session_state.gold = max(0, st.session_state.gold - penalty)
            st.error(f"☠️ **DEFEAT...** 괴물의 치명타를 맞아 {penalty:,} Gold를 잃었습니다.")
            st.session_state.log.append(f"💀 [{monster['name']}] 사냥 실패... (-{penalty:,} G)")

# 게임 리셋
st.markdown("---")
if st.button("🔄 게임 데이터 초기화", use_container_width=True):
    st.session_state.clear()
    safe_rerun()

# 로그
with st.expander("📜 모험 기록 일지", expanded=True):
    for log in reversed(st.session_state.log[-5:]):
        st.write(log)
