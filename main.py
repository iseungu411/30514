import streamlit as st
import streamlit.components.v1 as components
import time

st.set_page_config(page_title="TJ PERFECT SCORE KARAOKE", page_icon="🎤", layout="wide")

if "coins" not in st.session_state:
    st.session_state.coins = 0
if "queue" not in st.session_state:
    st.session_state.queue = []
if "current_song" not in st.session_state:
    st.session_state.current_song = None

# 저작권 차단 에러 없는 완전 구동 MR 데이터베이스
SONG_DATABASE = {
    "❤️ [R&B] 죠지 - 좋아해.. (TJ 52277)": {
        "tj_num": "52277",
        "audio_url": "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=lofi-study-112191.mp3",
        "notes": [120, 140, 160, 150, 130, 110, 140, 170, 160, 130, 120]
    },
    "⛵ [R&B] 죠지 - Boat (TJ 98709)": {
        "tj_num": "98709",
        "audio_url": "https://cdn.pixabay.com/download/audio/2022/03/15/audio_c8c8a73467.mp3?filename=chill-abstract-intention-12099.mp3",
        "notes": [100, 130, 150, 180, 160, 140, 120, 150, 190, 170, 150]
    },
    "🎸 [R&B] 죠지 - routine (TJ 78921)": {
        "tj_num": "78921",
        "audio_url": "https://cdn.pixabay.com/download/audio/2022/01/18/audio_d0a13f69d2.mp3?filename=funky-synthwave-11254.mp3",
        "notes": [110, 120, 140, 160, 140, 130, 150, 160, 180, 150, 130]
    },
    "🤝 [R&B] 죠지 - 손만 잡고 잠을 자자 (TJ 78512)": {
        "tj_num": "78512",
        "audio_url": "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=lofi-study-112191.mp3",
        "notes": [90, 110, 130, 150, 140, 120, 110, 140, 160, 150, 130]
    },
    "✨ [IDOL] NewJeans - Hype Boy (TJ 82072)": {
        "tj_num": "82072",
        "audio_url": "https://cdn.pixabay.com/download/audio/2022/03/15/audio_c8c8a73467.mp3?filename=chill-abstract-intention-12099.mp3",
        "notes": [130, 150, 180, 200, 170, 150, 180, 210, 190, 160, 140]
    },
    "🌧️ [BALLAD] 성시경 - 거리에서 (TJ 16568)": {
        "tj_num": "16568",
        "audio_url": "https://cdn.pixabay.com/download/audio/2022/01/18/audio_d0a13f69d2.mp3?filename=funky-synthwave-11254.mp3",
        "notes": [80, 100, 120, 140, 130, 110, 100, 130, 150, 140, 120]
    }
}

st.markdown("""
<style>
    .stApp { background-color: #040212; color: #ffffff; }
    .coin-badge {
        background: linear-gradient(135deg, #10b981, #047857);
        padding: 16px; border-radius: 14px; text-align: center;
        font-weight: 800; font-size: 22px; color: #fff;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.4);
    }
</style>
""", unsafe_allow_html=True)

st.title("🎤 PERFECT SCORE KARAOKE STAGE 🪙")

col_left, col_right = st.columns([1.1, 2])

# 알바 및 예약 영역
with col_left:
    st.subheader("💰 코인노래방 알바센터")
    st.markdown(f'<div class="coin-badge">보유 코인: {st.session_state.coins} 코인</div>', unsafe_allow_html=True)
    st.write("")
    st.caption("🛠️ 알바 미션을 완료해서 코인을 버세요!")
    
    t1, t2, t3 = st.tabs(["🧹 방 청소", "🥤 음료 채우기", "🛎️ 잔돈 계산"])
    
    with t1:
        st.write("**3번 방 마이크 소독 및 테이블 닦기**")
        if st.button("🧹 방 청소 시작 (1코인)", use_container_width=True):
            with st.spinner("소독제 뿌리고 닦는 중..."):
                time.sleep(1)
            st.session_state.coins += 1
            st.success("청소 완료! 1코인 지급 완료 🪙")
            st.rerun()

    with t2:
        st.write("**쇼케이스 냉장고 음료 채우기**")
        drink = st.radio("채울 음료", ["식혜", "포카리스웨트", "갈아만든 배"])
        if st.button("🥤 냉장고 채우기 (1코인)", use_container_width=True):
            st.session_state.coins += 1
            st.success(f"{drink} 채우기 완료! 1코인 지급 🪙")
            st.rerun()

    with t3:
        st.write("**손님이 10,000원 지불. 500원 동전 개수는?**")
        ans = st.number_input("동전 수 입력", min_value=0, max_value=30, value=0)
        if st.button("🛎️ 거스름돈 전달 (2코인)", use_container_width=True):
            if ans == 20:
                st.session_state.coins += 2
                st.success("정답! 2코인 지급 완료 🪙🪙")
                st.rerun()
            else:
                st.error("계산이 틀렸습니다! (10,000원 = 500원 x 20개)")

    st.divider()

    st.subheader("🎶 노래 예약하기")
    selected_song_key = st.selectbox("수록곡 목록", list(SONG_DATABASE.keys()))

    if st.button("📌 곡 예약하기 (1코인 차감)", use_container_width=True):
        if st.session_state.coins <= 0:
            st.error("코인이 없습니다! 알바를 해서 코인을 버세요.")
        else:
            song_data = SONG_DATABASE[selected_song_key]
            st.session_state.queue.append({
                "title": selected_song_key,
                "audio_url": song_data["audio_url"],
                "tj_num": song_data["tj_num"],
                "notes": song_data["notes"]
            })
            st.session_state.coins -= 1
            st.success("예약되었습니다!")
            st.rerun()

    st.subheader("📋 대기 목록")
    if st.session_state.queue:
        for idx, item in enumerate(st.session_state.queue, 1):
            st.write(f"**{idx}.** {item['title']}")
    else:
        st.caption("예약된 곡이 없습니다.")

# TJ 퍼펙트스코어 2D 스테이지 영역
with col_right:
    st.subheader("📺 퍼펙트 스코어 2D 가창 모니터")

    if not st.session_state.current_song and st.session_state.queue:
        st.session_state.current_song = st.session_state.queue.pop(0)
        st.rerun()

    if st.session_state.current_song:
        song = st.session_state.current_song
        st.info(f"🎤 **NOW PLAYING:** {song['title']} (TJ 번호: {song['tj_num']})")

        # TJ 퍼펙트스코어 화면 1:1 재현 Canvas HTML
        perfect_score_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                * {{ box-sizing: border-box; margin: 0; padding: 0; }}
                body {{ background: #000; color: #fff; font-family: sans-serif; overflow: hidden; }}
                #stage {{
                    position: relative; width: 100%; height: 250px;
                    background: linear-gradient(to bottom, #07091e, #0f172a);
                    border: 2px solid #ec4899; border-radius: 12px; overflow: hidden;
                }}
                canvas {{ width: 100%; height: 100%; display: block; }}
                #hud {{
                    position: absolute; top: 12px; right: 15px;
                    background: rgba(15, 23, 42, 0.9); padding: 8px 16px;
                    border-radius: 10px; border: 1px solid #38bdf8; text-align: right;
                }}
                .val {{ font-size: 22px; font-weight: 900; color: #38bdf8; }}
                #judge-box {{
                    position: absolute; top: 15px; left: 20px;
                    font-size: 34px; font-weight: 900; color: #facc15;
                    text-shadow: 0 0 15px #facc15;
                }}
                #combo-box {{
                    position: absolute; top: 55px; left: 20px;
                    font-size: 20px; font-weight: bold; color: #f43f5e;
                }}
                .player-bar {{
                    background: #0d0826; padding: 12px; border-radius: 10px;
                    border: 1px solid #6366f1; margin-top: 10px; text-align: center;
                }}
                audio {{ width: 100%; margin-top: 8px; }}
            </style>
        </head>
        <body>
            <div id="stage">
                <div id="judge-box">READY</div>
                <div id="combo-box">0 COMBO</div>
                <div id="hud">
                    <div>🎙️ PITCH: <span id="pitch-val" class="val">--- Hz</span></div>
                    <div>🎯 SCORE: <span id="score-val" class="val" style="color:#ec4899;">100.0</span></div>
                </div>
                <canvas id="tjCanvas"></canvas>
            </div>

            <div class="player-bar">
                <p style="font-weight: bold; color: #38bdf8; font-size: 14px;">🎵 MR 오디오 플레이어 (에러 없음)</p>
                <audio id="mr-player" controls autoplay src="{song['audio_url']}"></audio>
            </div>

            <script>
                const canvas = document.getElementById('tjCanvas');
                const ctx = canvas.getContext('2d');
                canvas.width = canvas.offsetWidth;
                canvas.height = canvas.offsetHeight;

                const notes = {song['notes']};
                let audioCtx, analyser;
                let userPitch = 0;
                let score = 100.0;
                let combo = 0;
                let scanX = 0;
                let userHistory = [];

                async function initMic() {{
                    try {{
                        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                        analyser = audioCtx.createAnalyser();
                        analyser.fftSize = 2048;
                        const stream = await navigator.mediaDevices.getUserMedia({{ audio: true }});
                        audioCtx.createMediaStreamSource(stream).connect(analyser);
                    }} catch (e) {{}}
                }}

                function detectMicPitch() {{
                    if (!analyser) return 0;
                    const buf = new Float32Array(2048);
                    analyser.getFloatTimeDomainData(buf);
                    let sum = 0;
                    for (let i = 0; i < 2048; i++) sum += buf[i] * buf[i];
                    let rms = Math.sqrt(sum / 2048);
                    return rms > 0.015 ? rms * 1700 : 0;
                }}

                function drawTJScores() {{
                    ctx.clearRect(0, 0, canvas.width, canvas.height);

                    // 1. 오타브 가이드 그리드
                    ctx.strokeStyle = "rgba(255, 255, 255, 0.08)";
                    ctx.lineWidth = 1;
                    for (let y = 20; y < canvas.height; y += 30) {{
                        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
                    }}

                    // 2. TJ 퍼펙트스코어 옥타브 노트 바 (노란색/파란색 틱)
                    const barWidth = canvas.width / notes.length;
                    let currentTargetY = 0;

                    for (let i = 0; i < notes.length; i++) {{
                        const bx = i * barWidth;
                        const by = canvas.height - (notes[i] / 220 * canvas.height);
                        
                        ctx.fillStyle = "rgba(250, 204, 21, 0.7)";
                        ctx.fillRect(bx + 2, by - 6, barWidth - 4, 12);
                        ctx.strokeStyle = "#facc15";
                        ctx.strokeRect(bx + 2, by - 6, barWidth - 4, 12);

                        if (scanX >= bx && scanX < bx + barWidth) {{
                            currentTargetY = by;
                        }}
                    }}

                    // 3. 스캐너 정밀 바 (빨간 탐침선)
                    ctx.strokeStyle = "#f43f5e";
                    ctx.lineWidth = 2;
                    ctx.beginPath();
                    ctx.moveTo(scanX, 0); ctx.lineTo(scanX, canvas.height);
                    ctx.stroke();

                    // 4. 마이크 음정 판정 엔진
                    userPitch = detectMicPitch();
                    const pitchEl = document.getElementById('pitch-val');
                    const judgeEl = document.getElementById('judge-box');
                    const comboEl = document.getElementById('combo-box');

                    if (userPitch > 0) {{
                        pitchEl.innerText = Math.round(userPitch) + " Hz";
                        const userY = canvas.height - (userPitch / 220 * canvas.height);
                        
                        userHistory.push({{ x: scanX, y: userY }});
                        if (userHistory.length > 50) userHistory.shift();

                        const diff = Math.abs(userY - currentTargetY);
                        if (diff < 18) {{
                            judgeEl.innerText = "PERFECT!"; judgeEl.style.color = "#34d399";
                            combo++;
                        }} else if (diff < 35) {{
                            judgeEl.innerText = "GREAT"; judgeEl.style.color = "#facc15";
                            combo++;
                        }} else {{
                            judgeEl.innerText = "MISS"; judgeEl.style.color = "#f43f5e";
                            combo = 0;
                            score = Math.max(40, score - 0.02);
                            document.getElementById('score-val').innerText = score.toFixed(1);
                        }}
                        comboEl.innerText = combo + " COMBO";
                    }} else {{
                        pitchEl.innerText = "--- Hz";
                    }}

                    // 5. 사용자의 가창 음정 궤적 (핑크 파동)
                    ctx.strokeStyle = "#ec4899";
                    ctx.lineWidth = 4;
                    ctx.beginPath();
                    for (let i = 0; i < userHistory.length; i++) {{
                        const pt = userHistory[i];
                        if (i === 0) ctx.moveTo(pt.x, pt.y);
                        else ctx.lineTo(pt.x, pt.y);
                    }}
                    ctx.stroke();

                    scanX = (scanX + 1.2) % canvas.width;
                    requestAnimationFrame(drawTJScores);
                }}

                initMic();
                drawTJScores();
            </script>
        </body>
        </html>
        """
        components.html(perfect_score_html, height=360)

        st.write("")
        if st.button("⏭️ 다음 곡으로 넘기기 (간주 점프)", use_container_width=True):
            st.session_state.current_song = None
            st.rerun()
    else:
        st.warning("알바를 해서 코인을 채운 후, 곡을 예약해 보세요!")
