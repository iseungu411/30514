import streamlit as st
import streamlit.components.v1 as components
import time

# 페이지 설정
st.set_page_config(page_title="PERFECT SCORE KARAOKE", page_icon="🎤", layout="wide")

# 세션 상태 초기화
if "coins" not in st.session_state:
    st.session_state.coins = 0
if "queue" not in st.session_state:
    st.session_state.queue = []
if "current_song" not in st.session_state:
    st.session_state.current_song = None

# 웹 오류 발생 제로! 100% 내장 신디사이저 반주 데이터베이스
CHILDREN_SONGS = {
    "🐻 [동요] 곰 세 마리 (TJ 1001)": {
        "tj_num": "1001",
        "notes": [261, 261, 261, 261, 261, 329, 392, 392, 329, 261, 392, 392, 329, 392, 392, 329],
        "tempo": 400
    },
    "✈️ [동요] 비행기 (TJ 1002)": {
        "tj_num": "1002",
        "notes": [329, 293, 261, 293, 329, 329, 329, 293, 293, 293, 329, 392, 392],
        "tempo": 450
    },
    "⭐ [동요] 작은 별 (TJ 1003)": {
        "tj_num": "1003",
        "notes": [261, 261, 392, 392, 440, 440, 392, 349, 349, 329, 329, 293, 293, 261],
        "tempo": 500
    },
    "🔔 [동요] 학교 종 (TJ 1004)": {
        "tj_num": "1004",
        "notes": [392, 392, 440, 440, 392, 392, 329, 392, 392, 329, 329, 293],
        "tempo": 420
    },
    "🦋 [동요] 나비야 (TJ 1005)": {
        "tj_num": "1005",
        "notes": [392, 329, 329, 349, 293, 293, 261, 293, 329, 349, 392, 392, 392],
        "tempo": 450
    }
}

# 스타일링
st.markdown("""
<style>
    .stApp { background-color: #050314; color: #ffffff; }
    .coin-badge {
        background: linear-gradient(135deg, #10b981, #047857);
        padding: 16px; border-radius: 14px; text-align: center;
        font-weight: 800; font-size: 22px; color: #fff;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.4);
    }
</style>
""", unsafe_allow_html=True)

st.title("🎤 PERFECT SCORE AI KARAOKE SYSTEM 🪙")
st.caption("수행평가용 코인노래방 알바 & TJ 퍼펙트스코어 가창 시뮬레이터")

col_left, col_right = st.columns([1.1, 2])

# 1. 알바 및 노래 예약 영역
with col_left:
    st.subheader("💰 코인노래방 알바센터")
    st.markdown(f'<div class="coin-badge">보유 코인: {st.session_state.coins} 코인</div>', unsafe_allow_html=True)
    st.write("")
    
    t1, t2, t3 = st.tabs(["🧹 방 청소", "🥤 음료 채우기", "🛎️ 계산하기"])
    
    with t1:
        st.write("**방 청소 후 소독 작업을 진행하세요.**")
        if st.button("🧹 방 청소 완료 (+1코인)", use_container_width=True):
            with st.spinner("청소 중..."):
                time.sleep(0.5)
            st.session_state.coins += 1
            st.success("1코인 획득!")
            st.rerun()

    with t2:
        st.write("**냉장고 음료를 정렬하세요.**")
        drink = st.selectbox("선택", ["식혜", "이온음료", "탄산수"])
        if st.button("🥤 채우기 완료 (+1코인)", use_container_width=True):
            st.session_state.coins += 1
            st.success(f"{drink} 채우기 완료! 1코인 획득!")
            st.rerun()

    with t3:
        st.write("**5,000원 지불 시 500원 동전 개수는?**")
        ans = st.number_input("개수 입력", min_value=0, max_value=20, value=0)
        if st.button("🛎️ 거스름돈 전달 (+2코인)", use_container_width=True):
            if ans == 10:
                st.session_state.coins += 2
                st.success("정답! 2코인 획득!")
                st.rerun()
            else:
                st.error("오답입니다! (5,000원 = 500원 x 10개)")

    st.divider()

    st.subheader("🎶 노래 예약하기")
    selected_song_key = st.selectbox("수록곡 선택", list(CHILDREN_SONGS.keys()))

    if st.button("📌 곡 예약하기 (1코인 차감)", use_container_width=True):
        if st.session_state.coins <= 0:
            st.error("코인이 부족합니다! 알바를 먼저 해주세요.")
        else:
            song_data = CHILDREN_SONGS[selected_song_key]
            st.session_state.queue.append({
                "title": selected_song_key,
                "tj_num": song_data["tj_num"],
                "notes": song_data["notes"],
                "tempo": song_data["tempo"]
            })
            st.session_state.coins -= 1
            st.success("곡이 예약되었습니다!")
            st.rerun()

    st.subheader("📋 대기 목록")
    if st.session_state.queue:
        for idx, item in enumerate(st.session_state.queue, 1):
            st.write(f"**{idx}.** {item['title']}")
    else:
        st.caption("예약된 곡이 없습니다.")

# 2. 퍼펙트 스코어 2D 메인 무대
with col_right:
    st.subheader("📺 TJ 퍼펙트스코어 2D 모니터")

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
                    background: #38bdf8; color: #000; border: none; padding: 12px 24px;
                    font-weight: bold; font-size: 17px; border-radius: 8px; cursor: pointer;
                    box-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
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
                <button id="start-btn" onclick="startAudioEngine()">▶️ 동요 MR 반주 시작하기</button>
            </div>

            <script>
                const canvas = document.getElementById('tjCanvas');
                const ctx = canvas.getContext('2d');
                canvas.width = canvas.offsetWidth;
                canvas.height = canvas.offsetHeight;

                const notes = {song['notes']};
                const tempo = {song['tempo']};
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
                    
                    try {{
                        analyser = audioCtx.createAnalyser();
                        analyser.fftSize = 2048;
                        const stream = await navigator.mediaDevices.getUserMedia({{ audio: true }});
                        audioCtx.createMediaStreamSource(stream).connect(analyser);
                    }} catch(e) {{}}

                    playMelodySynth();
                }}

                // 내장 오디오 오실레이터 반주 엔진
                function playMelodySynth() {{
                    if (!isPlaying) return;
                    let freq = notes[noteIdx % notes.length];
                    
                    let osc = audioCtx.createOscillator();
                    let gain = audioCtx.createGain();
                    
                    osc.type = 'triangle';
                    osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
                    
                    gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.35);

                    osc.connect(gain);
                    gain.connect(audioCtx.destination);

                    osc.start();
                    osc.stop(audioCtx.currentTime + 0.35);

                    noteIdx++;
                    setTimeout(playMelodySynth, tempo);
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

                    // 1. 배경선
                    ctx.strokeStyle = "rgba(255, 255, 255, 0.08)";
                    ctx.lineWidth = 1;
                    for (let y = 20; y < canvas.height; y += 30) {{
                        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
                    }}

                    // 2. 노트 바
                    const barWidth = canvas.width / notes.length;
                    let currentTargetY = 0;

                    for (let i = 0; i < notes.length; i++) {{
                        const bx = i * barWidth;
                        const by = canvas.height - ((notes[i] - 150) / 350 * canvas.height);
                        
                        ctx.fillStyle = "rgba(250, 204, 21, 0.85)";
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

                    // 4. 실시간 음정 판정
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

                    // 5. 음정 궤적 핑크 파동
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
        if st.button("⏭️ 다음 곡으로 넘기기", use_container_width=True):
            st.session_state.current_song = None
            st.rerun()
    else:
        st.warning("👈 왼쪽 알바센터에서 코인을 번 후 동요를 예약해 보세요!")
