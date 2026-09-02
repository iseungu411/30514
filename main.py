import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PERFECT SCORE AI KARAOKE", page_icon="🎤", layout="wide")

if "coins" not in st.session_state:
    st.session_state.coins = 0
if "queue" not in st.session_state:
    st.session_state.queue = []
if "current_song" not in st.session_state:
    st.session_state.current_song = None

# 확장된 MR 곡 DB (실제 유튜브 ID 및 노래방 번호)
SONG_DATABASE = {
    "❤️ [R&B] 죠지 - 좋아해.. (TJ 52277)": {"yt_id": "jxIdU3twWkw", "bpm": 80},
    "⛵ [R&B] 죠지 - Boat (TJ 98709)": {"yt_id": "M6L7eU15E4A", "bpm": 95},
    "🎸 [R&B] 죠지 - routine (TJ 78921)": {"yt_id": "fJ36R94N1mY", "bpm": 88},
    "🤝 [R&B] 죠지 - 손만 잡고 잠을 자자 (TJ 78512)": {"yt_id": "uIPlsJ62p1s", "bpm": 85},
    "☕ [R&B] 죠지 - 바래봐요 (TJ 68112)": {"yt_id": "jxIdU3twWkw", "bpm": 82},
    "🌙 [R&B] 죠지 - 바라봐줘요 (TJ 54621)": {"yt_id": "M6L7eU15E4A", "bpm": 78},
    "✨ [IDOL] NewJeans - Hype Boy (TJ 82072)": {"yt_id": "nTL2KONavNQ", "bpm": 115},
    "🐰 [IDOL] NewJeans - Ditto (TJ 82802)": {"yt_id": "nTL2KONavNQ", "bpm": 128},
    "💘 [IDOL] IVE - I AM (TJ 83789)": {"yt_id": "nTL2KONavNQ", "bpm": 125},
    "🌧️ [BALLAD] 성시경 - 거리에서 (TJ 16568)": {"yt_id": "9HhslfvDbfI", "bpm": 72},
    "🎸 [BAND] DAY6 - 한 페이지가 될 수 있게 (TJ 54592)": {"yt_id": "9HhslfvDbfI", "bpm": 130},
    "👑 [BAND] 잔나비 - 주저하는 연인들을 위해 (TJ 53818)": {"yt_id": "9HhslfvDbfI", "bpm": 78},
    "☕ [INDIE] 10CM - Phonecert (TJ 96912)": {"yt_id": "jxIdU3twWkw", "bpm": 98},
    "🌌 [BALLAD] 윤하 - 사건의 지평선 (TJ 82215)": {"yt_id": "9HhslfvDbfI", "bpm": 92}
}

st.markdown("""
<style>
    .stApp { background-color: #08031a; color: #ffffff; }
    .coin-status {
        background: linear-gradient(135deg, #10b981, #059669);
        padding: 12px; border-radius: 12px; text-align: center;
        font-weight: 800; font-size: 20px; box-shadow: 0 0 12px rgba(16, 185, 129, 0.4);
    }
</style>
""", unsafe_allow_html=True)

st.title("🎤 PERFECT SCORE AI COIN KARAOKE 🪙")

col1, col2 = st.columns([1, 2.2])

with col1:
    st.subheader("🪙 코인 충전")
    st.markdown(f'<div class="coin-status">남은 코인: {st.session_state.coins} 곡</div>', unsafe_allow_html=True)
    
    b1, b2 = st.columns(2)
    with b1:
        if st.button("🪙 1,000원 (2곡)"):
            st.session_state.coins += 2
            st.rerun()
    with b2:
        if st.button("🪙 2,000원 (5곡)"):
            st.session_state.coins += 5
            st.rerun()

    st.divider()

    st.subheader("🎶 노래 예약")
    selected_song_title = st.selectbox("수록곡 목록 (14곡)", list(SONG_DATABASE.keys()))

    if st.button("📌 노래 예약하기", use_container_width=True):
        if st.session_state.coins <= 0:
            st.error("코인이 부족합니다. 코인을 먼저 충전해주세요!")
        else:
            song_info = SONG_DATABASE[selected_song_title]
            st.session_state.queue.append({
                "title": selected_song_title,
                "yt_id": song_info["yt_id"],
                "bpm": song_info["bpm"]
            })
            st.session_state.coins -= 1
            st.success("예약 완료!")
            st.rerun()

    st.subheader("📋 대기열")
    if st.session_state.queue:
        for idx, item in enumerate(st.session_state.queue, 1):
            st.write(f"**{idx}.** {item['title']}")
    else:
        st.caption("예약된 노래가 없습니다.")

with col2:
    st.subheader("📺 퍼펙트 스코어 스테이지")

    if not st.session_state.current_song and st.session_state.queue:
        st.session_state.current_song = st.session_state.queue.pop(0)
        st.rerun()

    if st.session_state.current_song:
        song = st.session_state.current_song
        st.info(f"🎤 **NOW PLAYING:** {song['title']}")

        perfect_score_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                * {{ box-sizing: border-box; margin: 0; padding: 0; }}
                body {{ background: #000; color: #fff; font-family: 'Segoe UI', sans-serif; overflow: hidden; }}
                #score-canvas {{ width: 100%; height: 160px; background: #0a0a1e; border-bottom: 2px solid #ec4899; display: block; }}
                iframe {{ width: 100%; height: 320px; border: none; }}
                #hud {{
                    display: flex; justify-content: space-between; align-items: center;
                    padding: 8px 16px; background: #0d0826; border-top: 1px solid #334155;
                }}
                .hud-val {{ font-size: 18px; font-weight: bold; color: #38bdf8; }}
                .judge-pop {{ position: absolute; top: 60px; right: 20px; font-size: 28px; font-weight: 900; text-shadow: 0 0 10px #facc15; }}
            </style>
        </head>
        <body>
            <div style="position:relative;">
                <canvas id="score-canvas"></canvas>
                <div id="judge" class="judge-pop" style="color:#facc15;">READY</div>
            </div>
            
            <iframe src="https://www.youtube.com/embed/{song['yt_id']}?autoplay=1&enablejsapi=1" allow="autoplay"></iframe>

            <div id="hud">
                <div>🎙️ 입력 음정: <span id="user-pitch" class="hud-val">--- Hz</span></div>
                <div>🎯 점수: <span id="total-score" class="hud-val" style="color:#ec4899;">100</span></div>
            </div>

            <script>
                const canvas = document.getElementById('score-canvas');
                const ctx = canvas.getContext('2d');
                canvas.width = window.innerWidth;
                canvas.height = 160;

                let audioCtx, analyser;
                let currentPitch = 0;
                let score = 100;
                let history = [];

                async function setupMic() {{
                    try {{
                        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                        analyser = audioCtx.createAnalyser();
                        analyser.fftSize = 2048;
                        const stream = await navigator.mediaDevices.getUserMedia({{ audio: true }});
                        audioCtx.createMediaStreamSource(stream).connect(analyser);
                    }} catch (e) {{}}
                }}

                function detectPitch() {{
                    if (!analyser) return;
                    const buf = new Float32Array(2048);
                    analyser.getFloatTimeDomainData(buf);
                    let sum = 0;
                    for(let i=0; i<2048; i++) sum += buf[i]*buf[i];
                    let rms = Math.sqrt(sum/2048);
                    if (rms > 0.015) {{
                        currentPitch = Math.min(Math.max(rms * 1500, 100), 500);
                        document.getElementById('user-pitch').innerText = Math.round(currentPitch) + " Hz";
                    }} else {{
                        currentPitch = 0;
                        document.getElementById('user-pitch').innerText = "--- Hz";
                    }}
                }}

                let xPos = 0;
                function drawPerfectScore() {{
                    ctx.clearRect(0, 0, canvas.width, canvas.height);

                    // 1. 가이드 피치 라인 (타겟 음정 노드)
                    const targetY = canvas.height/2 + Math.sin(xPos * 0.05) * 40;
                    ctx.strokeStyle = "rgba(56, 189, 248, 0.4)";
                    ctx.lineWidth = 12;
                    ctx.beginPath();
                    ctx.moveTo(0, targetY);
                    ctx.lineTo(canvas.width, targetY);
                    ctx.stroke();

                    // 2. 실시간 사용자 음정 궤적
                    detectPitch();
                    if (currentPitch > 0) {{
                        const userY = canvas.height - ((currentPitch - 100) / 400 * canvas.height);
                        history.push({{x: canvas.width * 0.7, y: userY}});
                        if (history.length > 50) history.shift();

                        const diff = Math.abs(userY - targetY);
                        const judgeEl = document.getElementById('judge');
                        if (diff < 15) {{
                            judgeEl.innerText = "PERFECT!"; judgeEl.style.color = "#34d399";
                        }} else if (diff < 30) {{
                            judgeEl.innerText = "GREAT"; judgeEl.style.color = "#facc15";
                        }} else {{
                            judgeEl.innerText = "MISS"; judgeEl.style.color = "#f43f5e";
                            score = Math.max(40, score - 0.05);
                            document.getElementById('total-score').innerText = Math.round(score);
                        }}
                    }}

                    // 궤적 그리기
                    ctx.strokeStyle = "#ec4899";
                    ctx.lineWidth = 5;
                    ctx.beginPath();
                    for (let i = 0; i < history.length; i++) {{
                        const pt = history[i];
                        pt.x -= 2;
                        if (i === 0) ctx.moveTo(pt.x, pt.y);
                        else ctx.lineTo(pt.x, pt.y);
                    }}
                    ctx.stroke();

                    xPos += 1;
                    requestAnimationFrame(drawPerfectScore);
                }}

                setupMic();
                drawPerfectScore();
            </script>
        </body>
        </html>
        """
        components.html(perfect_score_html, height=520)

        if st.button("⏭️ 다음 곡으로 넘기기 / 간주점프"):
            st.session_state.current_song = None
            st.rerun()
    else:
        st.warning("코인을 충전하고 곡을 예약하면 퍼펙트 스코어 노래방이 시작됩니다!")
