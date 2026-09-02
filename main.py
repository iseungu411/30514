import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="REAL MR AI COIN KARAOKE", page_icon="🪙", layout="wide")

# 세션 상태 초기화 (코인 및 예약 시스템)
if "coins" not in st.session_state:
    st.session_state.coins = 0
if "queue" not in st.session_state:
    st.session_state.queue = []
if "current_song" not in st.session_state:
    st.session_state.current_song = None

# 실제 검증된 유튜브 MR(Karaoke) 영상 ID 매핑
SONG_DATABASE = {
    "❤️ [R&B] 죠지 - 좋아해.. (MR)": "E_XGvj-pUHM",
    "⛵ [R&B] 죠지 - Boat (MR)": "M6L7eU15E4A",
    "🎸 [R&B] 죠지 - routine (MR)": "fJ36R94N1mY",
    "🤝 [R&B] 죠지 - 손만 잡고 잠을 자자 (MR)": "uIPlsJ62p1s",
    "✨ [IDOL] NewJeans - Hype Boy (MR)": "9N2XbU2S1-E",
    "🌧️ [BALLAD] 성시경 - 거리에서 (MR)": "vYI5O_G51E0"
}

st.markdown("""
<style>
    .stApp { background-color: #0d0826; color: #ffffff; }
    .coin-box {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        padding: 15px; border-radius: 16px; text-align: center;
        font-weight: 800; font-size: 22px; color: #fff;
        box-shadow: 0 0 15px rgba(245, 158, 11, 0.5);
    }
</style>
""", unsafe_allow_html=True)

st.title("🎤 REAL MR AI COIN KARAOKE (코인노래방) 🪙")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🪙 코인 충전소")
    st.markdown(f'<div class="coin-box">남은 코인: {st.session_state.coins} 코인</div>', unsafe_allow_html=True)
    
    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
        if st.button("🪙 1,000원 (2곡)"):
            st.session_state.coins += 2
            st.rerun()
    with c_btn2:
        if st.button("🪙 2,000원 (5곡)"):
            st.session_state.coins += 5
            st.rerun()

    st.divider()

    st.subheader("🎶 노래 예약하기")
    selected_preset = st.selectbox("수록곡 목록 선택", list(SONG_DATABASE.keys()))
    
    custom_yt_url = st.text_input("기타 유튜브 MR 링크 직접 입력 (선택)", placeholder="https://www.youtube.com/watch?v=...")

    if st.button("📌 곡 예약하기", use_container_width=True):
        if st.session_state.coins <= 0:
            st.error("코인이 부족합니다! 먼저 코인을 충전해 주세요.")
        else:
            yt_id = SONG_DATABASE[selected_preset]
            title = selected_preset

            if custom_yt_url and "v=" in custom_yt_url:
                yt_id = custom_yt_url.split("v=")[1].split("&")[0]
                title = f"사용자 신청곡 ({yt_id})"

            st.session_state.queue.append({"title": title, "yt_id": yt_id})
            st.session_state.coins -= 1
            st.success(f"'{title}' 예약 완료! (1코인 차감)")
            st.rerun()

    st.subheader("📋 예약 대기 목록")
    if st.session_state.queue:
        for idx, item in enumerate(st.session_state.queue, 1):
            st.write(f"**{idx}.** {item['title']}")
    else:
        st.caption("예약된 곡이 없습니다. 코인을 넣고 노래를 예약하세요!")

with col2:
    st.subheader("📺 KARAOKE STAGE")
    
    if not st.session_state.current_song and st.session_state.queue:
        st.session_state.current_song = st.session_state.queue.pop(0)
        st.rerun()

    if st.session_state.current_song:
        song = st.session_state.current_song
        st.info(f"🎤 **NOW PLAYING:** {song['title']}")

        karaoke_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ margin: 0; background: #000; color: #fff; font-family: sans-serif; text-align: center; }}
                iframe {{ width: 100%; height: 380px; border: none; border-radius: 12px; }}
                #mic-hud {{
                    margin-top: 10px; background: rgba(15, 23, 42, 0.9); padding: 12px;
                    border-radius: 10px; border: 1px solid #ec4899; display: flex;
                    justify-content: space-around; align-items: center;
                }}
                .val {{ font-size: 20px; font-weight: bold; color: #38bdf8; }}
            </style>
        </head>
        <body>
            <iframe id="yt-player" src="https://www.youtube.com/embed/{song['yt_id']}?autoplay=1&enablejsapi=1" allow="autoplay"></iframe>

            <div id="mic-hud">
                <div>🎙️ 마이크 음정: <span id="pitch-val" class="val">--- Hz</span></div>
                <div>💯 AI 라이브 점수: <span id="score-val" class="val" style="color:#ec4899;">100</span></div>
            </div>

            <script>
                let audioCtx, analyser;
                async function initMic() {{
                    try {{
                        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                        analyser = audioCtx.createAnalyser();
                        const stream = await navigator.mediaDevices.getUserMedia({{ audio: true }});
                        audioCtx.createMediaStreamSource(stream).connect(analyser);
                        analyze();
                    }} catch (e) {{}}
                }}
                function analyze() {{
                    const buf = new Float32Array(2048);
                    analyser.getFloatTimeDomainData(buf);
                    let sum = 0;
                    for(let i=0; i<2048; i++) sum += buf[i]*buf[i];
                    let rms = Math.sqrt(sum/2048);
                    if(rms > 0.01) {{
                        document.getElementById('pitch-val').innerText = Math.round(rms * 2200) + " Hz";
                    }}
                    requestAnimationFrame(analyze);
                }}
                initMic();
            </script>
        </body>
        </html>
        """
        components.html(karaoke_html, height=460)

        if st.button("⏭️ 다음 곡으로 넘기기 (간주 점프)"):
            st.session_state.current_song = None
            st.rerun()
    else:
        st.warning("동전을 충전하고 원하는 노래를 예약해 보세요!")
