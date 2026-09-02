import streamlit as st
import streamlit.components.v1 as components
import time

st.set_page_config(page_title="REAL PERFECT SCORE KARAOKE", page_icon="🎤", layout="wide")

# 세션 상태 초기화
if "coins" not in st.session_state:
    st.session_state.coins = 0
if "queue" not in st.session_state:
    st.session_state.queue = []
if "current_song" not in st.session_state:
    st.session_state.current_song = None

# 저작권 에러 없이 직접 재생 가능한 고음질 샘플 MR 데이터베이스 (노래방 번호 포함)
SONG_DATABASE = {
    "❤️ [R&B] 죠지 - 좋아해.. (TJ 52277)": {
        "tj_num": "52277",
        "audio_url": "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=lofi-study-112191.mp3",
        "bpm": 80
    },
    "⛵ [R&B] 죠지 - Boat (TJ 98709)": {
        "tj_num": "98709",
        "audio_url": "https://cdn.pixabay.com/download/audio/2022/03/15/audio_c8c8a73467.mp3?filename=chill-abstract-intention-12099.mp3",
        "bpm": 95
    },
    "🎸 [R&B] 죠지 - routine (TJ 78921)": {
        "tj_num": "78921",
        "audio_url": "https://cdn.pixabay.com/download/audio/2022/01/18/audio_d0a13f69d2.mp3?filename=funky-synthwave-11254.mp3",
        "bpm": 88
    },
    "🤝 [R&B] 죠지 - 손만 잡고 잠을 자자 (TJ 78512)": {
        "tj_num": "78512",
        "audio_url": "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=lofi-study-112191.mp3",
        "bpm": 85
    },
    "✨ [IDOL] NewJeans - Hype Boy (TJ 82072)": {
        "tj_num": "82072",
        "audio_url": "https://cdn.pixabay.com/download/audio/2022/03/15/audio_c8c8a73467.mp3?filename=chill-abstract-intention-12099.mp3",
        "bpm": 115
    },
    "🌧️ [BALLAD] 성시경 - 거리에서 (TJ 16568)": {
        "tj_num": "16568",
        "audio_url": "https://cdn.pixabay.com/download/audio/2022/01/18/audio_d0a13f69d2.mp3?filename=funky-synthwave-11254.mp3",
        "bpm": 72
    }
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
</style>
""", unsafe_allow_html=True)

st.title("🎤 PERFECT SCORE AI KARAOKE 🪙")

col_left, col_right = st.columns([1.1, 2])

# 알바 및 노래 예약 영역
with col_left:
    st.subheader("💰 코인노래방 알바센터")
    st.markdown(f'<div class="coin-badge">보유 코인: {st.session_state.coins} 코인</div>', unsafe_allow_html=True)
    
    st.write("")
    st.caption("🛠️ 알바를 완료해야 노래방 코인이 충전됩니다!")
    
    work_tab1, work_tab2, work_tab3 = st.tabs(["🧹 방 청소", "🥤 음료 채우기", "🛎️ 카운터 응대"])
    
    with work_tab1:
        st.write("**3번 방 마이크와 테이블을 청소하세요!**")
        if st.button("🧹 열심히 청소하기", use_container_width=True):
            with st.spinner("방 소독 및 청소 중..."):
                time.sleep(1)
            st.session_state.coins += 1
            st.success("청소 완료! 1코인 획득 🪙")
            st.rerun()

    with work_tab2:
        st.write("**냉장고에 음료수를 채워주세요!**")
        drink = st.radio("채울 음료", ["식혜", "포카리스웨트", "옥수수수염차"])
        if st.button("🥤 냉장고 채우기", use_container_width=True):
            st.session_state.coins += 1
            st.success(f"{drink} 채우기 완료! 1코인 획득 🪙")
            st.rerun()

    with work_tab3:
        st.write("**손님이 5,000원을 냈습니다. 500원짜리 동전 개수는?**")
        ans = st.number_input("동전 개수 입력", min_value=0, max_value=20, value=0)
        if st.button("🛎️ 계산 완료", use_container_width=True):
            if ans == 10:
                st.session_state.coins += 2
                st.success("정답! 2코인 획득 🪙🪙")
                st.rerun()
            else:
                st.error("계산이 틀렸습니다! (5,000원 = 500원 x 10개)")

    st.divider()

    st.subheader("🎶 노래 예약하기")
    selected_song_key = st.selectbox("노래 목록 선택", list(SONG_DATABASE.keys()))

    if st.button("📌 곡 예약하기 (1코인 차감)", use_container_width=True):
        if st.session_state.coins <= 0:
            st.error("코인이 부족합니다! 탭에서 알바를 하고 코인을 버세요.")
        else:
            song_data = SONG_DATABASE[selected_song_key]
            st.session_state.queue.append({
                "title": selected_song_key,
                "audio_url": song_data["audio_url"],
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

# 플레이어 & 퍼펙트 스코어 영역
with col_right:
    st.subheader("📺 퍼펙트스코어 2D 무대")

    if not st.session_state.current_song and st.session_state.queue:
        st.session_state.current_song = st.session_state.queue.pop(0)
        st.rerun()

    if st.session_state.current_song:
        song = st.session_state.current_song
        st.info(f"🎤 **NOW PLAYING:** {song['title']} (TJ 번호: {song['tj_num']})")

        player_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                * {{ box-sizing: border-box; margin: 0; padding: 0; }}
                body {{ background: #030014; color: #fff; font-family: 'Segoe UI', sans-serif; overflow: hidden; }}
                #canvas-container {{ position: relative; width: 100%; height: 200px; background: #09051d; border: 2px solid #ec4899; border-radius: 12px; overflow: hidden; margin-bottom: 15px; }}
                canvas {{ width: 100%; height: 100%; display: block; }}
                #hud-overlay {{
                    position: absolute; top: 10px; right: 15px; background: rgba(15, 23, 42, 0.85);
                    padding: 8px 16px; border-radius: 12px; border: 1px solid #38bdf8; text-align: right;
                }}
                .hud-val {{ font-size: 20px; font-weight: bold; color: #38bdf8; }}
                #judge-txt {{ position: absolute; top: 15px; left: 20px; font-size: 30px; font-weight: 900; color: #facc15; text-shadow: 0 0 12px #facc15; }}
                .audio-box {{
                    background: rgba(15, 23, 42, 0.9); padding: 15px; border-radius: 12px;
                    border: 1px solid #6366f1; text-align: center;
                }}
                audio {{ width: 100%; margin-top: 10px; border-radius: 8px; }}
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

            <div class="audio-box">
                <p style="font-weight: bold; color: #38bdf8;">🎵 MR 반주 오디오 플레이어 (에러 없음)</p>
                <audio id="mr-player" controls autoplay loop src="{song['audio_url']}"></audio>
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

                    ctx.strokeStyle = "rgba(255, 255, 255, 0.08)";
                    ctx.lineWidth = 1;
                    for (let y = 30; y < canvas.height; y += 35) {{
                        ctx.beginPath();
                        ctx.moveTo(0, y);
                        ctx.lineTo(canvas.width, y);
                        ctx.stroke();
                    }}

                    const targetY = canvas.height / 2 + Math.sin(step * 0.04) * 45;
                    ctx.fillStyle = "rgba(56, 189, 248, 0.6)";
                    ctx.fillRect(canvas.width * 0.6, targetY - 8, 80, 16);

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
                            currentScore = Math.max(50, currentScore - 0.03);
                            document.getElementById('score-val').innerText = Math.round(currentScore);
                        }}
                    }} else {{
                        pitchEl.innerText = "--- Hz";
                    }}

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
        components.html(player_html, height=350)

        st.write("")
        if st.button("⏭️ 다음 곡으로 넘기기 (간주 점프)", use_container_width=True):
            st.session_state.current_song = None
            st.rerun()
    else:
        st.warning("알바를 완료해 코인을 번 후, 원하시는 곡을 예약해 보세요!")
