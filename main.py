import streamlit as st
import random

# 페이지 기본 설정
st.set_page_config(page_title="Dark Fantasy RPG", page_icon="⚔️", layout="wide")

# Custom CSS로 퀄리티 업그레이드 (네온 효과 및 카드 스타일)
st.markdown("""
<style>
    .stat-card {
        background-color: #1e1e2e;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #313244;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .hero-name { color: #89b4fa; font-weight: bold; font-size: 20px; }
    .monster-name { color: #f38ba8; font-weight: bold; font-size: 20px; }
    .weapon-name { color: #f9e2af; font-weight: bold; font-size: 18px; }
</style>
""", unsafe_allow_html=True)

st.title("⚔️ 전설의 전사 vs 기형의 몬스터")

col1, col2, col3 = st.columns(3)

# 1. 전사 (Warrior) 섹션
with col1:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<p class="hero-name">🛡️ 칠흑의 룬 기사 (Warrior)</p>', unsafe_allow_html=True)
    
    # 전사 시각화 (ASCII Art)
    st.code("""
      /\\
     /  \\
    | [] |   [전투 태세]
    (|==|)   "전장의 혈기를 느낀다."
    /|  |\\
   / |__| \\
    """, language="text")
    
    st.write("**특성:** 전투 광란 (공격 시 15% 확률로 2배 데미지)")
    hp_warrior = st.slider("전사 체력 (HP)", 0, 200, 150, key="w_hp")
    st.progress(hp_warrior / 200)
    st.markdown('</div>', unsafe_allow_html=True)

# 2. 칼 (Sword) 섹션
with col2:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<p class="weapon-name">🗡️ 룬 각인 서리검 (Mythic Sword)</p>', unsafe_allow_html=True)
    
    # 무기 시각화 (ASCII Art)
    st.code("""
       /| ________________
O|===|* >________________>
       \\|
    [강화: +12] [속성: 빙결]
    """, language="text")
    
    st.write("**검의 효과:** 공격 시 대상을 20% 확률로 둔화")
    sword_atk = st.number_input("무기 공격력", value=45, step=5)
    st.caption(f"✨ 명중 시 방어구 무시 데미지 +{sword_atk // 5} 추가")
    st.markdown('</div>', unsafe_allow_html=True)

# 3. 몬스터 (Monster) 섹션
with col3:
    st.markdown('<div class="stat-card">', unsafe_allow_html=True)
    st.markdown('<p class="monster-name">👹 심연의 아바돈 (Abyssal Monster)</p>', unsafe_allow_html=True)
    
    # 몬스터 시각화 (ASCII Art)
    st.code("""
     (o.O)   < Grrr...
    /  :  \\  [산성 침을 흘리는 중]
   (  :::  )
   ^^-----^^
    """, language="text")
    
    st.write("**특성:** 산성 피부 (접촉 시 반사 데미지)")
    hp_monster = st.slider("몬스터 체력 (HP)", 0, 300, 220, key="m_hp")
    st.progress(hp_monster / 300)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# 전투 로직 테스트 버튼
if st.button("⚔️ 공격 실행하기", type="primary", use_container_width=True):
    critical = random.choice([True, False, False])
    damage = sword_atk * 2 if critical else sword_atk
    
    if critical:
        st.error(f"💥 크리티컬 히트! 전사가 몬스터에게 **{damage}**의 궤멸적인 데미지를 입혔습니다!")
    else:
        st.success(f"🗡️ 전사가 칼을 휘둘러 몬스터에게 **{damage}**의 데미지를 입혔습니다.")
