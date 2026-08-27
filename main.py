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
def initialize_game():
st.session_state.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
st.session_state.score = 0
st.session_state.available_blocks = generate_new_blocks()
st.session_state.selected_block_index = None
st.session_state.game_over = False
def generate_new_blocks():
names = list(BLOCK_SHAPES.keys())
return [{"name": n, "shape": BLOCK_SHAPES[n]} for n in random.choices(names, k=3)]
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
st.toast(f" {cleared}줄 제거! +{cleared * GRID_SIZE * 2}점")
def check_game_over():
grid = st.session_state.grid
for block in st.session_state.available_blocks:
if block is None: continue
shape = block["shape"]
for r in range(GRID_SIZE):
for c in range(GRID_SIZE):
if can_place_block(grid, shape, r, c): return
st.session_state.game_over = True
