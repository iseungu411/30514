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
""", unsafe_allow_html=True)

st.title("👑 TJ PERFECT SCORE ULTIMATE KARAOKE MAX 🪙")
st.caption("수행평가 최종 시연용 코인노래방 알바 & 퍼펙트스코어 오디오 엔진 시뮬레이터")

col_left, col_right = st.columns([1.1, 2])

# 1. 알바센터 & 예약 시스템
with col_left:
    st.subheader("💰 코인노래방 알바센터")
    st.markdown(f'<div class="coin-badge">보유 코인: {st.session_state.coins} 코인</div>', unsafe_allow_html=True)
    st.write("")
    
    t1, t2, t3 = st.tabs(["🧹 방 청소", "🥤 음료 채우기", "🛎️ 카운터 계산"])
    
    with t1:
        st.write("**3번 방 마이크 소독 및 테이블 닦기**")
        if st.button("🧹 방 청소 완료 (+1코인)", use_container_width=True):
            with st.spinner("소독제 뿌리는 중..."):
                time.sleep(0.3)
            st.session_state.coins += 1
            st.success("1코인 획득!")
            st.rerun()

    with t2:
        st.write("**냉장고 음료 정렬하기**")
        drink = st.selectbox("선택", ["식혜", "이온음료", "탄산수"])
        if st.button("🥤 정렬 완료 (+1코인)", use_container_width=True):
            st.session_state.coins += 1
            st.success(f"{drink} 정렬 완료! 1코인 획득!")
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
    selected_song_key = st.selectbox("수록곡 선택", list(SONG_DATABASE.keys()))

    if st.button("📌 곡 예약하기 (1코인 차감)", use_container_width=True):
        if st.session_state.coins <= 0:
            st.error("코인이 부족합니다! 알바를 먼저 수행하세요.")
        else:
            song_data = SONG_DATABASE[selected_song_key]
            st.session_state.queue.append({
                "title": selected_song_key,
                "tj_num": song_data["tj_num"],
                "notes": song_data["notes"],
                "lyrics": song_data["lyrics"],
                "chords": song_data["chords"],
                "bpm": song_data["bpm"]
            })
            st.session_state.coins -= 1
            st.success("곡이 성공적으로 예약되었습니다!")
            st.rerun()

    st.subheader("📋 대기 목록")
    if st.session_state.queue:
        for idx, item in enumerate(st.session_state.queue, 1):
            st.write(f"**{idx}.** {item['title']}")
    else:
        st.caption("예약된 곡이 없습니다.")

# 2. 퍼펙트 스코어 2D 엔진 메인 화면
with col_right:
    st.subheader("📺 TJ 퍼펙트스코어 가창 모니터")

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
                body {{ background: #000; color: #fff; font-family: 'Segoe UI', sans-serif; overflow: hidden; }}
                #stage {{
                    position: relative; width: 100%; height: 300px;
                    background: radial-gradient(circle at center, #1e1b4b 0%, #030014 100%);
                    border: 3px solid #ec4899; border-radius: 14px; overflow: hidden;
                    box-shadow: 0 0 25px rgba(236, 72, 153, 0.4);
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
                    font-size: 36px; font-weight: 900; color: #facc15;
                    text-shadow: 0 0 20px #facc15;
                }}
                #combo-box {{
                    position: absolute; top: 60px; left: 20px;
                    font-size: 20px; font-weight: bold; color: #f43f5e;
                }}
                #lyrics-box {{
                    position: absolute; bottom: 10px; width: 100%; text-align: center;
                    font-size: 24px; font-weight: 900; color: #38bdf8;
                    text-shadow: 0 0 12px #0284c7; background: rgba(0,0,0,0.6); padding: 6px 0;
                }}
                .controls {{
                    background: #0d0826; padding: 12px; border-radius: 10px;
                    border: 1px solid #6366f1; margin-top: 10px; text-align: center;
                    display: flex; gap: 8px; justify-content: center; flex-wrap: wrap;
                }}
                button {{
                    background: linear-gradient(135deg, #38bdf8, #0284c7);
                    color: #fff; border: none; padding: 10px 20px;
                    font-weight: bold; font-size: 15px; border-radius: 8px; cursor: pointer;
                    box-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
                }}
                button.fx-btn {{ background: linear-gradient(135deg, #a855f7, #7e22ce); }}
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
                <div id="lyrics-box">🎤 [반주 시작] 버튼을 클릭하세요</div>
            </div>

            <div class="controls">
                <button id="start-btn" onclick="startMR()">▶️ 리얼 다채널 MR 시작</button>
                <button id="ai-sing-btn" onclick="toggleAISing()">🤖 AI 가창 시연 (마이크 테스트)</button>
                <button class="fx-btn" onclick="playApplause()">👏 환호 박수</button>
            </div>

            <script>
                const canvas = document.getElementById('tjCanvas');
                const ctx = canvas.getContext('2d');
                canvas.width = canvas.offsetWidth;
                canvas.height = canvas.offsetHeight;

                const notes = {song['notes']};
                const lyrics = {song['lyrics']};
                const chords = {song['chords']};
                const bpm = {song['bpm']};

                let audioCtx, analyser, isPlaying = false, aiSinging = false;
                let userPitch = 0, score = 100.0, combo = 0, scanX = 0;
                let userHistory = [], particles = [], noteIdx = 0;

                async function startMR() {{
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

                    playMultiChannelMREngine();
                }}

                function toggleAISing() {{
                    aiSinging = !aiSinging;
                    const btn = document.getElementById('ai-sing-btn');
                    btn.innerText = aiSinging ? "🤖 AI 가창 중지" : "🤖 AI 가창 시연 (마이크 테스트)";
                    btn.style.background = aiSinging ? "linear-gradient(135deg, #ef4444, #b91c1c)" : "linear-gradient(135deg, #38bdf8, #0284c7)";
                }}

                function playApplause() {{
                    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                    for(let i=0; i<15; i++) {{
                        setTimeout(() => {{
                            let osc = audioCtx.createOscillator();
                            let gain = audioCtx.createGain();
                            osc.type = 'sine';
                            osc.frequency.setValueAtTime(400 + Math.random()*800, audioCtx.currentTime);
                            gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
                            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.1);
                            osc.connect(gain); gain.connect(audioCtx.destination);
                            osc.start(); osc.stop(audioCtx.currentTime + 0.1);
                        }}, i * 40);
                    }}
                }}

                function playMultiChannelMREngine() {{
                    if (!isPlaying) return;
                    const time = audioCtx.currentTime;
                    const interval = (60 / bpm) * 1000;

                    const melFreq = notes[noteIdx % notes.length];
                    const chordFreq = chords[noteIdx % chords.length] / 2;

                    // Lead Melody
                    let melOsc = audioCtx.createOscillator();
                    let melGain = audioCtx.createGain();
                    melOsc.type = 'sawtooth';
                    melOsc.frequency.setValueAtTime(melFreq, time);
                    melGain.gain.setValueAtTime(0.18, time);
                    melGain.gain.exponentialRampToValueAtTime(0.001, time + 0.35);
                    melOsc.connect(melGain); melGain.connect(audioCtx.destination);
                    melOsc.start(time); melOsc.stop(time + 0.35);

                    // AI가 가창 시연 중일 때의 오디오
                    if (aiSinging) {{
                        let aiOsc = audioCtx.createOscillator();
                        let aiGain = audioCtx.createGain();
                        aiOsc.type = 'sine';
                        aiOsc.frequency.setValueAtTime(melFreq * 2, time);
                        aiGain.gain.setValueAtTime(0.2, time);
                        aiGain.gain.exponentialRampToValueAtTime(0.001, time + 0.3);
                        aiOsc.connect(aiGain); aiGain.connect(audioCtx.destination);
                        aiOsc.start(time); aiOsc.stop(time + 0.3);
                    }}

                    // Chords Pad
                    let chordOsc = audioCtx.createOscillator();
                    let chordGain = audioCtx.createGain();
                    chordOsc.type = 'triangle';
                    chordOsc.frequency.setValueAtTime(chordFreq, time);
                    chordGain.gain.setValueAtTime(0.1, time);
                    chordGain.gain.exponentialRampToValueAtTime(0.001, time + 0.4);
                    chordOsc.connect(chordGain); chordGain.connect(audioCtx.destination);
                    chordOsc.start(time); chordOsc.stop(time + 0.4);

                    // Drum Kick
                    let kickOsc = audioCtx.createOscillator();
                    let kickGain = audioCtx.createGain();
                    kickOsc.frequency.setValueAtTime(120, time);
                    kickOsc.frequency.exponentialRampToValueAtTime(0.01, time + 0.1);
                    kickGain.gain.setValueAtTime(0.25, time);
                    kickGain.gain.exponentialRampToValueAtTime(0.001, time + 0.1);
                    kickOsc.connect(kickGain); kickGain.connect(audioCtx.destination);
                    kickOsc.start(time); kickOsc.stop(time + 0.1);

                    document.getElementById('lyrics-box').innerText = lyrics[noteIdx % lyrics.length];

                    noteIdx++;
                    setTimeout(playMultiChannelMREngine, interval);
                }}

                function detectMicPitch() {{
                    if (aiSinging) {{
                        let currentTargetFreq = notes[(noteIdx - 1 + notes.length) % notes.length];
                        return currentTargetFreq;
                    }}
                    if (!analyser) return 0;
                    const buf = new Float32Array(2048);
                    analyser.getFloatTimeDomainData(buf);
                    let sum = 0;
                    for (let i = 0; i < 2048; i++) sum += buf[i] * buf[i];
                    let rms = Math.sqrt(sum / 2048);
                    return rms > 0.015 ? rms * 1500 : 0;
                }}

                function createExplosion(x, y) {{
                    for(let i=0; i<5; i++) {{
                        particles.push({{
                            x: x, y: y,
                            vx: (Math.random() - 0.5) * 4,
                            vy: (Math.random() - 0.5) * 4,
                            life: 1.0, color: "#34d399"
                        }});
                    }}
                }}

                function drawTJScores() {{
                    ctx.clearRect(0, 0, canvas.width, canvas.height);

                    // 가이드라인
                    ctx.strokeStyle = "rgba(255, 255, 255, 0.08)";
                    ctx.lineWidth = 1;
                    for (let y = 20; y < canvas.height; y += 30) {{
                        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
                    }}

                    // 노트 바
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

                    // 스캐너 정밀 탐침선
                    ctx.strokeStyle = "#f43f5e";
                    ctx.lineWidth = 2;
                    ctx.beginPath();
                    ctx.moveTo(scanX, 0); ctx.lineTo(scanX, canvas.height);
                    ctx.stroke();

                    // 실시간 판정
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
                            createExplosion(scanX, userY);
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

                    // 핑크 궤적
                    ctx.strokeStyle = "#ec4899";
                    ctx.lineWidth = 4;
                    ctx.beginPath();
                    for (let i = 0; i < userHistory.length; i++) {{
                        const pt = userHistory[i];
                        if (i === 0) ctx.moveTo(pt.x, pt.y);
                        else ctx.lineTo(pt.x, pt.y);
                    }}
                    ctx.stroke();

                    // 파티클 그리기
                    for(let i=particles.length-1; i>=0; i--) {{
                        let p = particles[i];
                        p.x += p.vx; p.y += p.vy; p.life -= 0.03;
                        if(p.life <= 0) particles.splice(i, 1);
                        else {{
                            ctx.fillStyle = p.color;
                            ctx.globalAlpha = p.life;
                            ctx.fillRect(p.x, p.y, 4, 4);
                            ctx.globalAlpha = 1.0;
                        }}
                    }}

                    if (isPlaying) scanX = (scanX + 1.5) % canvas.width;
                    requestAnimationFrame(drawTJScores);
                }}

                drawTJScores();
            </script>
        </body>
        </html>
        """
        components.html(perfect_score_html, height=400)

        st.write("")
        if st.button("⏭️ 다음 곡으로 넘기기", use_container_width=True):
            st.session_state.current_song = None
            st.rerun()
    else:
        st.warning("👈 왼쪽 알바센터에서 코인을 번 후 곡을 예약해 보세요!")
