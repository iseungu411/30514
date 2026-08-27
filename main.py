import streamlit as st
import numpy as np
import random

st.set_page_config(page_title="Streamlit Block Blast", layout="centered")

GRID_SIZE = 8
EMPTY_CELL, FILLED_CELL = 0, 1

BLOCK_SHAPES = {
    "Square 2x2": np.ones((2, 2)),
    "Line H 3x1": np.ones((1, 3)),
    "Line V 1x3": np.ones((3, 1)),
    "L-Shape 2x2": np.array([[1, 0], [1, 1]]),
    "T-Shape 3x2": np.array([[1, 1, 1], [0, 1, 0]]),
    "Single": np.ones((1, 1)),
}

def generate_new_blocks():
    names = list(BLOCK_SHAPES.keys())
    return [{"name": n, "shape": BLOCK_SHAPES[n]} for n in random.choices(names, k=3)]

def initialize_game():
    st.session_state.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    st.session_state.score = 0
    st.session_state.available_blocks = generate_new_blocks()
    st.session_state.selected_block_index = None
    st.session_state.game_over = False

# Session State 초기화 체크
if "grid" not in st.session_state:
    initialize_game()

def can_place_block(grid, shape, row, col):
    h, w = shape.shape
    if row < 0 or col < 0 or row + h > GRID_SIZE or col + w > GRID_SIZE:
        return False
    target = grid[row:row+h, col:col+w]
    return not np.any((target == FILLED_CELL) & (shape == 1))

def place_block(row, col):
    if st.session_state.selected_block_index is None:
        st.warning("먼저 블록을 선택하세요.")
        return
    idx = st.session_state.selected_block_index
    shape = st.session_state.available_blocks[idx]["shape"]
    
    if can_place_block(st.session_state.grid, shape, row, col):
        h, w = shape.shape
        for r in range(h):
            for c in range(w):
                if shape[r, c] == 1:
                    st.session_state.grid[row + r, col + c] = FILLED_CELL
        st.session_state.score += int(np.sum(shape))
        check_and_clear_lines()
        st.session_state.available_blocks[idx] = None
        st.session_state.selected_block_index = None
        
        if all(b is None for b in st.session_state.available_blocks):
            st.session_state.available_blocks = generate_new_blocks()

        check_game_over()
        st.rerun()

def check_and_clear_lines():
    grid = st.session_state.grid
    rows = [r for r in range(GRID_SIZE) if np.all(grid[r, :] == FILLED_CELL)]
    cols = [c for c in range(GRID_SIZE) if np.all(grid[:, c] == FILLED_CELL)]
    
    for r in rows: grid[r, :] = EMPTY_CELL
    for c in cols: grid[:, c] = EMPTY_CELL
    
    cleared = len(rows) + len(cols)
    if cleared > 0:
        st.session_state.score += cleared * GRID_SIZE * 2
        st.toast(f"🎉 {cleared}줄 제거! +{cleared * GRID_SIZE * 2}점")

def check_game_over():
    grid = st.session_state.grid
    for block in st.session_state.available_blocks:
        if block is None: continue
        shape = block["shape"]
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if can_place_block(grid, shape, r, c): return
    st.session_state.game_over = True

# --- UI 레이아웃 구현 ---
st.title("🧩 Streamlit Block Blast")

st.metric("Score", st.session_state.score)

if st.session_state.game_over:
    st.error("Game Over! 더 이상 블록을 놓을 수 없습니다.")
    if st.button("새 게임 시작"):
        initialize_game()
        st.rerun()

# 8x8 메인 그리드 출력
st.subheader("보드")
for r in range(GRID_SIZE):
    cols = st.columns(GRID_SIZE)
    for c in range(GRID_SIZE):
        is_filled = st.session_state.grid[r, c] == FILLED_CELL
        label = "⬛" if is_filled else "⬜"
        if cols[c].button(label, key=f"cell_{r}_{c}", disabled=st.session_state.game_over):
            place_block(r, c)

st.markdown("---")

# 사용 가능한 블록 선택 UI
st.subheader("사용 가능한 블록 선택")
block_cols = st.columns(3)

for idx, block in enumerate(st.session_state.available_blocks):
    if block is not None:
        with block_cols[idx]:
            is_selected = st.session_state.selected_block_index == idx
            button_label = f"{"👉 " if is_selected else ""}{block['name']}"
            
            if st.button(button_label, key=f"block_select_{idx}", disabled=st.session_state.game_over):
                st.session_state.selected_block_index = idx
                st.rerun()
            
            # 선택한 블록 형태 미리보기
            shape_preview = ""
            for row in block["shape"]:
                shape_preview += "".join(["🟦" if cell == 1 else "⬜" for cell in row]) + "\n"
            st.code(shape_preview, language=None)
    else:
        block_cols[idx].write("사용됨")
