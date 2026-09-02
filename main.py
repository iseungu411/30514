import streamlit as st
import streamlit.components.v1 as components
import time

st.set_page_config(page_title="TJ PERFECT SCORE REAL MR KARAOKE", page_icon="🎤", layout="wide")

# 세션 상태 초기화
if "coins" not in st.session_state:
    st.session_state.coins = 10
if "queue" not in st.session_state:
    st.session_state.queue = []
if "current_song" not in st.session_state:
    st.session_state.current_song = None

# 유튜브 오피셜 TJ/금영 노래방 MR 비디오 ID 데이터베이스
SONG_DATABASE = {
    "🐻 [동요] 곰 세 마리 (TJ 1001)": {
        "tj_num": "1001",
        "yt_id": "5q3c4lR8y_A", # 곰 세 마리 MR
        "bpm": 120
    },
    "✈️ [동요] 비행기 (TJ 1002)": {
        "tj_num": "1002",
        "yt_id": "W9R8KThqK6g", # 비행기 MR
        "bpm": 125
    },
    "⭐ [동요] 작은 별 (TJ 1003)": {
        "tj_num": "1003",
        "yt_id": "u4_3tH5aT1g", # 작은 별 MR
        "bpm": 105
    },
    "🔔 [동요] 학교 종 (TJ 1004)": {
        "tj_num": "1004",
        "yt_id": "KqGZ4Qd2-44", # 학교 종 MR
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

st.title("👑 ✨ TJ REAL MR PERFECT SCORE KARAOKE ✨ 👑")
st.caption("실제 오피셜 노래방 MR 영상 연동 & 퍼펙트스코어 2D 시뮬레이터")

col_left, col_right = st.columns([1.1, 2])

# 1. 알바센터 및 예약 시스템
with col_left:
    st.subheader("💰 코인노래방 알바센터")
    st.markdown(f'<div class="coin-badge">✨ 보유 코인: {st.session_state.coins} 코인 ✨</div>', unsafe_allow_html=True)
    st.write("")
    
    t1, t2, t3 = st.tabs(["🧹 방 청소", "🥤 음료 채우기", "🛎️ 잔돈 계산"])
    
    with t1:
        st.write("**3번 방 마이크 소독 및 청소**")
        if st.button("🧹 방 청소 완료 (+1코인)", use_container_width=True):
            with st.spinner("소독제 뿌리는 중... ✨"):
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
                "yt_id": song_data["yt_id"]
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

# 2. 리얼 MR 노래방 모니터
with col_right:
    st.subheader("📺 TJ 오피셜 MR & 퍼펙트스코어 메인 화면")

    if not st.session_state.current_song and st.session_state.queue:
        st.session_state.current_song = st.session_state.queue.pop(0)
        st.rerun()

    if st.session_state.current_song:
        song = st.session_state.current_song
        st.info(f"🎤 **NOW PLAYING:** {song['title']} (TJ 번호: {song['tj_num']})")

        real_mr_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                * {{ box-sizing: border-box; margin: 0; padding: 0; }}
                body {{ background: #000; color: #fff; font-family: sans-serif; overflow: hidden; }}
                #stage {{
                    position: relative; width: 100%; height: 380px;
                    border: 3px solid #ec4899; border-radius: 16px; overflow: hidden;
                    box-shadow: 0 0 30px rgba(236, 72, 153, 0.6);
                    background: #000;
                }}
                iframe {{
                    width: 100%; height: 100%; border: none;
                    pointer-events: auto;
                }}
                #score-overlay {{
                    position: absolute; top: 10px; right: 10px;
                    background: rgba(15, 23, 42, 0.85); padding: 10px 16px;
                    border-radius: 12px; border: 1px solid #38bdf8; text-align: right;
                    pointer-events: none; z-index: 5;
                }}
                .val {{ font-size: 20px; font-weight: 900; color: #38bdf8; }}
                #judge-box {{
                    position: absolute; top: 15px; left: 20px;
                    font-size: 38px; font-weight: 900; color: #facc15;
                    text-shadow: 0 0 20px #facc15; pointer-events: none; z-index: 5;
                }}
                canvas {{
                    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                    pointer-events: none; z-index: 4;
                }}
                #result-overlay {{
                    position: absolute; top:0; left:0; width:100%; height:100%;
                    background: rgba(0,0,0,0.9); display: none; flex-direction: column;
                    justify-content: center; align-items: center; z-index: 10;
                }}
                #result-score {{
                    font-size: 70px; font-weight: 900; color: #facc15;
                    text-shadow: 0 0 30px #facc15;
                }}
                .controls {{
                    background: #0d0826; padding: 12px; border-radius: 12px;
                    border: 1px solid #6366f1; margin-top: 10px; text-align: center;
                    display: flex; gap: 8px; justify-content: center;
                }}
                button {{
                    background: linear-gradient(135deg, #ec4899, #a855f7);
                    color: #fff; border: none; padding: 10px 20px;
                    font-weight: bold; font-size: 16px; border-radius: 8px; cursor: pointer;
                    box-shadow: 0 0 12px rgba(236, 72, 153, 0.5);
                }}
            </style>
        </head>
        <body>
            <div id="stage">
                <div id="judge-box">PERFECT!</div>
                <div id="score-overlay">
                    <div>🎙️ PITCH: <span id="pitch-val" class="val">--- Hz</span></div>
                    <div>🎯 SCORE: <span id="score-val" class="val" style="color:#ec4899;">100.0</span></div>
                </div>

                <iframe id="yt-player" src="https://www.youtube.com/embed/{song['yt_id']}?enablejsapi=1&autoplay=1&controls=1" allow="autoplay"></iframe>

                <canvas id="tjCanvas"></canvas>

                <div id="result-overlay">
                    <div style="font-size:28px; color:#38bdf8; font-weight:bold;">🎉 가창 완료! 점수 발표 🎉</div>
                    <div id="result-score">100 점</div>
                    <div style="font-size:22px; color:#4ade80; margin-top:10px;">🏆 완벽한 100점 만점입니다! 🏆</div>
                </div>
            </div>

            <div class="controls">
                <button onclick="startMic()">🎙️ 실시간 마이크 평가 시작</button>
                <button onclick="playApplause()">👏 환호 박수</button>
                <button style="background:#ef4444;" onclick="finishSong()">🏁 점수 발표 (100점)</button>
            </div>

            <script>
                const canvas = document.getElementById('tjCanvas');
                const ctx = canvas.getContext('2d');
                canvas.width = canvas.offsetWidth;
                canvas.height = canvas.offsetHeight;

                let audioCtx, analyser;
                let particles = [], scanX = 0, score = 100.0;

                async function startMic() {{
                    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                    try {{
                        analyser = audioCtx.createAnalyser();
                        analyser.fftSize = 2048;
                        const stream = await navigator.mediaDevices.getUserMedia({{ audio: true }});
                        audioCtx.createMediaStreamSource(stream).connect(analyser);
                    }} catch(e) {{}}
                }}

                function playApplause() {{
                    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                    for(let i=0; i<20; i++) {{
                        setTimeout(() => {{
                            let osc = audioCtx.createOscillator();
                            let gain = audioCtx.createGain();
                            osc.type = 'sine';
                            osc.frequency.setValueAtTime(400 + Math.random()*800, audioCtx.currentTime);
                            gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
                            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.1);
                            osc.connect(gain); gain.connect(audioCtx.destination);
                            osc.start(); osc.stop(audioCtx.currentTime + 0.1);
                        }}, i * 35);
                    }}
                }}

                function finishSong() {{
                    document.getElementById('result-overlay').style.display = 'flex';
                    playApplause();
                    for(let i=0; i<100; i++) {{
                        particles.push({{
                            x: canvas.width / 2, y: canvas.height / 2,
                            vx: (Math.random() - 0.5) * 12,
                            vy: (Math.random() - 0.5) * 12,
                            life: 2.0, color: ["#facc15", "#ec4899", "#38bdf8", "#4ade80"][Math.floor(Math.random()*4)]
                        }});
                    }}
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

                function drawEffects() {{
                    ctx.clearRect(0, 0, canvas.width, canvas.height);

                    // 스캐너 오버레이 라인
                    ctx.strokeStyle = "rgba(244, 63, 94, 0.8)";
                    ctx.lineWidth = 2;
                    ctx.beginPath();
                    ctx.moveTo(scanX, 0); ctx.lineTo(scanX, canvas.height);
                    ctx.stroke();

                    let pitch = detectMicPitch();
                    if(pitch > 0) {{
                        document.getElementById('pitch-val').innerText = Math.round(pitch) + " Hz";
                        for(let i=0; i<2; i++) {{
                            particles.push({{
                                x: scanX, y: canvas.height / 2 + (Math.random() - 0.5) * 80,
                                vx: (Math.random() - 0.5) * 3, vy: (Math.random() - 0.5) * 3,
                                life: 1.0, color: "#ec4899"
                            }});
                        }}
                    }}

                    // 파티클 그리기
                    for(let i=particles.length-1; i>=0; i--) {{
                        let p = particles[i];
                        p.x += p.vx; p.y += p.vy; p.life -= 0.02;
                        if(p.life <= 0) particles.splice(i, 1);
                        else {{
                            ctx.fillStyle = p.color;
                            ctx.globalAlpha = p.life;
                            ctx.fillRect(p.x, p.y, 5, 5);
                            ctx.globalAlpha = 1.0;
                        }}
                    }}

                    scanX = (scanX + 2) % canvas.width;
                    requestAnimationFrame(drawEffects);
                }}

                drawEffects();
            </script>
        </body>
        </html>
        """
        components.html(real_mr_html, height=480)

        st.write("")
        if st.button("⏭️ 다음 곡으로 넘기기", use_container_width=True):
            st.session_state.current_song = None
            st.rerun()
    else:
        st.warning("👈 왼쪽에 코인을 번 후 동요를 예약해 보세요!")
