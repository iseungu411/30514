import random
import time
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Cyberpunk Hero RPG: Rise of Light",
    layout="centered",
    page_icon="⚔️",
)

# --- 효과음 및 사운드 재생 함수 ---
SOUNDS = {
    "click": "https://assets.mixkit.co/active_storage/sfx/2568/2568-preview.mp3",
    "win": "https://assets.mixkit.co/active_storage/sfx/1435/1435-preview.mp3",
    "lose": "https://assets.mixkit.co/active_storage/sfx/2573/2573-preview.mp3",
    "upgrade": "https://assets.mixkit.co/active_storage/sfx/2019/2019-preview.mp3",
    "boss": "https://assets.mixkit.co/active_storage/sfx/2670/2670-preview.mp3",
}


def play_sound(sound_key):
    if sound_key in SOUNDS:
        components.html(
            f"""
            <audio autoplay style="display:none;">
                <source src="{SOUNDS[sound_key]}" type="audio/mpeg">
            </audio>
            """,
            height=0,
        )


# --- 사이버펑크 RPG CSS 스타일 ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b0e14;
        color: #e6e6e6;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .main-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ff007f 0%, #7928ca 50%, #00f0ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .story-box {
        background: rgba(0, 240, 255, 0.05);
        border-left: 4px solid #00f0ff;
        padding: 12px 15px;
        margin-bottom: 20px;
        font-style: italic;
        color: #b3f5ff;
        font-size: 0.95rem;
    }
    .card-box {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid #00f0ff;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.2);
        margin-bottom: 15px;
    }
    .card-title {
        font-size: 1.4rem;
        font-weight: bold;
        color: #ff007f;
        text-shadow: 0 0 8px #ff007f;
    }
    .art-display {
        font-size: 3rem;
        margin: 10px 0;
    }
    .battle-field {
        background: linear-gradient(180deg, #150022 0%, #080010 100%);
        border: 2px solid #ff007f;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        font-size: 2.5rem;
        margin: 15px 0;
    }
    div.stButton > button {
        width: 100% !important;
        height: 50px !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        font-size: 1rem !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)


def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()


# --- 데이터 정의 ---
WEAPON_DATA = [
    {"name": "녹슨 단검", "art": "🗡️", "base": 10},
    {"name": "강철 장검", "art": "⚔️", "base": 25},
    {"name": "빛나는 성검", "art": "🗡️✨", "base": 50},
    {"name": "드래곤 슬레이어", "art": "⚔️🔥", "base": 90},
    {"name": "신을 찌르는 창", "art": "🔱⚡", "base": 150},
]

MONSTERS = [
    {"name": "슬라임", "art": "🟢", "req_atk": 20, "reward": 300},
    {"name": "고블린", "art": "👺", "req_atk": 50, "reward": 800},
    {"name": "오크 족장", "art": "👹", "req_atk": 100, "reward": 2000},
    {"name": "화염 드래곤", "art": "🐉🔥", "req_atk": 200, "reward": 5000},
]

BOSS_DATA = {
    "name": "네오 사이버 아바돈",
    "art": "👾⚡",
    "req_atk": 400,
    "reward": 25000,
    "desc": "도시를 지배하려는 인공지능 마왕. 막강한 디버프와 공격력을 지니고 있습니다.",
}

# --- 게임 초기화 ---
def init_game():
    st.session_state.hero_name = "용사님"
    st.session_state.hero_level = 1
    st.session_state.gold = 1000
    st.session_state.weapon_lvl = 0
    st.session_state.weapon_tier = 0
    st.session_state.shield_potions = 1
    st.session_state.exp_potions = 0
    st.session_state.story_chapter = 1
    st.session_state.boss_cleared = False
    st.session_state.log = ["⚒️ 네오 네온 시티에서의 모험이 시작됩니다."]


if "gold" not in st.session_state:
    init_game()


# --- 수치 계산 ---
def get_hero_atk():
    return st.session_state.hero_level * 15


def get_weapon_atk():
    w = WEAPON_DATA[st.session_state.weapon_tier]
    return w["base"] + (st.session_state.weapon_lvl * 10)


def get_total_atk():
    return get_hero_atk() + get_weapon_atk()


def get_w_cost():
    return (st.session_state.weapon_lvl + 1) * 120


def get_h_cost():
    return st.session_state.hero_level * 150


def get_w_rate():
    return max(20, 100 - (st.session_state.weapon_lvl * 7))


# --- 스토리 관리 ---
def get_current_story():
    chapter = st.session_state.story_chapter
    if st.session_state.boss_cleared:
        return "🏆 **[Chapter 5: 평화의 신호탄]** 최종 보스 '네오 사이버 아바돈'을 물리쳤습니다! 당신은 도시의 위대한 전설입니다."

    stories = {
        1: "📖 **[Chapter 1: 어두운 골목길]** 네온 불빛이 사그라든 도시, 몬스터들이 위협해옵니다. 기초 훈련과 무기 강화로 힘을 키우세요.",
        2: "📖 **[Chapter 2: 본격적인 탐험]** 전투에 익숙해졌습니다. 상점에서 방어 포션을 챙겨 더 깊은 던전으로 향하세요.",
        3: "📖 **[Chapter 3: 드래곤의 그림자]** 막강한 몬스터들이 출몰합니다. 레벨 10 이상을 달성해 보스 레이드를 준비하세요.",
        4: "📖 **[Chapter 4: 마왕과의 결전]** 마왕 '네오 사이버 아바돈'을 쓰러뜨리고 네오 네온 시티를 구원해야 합니다!",
    }
    return stories.get(chapter, stories[1])


def update_story_chapter():
    lvl = st.session_state.hero_level
    if lvl >= 10 and st.session_state.story_chapter < 4:
        st.session_state.story_chapter = 4
    elif lvl >= 6 and st.session_state.story_chapter < 3:
        st.session_state.story_chapter = 3
    elif lvl >= 3 and st.session_state.story_chapter < 2:
        st.session_state.story_chapter = 2


# --- 강화 로직 ---
def enhance_weapon():
    cost = get_w_cost()
    if st.session_state.gold < cost:
        st.toast("⚠️ 골드가 부족합니다!", icon="💰")
        return
    st.session_state.gold -= cost

    if random.randint(1, 100) <= get_w_rate():
        st.session_state.weapon_lvl += 1
        play_sound("upgrade")
        if (
            st.session_state.weapon_lvl % 4 == 0
            and st.session_state.weapon_tier < len(WEAPON_DATA) - 1
        ):
            st.session_state.weapon_tier += 1
            st.toast("🎉 무기가 한 단계 더 진화했습니다!", icon="✨")
        st.session_state.log.append(
            f"⚔️ 무기 강화 성공! (+{st.session_state.weapon_lvl})"
        )
    else:
        st.session_state.weapon_lvl = max(0, st.session_state.weapon_lvl - 1)
        play_sound("lose")
        st.session_state.log.append("❌ 무기 강화 실패! 단계 하락")
    safe_rerun()


def enhance_hero():
    cost = get_h_cost()
    if st.session_state.gold < cost:
        st.toast("⚠️ 골드가 부족합니다!", icon="💰")
        return
    st.session_state.gold -= cost
    st.session_state.hero_level += 1
    play_sound("upgrade")
    update_story_chapter()
    st.session_state.log.append(
        f"🦸 {st.session_state.hero_name} 훈련 성공! (Lv.{st.session_state.hero_level})"
    )
    safe_rerun()


# --- 상점 모달 ---
@st.dialog("🛒 사이버 상점")
def open_shop():
    st.write("### 🧪 보조 아이템 구매")
    st.caption("전투 및 성장에 유용한 물약들을 판매합니다.")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**🛡️ 손실 방지 포션**")
        st.write("패배 시 골드 차감을 1회 막아줍니다.")
        st.write("가격: **500 G**")
        if st.button("구매하기 (500G)", key="buy_shield"):
            if st.session_state.gold >= 500:
                st.session_state.gold -= 500
                st.session_state.shield_potions += 1
                play_sound("click")
                st.toast("🛡️ 방지 포션을 구매했습니다!")
                safe_rerun()
            else:
                st.toast("⚠️ 골드가 부족합니다!")

    with c2:
        st.markdown("**⚡ 경험치 즉시 상승 물약**")
        st.write("히어로 레벨을 즉시 1 상승시킵니다.")
        st.write("가격: **1,200 G**")
        if st.button("구매하기 (1200G)", key="buy_exp"):
            if st.session_state.gold >= 1200:
                st.session_state.gold -= 1200
                st.session_state.hero_level += 1
                play_sound("upgrade")
                update_story_chapter()
                st.toast("⚡ 레벨이 즉시 상승했습니다!")
                safe_rerun()
            else:
                st.toast("⚠️ 골드가 부족합니다!")


# --- ⚔️ 일반 사냥터 모달 ---
@st.dialog("⚔️ 몬스터 사냥터")
def start_battle():
    monster = random.choice(MONSTERS)
    w_art = WEAPON_DATA[st.session_state.weapon_tier]["art"]
    total_atk = get_total_atk()

    st.write(f"### 야생의 **[{monster['name']}]** 이(가) 나타났다!")
    st.caption(f"권장 공격력: {monster['req_atk']} | 내 공격력: {total_atk}")

    battle_area = st.empty()
    msg_area = st.empty()

    battle_area.markdown(
        f"<div class='battle-field'>🦸‍♂️{w_art} &nbsp;&nbsp;&nbsp;&nbsp; {monster['art']}</div>",
        unsafe_allow_html=True,
    )
    msg_area.info("⚔️ 돌격 준비 중...")
    time.sleep(0.8)

    battle_area.markdown(
        f"<div class='battle-field'>&nbsp;&nbsp;🦸‍♂️{w_art}💥{monster['art']}</div>",
        unsafe_allow_html=True,
    )
    msg_area.warning("💥 챙-캉! 격렬하게 전투 중!")
    time.sleep(1.0)

    win_chance = min(95, max(10, int((total_atk / monster["req_atk"]) * 70)))

    if random.randint(1, 100) <= win_chance:
        play_sound("win")
        battle_area.markdown(
            f"<div class='battle-field'>🦸‍♂️{w_art} 👑 &nbsp;&nbsp; 💥💀</div>",
            unsafe_allow_html=True,
        )
        reward = monster["reward"] + random.randint(0, 200)
        st.session_state.gold += reward
        st.session_state.log.append(
            f"🎉 {monster['art']} [{monster['name']}] 처치! (+{reward:,} G)"
        )
        msg_area.success(
            f"🏆 승리! [{monster['name']}]을 처치하고 {reward:,} 골드를 획득했습니다!"
        )
    else:
        play_sound("lose")
        battle_area.markdown(
            f"<div class='battle-field'>💥💫🏃‍♂️ &nbsp;&nbsp; {monster['art']}😈</div>",
            unsafe_allow_html=True,
        )
        if st.session_state.shield_potions > 0:
            st.session_state.shield_potions -= 1
            msg_area.error(
                f"☠️ 패배했으나 방지 포션 사용으로 골드를 지켰습니다! (남은 포션: {st.session_state.shield_potions}개)"
            )
            st.session_state.log.append(
                f"🛡️ [{monster['name']}] 사냥 실패 (포션으로 골드 보호)"
            )
        else:
            penalty = random.randint(100, 300)
            st.session_state.gold = max(0, st.session_state.gold - penalty)
            st.session_state.log.append(
                f"💀 [{monster['name']}] 사냥 실패... (-{penalty:,} G)"
            )
            msg_area.error(
                f"☠️ 패배! 몬스터가 너무 강해 도망쳤습니다... (-{penalty:,} G)"
            )

    if st.button("확인 및 돌아가기", use_container_width=True):
        safe_rerun()


# --- 👹 보스 레이드 모달 ---
@st.dialog("🔥 [BOSS RAID] 마왕 결전")
def start_boss_raid():
    boss = BOSS_DATA
    w_art = WEAPON_DATA[st.session_state.weapon_tier]["art"]
    total_atk = get_total_atk()

    play_sound("boss")
    st.write(f"### 👾 최종 보스 **[{boss['name']}]** 등장!")
    st.write(boss["desc"])
    st.caption(f"권장 공격력: {boss['req_atk']} | 내 공격력: {total_atk}")

    battle_area = st.empty()
    msg_area = st.empty()

    battle_area.markdown(
        f"<div class='battle-field'>🦸‍♂️{w_art} &nbsp;&nbsp;⚡⚡&nbsp;&nbsp; {boss['art']}</div>",
        unsafe_allow_html=True,
    )
    msg_area.error("🔥 마왕의 엄청난 에너지가 느껴집니다!")
    time.sleep(1.2)

    battle_area.markdown(
        f"<div class='battle-field'>⚡🦸‍♂️{w_art}💥⚔️💥{boss['art']}⚡</div>",
        unsafe_allow_html=True,
    )
    msg_area.warning("💥 도시의 운명을 건 치열한 격전이 벌어집니다!")
    time.sleep(1.5)

    win_chance = min(90, max(5, int((total_atk / boss["req_atk"]) * 60)))

    if random.randint(1, 100) <= win_chance:
        play_sound("win")
        battle_area.markdown(
            f"<div class='battle-field'>🏆🦸‍♂️{w_art}👑 &nbsp;&nbsp; 💥💀💥</div>",
            unsafe_allow_html=True,
        )
        st.session_state.gold += boss["reward"]
        st.session_state.boss_cleared = True
        st.session_state.log.append(
            f"👑 [보스 레이드 성공] {boss['name']}을 제압하고 네오 시티를 구했습니다! (+{boss['reward']:,} G)"
        )
        msg_area.success(
            f"🎉 대승리! [{boss['name']}]을 격파하고 {boss['reward']:,} 골드를 획득했습니다!"
        )
    else:
        play_sound("lose")
        battle_area.markdown(
            f"<div class='battle-field'>💥💀🏃‍♂️ &nbsp;&nbsp;&nbsp;&nbsp; {boss['art']}😈</div>",
            unsafe_allow_html=True,
        )
        penalty = 1000
        st.session_state.gold = max(0, st.session_state.gold - penalty)
        st.session_state.log.append(
            f"💀 [{boss['name']}] 레이드 실패... (-{penalty:,} G)"
        )
        msg_area.error(
            f"☠️ 패배! 마왕의 압도적인 힘에 후퇴했습니다... (-{penalty:,} G)"
        )

    if st.button("확인 및 돌아가기", use_container_width=True):
        safe_rerun()


# --- UI 레이아웃 ---
st.markdown(
    "<h1 class='main-title'>⚔️ CYBER HERO: RISE OF LIGHT ⚔️</h1>",
    unsafe_allow_html=True,
)

# 스토리 영역
st.markdown(
    f"<div class='story-box'>{get_current_story()}</div>",
    unsafe_allow_html=True,
)

# 사이드바
with st.sidebar:
    st.header("⚙️ 히어로 설정")
    st.text_input("히어로 이름", key="hero_name")
    st.markdown("---")
    st.markdown("**🎒 소지품 목록**")
    st.write(f"🛡️ 방지 포션: **{st.session_state.shield_potions}개**")

# 상태바
c1, c2, c3 = st.columns(3)
c1.metric("💰 골드", f"{st.session_state.gold:,} G")
c2.metric("⚔️ 총 공격력", f"{get_total_atk():,} ATK")
c3.metric("🦸 히어로 레벨", f"Lv.{st.session_state.hero_level}")

st.markdown("---")

# 캐릭터 & 무기 카드
w_info = WEAPON_DATA[st.session_state.weapon_tier]
col_hero, col_weapon = st.columns(2)

with col_hero:
    st.markdown(
        f"""
        <div class='card-box'>
            <div style='color:#a0a0a0; font-size:0.85rem;'>MY HERO</div>
            <div class='art-display'>🦸‍♂️</div>
            <div class='card-title'>{st.session_state.hero_name}</div>
            <div>기본 ATK: <b>{get_hero_atk()}</b></div>
            <div style='color:#00f0ff; margin-top:5px;'>훈련 비용: <b>{get_h_cost():,} G</b></div>
        </div>
    """,
        unsafe_allow_html=True,
    )
    if st.button("💪 히어로 훈련하기", use_container_width=True):
        enhance_hero()

with col_weapon:
    st.markdown(
        f"""
        <div class='card-box'>
            <div style='color:#a0a0a0; font-size:0.85rem;'>EQUIPPED WEAPON</div>
            <div class='art-display'>{w_info['art']}</div>
            <div class='card-title'>+{st.session_state.weapon_lvl} {w_info['name']}</div>
            <div>무기 ATK: <b>{get_weapon_atk()}</b></div>
            <div style='color:#ff007f; margin-top:5px;'>성공률: <b>{get_w_rate()}%</b> | 비용: <b>{get_w_cost():,} G</b></div>
        </div>
    """,
        unsafe_allow_html=True,
    )
    if st.button("🔨 무기 강화하기", use_container_width=True):
        enhance_weapon()

st.markdown("---")

# 액션 영역 (상점 / 사냥 / 보스 레이드)
st.subheader("🏙️ 네오 시티 구역")
col_battle, col_shop, col_boss = st.columns([2, 1, 2])

with col_battle:
    if st.button("⚔️ 일반 사냥터", use_container_width=True):
        start_battle()

with col_shop:
    if st.button("🛒 상점", use_container_width=True):
        open_shop()

with col_boss:
    boss_btn_label = (
        "👑 마왕 격파 완료"
        if st.session_state.boss_cleared
        else "🔥 [BOSS] 마왕 레이드"
    )
    if st.button(
        boss_btn_label,
        use_container_width=True,
        disabled=st.session_state.boss_cleared,
    ):
        start_boss_raid()

st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔄 게임 초기화", use_container_width=True):
    init_game()
    safe_rerun()

# 기록 로그
with st.expander("📜 모험 기록", expanded=True):
    for log in reversed(st.session_state.log[-5:]):
        st.write(log)
