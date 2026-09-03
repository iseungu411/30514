import streamlit as st
import random
import time

# 페이지 기본 설정
st.set_page_config(
    page_title="RPG: 용사와 전설의 성검",
    page_icon="⚔️",
    layout="wide"
)

# -------------------------------------------------------------------
# 1. 세션 상태 (Game State) 초기화
# -------------------------------------------------------------------
if "hero_level" not in st.session_state:
    st.session_state.hero_level = 1
if "sword_level" not in st.session_state:
    st.session_state.sword_level = 0
if "gold" not in st.session_state:
    st.session_state.gold = 2000

# 기초 스탯 계산 (성검 강화도가 공격력에 폭발적 추가)
hero_atk = 15 + (st.session_state.hero_level * 15) + (st.session_state.sword_level * 25)
hero_hp = 120 + (st.session_state.hero_level * 60)

hero_cost = int(120 * (1.35 ** (st.session_state.hero_level - 1)))
sword_cost = int(200 * (1.5 ** st.session_state.sword_level))

# -------------------------------------------------------------------
# 2. 고급 CSS 연출 (네온, 검 이펙트, 카드 스타일)
# -------------------------------------------------------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0c10;
        color: #c5c6c7;
    }
    
    /* 성검 표시 영역 */
    .sword-card {
        background: linear-gradient(135deg, #1f2833 0%, #0b0c10 100%);
        border: 2px solid #66fcf1;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 15px rgba(102, 252, 241, 0.3);
    }
    .sword-title {
        color: #66fcf1;
        font-weight: bold;
        font-size: 22px;
        margin-bottom: 5px;
    }

    /* 몬스터 회전 마법진 */
    .magic-circle-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px 0;
    }
    .magic-circle {
        width: 160px;
        height: 160px;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 55px;
        animation: rotateMagic 8s linear infinite;
        box-shadow: 0 0 30px #45a29e;
        border: 4px dashed #45a29e;
        background: radial-gradient(circle, rgba(102,252,241,0.15) 0%, rgba(11,12,16,0.9) 80%);
    }
    @keyframes rotateMagic {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    /* 용사 스탯 박스 */
    .hero-card {
        background-color: #1f2833;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #45a29e;
        text-align: center;
    }
    </style>
""", unsafe_allowed_html=True)

# -------------------------------------------------------------------
# 3. 데이터 및 AI 로직
# -------------------------------------------------------------------
MONSTER_NAMES = ["고블린 주술사", "아크 오크", "암흑 골렘", "심해 몬스터", "화염 드래곤", "마왕 아스타로트"]
MONSTER_ICONS = ["👹", "👺", "🗿", "🐙", "🐉", "💀"]
SWORD_NAMES = ["녹슨 철검", "강철 장검", "빛의 룬소드", "용살자의 대검", "신성한 엑스칼리버"]

def get_sword_info(lvl):
    idx = min(lvl // 3, len(SWORD_NAMES) - 1)
    name = f"{SWORD_NAMES[idx]} (+{lvl})"
    return name

def get_monster_stats(level):
    name = f"Lvl.{level} {MONSTER_NAMES[(level-1) % len(MONSTER_NAMES)]}"
    hp = int(100 * (1.27 ** (level - 1)))
    atk = int(12 * (1.24 ** (level - 1)))
    reward = int(70 * (1.33 ** (level - 1)))
    icon = MONSTER_ICONS[(level-1) % len(MONSTER_ICONS)]
    return {"level": level, "name": name, "hp": hp, "atk": atk, "reward": reward, "icon": icon}

def recommend_monster(h_atk, h_hp):
    best_level = 1
    for lvl in range(1, 51):
        m = get_monster_stats(lvl)
        turns_to_kill_m = (m["hp"] + h_atk - 1) // h_atk
        turns_to_kill_h = (h_hp + m["atk"] - 1) // m["atk"]
        if turns_to_kill_m <= turns_to_kill_h:
            best_level = lvl
    return best_level

# -------------------------------------------------------------------
# 4. UI 레이아웃
# -------------------------------------------------------------------
st.title("⚔️ 전설의 용사와 AI 토벌전")
st.caption("고화질 그래픽과 성장 시스템이 적용된 몬스터 토벌 RPG입니다.")

col1, col2 = st.columns([1, 1])

# --- [좌측: 용사 & 검 스탯 관리] ---
with col1:
    st.subheader("🛡️ 용사 & 전설의 성검")
    
    # 성검 외형 카드
    sword_name = get_sword_info(st.session_state.sword_level)
    st.markdown(f"""
    <div class="sword-card">
        <div class="sword-title">🗡️ {sword_name}</div>
        <p style="color: #66fcf1; margin:0;">공격력 보너스: +{st.session_state.sword_level * 25}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # 용사 스탯 표시
    st.markdown(f"""
    <div class="hero-card">
        <h4>🎖️ 용사 레벨 {st.session_state.hero_level}</h4>
        <p>❤️ <b>체력:</b> {hero_hp} | ⚔️ <b>총 공격력:</b> {hero_atk}</p>
        <p style="color:#66fcf1;">💰 <b>보유 골드:</b> {st.session_state.gold:,} G</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button(f"⬆️ 용사 레벨업\n({hero_cost:,} G)", use_container_width=True):
            if st.session_state.gold >= hero_cost:
                st.session_state.gold -= hero_cost
                st.session_state.hero_level += 1
                st.rerun()
            else:
                st.error("골드가 부족합니다!")
                
    with btn_col2:
        if st.button(f"🗡️ 검 제련하기\n({sword_cost:,} G)", use_container_width=True):
            if st.session_state.gold >= sword_cost:
                st.session_state.gold -= sword_cost
                st.session_state.sword_level += 1
                st.success("성검 강화에 성공했습니다!")
                st.rerun()
            else:
                st.error("골드가 부족합니다!")

    st.divider()

    # AI 추천
    st.subheader("🤖 AI 맞춤 토벌 분석")
    if st.button("🔍 최적 몬스터 추천받기", type="secondary", use_container_width=True):
        rec_lvl = recommend_monster(hero_atk, hero_hp)
        rec_m = get_monster_stats(rec_lvl)
        st.info(f"💡 AI 추천: **{rec_m['name']}** (승리 확률 85% 이상, 최적 골드 효율)")
        st.session_state.selected_level = rec_lvl

# --- [우측: 몬스터 및 전투 연출] ---
with col2:
    st.subheader("👾 몬스터 토벌전")
    
    default_lvl = st.session_state.get("selected_level", 1)
    target_level = st.slider("몬스터 단계 (1~50)", 1, 50, value=default_lvl)
    monster = get_monster_stats(target_level)

    # 몬스터 회전 연출
    st.markdown(f"""
    <div class="magic-circle-container">
        <div class="magic-circle">
            {monster['icon']}
        </div>
    </div>
    <div style="text-align: center;">
        <h3 style="color:#45a29e;">{monster['name']}</h3>
        <p>❤️ HP: {monster['hp']:,} | ⚔️ ATK: {monster['atk']:,} | 💎 보상: {monster['reward']:,} G</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    
    if st.button("⚔️ 전장으로 돌진!", type="primary", use_container_width=True):
        st.write("---")
        st.subheader("⚡ 실시간 교전 브리핑")
        
        h_hp_curr = hero_hp
        m_hp_curr = monster["hp"]
        
        hero_bar = st.progress(1.0, text=f"용사 HP: {h_hp_curr}/{hero_hp}")
        monster_bar = st.progress(1.0, text=f"{monster['name']} HP: {m_hp_curr}/{monster['hp']}")
        
        status_text = st.empty()
        
        while h_hp_curr > 0 and m_hp_curr > 0:
            time.sleep(0.3)
            
            # 용사 공격
            damage = int(hero_atk * random.uniform(0.9, 1.15))
            m_hp_curr = max(0, m_hp_curr - damage)
            monster_bar.progress(m_hp_curr / monster["hp"], text=f"{monster['name']} HP: {m_hp_curr}/{monster['hp']}")
            status_text.markdown(f"🗡️ **성검의 일격!** `{damage}`의 강력한 물리 피해를 입혔습니다.")
            
            if m_hp_curr <= 0:
                break
                
            time.sleep(0.3)
            
            # 몬스터 반격
            m_damage = int(monster["atk"] * random.uniform(0.85, 1.1))
            h_hp_curr = max(0, h_hp_curr - m_damage)
            hero_bar.progress(h_hp_curr / hero_hp, text=f"용사 HP: {h_hp_curr}/{hero_hp}")
            status_text.markdown(f"🔥 **{monster['name']}의 공격!** `{m_damage}`의 피해를 입었습니다.")

        st.write("---")
        if m_hp_curr <= 0:
            st.balloons()
            st.success(f"🏆 **토벌 성공!** {monster['name']}를 제압하고 **{monster['reward']:,} G**를 수확했습니다!")
            st.session_state.gold += monster["reward"]
        else:
            st.error("☠️ **패배...** 성검을 추가 제련하거나 용사를 레벨업한 뒤 다시 도전하세요.")
