import streamlit as st
import random
import time

# 페이지 설정 (화려한 네온 다크 테 테마)
st.set_page_config(page_title="GEOMETRY DASH STREAMLIT", layout="centered", initial_sidebar_state="collapsed")

# --- 고급 네온/사이버펑크 CSS ---
st.markdown("""
    <style>
    .stApp {
        background: #080810;
        color: #ffffff;
        font-family: 'Courier New', monospace;
    }
    
    /* 타이틀 레트로 네온 효과 */
    .gd-title {
        text-align: center;
        font-size: 2.8rem;
        font-weight: 900;
        color: #fff;
        text-shadow: 0 0 10px #00f0ff, 0 0 20px #00f0ff, 0 0 40px #00f0ff, 0 0 80px #ff007f;
        margin-bottom: 5px;
        letter-spacing: 3px;
    }

    /* 게임 스테이지 화면 (격자무늬 + 네온 테두리) */
    .game-screen {
        background: linear-gradient(180deg, #05050a 0%, #1a0022 100%);
        border: 3px solid #00f0ff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.4), inset 0 0 15px rgba(255, 0, 127, 0.3);
        background-size: 40px 40px;
        background-image: 
            linear-gradient(to right, rgba(255, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
    }

    /* 난이도 배지 */
    .level-badge {
        font-size: 1.1rem;
        font-weight: bold;
        padding: 6px 16px;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 10px;
    }
    .easy { background-color: #00b894; box-shadow: 0 0 10px #00b894; }
    .hard { background-color: #fdcb6e; color: #000; box-shadow: 0 0 10px #fdcb6e; }
    .demon { background-color: #d63031; box-shadow: 0 0 15px #d63031; }

    /* 대시 트랙 라인 */
    .track-row {
        font-size: 2rem;
        letter-spacing: 5px;
        background: rgba(0,0,0,0.5);
        padding: 10px;
        border-radius: 8px;
        border-bottom: 2px solid #ff007f;
        text-align: center;
        white-space: nowrap;
        overflow: hidden;
    }

    /* 점프 버튼 메가 네온 스타일 */
    div.stButton > button {
        width: 100% !important;
        height: 70px !important;
        background: linear-gradient(45deg, #ff007f, #7928ca) !important;
        color: white !important;
        font-size: 1.6rem !important;
        font-weight: 900 !important;
        border-radius: 12px !important;
        border: 2px solid #00f0ff !important;
        box-shadow: 0 0 20px rgba(255, 0, 127, 0.6) !important;
        text-shadow: 0 0 5px #ffffff;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.9) !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 레벨별 설정 ---
LEVEL_SETTINGS = {
    "1. Stereo Madness (Easy)": {
        "badge": "EASY", "class": "easy",
        "length": 20, "trap_rate": 0.25, "speed": 1
    },
    "2. Electrodynamix (Hard)": {
        "badge": "HARD", "class": "hard",
        "length": 30, "trap_rate": 0.40, "speed": 2
    },
    "3. Clubstep (Extreme Demon)": {
        "badge": "DEMON ☠️", "class": "demon",
        "length": 40, "trap_rate": 0.55, "speed": 3
    }
}

OBSTACLES = ["▲", "▲▲", "⚡", "🔴"]  # 가시, 이중가시, 레이저, 구체

def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

def init_level(selected_level_name):
    cfg = LEVEL_SETTINGS[selected_level_name]
    st.session_state.current_level = selected_level_name
    st.session_state.pos = 0
    st.session_state.track_length = cfg["length"]
    
    # 맵 트랙 생성 (0: 안전, 1~4: 장애물)
    track = [0] * cfg["length"]
    for i in range(3, cfg["length"] - 2): # 초반 3칸은 안전지대
        if random.random() < cfg["trap_rate"]:
            track[i] = random.randint(1, len(OBSTACLES))
            # 연속 극악 난이도 방지
            if i > 0 and track[i-1] != 0:
                track[i] = 0
                
    st.session_state.track = track
    st.session_state.is_jumping = False
    st.session_state.game_over = False
    st.session_state.clear = False

if "pos" not in st.session_state:
    init_level("1. Stereo Madness (Easy)")

# --- 게임 제어 로직 ---
def step_forward(jump=False):
    if st.session_state.game_over or st.session_state.clear:
        return

    # 다음 위치 이동
    st.session_state.pos += 1
    current_pos = st.session_state.pos

    # 완주 체크
    if current_pos >= st.session_state.track_length:
        st.session_state.clear = True
        safe_rerun()
        return

    # 충돌 판정
    obstacle = st.session_state.track[current_pos]
    if obstacle != 0:
        if not jump:  # 장애물이 있는데 점프를 안함 -> 사망!
            st.session_state.game_over = True
        else:
            # 점프 성공 시 소소한 피드백
            st.toast("⚡ PERFECT JUMP!", icon="🔥")

    safe_rerun()

# --- 화면 UI 구성 ---
st.markdown("<h1 class='gd-title'>📐 GEOMETRY DASH</h1>", unsafe_allow_html=True)

# 레벨 선택 드롭다운
selected_level = st.selectbox(
    "SELECT LEVEL", 
    list(LEVEL_SETTINGS.keys()),
    index=list(LEVEL_SETTINGS.keys()).index(st.session_state.get("current_level", "1. Stereo Madness (Easy)"))
)

if selected_level != st.session_state.get("current_level"):
    init_level(selected_level)
    safe_rerun()

cfg = LEVEL_SETTINGS[selected_level]

# 헤더 정보
progress_pct = int((st.session_state.pos / st.session_state.track_length) * 100)
st.markdown(f"""
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <span class='level-badge {cfg["class"]}'>{cfg["badge"]}</span>
        <span style='font-size: 1.3rem; font-weight: bold; color: #00f0ff;'>PROGRESS: {progress_pct}%</span>
    </div>
""", unsafe_allow_html=True)

st.progress(progress_pct / 100)

# 메인 트랙 렌더링 화면
st.markdown("<div class='game-screen'>", unsafe_allow_html=True)

# 시야(View Window): 플레이어 주변 10칸 시각화
window_size = 10
start_idx = max(0, st.session_state.pos - 2)
end_idx = min(st.session_state.track_length, start_idx + window_size)

track_display = ""
for i in range(start_idx, end_idx):
    if i == st.session_state.pos:
        if st.session_state.game_over:
            track_display += "<span style='color:#ff0000; font-size:2.5rem;'>💥</span> "
        else:
            track_display += "<span style='color:#00f0ff; text-shadow:0 0 10px #00f0ff;'>🟩</span> " # 플레이어 아이콘
    else:
        obs_code = st.session_state.track[i]
        if obs_code == 0:
            track_display += "<span style='color:#333;'>_</span> "
        else:
            obs_symbol = OBSTACLES[obs_code - 1]
            track_display += f"<span style='color:#ff007f; text-shadow:0 0 8px #ff007f;'>{obs_symbol}</span> "

st.markdown(f"<div class='track-row'>{track_display}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
st.write("")

# 게임 상태별 콘트롤러
if st.session_state.clear:
    st.balloons()
    st.success(f"🏆 LEVEL COMPLETE! {selected_level} 클리어!")
    if st.button("🔄 NEXT / RETRY"):
        init_level(selected_level)
        safe_rerun()

elif st.session_state.game_over:
    st.error(f"☠️ DESTROYED at {progress_pct}%!")
    if st.button("💥 TRY AGAIN"):
        init_level(selected_level)
        safe_rerun()

else:
    # 실시간 액션 버튼 (두 개의 타이밍 제어)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("▶️ DASH (직진)"):
            step_forward(jump=False)
    with c2:
        if st.button("🚀 JUMP! (점프)"):
            step_forward(jump=True)

# 가이드
with st.expander("🎮 HOW TO PLAY"):
    st.write("""
    - **_ (평지)**: ▶️ DASH 버튼을 눌러 빠르게 전진하세요.
    - **▲, ⚡, 🔴 (장애물)**: 장애물이 바로 앞에 올 때 반드시 **🚀 JUMP!** 버튼을 눌러 피해야 합니다.
    - **Demon 난이도**: 장애물 배치가 훨씬 빽빽하고 극악의 반응 속도를 요구합니다!
    """)
