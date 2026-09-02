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

# 인터넷 연결 없이 100% 자체 재생되는 동요 데이터베이스 (주파수 멜로디 패턴)
CHILDREN_SONGS = {
    "🐻 [동요] 곰 세 마리 (TJ 1001)": {
        "tj_num": "1001",
        "notes": [261, 261, 261, 261, 261, 329, 392, 392, 329, 261, 392, 392, 329, 392, 392, 329],
        "bpm": 120
    },
    "✈️ [동요] 비행기 (TJ 1002)": {
        "tj_num": "1002",
        "notes": [329, 293, 261, 293, 329, 329, 329, 293, 293, 293, 329, 392, 392],
        "bpm": 110
    },
    "⭐ [동요] 작은 별 (TJ 1003)": {
        "tj_num": "1003",
        "notes": [261, 261, 392, 392, 440, 440, 392, 349, 349, 329, 329, 293, 293, 261],
        "bpm": 100
    },
    "🔔 [동요] 학교 종 (TJ 1004)": {
        "tj_num": "1004",
        "notes": [392, 392, 440, 440, 392, 392, 329, 392, 392, 329, 329, 293],
        "bpm": 115
    },
    "🦋 [동요] 나비야 (TJ 1005)": {
        "tj_num": "1005",
        "notes": [392, 329, 329, 349, 293, 293, 261, 293, 329, 349, 392, 392, 392],
        "bpm": 105
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

st.title("🎤 PERFECT SCORE CHILD SONG KARAOKE 🪙")

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

    st.subheader("🎶 동요 예약하기")
    selected_song_key = st.selectbox("수록 동요 목록", list(CHILDREN_SONGS.keys()))

    if st.button("📌 곡 예약하기 (1코인 차감)", use_container_width=True):
        if st.session_state.coins <= 0:
            st.error("코인이 없습니다! 알바를 해서 코인을 버세요.")
        else:
            song_data = CHILDREN_SONGS[selected_song_key]
            st.session_state.queue.append({
                "title": selected_song_key,
                "tj_num": song_data["tj_num"],
                "notes": song_data["notes"],
                "bpm": song_data["bpm"]
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

# TJ 퍼펙트스코어 무대
with col_right:
    st.subheader("📺 퍼펙트 스코어 2D 가창 모니터")

    if not st.session_state.current_song and st.session_state.queue:
        st.session_state.current_song = st.session_state.queue.pop(0)
        st.rerun()

    if st.session_state.current_song:
        song = st.session_state.current_song
        st.info(f"🎤 **NOW PLAYING:** {song['title']} (TJ 번호: {song['tj_num']})")

        perfect_score_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                * {{ box-sizing: border-box; margin: 0; padding: 0; }}
                body {{ background: #000; color: #fff; font-family: sans-serif; overflow: hidden; }}
                #stage {{
                    position: relative; width: 100%; height: 260px;
                    background: linear-gradient(to bottom, #07091e, #0f172a);
                    border: 2px solid #ec4899; border-radius: 12px; overflow: hidden;
                }}
                canvas {{ width: 100%; height: 100%; display: block; }}
                #hud {{
                    position: absolute; top: 12px; right: 15px;
                    background: rgba(15, 23, 42, 0.9); padding: 8px 16px;
                    border-radius: 10px; border: 1px solid #38bdf8; text-align: right;
                }}
                .val {{ font-size: 20px; font-weight: 900; color: #38bdf8; }}
                #judge-box {{
                    position: absolute; top: 15px; left: 20px;
                    font-size: 32px; font-weight: 900; color: #facc15;
                    text-shadow: 0 0 15px #facc15;
                }}
                #combo-box {{
                    position: absolute; top: 55px; left: 20px;
                    font-size: 18px; font-weight: bold; color: #f43f5e;
                }}
                .controls {{
                    background: #0d0826; padding: 12px; border-radius: 10px;
                    border: 1px solid #6366f1; margin-top: 10px; text-align: center;
                }}
                button {{
                    background: #38bdf8; color: #000; border: none; padding: 10px 20px;
                    font-weight: bold; font-size: 16px; border-radius: 8px; cursor: pointer;
                }}
                button:hover {{ background: #0284c7; color: #fff; }}
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

            <div class="controls">
                <button id="start-btn" onclick="startAudioEngine()">▶️ 동요 MR 반주 재생 시작</button>
            </div>

            <script>
                const canvas = document.getElementById('tjCanvas');
                const ctx = canvas.getContext('2d');
                canvas.width = canvas.offsetWidth;
                canvas.height = canvas.offsetHeight;

                const notes = {song['notes']};
                let audioCtx, analyser, isPlaying = false;
                let userPitch = 0;
                let score = 100.0;
                let combo = 0;
                let scanX = 0;
                let userHistory = [];
                let noteIdx = 0;

                async function startAudioEngine() {{
                    if (isPlaying) return;
                    document.getElementById('start-btn').style.display = 'none';
                    isPlaying = true;

                    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                    
                    // 마이크 연결
                    try {{
                        analyser = audioCtx.createAnalyser();
                        analyser.fftSize = 2048;
                        const stream = await navigator.mediaDevices.getUserMedia({{ audio: true }});
                        audioCtx.createMediaStreamSource(stream).connect(analyser);
                    }} catch(e) {{}}

                    playMelodySynth();
                }}

                // 외부 mp3 대신 브라우저가 자체 합성하는 동요 반주 엔진
                function playMelodySynth() {{
                    if (!isPlaying) return;
                    let freq = notes[noteIdx % notes.length];
                    
                    let osc = audioCtx.createOscillator();
                    let gain = audioCtx.createGain();
                    
                    osc.type = 'triangle';
                    osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
                    
                    gain.gain.setValueAtTime(0.15, audioCtx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.4);

                    osc.connect(gain);
                    gain.connect(audioCtx.destination);

                    osc.start();
                    osc.stop(audioCtx.currentTime + 0.4);

                    noteIdx++;
                    setTimeout(playMelodySynth, 450);
                }}

                function detectMicPitch() {{
                    if (!analyser) return 0;
                    const buf = new Float32Array(2048);
                    analyser.getFloatTimeDomainData(buf);
                    let sum = 0;
                    for (let i = 0; i < 2048; i++) sum += buf[i] * buf[i];
                    let rms = Math.sqrt(sum / 2048);
                    return rms > 0.015 ? rms * 1500 : 0;
                }}

                function drawTJScores() {{
                    ctx.clearRect(0, 0, canvas.width, canvas.height);

                    // 1. 가이드 라인
                    ctx.strokeStyle = "rgba(255, 255, 255, 0.08)";
                    ctx.lineWidth = 1;
                    for (let y = 20; y < canvas.height; y += 30) {{
                        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
                    }}

                    // 2. TJ 동요 퍼펙트스코어 노트 바
                    const barWidth = canvas.width / notes.length;
                    let currentTargetY = 0;

                    for (let i = 0; i < notes.length; i++) {{
                        const bx = i * barWidth;
                        const by = canvas.height - ((notes[i] - 150) / 350 * canvas.height);
                        
                        ctx.fillStyle = "rgba(250, 204, 21, 0.75)";
                        ctx.fillRect(bx + 2, by - 6, barWidth - 4, 12);
                        ctx.strokeStyle = "#facc15";
                        ctx.strokeRect(bx + 2, by - 6, barWidth - 4, 12);

                        if (scanX >= bx && scanX < bx + barWidth) {{
                            currentTargetY = by;
                        }}
                    }}

                    // 3. 스캐너 정밀 탐침선
                    ctx.strokeStyle = "#f43f5e";
                    ctx.lineWidth = 2;
                    ctx.beginPath();
                    ctx.moveTo(scanX, 0); ctx.lineTo(scanX, canvas.height);
                    ctx.stroke();

                    // 4. 마이크 음정 판정
                    userPitch = detectMicPitch();
                    const pitchEl = document.getElementById('pitch-val');
                    const judgeEl = document.getElementById('judge-box');
                    const comboEl = document.getElementById('combo-box');

                    if (userPitch > 0) {{
                        pitchEl.innerText = Math.round(userPitch) + " Hz";
                        const userY = canvas.height - ((userPitch - 150) / 350 * canvas.height);
                        
                        userHistory.push({{ x: scanX, y: userY }});
                        if (userHistory.length > 50) userHistory.shift();

                        const diff = Math.abs(userY - currentTargetY);
                        if (diff < 22) {{
                            judgeEl.innerText = "PERFECT!"; judgeEl.style.color = "#34d399";
                            combo++;
                        }} else if (diff < 40) {{
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

                    // 5. 음정 궤적
                    ctx.strokeStyle = "#ec4899";
                    ctx.lineWidth = 4;
                    ctx.beginPath();
                    for (let i = 0; i < userHistory.length; i++) {{
                        const pt = userHistory[i];
                        if (i === 0) ctx.moveTo(pt.x, pt.y);
                        else ctx.lineTo(pt.x, pt.y);
                    }}
                    ctx.stroke();

                    if (isPlaying) {{
                        scanX = (scanX + 1.5) % canvas.width;
                    }}
                    requestAnimationFrame(drawTJScores);
                }}

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
        st.warning("알바를 해서 코인을 채운 후, 동요를 예약해 보세요!")
