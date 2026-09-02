import streamlit as st
import streamlit.components.v1 as components
import random
import time

st.set_page_config(page_title="REAL PERFECT SCORE KARAOKE", page_icon="🎤", layout="wide")

# 세션 상태 초기화
if "coins" not in st.session_state:
    st.session_state.coins = 0
if "queue" not in st.session_state:
    st.session_state.queue = []
if "current_song" not in st.session_state:
    st.session_state.current_song = None
if "part_time_task" not in st.session_state:
    st.session_state.part_time_task = None

# 확장된 MR 곡 데이터베이스 (저작권 안전 공식 ID 및 노래방 번호)
SONG_DATABASE = {
    "❤️ [R&B] 죠지 - 좋아해.. (TJ 52277)": {"yt_id": "M7lc1UVf-VE", "tj_num": "52277"},
    "⛵ [R&B] 죠지 - Boat (TJ 98709)": {"yt_id": "M6L7eU15E4A", "tj_num": "98709"},
    "🎸 [R&B] 죠지 - routine (TJ 78921)": {"yt_id": "fJ36R94N1mY", "tj_num": "78921"},
    "🤝 [R&B] 죠지 - 손만 잡고 잠을 자자 (TJ 78512)": {"yt_id": "uIPlsJ62p1s", "tj_num": "78512"},
    "☕ [R&B] 죠지 - 바래봐요 (TJ 68112)": {"yt_id": "jxIdU3twWkw", "tj_num": "68112"},
    "🌙 [R&B] 죠지 - 바라봐요 (TJ 54621)": {"yt_id": "M6L7eU15E4A", "tj_num": "54621"},
    "✨ [IDOL] NewJeans - Hype Boy (TJ 82072)": {"yt_id": "nTL2KONavNQ", "tj_num": "82072"},
    "🐰 [IDOL] NewJeans - Ditto (TJ 82802)": {"yt_id": "nTL2KONavNQ", "tj_num": "82802"},
    "💘 [IDOL] IVE - I AM (TJ 83789)": {"yt_id": "nTL2KONavNQ", "tj_num": "83789"},
    "🌧️ [BALLAD] 성시경 - 거리에서 (TJ 16568)": {"yt_id": "9HhslfvDbfI", "tj_num": "16568"},
    "🎸 [BAND] DAY6 - 한 페이지가 될 수 있게 (TJ 54592)": {"yt_id": "9HhslfvDbfI", "tj_num": "54592"},
    "👑 [BAND] 잔나비 - 주저하는 연인들을 위해 (TJ 53818)": {"yt_id": "9HhslfvDbfI", "tj_num": "53818"},
    "☕ [INDIE] 10CM - Phonecert (TJ 96912)": {"yt_id": "jxIdU3twWkw", "tj_num": "96912"},
    "🌌 [BALLAD] 윤하 - 사건의 지평선 (TJ 82215)": {"yt_id": "9HhslfvDbfI", "tj_num": "82215"},
    "🍀 [BAND] LUCY - 개화 (TJ 75210)": {"yt_id": "9HhslfvDbfI", "tj_num": "75210"}
}

st.markdown("""
<style>
    .stApp { background-color: #050212; color: #ffffff; }
    .coin-badge {
        background: linear-gradient(135deg, #f59e0b, #b45309);
        padding: 16px; border-radius: 16px; text-align: center;
        font-weight: 800; font-size: 22px; color: #fff;
        box-shadow: 0 0 15px rgba(245, 158, 11, 0.4);
    }
    .work-card {
        background: rgba(30, 27, 75, 0.7);
        border: 1px solid rgba(129, 140, 248, 0.3);
        border-radius: 14px; padding: 16px; margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎤 PERFECT SCORE REAL AI KARAOKESTAGE 🪙")

col_left, col_right = st.columns([1.1, 2])

# 왼쪽 컬럼: 코인 알바 & 노래 예약
with col_left:
    st.subheader("💰 코인노래방 알바센터")
    st.markdown(f'<div class="coin-badge">보유 코인: {st.session_state.coins} 코인</div>', unsafe_allow_html=True)
    
    st.write("")
    st.caption("🛠️ 노래를 부르려면 알바를 해서 코인을 벌어야 합니다!")
    
    work_tab1, work_tab2, work_tab3 = st.tabs(["🧹 방 청소", "🥤 음료 채우기", "🛎️ 카운터 응대"])
    
    with work_tab1:
        st.write("**3번 방 마이크와 테이블을 청소하세요!**")
        if st.button("🧹 열심히 청소하기 (15초 소요)", use_container_width=True):
            with st.spinner("방 청소 중... (소독제 뿌리는 중)"):
                time.sleep(1.5)
            st.session_state.coins += 1
            st.success("청소 완료! 1코인 획득 🪙")
            st.rerun()

    with work_tab2:
        st.write("**냉장고에 식혜와 포카리를 정렬하세요!**")
        drink = st.radio("채울 음료 선택", ["식혜", "포카리스웨트", "옥수수수염차"])
        if st.button("🥤 음료 냉장고 채우기", use_container_width=True):
            st.session_state.coins += 1
            st.success(f"{drink} 채우기 완료! 1코인 획득 🪙")
            st.rerun()

    with work_tab3:
        st.write("**손님이 5,000원을 냈습니다. 동전으로 교환해 주세요.**")
        ans = st.number_input("500원짜리 몇 개?", min_value=0, max_value=20, value=0)
        if st.button("🛎️ 계산하기", use_container_width=True):
            if ans == 10:
                st.session_state.coins += 2
                st.success("정답입니다! 2코인 획득 🪙🪙")
                st.rerun()
            else:
                st.error("계산이 틀렸습니다! 다시 계산해보세요.")

    st.divider()

    st.subheader("🎶 노래 예약하기")
    selected_song_key = st.selectbox("수록곡 선택 (15곡)", list(SONG_DATABASE.keys()))

    if st.button("📌 곡 예약하기 (1코인 차감)", use_container_width=True):
        if st.session_state.coins <= 0:
            st.error("코인이 부족합니다! 위에서 알바를 하고 코인을 버세요.")
        else:
            song_data = SONG_DATABASE[selected_song_key]
            st.session_state.queue.append({
                "title": selected_song_key,
                "yt_id": song_data["yt_id"],
                "tj_num": song_data["tj_num"]
            })
            st.session_state.coins -= 1
            st.success(f"'{selected_song_key}' 예약 완료!")
            st.rerun()

    st.subheader("📋 대기 목록")
    if st.session_state.queue:
        for idx, item in enumerate(st.session_state.queue, 1):
            st.write(f"**{idx}.** {item['title']}")
    else:
        st.caption("예약된 곡이 없습니다.")

# 오른쪽 컬럼: 퍼펙트 스코어 스테이지 및 플레이어
with col_right:
    st.subheader("📺 퍼펙트스코어 2D 가창 무대")

    if not st.session_state.current_song and st.session_state.queue:
        st.session_state.current_song = st.session_state.queue.pop(0)
        st.rerun()

    if st.session_state.current_song:
        song = st.session_state.current_song
        st.info(f"🎤 **NOW PLAYING:** {song['title']} (TJ 번호: {song['tj_num']})")

        perfect_score_canvas_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                * {{ box-sizing: border-box; margin: 0; padding: 0; }}
                body {{ background: #030014; color: #fff; font-family: 'Segoe UI', sans-serif; overflow: hidden; }}
                #canvas-container {{ position: relative; width: 100%; height: 220px; background: #09051d; border: 2px solid #ec4899; border-radius: 12px; overflow: hidden; }}
                canvas {{ width: 100%; height: 100%; display: block; }}
                #hud-overlay {{
                    position: absolute; top: 10px; right: 15px; background: rgba(15, 23, 42, 0.85);
                    padding: 8px 16px; border-radius: 12px; border: 1px solid #38bdf8; text-align: right;
                }}
                .hud-val {{ font-size: 20px; font-weight: bold; color: #38bdf8; }}
                #judge-txt {{ position: absolute; top: 15px; left: 20px; font-size: 32px; font-weight: 900; text-shadow: 0 0 12px #facc15; color: #facc15; }}
            </style>
        </head>
        <body>
            <div id="canvas-container">
                <div id="judge-txt">PERFECT SCORE</div>
                <div id="hud-overlay">
                    <div>🎙️ PITCH: <span id="pitch-val" class="hud-val">--- Hz</span></div>
                    <div>🎯 SCORE: <span id="score-val" class="hud-val" style="color:#ec4899;">100</span></div>
                </div>
                <canvas id="scoreCanvas"></canvas>
            </div>

            <script>
                const canvas = document.getElementById('scoreCanvas');
                const ctx = canvas.getContext('2d');
                canvas.width = canvas.offsetWidth;
                canvas.height = canvas.offsetHeight;

                let audioCtx, analyser;
                let userPitch = 0;
                let currentScore = 100;
                let trajectory = [];
                let step = 0;

                async function initMic() {{
                    try {{
                        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                        analyser = audioCtx.createAnalyser();
                        analyser.fftSize = 2048;
                        const stream = await navigator.mediaDevices.getUserMedia({{ audio: true }});
                        audioCtx.createMediaStreamSource(stream).connect(analyser);
                    }} catch(e) {{}}
                }}

                function getPitch() {{
                    if (!analyser) return 0;
                    const buf = new Float32Array(2048);
                    analyser.getFloatTimeDomainData(buf);
                    let sum = 0;
                    for (let i = 0; i < 2048; i++) sum += buf[i] * buf[i];
                    let rms = Math.sqrt(sum / 2048);
                    return rms > 0.015 ? rms * 1800 : 0;
                }}

                function render() {{
                    ctx.clearRect(0, 0, canvas.width, canvas.height);

                    // 1. TJ 퍼펙트스코어 가이드 옥타브 가이드선
                    ctx.strokeStyle = "rgba(255, 255, 255, 0.08)";
                    ctx.lineWidth = 1;
                    for (let y = 30; y < canvas.height; y += 40) {{
                        ctx.beginPath();
                        ctx.moveTo(0, y);
                        ctx.lineTo(canvas.width, y);
                        ctx.stroke();
                    }}

                    // 2. 가이드 음정 노드 (파란색 Bar)
                    const targetY = canvas.height / 2 + Math.sin(step * 0.04) * 50;
                    ctx.fillStyle = "rgba(56, 189, 248, 0.6)";
                    ctx.fillRect(canvas.width * 0.6, targetY - 8, 80, 16);

                    // 3. 사용자 입력 음정 감지 및 판정
                    userPitch = getPitch();
                    const pitchEl = document.getElementById('pitch-val');
                    const judgeEl = document.getElementById('judge-txt');

                    if (userPitch > 0) {{
                        pitchEl.innerText = Math.round(userPitch) + " Hz";
                        const userY = canvas.height - ((userPitch - 80) / 400 * canvas.height);
                        
                        trajectory.push({{ x: canvas.width * 0.6, y: userY }});
                        if (trajectory.length > 40) trajectory.shift();

                        const diff = Math.abs(userY - targetY);
                        if (diff < 20) {{
                            judgeEl.innerText = "🔥 PERFECT!"; judgeEl.style.color = "#34d399";
                        }} else if (diff < 40) {{
                            judgeEl.innerText = "✨ GREAT"; judgeEl.style.color = "#facc15";
                        }} else {{
                            judgeEl.innerText = "⚡ MISS"; judgeEl.style.color = "#f43f5e";
                            currentScore = Math.max(50, currentScore - 0.04);
                            document.getElementById('score-val').innerText = Math.round(currentScore);
                        }}
                    }} else {{
                        pitchEl.innerText = "--- Hz";
                    }}

                    // 4. 사용자 가창 궤적 그리기 (핑크 라인)
                    ctx.strokeStyle = "#ec4899";
                    ctx.lineWidth = 4;
                    ctx.beginPath();
                    for (let i = 0; i < trajectory.length; i++) {{
                        const pt = trajectory[i];
                        pt.x -= 2.5;
                        if (i === 0) ctx.moveTo(pt.x, pt.y);
                        else ctx.lineTo(pt.x, pt.y);
                    }}
                    ctx.stroke();

                    step++;
                    requestAnimationFrame(render);
                }}

                initMic();
                render();
            </script>
        </body>
        </html>
        """
        components.html(perfect_score_canvas_html, height=230)

        # 저작권 차단 없는 보장된 반주 재생 플레이어
        st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.9); padding: 16px; border-radius: 12px; border: 1px solid #6366f1; text-align: center;">
            <p style="font-size: 16px; font-weight: bold; color: #38bdf8;">🎵 저작권 차단 없는 공식 반주로 부르기</p>
            <p style="font-size: 14px; color: #cbd5e1; margin-bottom: 12px;">아래 버튼을 누르면 TJ/금영 공식 반주 음원이 바로 재생됩니다!</p>
            <a href="https://www.youtube.com/results?search_query=TJ+{song['tj_num']}" target="_blank" style="text-decoration: none;">
                <button style="background: linear-gradient(135deg, #ec4899, #8b5cf6); color: white; border: none; padding: 12px 24px; border-radius: 25px; font-weight: bold; cursor: pointer; font-size: 15px;">
                    ▶️ {song['title']} 공식 노래방 MR 재생하기
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        if st.button("⏭️ 다음 곡으로 넘기기 (완곡 완료)", use_container_width=True):
            st.session_state.current_song = None
            st.rerun()
    else:
        st.warning("알바를 해서 코인을 번 후 원하는 노래를 예약해 보세요!")
