import streamlit as st
import random

# 1. 페이지 및 레이아웃 기본 설정
st.set_page_config(page_title="Dark Fantasy RPG - Visual Upgrade", page_icon="⚔️", layout="wide")

# Custom CSS로 텍스처 및 비주얼 테마 강화
st.markdown("""
<style>
    .card {
        background-color: #181825;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #313244;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }
    .warrior-title { color: #89b4fa; font-weight: bold; font-size: 22px; }
    .sword-title { color: #f9e2af; font-weight: bold; font-size: 22px; }
    .monster-title { color: #f38ba8; font-weight: bold; font-size: 22px; }
    .detail-tag {
        background-color: #313244;
        color: #cdd6f4;
        padding: 3px 8px;
        border-radius: 5px;
        font-size: 12px;
        margin-right: 5px;
    }
</style>
""", unsafe_allow_html=True)

st.title("⚔️ 다크 판타지: 디테일 강화 비주얼 코딩")
st.caption("몬스터, 전사, 검의 퀄리티 요소가 모두 반영된 Streamlit 인터페이스입니다.")

col1, col2, col3 = st.columns(3)

# ---------------------------------------------------------
# [전사] 섹션: 전투 흔적, 룬 문양이 새겨진 갑옷, 억센 근육 표현
# ---------------------------------------------------------
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="warrior-title">🛡️ 칠흑의 룬 기사 (Warrior)</p>', unsafe_allow_html=True)
    
    # 퀄리티 디테일 태그
    st.markdown('<span class="detail-tag">거친 흠집</span><span class="detail-tag">실핏줄 선 눈매</span><span class="detail-tag">룬 문양</span>', unsafe_allow_html=True)
    
    st.code("""
       /\\
      /  \\       [전투 흔적이 가득한 갑옷]
     | [] |      "핏줄 선 눈으로 적을 노려본다."
    (|==|)      어깨 스파이크 & 찢어진 천 망토
    /|  |\\
   / |__| \\
    """, language="text")
    
    st.write("**고유 특성:** `전투 광란` (공격 시 15% 확률로 궤멸적 피해)")
    
    # 체력 및 상태 제어
    warrior_hp = st.slider("전사 체력 (HP)", 0, 200, 180, key="w_hp")
    st.progress(warrior_hp / 200)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# [칼] 섹션: 날카로운 빛 반사, 룬 발광, 검기 및 이펙트 연출
# ---------------------------------------------------------
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="sword-title">🗡️ 룬 각인 서리검 (Mythic Sword)</p>', unsafe_allow_html=True)
    
    # 퀄리티 디테일 태그
    st.markdown('<span class="detail-tag">날카로운 빛 반사</span><span class="detail-tag">룬 문자 발광</span><span class="detail-tag">검기 이펙트</span>', unsafe_allow_html=True)
    
    st.code("""
       /| ________________
O|===|* >________________>
       \\|
    ✨ 칼날 끝에 감도는 푸른 검기 (Emanating Frost)
    📜 손잡이: 가죽 끈 촘촘함 + 보석 장식
    """, language="text")
    
    sword_atk = st.number_input("검 기본 공격력", value=65, step=5)
    st.write(f"**추가 효과:** 명중 시 둔화 부여 + 방어 무시 피해 (+{sword_atk // 5})")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# [몬스터] 섹션: 점액질 피부, 산성 침, 비대칭 뿔, 발광하는 눈
# ---------------------------------------------------------
with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="monster-name">👹 심연의 아바돈 (Monster)</p>', unsafe_allow_html=True)
    
    # 퀄리티 디테일 태그
    st.markdown('<span class="detail-tag">점액질 피부</span><span class="detail-tag">부러진 뿔(비대칭)</span><span class="detail-tag">산성 침</span>', unsafe_allow_html=True)
    
    st.code("""
     (o.O)   < *뚝.. 뚝..* (산성 침 방울)
    /  :  \\  [붉게 발광하는 눈동자]
   (  :::  ) 불균일한 거친 피부 & 마기(魔氣)
   ^^-----^^
    """, language="text")
    
    st.write("**고유 특성:** `산성 피부` (근접 공격 시 반사 데미지)")
    
    # 체력 및 상태 제어
    monster_hp = st.slider("몬스터 체력 (HP)", 0, 300, 250, key="m_hp")
    st.progress(monster_hp / 300)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# 전투 실행 로직 (디테일 텍스트 출력)
if st.button("⚔️ 강화된 전투 이펙트 실행", type="primary", use_container_width=True):
    is_crit = random.choice([True, False, False])
    
    if is_crit:
        damage = sword_atk * 2
        st.error(f"💥 **크리티컬 히트!** 서리검의 룬 문자가 강하게 발광하며 몬스터에게 **{damage}**의 피할 수 없는 검기 피해를 입혔습니다!")
    else:
        damage = sword_atk
        st.success(f"🗡️ 전사가 칼을 휘둘렀습니다! 몬스터의 거친 비늘을 떪으며 **{damage}**의 데미지를 주었습니다.")
