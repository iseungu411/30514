import streamlit as st
import numpy as np
import random

# --- 스트림릿 페이지 설정 ---
st.set_page_config(page_title="Streamlit Block Blast", layout="centered")

# --- 게임 상수의 및 설정 ---
GRID_SIZE = 8
EMPTY_CELL = 0
FILLED_CELL = 1

# 블록 모양 정의 (numpy 배열 사용)
BLOCK_SHAPES = {
    "Square 2x2": np.ones((2, 2)),
    "Line H 3x1": np.ones((1, 3)),
    "Line V 1x3": np.ones((3, 1)),
    "L-Shape 2x2": np.array([[1, 0], [1, 1]]),
    "T-Shape 3x2": np.array([[1, 1, 1], [0, 1, 0]]),
    "Single": np.ones((1, 1)),
}

BLOCK_COLORS = {
    "Square 2x2": "#FF4B4B", # Red
    "Line H 3x1": "#1C83E1", # Blue
    "Line V 1x3": "#00C04A", # Green
    "L-Shape 2x2": "#FFD700", # Gold
    "T-Shape 3x2": "#A35CFF", # Purple
    "Single": "#F067C6",     # Pink
}

# --- 게임 로직 함수 ---

def initialize_game():
    """게임 상태 초기화"""
    st.session_state.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    st.session_state.score = 0
    st.session_state.available_blocks = generate_new_blocks()
    st.session_state.selected_block_index = None # 현재 선택한 블록 번호 (0, 1, 2)
    st.session_state.game_over = False

def generate_new_blocks():
    """새로운 3개의 랜덤 블록 생성"""
    names = list(BLOCK_SHAPES.keys())
    selected_names = random.choices(names, k=3)
    return [{"name": name, "shape": BLOCK_SHAPES[name]} for name in selected_names]

def can_place_block(grid, shape, row, col):
    """지정한 위치에 블록을 놓을 수 있는지 확인"""
    h, w = shape.shape
    if row < 0 or col < 0 or row + h > GRID_SIZE or col + w > GRID_SIZE:
        return False # 그리드 범위를 벗어남
    
    # 겹치는 부분이 있는지 확인
    target_area = grid[row:row+h, col:col+w]
    if np.any((target_area == FILLED_CELL) & (shape == 1)):
        return False # 이미 차 있음
    return True

def place_block(row, col):
    """선택한 블록을 그리드에 배치하고 줄 삭제 처리"""
    if st.session_state.selected_block_index is None:
        st.warning("먼저 블록을 선택하세요.")
        return

    block_data = st.session_state.available_blocks[st.session_state.selected_block_index]
    shape = block_data["shape"]
    
    if can_place_block(st.session_state.grid, shape, row, col):
        # 1. 블록 배치
        h, w = shape.shape
        for r in range(h):
            for c in range(w):
                if shape[r, c] == 1:
                    st.session_state.grid[row + r, col + c] = FILLED_CELL
        
        # 2. 점수 계산 (배치 점수)
        block_points = int(np.sum(shape))
        st.session_state.score += block_points
        
        # 3. 줄 삭제 확인 및 삭제
        check_and_clear_lines()
        
        # 4. 사용한 블록 제거 및 상태 업데이트
        st.session_state.available_blocks[st.session_state.selected_block_index] = None
        st.session_state.selected_block_index = None # 선택 초기화
        
        # 5. 블록 다 썼는지 확인 후 새 블록 생성
        if all(b is None for b in st.session_state.available_blocks):
            st.session_state.available_blocks = generate_new_blocks()
            
        # 6. 게임 오버 확인
        check_game_over()
        st.rerun() # 화면 업데이트
    else:
        st.error("그 위치에는 블록을 놓을 수 없습니다.")

def check_and_clear_lines():
    """가득 찬 행과 열을 찾아 삭제하고 점수 추가"""
    grid = st.session_state.grid
    lines_to_clear_row = []
    lines_to_clear_col = []
    
    # 가득 찬 행 찾기
    for r in range(GRID_SIZE):
        if np.all(grid[r, :] == FILLED_CELL):
            lines_to_clear_row.append(r)
            
    # 가득 찬 열 찾기
    for c in range(GRID_SIZE):
        if np.all(grid[:, c] == FILLED_CELL):
            lines_to_clear_col.append(c)
            
    # 행 삭제
    for r in lines_to_clear_row:
        grid[r, :] = EMPTY_CELL
        
    # 열 삭제
    for c in lines_to_clear_col:
        grid[:, c] = EMPTY_CELL
        
    # 점수 추가 (줄당 GRID_SIZE*2 점)
    cleared_lines = len(lines_to_clear_row) + len(lines_to_clear_col)
    if cleared_lines > 0:
        st.session_state.score += cleared_lines * GRID_SIZE * 2
        st.toast(f"🎉 {cleared_lines}줄 제거! +{cleared_lines * GRID_SIZE * 2}점")

def check_game_over():
    """현재 그리드에 남은 블록 중 하나라도 놓을 수 있는지 확인"""
    grid = st.session_state.grid
    available_blocks = st.session_state.available_blocks
    
    for block in available_blocks:
        if block is None: continue # 이미 사용한 칸은 스킵
        
        shape = block["shape"]
        can_place_anywhere = False
        
        # 그리드 전역을 탐색하며 놓을 수 있는지 확인
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if can_place_block(grid, shape, r, c):
                    can_place_anywhere = True
                    break
            if can_place_anywhere: break
            
        if can_place_anywhere:
            return # 하나라도 놓을 수 있으면 게임 계속 진행
            
    # 모든 남은 블록을 놓을 수 없으면 게임 오버
    st.session_state.game_over = True

# --- UI 렌더링 함수 ---

def render_grid():
    """현재 게임 그리드를 이모지로 렌더링"""
    grid = st.session_state.grid
    
    st.write("### 🎮 게임 보드")
    
    # CSS를 사용하여 버튼 모양의 셀 만들기
    st.markdown("""
        <style>
        .stButton>button {
            width: 40px;
            height: 40px;
            padding: 0px;
            border: 1px solid #444;
            border-radius: 4px;
        }
        .filled-cell { background-color: #333 !important; color: white; }
        .empty-cell { background-color: #eee !important; }
        </style>
    """, unsafe_allow_stdio=True)
    
    cols = st.columns(GRID_SIZE)
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            with cols[c]:
                # 각 셀을 하나의 버튼으로 만듦 (클릭 시 배치)
                cell_value = grid[r, c]
                
                # 버튼 텍스트 (빈칸 또는 블록)
                cell_text = "⬛" if cell_value == FILLED_CELL else "⬜"
                
                # 게임 오버가 아닐 때만 클릭 가능
                if not st.session_state.game_over:
                    # key는 고유해야 함 (row_col 형식을 사용)
                    if st.button(cell_text, key=f"cell_{r}_{c}"):
                        place_block(r, c)
                else:
                    # 게임 오버 시 클릭 불가
                    st.button(cell_text, key=f"cell_{r}_{c}_disabled", disabled=True)

def render_available_blocks():
    """사용 가능한 블록 3개를 하단에 표시하고 선택 버튼 제공"""
    st.write("---")
    st.write("### ➕ 놓을 블록 선택")
    
    blocks = st.session_state.available_blocks
    
    # 3개의 컬럼으로 나눔
    cols = st.columns(3)
    
    for i in range(3):
        with cols[i]:
            block = blocks[i]
            if block:
                # 블록 이름을 버튼 이름으로 사용
                name = block["name"]
                shape = block["shape"]
                
                st.write(f"**{name}** ({int(np.sum(shape))}칸)")
                
                # 블록 모양을 텍스트로 미리보기
                preview_text = ""
                h, w = shape.shape
                for r in range(h):
                    for c in range(w):
                        preview_text += "⬛" if shape[r, c] == 1 else "⬜"
                    preview_text += "\n"
                st.text(preview_text)
                
                # 선택 버튼 (현재 선택된 블록은 disabled)
                is_selected = (st.session_state.selected_block_index == i)
                if st.button(f"{i+1}번 블록 선택", key=f"select_block_{i}", disabled=is_selected):
                    st.session_state.selected_block_index = i
                    st.rerun()
            else:
                st.write("*사용함*")
                st.button("빈칸", key=f"select_block_{i}_empty", disabled=True)

# --- 메인 실행 ---

# 1. 상태 초기화
if 'grid' not in st.session_state:
    initialize_game()

# 2. 헤더 및 점수 표시
st.title("Streamlit Block Blast")
st.sidebar.write(f"## 🏆 Score: {st.session_state.score}")

if st.sidebar.button("게임 초기화/새 게임"):
    initialize_game()
    st.rerun()

# 3. 게임 오버 메시지
if st.session_state.game_over:
    st.error(f"❌ GAME OVER! 최종 점수: {st.session_state.score}")
    st.balloons()
elif st.session_state.selected_block_index is not None:
    block_name = st.session_state.available_blocks[st.session_state.selected_block_index]["name"]
    st.info(f"👉 {st.session_state.selected_block_index+1}번 블록 '{block_name}'이(가) 선택되었습니다. 보드를 클릭하여 배치하세요.")
else:
    st.info("👇 아래에서 블록을 먼저 선택하세요.")

# 4. 화면 렌더링
render_grid()
render_available_blocks()
