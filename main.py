import streamlit as st
import numpy as np
import random

# 페이지 설정
st.set_page_config(page_title="Neon Block Blast", layout="centered")

# --- CSS 스타일 정의 ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .neon-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 800;
        color: #00f0ff;
        text-shadow: 0 0 10px #00f0ff, 0 0 20px #00f0ff;
        margin-bottom: 20px;
    }
    div.stButton > button {
        width: 100% !important;
        height: 50px !important;
        border-radius: 8px !important;
        background-color: #1a1c23 !important;
        border: 1px solid #333 !important;
        font-size: 1.4rem !important;
    }
    div.stButton > button:hover {
        border-color: #00f0ff !important;
        color: #00f0ff !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 게임 상상 및 데이터 ---
GRID_SIZE = 8
EMPTY_CELL = 0

GEM_TYPES = {
    1: "💎", 2: "🔮", 3: "🟩", 
    4: "🟥", 5: "🟨", 6: "🟦"
}

BLOCK_SHAPES = {
    "Square 2x2": {"shape": np.ones((2, 2)), "color_id": 1, "name": "💎 2x2"},
    "Line H 3x1": {"shape": np.ones((1, 3)), "color_id": 2, "name": "🔮 Line 3"},
    "Line V 1x3": {"shape": np.ones((3, 1)), "color_id": 3, "name": "🟩 Column 3"},
    "L-Shape 2x2": {"shape": np.array([[1, 0], [1, 1]]), "color_id": 4, "name": "🟥 L-Block"},
    "T-Shape 3x2": {"shape": np.array([[1, 1, 1], [0, 1, 0]]), "color_id": 5, "name": "🟨 T-Block"},
    "Single Gem": {"shape": np.ones((1, 1)), "color_id": 6, "name": "🟦 Gem 1x1"},
}

def generate_new_blocks():
    names = list(BLOCK_SHAPES.keys())
    selected = random.choices(names, k=3)
    return [
        {
            "shape": BLOCK_SHAPES[n]["shape"],
            "color_id": BLOCK_SHAPES[n]["color_id"],
            "name": BLOCK_SHAPES[n]["name"]
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

# 안전한 rerun 함수 (버전 호환성 문제 해결)
def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

# 상태 초기화
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
        st.toast("⚠️ 배치할 블록을 먼저 아래에서 선택하세요!")
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
        safe_rerun()

def check_and_clear_lines():
    grid = st.session_state.grid
    rows = [r for r in range(GRID_SIZE) if np.all(grid[r, :] != EMPTY_CELL)]
    cols = [c for c in range(GRID_SIZE) if np.all(grid[:, c] != EMPTY_CELL)]
    
    for r in rows: grid[r, :] = EMPTY_CELL
    for c in cols: grid[:, c] = EMPTY_CELL
    
    cleared = len(rows) + len(cols)
    if cleared > 0:
        bonus = cleared * 150
        st.session_state.score += bonus
        st.toast(f"💥 BLAST! {cleared}줄 제거 (+{bonus}점)")

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

# --- UI 레이아웃 ---
st.markdown("<h1 class='neon-title'>✨ BLOCK BLAST ✨</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
col1.metric("Score", f"{st.session_state.score:,}")
col2.metric("Best", f"{st.session_state.high_score:,}")

if st.session_state.game_over:
    st.error("🎮 GAME OVER! 더 이상 블록을 놓을 수 없습니다.")
    if st.button("🔄 다시 시작하기"):
        initialize_game()
        safe_rerun()

# 8x8 보드
for r in range(GRID_SIZE):
    cols = st.columns(GRID_SIZE)
    for c in range(GRID_SIZE):
        cell_val = st.session_state.grid[r, c]
        label = GEM_TYPES.get(cell_val, "⬛")
        
        if cols[c].button(label, key=f"cell_{r}_{c}", disabled=st.session_state.game_over):
            place_block(r, c)

st.write("")
st.subheader("📦 사용 가능한 블록")
block_cols = st.columns(3)

for idx, block in enumerate(st.session_state.available_blocks):
    with block_cols[idx]:
        if block is not None:
            is_selected = (st.session_state.selected_block_index == idx)
            btn_label = f"✅ {block['name']}" if is_selected else block['name']
            
            if st.button(btn_label, key=f"select_{idx}", disabled=st.session_state.game_over):
                st.session_state.selected_block_index = idx
                safe_rerun()
                
            shape_matrix = block["shape"]
            color_emoji = GEM_TYPES[block["color_id"]]
            
            preview_str = ""
            for row in shape_matrix:
                preview_str += "".join([color_emoji if cell == 1 else "⬛" for cell in row]) + "\n"
            
            st.code(preview_str, language=None)
        else:
            st.caption("사용됨")
