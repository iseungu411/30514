import streamlit as st
import numpy as np
import random

st.set_page_config(page_title="Neon Block Blast", layout="centered", initial_sidebar_state="collapsed")

# --- 고급 테마 & UI 스타일링 (CSS) ---
st.markdown("""
    <style>
    /* 메인 배경 스타일 */
    .stApp {
        background: linear-gradient(135deg, #0d0e15 0%, #1a1c29 50%, #0d0e15 100%);
        color: #ffffff;
    }
    
    /* 타이틀 네온 효과 */
    .neon-title {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: center;
        font-size: 2.8rem;
        font-weight: 800;
        color: #fff;
        text-shadow: 0 0 10px #ff007f, 0 0 20px #ff007f, 0 0 40px #ff007f;
        margin-bottom: 5px;
    }
    
    .score-container {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin-bottom: 25px;
    }
    
    .score-box {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 10px 25px;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    .score-label {
        font-size: 0.85rem;
        color: #a0a5b5;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    .score-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #00f0ff;
        text-shadow: 0 0 10px rgba(0,240,255,0.5);
    }

    /* 그리드 버튼 스타일 재정의 */
    div.stButton > button {
        width: 100% !important;
        height: 52px !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        background-color: rgba(255, 255, 255, 0.03) !important;
        font-size: 1.6rem !important;
        transition: all 0.2s ease-in-out !important;
        padding: 0 !important;
    }
    
    div.stButton > button:hover {
        transform: scale(1.05);
        border-color: #00f0ff !important;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.4) !important;
    }

    /* 선택된 카드 스타일 */
    .block-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .block-card-selected {
        background: rgba(255, 0, 127, 0.1);
        border: 2px solid #ff007f;
        box-shadow: 0 0 20px rgba(255, 0, 127, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# --- 게임 상상 및 데이터 로직 ---
GRID_SIZE = 8
EMPTY_CELL = 0

# 블록 디자인 & 이모지 테마 매핑
GEM_TYPES = {
    1: "💎",  # 다이아몬드
    2: "🔮",  # 자수정
    3: "🟩",  # 에메랄드
    4: "🟥",  # 루비
    5: "🟨",  # 토파즈
    6: "🟦",  # 사파이어
}

BLOCK_SHAPES = {
    "Square 2x2": {"shape": np.ones((2, 2)), "color_id": 1, "icon": "💎 2x2"},
    "Line H 3x1": {"shape": np.ones((1, 3)), "color_id": 2, "icon": "🔮 Line 3"},
    "Line V 1x3": {"shape": np.ones((3, 1)), "color_id": 3, "icon": "🟩 Column 3"},
    "L-Shape 2x2": {"shape": np.array([[1, 0], [1, 1]]), "color_id": 4, "icon": "🟥 L-Block"},
    "T-Shape 3x2": {"shape": np.array([[1, 1, 1], [0, 1, 0]]), "color_id": 5, "icon": "🟨 T-Block"},
    "Single Gem": {"shape": np.ones((1, 1)), "color_id": 6, "icon": "🟦 Gem 1x1"},
}

def generate_new_blocks():
    names = list(BLOCK_SHAPES.keys())
    selected = random.choices(names, k=3)
    return [
        {
            "name": n,
            "shape": BLOCK_SHAPES[n]["shape"],
            "color_id": BLOCK_SHAPES[n]["color_id"],
            "icon": BLOCK_SHAPES[n]["icon"]
        } 
        for n in selected
    ]

def initialize_game():
    st.session_state.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    st.session_state.score = 0
    if "high_score" not in st.session_state:
        st.session_state.high_score = 0
    st.session_state.available_blocks = generate_new_blocks()
    st.session_state.selected_block_index = None
    st.session_state.game_over = False

if "grid" not in st.session_state:
    initialize_game()

def can_place_block(grid, shape, row, col):
    h, w = shape.shape
    if row < 0 or col < 0 or row + h > GRID_SIZE or col + w > GRID_SIZE:
        return False
    target = grid[row:row+h, col:col+w]
    return not np.any((target != EMPTY_CELL) & (shape == 1))

def place_block(row, col):
    if st.session_state.selected_block_index is None:
        st.toast("⚠️ 배치할 블록을 먼저 아래에서 선택하세요!", icon="⚠️")
        return
    
    idx = st.session_state.selected_block_index
    block_data = st.session_state.available_blocks[idx]
    shape = block_data["shape"]
    color_id = block_data["color_id"]
    
    if can_place_block(st.session_state.grid, shape, row, col):
        h, w = shape.shape
        for r in range(h):
            for c in range(w):
                if shape[r, c] == 1:
                    st.session_state.grid[row + r, col + c] = color_id
                    
        st.session_state.score += int(np.sum(shape)) * 10
        check_and_clear_lines()
        
        st.session_state.available_blocks[idx] = None
        st.session_state.selected_block_index = None
        
        if all(b is None for b in st.session_state.available_blocks):
            st.session_state.available_blocks = generate_new_blocks()

        if st.session_state.score > st.session_state.high_score:
            st.session_state.high_score = st.session_state.score

        check_game_over()
        st.rerun()

def check_and_clear_lines():
    grid = st.session_state.grid
    rows = [r for r in range(GRID_SIZE) if np.all(grid[r, :] != EMPTY_CELL)]
    cols = [c for c in range(GRID_SIZE) if np.all(grid[:, c] != EMPTY_CELL)]
    
    for r in rows: grid[r, :] = EMPTY_CELL
    for c in cols: grid[:, c] = EMPTY_CELL
    
    cleared = len(rows) + len(cols)
    if cleared > 0:
        bonus = cleared * 160
        st.session_state.score += bonus
        st.toast(f"💥 BLAST! {cleared}개 라인 제거 (+{bonus}점)", icon="🔥")

def check_game_over():
    grid = st.session_state.grid
    for block in st.session_state.available_blocks:
        if block is None: continue
        shape = block["shape"]
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if can_place_block(grid, shape, r, c): 
                    return
    st.session_state.game_over = True

# --- 화면 레이아웃 구성 ---
st.markdown("<h1 class='neon-title'>✨ BLOCK BLAST ✨</h1>", unsafe_allow_html=True)

# Score Board
st.markdown(f"""
    <div class='score-container'>
        <div class='score-box'>
            <div class='score-label'>Score</div>
            <div class='score-value'>{st.session_state.score:,}</div>
        </div>
        <div class='score-box'>
            <div class='score-label'>Best</div>
            <div class='score-value' style='color: #ff007f;'>{st.session_state.high_score:,}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

if st.session_state.game_over:
    st.error("🎮 GAME OVER! 더 이상 놓을 수 있는 공간이 없습니다.")
    if st.button("🔄 다시 도전하기", use_container_width=True):
        initialize_game()
        st.rerun()

# 메인 8x8 보드
for r in range(GRID_SIZE):
    cols = st.columns(GRID_SIZE)
    for c in range(GRID_SIZE):
        cell_val = st.session_state.grid[r, c]
        label = GEM_TYPES.get(cell_val, "⬛") # 빈 칸은 어두운 블록
        
        if cols[c].button(label, key=f"cell_{r}_{c}", disabled=st.session_state.game_over):
            place_block(r, c)

st.markdown("<br>", unsafe_allow_html=True)

# 하단 사용 가능 블록 카드 영역
st.markdown("##### 📦 사용할 블록 선택")
block_cols = st.columns(3)

for idx, block in enumerate(st.session_state.available_blocks):
    with block_cols[idx]:
        if block is not None:
            is_selected = (st.session_state.selected_block_index == idx)
            card_class = "block-card-selected" if is_selected else "block-card"
            
            # 카드 및 미리보기
            shape_matrix = block["shape"]
            color_emoji = GEM_TYPES[block["color_id"]]
            
            preview_str = ""
            for row in shape_matrix:
                preview_str += "".join([color_emoji if cell == 1 else "⬛" for cell in row]) + "\n"
            
            if st.button(f"{'✅ ' if is_selected else ''}{block['icon']}", key=f"select_{idx}", disabled=st.session_state.game_over, use_container_width=True):
                st.session_state.selected_block_index = idx
                st.rerun()
                
            st.code(preview_str, language=None)
        else:
            st.markdown("<div style='text-align:center; padding:30px; color:#555;'>USED</div>", unsafe_allow_html=True)
