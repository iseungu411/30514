import streamlit as st
import random
import time

# ---------------------------------------------------------
# 1. 페이지 설정 및 다크 판타지 Custom CSS
# ---------------------------------------------------------
st.set_page_config(page_title="검 강화하기: 전설의 시작", page_icon="⚔️", layout="wide")

st.markdown("""
<style>
    /* 전체 배경 및 폰트 */
    .stApp {
        background-color: #0d0e15;
        color: #e0e0e0;
    }
    
    /* 네온 카드 스타일 */
    .game-card {
        background: linear-gradient(145deg, #161925, #0f111a);
        border: 2px solid #2a2e3d;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.7);
        text-align: center;
        margin-bottom: 20px;
    }
    
    .sword-card {
        border: 2px solid #ffd700;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.2);
    }
    
    /* 텍스트 퀄리티 디테일 */
    .weapon-title { font-size: 28px; font-weight: 800; color: #ffd700; text-shadow: 0 0 10px #ffd700; }
    .warrior-title { font-size: 22px; font-weight: bold; color: #40a9ff; }
    .monster-title { font-size: 22px; font-weight: bold; color: #ff4d4f; }
    
    /* 상태 및 태그 */
    .badge {
        background-color: #1f2430;
        border: 1px solid #434c5e;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 13px;
        color: #88c0d0;
        margin: 2px;
        display: inline-block;
    }
    
    .status-box {
        background-color: #12141d;
        padding: 12px;
        border-radius: 8px;
        border-left: 4px solid #ffd700;
        text-align: left;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. 게임 세션 상태 초기화 (State Management)
# ---------------------------------------------------------
if 'level' not in st.session_state:
    st.session_state.level = 0
if 'gold' not in st.session_state:
    st.session_state.gold = 1000
if 'logs' not in st.session_state:
    st.session_state.logs = ["🗡️ 장인의 대장간에 입장하셨습니다."]
if 'monster_hp' not in st.session_state:
    st.session_state.monster_hp = 100

# 검 정보 테이블 (레벨별 명칭, 확률, 스탯)
SWORD_DATA = {
    0: {"name": "녹슨 연습용 단검", "atk": 10, "rate": 100, "cost": 100, "color": "#a0a0a0", "effect": "마모된 철재 / 빛바랜 표면"},
    1: {"name": "강철 이중날 검", "atk": 25, "rate": 90, "cost": 200, "color": "#ffffff", "effect": "날카로운 칼날 / 거친 흠집"},
    2: {"name": "기사의 제련된 롱소드", "atk": 50, "rate": 80, "cost": 400, "color": "#73d13d", "effect": "은빛 가죽 그립 / 정돈된 선채"},
    3: {"name": "푸른 불꽃의 룬 세이버", "atk": 90, "rate": 70, "cost": 800, "color": "#40a9ff", "effect": "검기를 감싸는 푸른 마기 / 룬 발광"},
    4: {"name": "심연 추적자의 성검", "atk": 150, "rate": 55, "cost": 1500, "color": "#9254de", "effect": "빛 무늬 섬광 / 이빨 빠진 전투 흔적"},
    5: {"name": "🔥 멸망의 드래곤 슬레이어", "atk": 300, "rate": 35, "cost": 3000, "color": "#ff4d4f", "effect": "용의 혈액 각인 / 화염 오라 방출"},
    6: {"name": "⚡ 신성 룬 각인: 엑스칼리버", "atk": 600, "rate": 15, "cost": 5000, "color": "#ffd700", "effect": "절대적 빛 반사 / 상공을 가르는 검기"},
}

curr_sword = SWORD_DATA.get(st.session_state.level, SWORD_DATA[6])

# ---------------------------------------------------------
# 3. 메인 레이아웃 및 대시보드
# ---------------------------------------------------------
st.title("⚔️ 검 강화하기: 다크 판타지 아레나")
st.caption("검을 강화하여 더 강력한 몬스터를 토벌하고 전설의 기사가 되어보세요.")

# 상단 유저 재화 및 상태 표시
stat_col1, stat_col2, stat_col3 = st.columns(3)
with stat_col1:
    st.metric(label="💰 보유 골드", value=f"{st.session_state.gold:,} Gold")
with stat_col2:
    st.metric(label="🗡️ 현재 강화 단계", value=f"+{st.session_state.level} 단계")
with stat_col3:
    st.metric(label="💥 검 공격력", value=f"{curr_sword['atk']} ATK")

st.divider()

col1, col2, col3 = st.columns([1, 1.2, 1])

# ---------------------------------------------------------
# [LEFT] 전사 (Warrior) 섹션
# ---------------------------------------------------------
with col1:
    st.markdown('<div class="game-card">', unsafe_allow_html=True)
    st.markdown('<p class="warrior-title">🛡️ 칠흑의 룬 기사</p>', unsafe_allow_html=True)
    
    st.code("""
       /\\
      /  \\      [전투 준비 완료]
     | [] |     - 실핏줄 선 눈매
    (|==|)     - 전투 흔적이 가득한 갑옷
    /|  |\\     - 찢어진 천 망토
   / |__| \\
    """, language="text")
    
    st.markdown('<span class="badge">갑옷 상처 연출</span><span class="badge">광란 패시브</span>', unsafe_allow_html=True)
    st.caption("전투 시 일정 확률로 2배의 크리티컬 검기 피해를 생성합니다.")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# [CENTER] 메인 메커니즘 - 검 정보 및 강화 대장간
# ---------------------------------------------------------
with col2:
    st.markdown('<div class="game-card sword-card">', unsafe_allow_html=True)
    st.markdown(f'<p class="weapon-title" style="color:{curr_sword["color"]};">{curr_sword["name"]}</p>', unsafe_allow_html=True)
    
    # 디테일한 비주얼 연출 (ASCII Art & Dynamic FX)
    st.code(f"""
       /| _____________________________________
O|===|* >___  +{st.session_state.level} {curr_sword['name']} ___>
       \\|
    ✨ 이펙트: {curr_sword['effect']}
    """, language="text")
    
    st.markdown(f"""
    <div class="status-box">
        <b>• 다음 단계 성공 확률:</b> {curr_sword['rate']}%<br>
        <b>• 강화 비용:</b> {curr_sword['cost']:,} Gold<br>
        <b>• 특수 효과:</b> 몬스터 방어력 무시 및 타격 시 시각 이펙트 발생
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # 강화 버튼 클릭 로직
    if st.button("🔨 대장장이 햄머질 (강화 실행)", type="primary", use_container_width=True):
        if st.session_state.gold < curr_sword['cost']:
            st.error("❌ 골드가 부족합니다! 몬스터를 토벌하여 골드를 수급하세요.")
        else:
            st.session_state.gold -= curr_sword['cost']
            
            # 성공 여부 판정
            if random.randint(1, 100) <= curr_sword['rate']:
                st.session_state.level += 1
                st.balloons()
                st.toast(f"🎉 강화 성공! +{st.session_state.level} 단계를 달성했습니다!", icon="✨")
                st.session_state.logs.append(f"✅ [{time.strftime('%H:%M:%S')}] 강화 성공! (+{st.session_state.level} {SWORD_DATA.get(st.session_state.level, SWORD_DATA[6])['name']})")
            else:
                st.snow()
                st.toast("💥 강화 실패! 검의 기운이 뒤흔들렸습니다.", icon="💔")
                if st.session_state.level > 0:
                    st.session_state.level -= 1
                st.session_state.logs.append(f"❌ [{time.strftime('%H:%M:%S')}] 강화 실패... (단계 하강: +{st.session_state.level})")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# [RIGHT] 몬스터 (Monster) & 던전 토벌
# ---------------------------------------------------------
with col3:
    st.markdown('<div class="game-card">', unsafe_allow_html=True)
    st.markdown('<p class="monster-title">👹 심연의 아바돈</p>', unsafe_allow_html=True)
    
    st.code("""
     (o.O)   < *뚝.. 뚝..* 
    /  :  \\  [산성 침 방울]
   (  :::  ) - 붉게 발광하는 눈동자
   ^^-----^^ - 부러진 비대칭 뿔
    """, language="text")
    
    st.markdown('<span class="badge">점액질 피부</span><span class="badge">산성 침</span>', unsafe_allow_html=True)
    
    # 몬스터 체력 바
    st.write(f"**몬스터 HP:** {st.session_state.monster_hp} / 500")
    st.progress(st.session_state.monster_hp / 500)
    
    # 공격 전투 로직
    if st.button("⚔️ 몬스터 공격 (골드 획득)", use_container_width=True):
        damage = curr_sword['atk'] + random.randint(0, 20)
        st.session_state.monster_hp -= damage
        
        if st.session_state.monster_hp <= 0:
            reward = 1000 + (st.session_state.level * 300)
            st.session_state.gold += reward
            st.session_state.monster_hp = 500
            st.success(f"☠️ 몬스터 토벌 완료! **+{reward:,} Gold** 획득!")
            st.session_state.logs.append(f"🗡️ [{time.strftime('%H:%M:%S')}] 몬스터 토벌 성공 (+{reward} Gold)")
        else:
            st.toast(f"⚔️ {damage}의 데미지를 입혔습니다!", icon="💥")
            
        st.rerun()
        
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. 하단 히스토리 로그
# ---------------------------------------------------------
st.divider()
st.subheader("📜 대장간 & 전투 기록")
for log in reversed(st.session_state.logs[-5:]):
    st.text(log)
