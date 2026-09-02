import streamlit as st
import streamlit.components.v1 as components
import time

st.set_page_config(page_title="TJ PERFECT SCORE ULTIMATE MAX", page_icon="🎤", layout="wide")

# 세션 상태 초기화
if "coins" not in st.session_state:
    st.session_state.coins = 10
if "queue" not in st.session_state:
    st.session_state.queue = []
if "current_song" not in st.session_state:
    st.session_state.current_song = None

# 최고의 노래방 데이터베이스
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
    .stApp { background-color: #020108; color: #ffffff; }
    .coin-badge {
        background: linear-gradient(135deg, #ec4899, #8b5cf6);
        padding: 16px; border-radius: 16px; text-align: center;
        font-weight: 900; font-size: 24px; color: #fff;
        box-shadow: 0 0 25px rgba(236, 72, 153, 0.6);
    }
</style>
""", unsafe_allow_html=True)

st.title("💖 ✨ TJ PERFECT SCORE ULTIMATE DREAM KARAOKE ✨ 💖")
st.caption("수행평가 만점 시연용 프리미엄 코인노래방 알바 & 퍼펙트스코어 시뮬레이터")

col_left, col_right = st.columns([1.1, 2])

# 1. 알바 및 예약 시스템
with col_left:
    st.subheader("💰 코인노래방 알바센터")
    st.markdown(f'<div class="coin-badge">✨ 보유 코인: {st.session_state.coins} 코인 ✨</div>', unsafe_allow_html=True)
    st.write("")
    
    t1, t2, t3 = st.tabs(["🧹 미러볼/방 청소", "🥤 음료 냉장고 정렬", "🛎️ 카운터 잔돈 계산"])
    
    with t1:
        st.write("**3번 방 마이크 소독 및 VIP 미러볼 청소**")
        if st.button("🧹 방 청소 완료 (+1코인)", use_container_width=True):
            with st.spinner("미러볼 닦는 중... ✨"):
                time.sleep(0.3)
            st.session_state.coins += 1
            st.success("1코인 획득!")
            st.rerun()

    with t2:
        st.write("**음료 냉장고 정렬하기**")
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

# 2. 퍼펙트 스코어 메인 무대
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
                body {{ background: #000; color: #fff; font-family: 'Malgun Gothic', sans-serif; overflow: hidden; }}
                #stage {{
                    position: relative; width: 100%; height: 320px;
                    background: radial-gradient(circle at center, #2e1065 0%, #030014 100%);
                    border: 3px solid #ec4899; border-radius: 16px; overflow: hidden;
                    box-shadow: 0 0 30px rgba(236, 72, 153, 0.6), inset 0 0 15px rgba(168, 85, 247, 0.4);
                }}
                canvas {{ width: 100%; height: 100%; display: block; }}
                #hud {{
                    position: absolute; top: 12px; right: 15px;
                    background: rgba(15, 23, 42, 0.85); padding: 8px 16px;
                    border-radius: 12px; border: 1px solid #38bdf8; text-align: right;
                    box-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
                }}
                .val {{ font-size: 20px; font-weight: 900; color: #38bdf8; }}
                #judge-box {{
                    position: absolute; top: 15px; left: 20px;
                    font-size: 38px; font-weight: 900; color: #facc15;
                    text-shadow: 0 0 20px #facc15, 0 0 30px #f59e0b;
                }}
                #combo-box {{
                    position: absolute; top: 62px; left: 20px;
                    font-size: 22px; font-weight: bold; color: #f43f5e;
                    text-shadow: 0 0 10px #f43f5e;
                }}
                #lyrics-box {{
                    position: absolute; bottom: 10px; width: 100%; text-align: center;
                    font-size: 26px; font-weight: 900; color: #38bdf8;
                    text-shadow: 0 0 15px #0284c7, 0 0 25px #38bdf8;
                    background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); padding: 8px 0;
                }}
                #result-overlay {{
                    position: absolute; top:0; left:0; width:100%; height:100%;
                    background: rgba(0,0,0,0.85); display: none; flex-direction: column;
                    justify-content: center; align-items: center; z-index: 10;
                }}
                #result-score {{
                    font-size: 60px; font-weight: 900; color: #facc15;
                    text-shadow: 0 0 30px #facc15, 0 0 50px #f59e0b;
                }}
                .controls {{
                    background: #0d0826; padding: 12px; border-radius: 12px;
                    border: 1px solid #6366f1; margin-top: 10px; text-align: center;
                    display: flex; gap: 8px; justify-content: center; flex-wrap: wrap;
                }}
                button {{
                    background: linear-gradient(135deg, #ec4899, #a855f7);
                    color: #fff; border: none; padding: 10px 18px;
                    font-weight: bold; font-size: 15px; border-radius: 8px; cursor: pointer;
                    box-shadow: 0 0 12px rgba(236, 72, 153, 0.5);
                }}
                button.remote-btn {{ background: linear-gradient(135deg, #38bdf8, #0284c7); }}
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
                <div id="lyrics-box">🎤 [▶️ 반주 시작] 버튼을 누르세요</div>

                <div id="result-overlay">
                    <div style="font-size:28px; color:#38bdf8; font-weight:bold;">🎉 가창 완료! 점수 발표 🎉</div>
                    <div id="result-score">100 점</div>
                    <div style="font-size:20px; color:#4ade80; margin-top:10px;">🏆 완벽한 퍼펙트 스코어입니다! 🏆</div>
                </div>
            </div>

            <div class="controls">
                <button id="start-btn" onclick="startMR()">▶️ 반주 시작</button>
                <button id="ai-sing-btn" onclick="toggleAISing()">🤖 AI 보컬 시연</button>
                <button class="remote-btn" onclick="changeKey(1)">🎼 Key +1</button>
                <button class="remote-btn" onclick="changeKey(-1)">🎼 Key -1</button>
                <button class="remote-btn" onclick="playApplause()">👏 박수/환호</button>
                <button class="remote-btn" onclick="playFanfare()">🎉 팡파레</button>
                <button style="background:#ef4444;" onclick="finishSong()">🏁 점수 발표</button>
            </div>

            <script>
                const canvas = document.getElementById('tjCanvas');
                const ctx = canvas.getContext('2d');
                canvas.width = canvas.offsetWidth;
                canvas.height = canvas.offsetHeight;

                const notes = {song['notes']};
                const lyrics = {song['lyrics']};
                const chords = {song['chords']};
                let bpm = {song['bpm']};
                let keyOffset = 0;

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

                function changeKey(delta) {{
                    keyOffset += delta;
                    playFanfare();
                }}

                function toggleAISing() {{
                    aiSinging = !aiSinging;
                    const btn = document.getElementById('ai-sing-btn');
                    btn.innerText = aiSinging ? "🤖 AI 가창 중지" : "🤖 AI 보컬 시연";
                    btn.style.background = aiSinging ? "linear-gradient(135deg, #ef4444, #b91c1c)" : "linear-gradient(135deg, #ec4899, #a855f7)";
                }}

                function playApplause() {{
                    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                    for(let i=0; i<20; i++) {{
                        setTimeout(() => {{
                            let osc = audioCtx.createOscillator();
                            let gain = audioCtx.createGain();
                            osc.type = 'sine';
                            osc.frequency.setValueAtTime(400 + Math.random()*900, audioCtx.currentTime);
                            gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
                            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.12);
                            osc.connect(gain); gain.connect(audioCtx.destination);
                            osc.start(); osc.stop(audioCtx.currentTime + 0.12);
                        }}, i * 35);
                    }}
                }}

                function playFanfare() {{
                    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                    const scale = [523, 659, 783, 1046];
                    scale.forEach((freq, idx) => {{
                        setTimeout(() => {{
                            let osc = audioCtx.createOscillator();
                            let gain = audioCtx.createGain();
                            osc.type = 'triangle';
                            osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
                            gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
                            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.3);
                            osc.connect(gain); gain.connect(audioCtx.destination);
                            osc.start(); osc.stop(audioCtx.currentTime + 0.3);
                        }}, idx * 100);
                    }});
                }}

                function finishSong() {{
                    document.getElementById('result-overlay').style.display = 'flex';
                    document.getElementById('result-score').innerText = Math.round(score) + " 점";
                    playFanfare();
                    playApplause();
                    for(let i=0; i<80; i++) {{
                        particles.push({{
                            x: canvas.width / 2, y: canvas.height / 2,
                            vx: (Math.random() - 0.5) * 12,
                            vy: (Math.random() - 0.5) * 12,
                            life: 2.0, color: ["#facc15", "#ec4899", "#38bdf8", "#4ade80"][Math.floor(Math.random()*4)]
                        }});
                    }}
                }}

                function playMultiChannelMREngine() {{
                    if (!isPlaying) return;
                    const time = audioCtx.currentTime;
                    const interval = (60 / bpm) * 1000;

                    const melFreq = notes[noteIdx % notes.length] * Math.pow(2, keyOffset / 12);
                    const chordFreq = (chords[noteIdx % chords.length] / 2) * Math.pow(2, keyOffset / 12);

                    // Lead Melody
                    let melOsc = audioCtx.createOscillator();
                    let melGain = audioCtx.createGain();
                    melOsc.type = 'sawtooth';
                    melOsc.frequency.setValueAtTime(melFreq, time);
                    melGain.gain.setValueAtTime(0.18, time);
                    melGain.gain.exponentialRampToValueAtTime(0.001, time + 0.35);
                    melOsc.connect(melGain); melGain.connect(audioCtx.destination);
                    melOsc.start(time); melOsc.stop(time + 0.35);

                    // AI 보컬
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
                    if (noteIdx >= notes.length * 2) {{
                        finishSong();
                    }} else {{
                        setTimeout(playMultiChannelMREngine, interval);
                    }}
                }}

                function detectMicPitch() {{
                    if (aiSinging) {{
                        let currentTargetFreq = notes[(noteIdx - 1 + notes.length) % notes.length] * Math.pow(2, keyOffset / 12);
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

                function
