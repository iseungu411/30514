import streamlit as st
import streamlit.components.v1 as components
import time

st.set_page_config(page_title="TJ PERFECT SCORE ULTIMATE MAX", page_icon="🎤", layout="wide")

# 세션 상태 초기화
if "coins" not in st.session_state:
    st.session_state.coins = 5
if "queue" not in st.session_state:
    st.session_state.queue = []
if "current_song" not in st.session_state:
    st.session_state.current_song = None

# 최고 퀄리티 악보 및 가사 데이터베이스
SONG_DATABASE = {
    "🐻 [동요] 곰 세 마리 (TJ 1001)": {
        "tj_num": "1001",
        "notes": [261, 261, 261, 261, 261, 329, 392, 392, 329, 261, 392, 392, 329, 261, 261, 261],
        "lyrics": ["곰 세 마 리 가", "한 집에 있어", "아 빠 곰", "엄 마 곰", "애 기 곰"],
        "chords": [261, 261, 329, 329, 392, 392, 261, 261],
        "bpm": 120
    },
    "✈️ [동요] 비행기 (TJ 1002)": {
        "tj_num": "1002",
        "notes": [329, 293, 261, 293, 329, 329, 329, 293, 293, 293, 329, 392, 392, 329, 293, 261],
        "lyrics": ["떴 다 떴 다", "비 행 기", "날 아 라", "날 아 라", "높 이 높 이 날 아 라"],
        "chords": [329, 293, 261, 293, 329, 329, 392, 392],
        "bpm": 125
    },
    "⭐ [동요] 작은 별 (TJ 1003)": {
        "tj_num": "1003",
        "notes": [261, 261, 392, 392, 440, 440, 392, 349, 349, 329, 329, 293, 293, 261],
        "lyrics": ["반 짝 반 짝", "작 은 별", "아 름 답 게", "비 치 네", "동 쪽 하 늘 에 서 도"],
        "chords": [261, 392, 440, 392, 349, 329, 293, 261],
        "bpm": 105
    },
    "🔔 [동요] 학교 종 (TJ 1004)": {
        "tj_num": "1004",
        "notes": [392, 392, 440, 440, 392, 392, 329, 392, 392, 329, 329, 293, 392, 392, 440],
        "lyrics": ["학 교 종 이", "땡 땡 땡", "어 어 서 모 이 자", "선 생 님 이", "기 다 리 신 다"],
        "chords": [392, 440, 392, 329, 392, 329, 293, 392],
        "bpm": 115
    }
}

st.markdown("""
<style>
    .stApp { background-color: #02010a; color: #ffffff; }
    .coin-badge {
        background: linear-gradient(135deg, #10b981, #047857);
        padding: 16px; border-radius: 14px; text-align: center;
        font-weight: 800; font-size: 22px; color: #fff;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.5);
    }
</style>
""", unsafe_allow_html
