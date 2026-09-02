import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="REAL SOUND AI KARAOKE", page_icon="🎤", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #030014; color: #ffffff; }
    .title-container {
        text-align: center;
        padding: 16px;
        background: rgba(15, 12, 41, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(236, 72, 153, 0.4);
        box-shadow: 0 0 20px rgba(236, 72, 153, 0.2);
        margin-bottom: 12px;
    }
    .title-text {
        font-size: 26px;
        font-weight: 800;
        background: linear-gradient(90deg, #a855f7, #ec4899, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
<div class="title-container">
    <div class="title-text">🎤 MULTI-GENRE REAL SOUND AI KARAOKE STAGE 🎤</div>
    <p style="color: #94a3b8; margin-top: 4px; font-size: 14px;">죠지의 다양한 명곡과 최신 트랙이 추가되었습니다. MR 반주와 함께 AI 음정 분석을 시작해보세요!</p>
</div>
""", unsafe_allow_html=True)

real_karaoke_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;900&family=Noto+Sans+KR:wght@500;800&display=swap');

        * { box-sizing: border-box; }
        body { margin: 0; overflow: hidden; background: #030014; font-family: 'Noto Sans KR', sans-serif; }
        canvas { width: 100vw; height: 100vh; display: block; }

        #ui-layer {
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 16px;
            z-index: 10;
        }

        .select-box {
            background: rgba(15, 23, 42, 0.85);
            color: #38bdf8;
            border: 2px solid #06b6d4;
            padding: 10px 20px;
            border-radius: 30px;
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 14px;
            font-weight: bold;
            outline: none;
            cursor: pointer;
            box-shadow: 0 0 15px rgba(6, 182, 212, 0.4);
            backdrop-filter: blur(8px);
        }

        .btn {
            background: linear-gradient(135deg, #ec4899, #8b5cf6);
            color: white;
            border: none;
            padding: 10px 26px;
            border-radius: 30px;
            font-family: 'Orbitron', sans-serif;
            font-weight: 900;
            font-size: 14px;
            cursor: pointer;
            box-shadow: 0 0 20px rgba(236, 72, 153, 0.6);
            transition: all 0.3s ease;
        }
        .btn:hover {
            transform: scale(1.08);
            box-shadow: 0 0 30px rgba(236, 72, 153, 0.9);
        }

        #pitch-hud {
            position: absolute;
            top: 20px;
            right: 25px;
            background: rgba(15, 23, 42, 0.8);
            border: 2px solid rgba(168, 85, 247, 0.6);
            padding: 14px 22px;
            border-radius: 20px;
            color: #fff;
            text-align: center;
            z-index: 10;
            min-width: 160px;
            backdrop-filter: blur(12px);
            box-shadow: 0 0 25px rgba(168, 85, 247, 0.3);
        }
        .hud-title { font-size: 11px; color: #cbd5e1; font-family: 'Orbitron', sans-serif; letter-spacing: 1px; }
        .hud-val { font-size: 24px; font-weight: 900; color: #38bdf8; font-family: 'Orbitron', sans-serif; text-shadow: 0 0 10px #38bdf8; }

        #lyrics-box {
            position: absolute;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            width: 88%;
            max-width: 850px;
            background: rgba(15, 12, 41, 0.9);
            border: 2px solid rgba(236, 72, 153, 0.7);
            border-radius: 24px;
            padding: 20px 30px;
            text-align: center;
            box-shadow: 0 0 35px rgba(236, 72, 153, 0.35);
            backdrop-filter: blur(15px);
            z-index: 10;
        }

        .lyric-title {
            font-size: 14px;
            color: #38bdf8;
            font-weight: 800;
            margin-bottom: 4px;
        }

        .lyric-cur {
            font-size: 28px;
            font-weight: 800;
            background: linear-gradient(90deg, #f43f5e, #facc15, #38bdf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
            filter: drop-shadow(0 0 12px rgba(250, 204, 21, 0.6));
        }

        .lyric-next { font-size: 17px; color: #94a3b8; font-weight: 500; }

        #ai-feedback {
            font-size: 16px;
            font-weight: 800;
            margin-top: 10px;
            color: #facc15;
            min-height: 24px;
            letter-spacing: 1px;
            text-shadow: 0 0 10px rgba(250, 204, 21, 0.5);
        }

        #modal {
            position: absolute;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(3, 0, 20, 0.94);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 100;
            display: none;
            backdrop-filter: blur(20px);
        }
        #modal h1 { font-size: 64px; color: #facc15; margin: 0; font-family: 'Orbitron', sans-serif; text-shadow: 0 0 30px #facc15; }
        #modal p { font-size: 22px; color: #e2e8f0; margin-top: 15px; text-align: center; max-width: 600px; line-height: 1.5; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

<div id="ui-layer">
    <select id="song-select" class="select-box">
        <option value="0">🎸 [R&B] 죠지 - routine</option>
        <option value="1">🤝 [R&B] 죠지 - 손만 잡고 잠을 자자</option>
        <option value="2">❤️ [R&B] 죠지 - 좋아해..</option>
        <option value="3">⛵ [R&B] 죠지 - Boat</option>
        <option value="4">✨ [IDOL] NewJeans - Hype Boy</option>
        <option value="5">🌧️ [BALLAD] 성시경 - 거리에서</option>
    </select>
    <button class="btn" onclick="initAudioAndStart()">🎤 예약 및 노래 시작 (MR 재생)</button>
</div>

<div id="pitch-hud">
    <div class="hud-title">USER PITCH</div>
    <div id="user-pitch" class="hud-val">--- Hz</div>
    <div class="hud-title" style="margin-top:8px;">AI SCORE</div>
    <div id="live-score" class="hud-val" style="color:#ec4899; text-shadow: 0 0 10px #ec4899;">100</div>
</div>

<div id="lyrics-box">
    <div id="song-label" class="lyric-title">선곡 대기 중</div>
    <div id="cur-lyric" class="lyric-cur">노래 시작 버튼을 누르면 MR 반주와 함께 가사가 나옵니다</div>
    <div id="next-lyric" class="lyric-next">마이크로 직접 노래를 따라 불러보세요!</div>
    <div id="ai-feedback">READY FOR STAGE</div>
</div>

<div id="modal">
    <h1 id="final-score">98 PTS</h1>
    <p id="final-eval">AI EVALUATION: 완벽한 박자감과 우수한 가창 음정을 보여주셨습니다!</p>
    <button class="btn" style="margin-top:25px;" onclick="closeModal()">다른 노래 부르기 🔄</button>
</div>

<script>
    const songDB = [
        {
            title: "죠지 - routine",
            bpm: 88,
            notes: [
                { time: 0.0, lyric: "반복되는 하루 속에서", next: "너를 생각하는 게 내 루틴이야", freq: 329.63, chord: [130.81, 164.81, 196.00] },
                { time: 2.2, lyric: "너를 생각하는 게 내 루틴이야", next: "아침에 눈을 떠 제일 먼저 너를 찾아", freq: 293.66, chord: [146.83, 174.61, 220.00] },
                { time: 4.8, lyric: "아침에 눈을 떠 제일 먼저 너를 찾아", next: "익숙해진 이 마음이 좋아", freq: 349.23, chord: [174.61, 220.00, 261.63] },
                { time: 7.2, lyric: "익숙해진 이 마음이 좋아", next: "FINISH", freq: 392.00, chord: [196.00, 246.94, 293.66] }
            ]
        },
        {
            title: "죠지 - 손만 잡고 잠을 자자",
            bpm: 85,
            notes: [
                { time: 0.0, lyric: "아무 걱정 하지 말고 내게 와", next: "오늘 밤은 그냥 편히 쉬어가", freq: 261.63, chord: [130.81, 164.81, 196.00] },
                { time: 2.5, lyric: "오늘 밤은 그냥 편히 쉬어가", next: "불을 끄고 조용히 눈을 감아봐", freq: 293.66, chord: [146.83, 174.61, 220.00] },
                { time: 5.0, lyric: "불을 끄고 조용히 눈을 감아봐", next: "손만 잡고 잠을 자자", freq: 329.63, chord: [164.81, 196.00, 246.94] },
                { time: 7.5, lyric: "손만 잡고 잠을 자자", next: "FINISH", freq: 349.23, chord: [174.61, 220.00, 261.63] }
            ]
        },
        {
            title: "죠지 - 좋아해..",
            bpm: 80,
            notes: [
                { time: 0.0, lyric: "왜 네 앞에서는 다 어색해지고", next: "꽤 자연스럽던 내 인사마저도", freq: 293.66, chord: [146.83, 174.61, 220.00] },
                { time: 2.5, lyric: "꽤 자연스럽던 내 인사마저도", next: "마음대로 되지가 않아", freq: 329.63, chord: [164.81, 196.00, 246.94] },
                { time: 5.0, lyric: "마음대로 되지가 않아", next: "그저 웃어주는 널 바라보면", freq: 261.63, chord: [130.81, 164.81, 196.00] },
                { time: 7.2, lyric: "그저 웃어주는 널 바라보면", next: "아무 이유 없이 행복해져", freq: 293.66, chord: [146.83, 174.61, 220.00] },
                { time: 9.5, lyric: "아무 이유 없이 행복해져", next: "널 좋아한다 말하고 집에 돌아가는 길에", freq: 329.63, chord: [164.81, 196.00, 246.94] },
                { time: 12.0, lyric: "널 좋아한다 말하고 집에 돌아가는 길에", next: "너의 얼굴이 자꾸 떠올라", freq: 349.23, chord: [174.61, 220.00, 261.63] },
                { time: 14.8, lyric: "너의 얼굴이 자꾸 떠올라", next: "나도 몰래 설레였어", freq: 329.63, chord: [164.81, 196.00, 246.94] },
                { time: 16.8, lyric: "나도 몰래 설레였어", next: "FINISH", freq: 293.66, chord: [146.83, 174.61, 220.00] }
            ]
        },
        {
            title: "죠지 - Boat",
            bpm: 95,
            notes: [
                { time: 0.0, lyric: "I'm on a boat", next: "눈에 보이는 사방이 바다야", freq: 329.63, chord: [130.81, 164.81, 196.00] },
                { time: 1.5, lyric: "눈에 보이는 사방이 바다야", next: "갓 잡아 올린 생선을 회 쳐서 먹어", freq: 293.66, chord: [146.83, 174.61, 220.00] },
                { time: 3.5, lyric: "갓 잡아 올린 생선을", next: "회 쳐서 먹어", freq: 329.63, chord: [164.81, 196.00, 246.94] },
                { time: 5.0, lyric: "회 쳐서 먹어", next: "I'm on a boat 멀어지는 도시", freq: 349.23, chord: [174.61, 220.00, 261.63] },
                { time: 6.8, lyric: "I'm on a boat", next: "멀어지는 도시", freq: 329.63, chord: [130.81, 164.81, 196.00] },
                { time: 8.2, lyric: "멀어지는 도시", next: "We're going on 어딘가로 멀리멀리", freq: 293.66, chord: [146.83, 174.61, 220.00] },
                { time: 10.0, lyric: "We're going on", next: "어딘가로 멀리멀리", freq: 329.63, chord: [164.81, 196.00, 246.94] },
                { time: 11.5, lyric: "어딘가로 멀리멀리", next: "FINISH", freq: 392.00, chord: [196.00, 246.94, 293.66] }
            ]
        },
        {
            title: "NewJeans - Hype Boy",
            bpm: 115,
            notes: [
                { time: 0.0, lyric: "Cause I know what you like boy", next: "You're my chemical hype boy", freq: 440.00, chord: [220.00, 261.63, 329.63] },
                { time: 1.8, lyric: "You're my chemical hype boy", next: "내 깊은 서랍 속에 넣어둔", freq: 392.00, chord: [196.00, 246.94, 293.66] },
                { time: 3.6, lyric: "내 깊은 서랍 속에 넣어둔", next: "너를 향한 내 마음을 꺼내볼 때", freq: 349.23, chord: [174.61, 220.00, 261.63] },
                { time: 5.4, lyric: "너를 향한 내 마음을 꺼내볼 때", next: "Take the party going on!", freq: 329.63, chord: [164.81, 196.00, 246.94] },
                { time: 7.2, lyric: "Take the party going on!", next: "FINISH", freq: 440.00, chord: [220.00, 277.18, 329.63] }
            ]
        },
        {
            title: "성시경 - 거리에서",
            bpm: 72,
            notes: [
                { time: 0.0, lyric: "널 기달리는 동안", next: "나에게 올 수 없을 걸 알면서", freq: 261.63, chord: [130.81, 164.81, 196.00] },
                { time: 2.2, lyric: "나에게 올 수 없을 걸 알면서", next: "그리운 너의 이름을 불러본다", freq: 293.66, chord: [146.83, 174.61, 220.00] },
                { time: 4.8, lyric: "그리운 너의 이름을 불러본다", next: "스쳐 가는 사람 속에", freq: 329.63, chord: [164.81, 196.00, 246.94] },
                { time: 7.2, lyric: "스쳐 가는 사람 속에", next: "FINISH", freq: 349.23, chord: [174.61, 220.00, 261.63] }
            ]
        }
    ];

    let audioCtx = null;
    let analyser = null;
    let micStream = null;
    let isMicActive = false;

    async function setupMicrophone() {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        analyser = audioCtx.createAnalyser();
        analyser.fftSize = 2048;

        try {
            micStream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const source = audioCtx.createMediaStreamSource(micStream);
            source.connect(analyser);
            isMicActive = true;
        } catch (err) {
            alert("마이크 연결 실패: 브라우저 마이크 접근을 허용해야 합니다.");
        }
    }

    function autoCorrelate(buf, sampleRate) {
        let SIZE = buf.length;
        let rms = 0;
        for (let i = 0; i < SIZE; i++) rms += buf[i] * buf[i];
        rms = Math.sqrt(rms / SIZE);
        if (rms < 0.012) return -1;

        let r1 = 0, r2 = SIZE - 1, thres = 0.2;
        for (let i = 0; i < SIZE / 2; i++) {
            if (Math.abs(buf[i]) < thres) { r1 = i; break; }
        }
        for (let i = 1; i < SIZE / 2; i++) {
            if (Math.abs(buf[SIZE - i]) < thres) { r2 = SIZE - i; break; }
        }

        buf = buf.slice(r1, r2);
        SIZE = buf.length;

        let c = new Array(SIZE).fill(0);
        for (let i = 0; i < SIZE; i++) {
            for (let j = 0; j < SIZE - i; j++) c[i] += buf[j] * buf[j + i];
        }

        let d = 0; while (c[d] > c[d + 1]) d++;
        let maxval = -1, maxpos = -1;
        for (let i = d; i < SIZE; i++) {
            if (c[i] > maxval) { maxval = c[i]; maxpos = i; }
        }
        return sampleRate / maxpos;
    }

    function playMRChordAndBass(chordArray, melodyFreq) {
        if (!audioCtx) return;
        
        chordArray.forEach(freq => {
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
            gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 1.2);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + 1.2);
        });

        const guideOsc = audioCtx.createOscillator();
        const guideGain = audioCtx.createGain();
        guideOsc.type = 'sine';
        guideOsc.frequency.setValueAtTime(melodyFreq, audioCtx.currentTime);
        guideGain.gain.setValueAtTime(0.12, audioCtx.currentTime);
        guideGain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.8);
        guideOsc.connect(guideGain);
        guideGain.connect(audioCtx.destination);
        guideOsc.start();
        guideOsc.stop(audioCtx.currentTime + 0.8);
    }

    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x030014, 0.05);

    const camera = new THREE.PerspectiveCamera(65, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 3, 10);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    document.body.appendChild(renderer.domElement);

    scene.add(new THREE.AmbientLight(0xffffff, 0.8));

    const coreGroup = new THREE.Group();
    const coreGeo = new THREE.IcosahedronGeometry(1.5, 2);
    const coreMat = new THREE.MeshStandardMaterial({
        color: 0xec4899,
        wireframe: true,
        emissive: 0x38bdf8,
        emissiveIntensity: 0.8
    });
    const coreMesh = new THREE.Mesh(coreGeo, coreMat);
    coreGroup.add(coreMesh);
    scene.add(coreGroup);

    const bars = [];
    const barCount = 32;
    const radius = 5.5;

    for (let i = 0; i < barCount; i++) {
        const angle = (i / barCount) * Math.PI * 2;
        const geo = new THREE.CylinderGeometry(0.12, 0.12, 2, 16);
        const color = new THREE.Color();
        color.setHSL(i / barCount, 0.9, 0.6);
        
        const mat = new THREE.MeshStandardMaterial({ color: color, emissive: color, emissiveIntensity: 0.6 });
        const mesh = new THREE.Mesh(geo, mat);
        mesh.position.set(Math.cos(angle) * radius, 0, Math.sin(angle) * radius - 2);
        scene.add(mesh);
        bars.push(mesh);
    }

    let isPlaying = false;
    let currentSong = null;
    let startTime = 0;
    let noteIdx = 0;
    let currentScore = 100;
    let totalDeductions = 0;

    async function initAudioAndStart() {
        if (!isMicActive) await setupMicrophone();
        const songIdx = document.getElementById('song-select').value;
        currentSong = songDB[songIdx];

        document.getElementById('song-label').innerText = "NOW PLAYING: " + currentSong.title;

        isPlaying = true;
        noteIdx = 0;
        currentScore = 100;
        totalDeductions = 0;
        startTime = Date.now();
    }

    function animate() {
        requestAnimationFrame(animate);

        coreGroup.rotation.y += 0.01;
        coreGroup.rotation.x += 0.005;

        if (isMicActive && analyser) {
            const buffer = new Float32Array(analyser.fftSize);
            analyser.getFloatTimeDomainData(buffer);
            const userPitch = autoCorrelate(buffer, audioCtx.sampleRate);

            for (let i = 0; i < bars.length; i++) {
                const val = Math.abs(buffer[i * 8] || 0) * 12 + 0.3;
                bars[i].scale.y = val;
            }

            if (userPitch > 0) {
                document.getElementById('user-pitch').innerText = Math.round(userPitch) + " Hz";
            } else {
                document.getElementById('user-pitch').innerText = "--- Hz";
            }

            if (isPlaying && currentSong && noteIdx < currentSong.notes.length) {
                const targetFreq = currentSong.notes[noteIdx].freq;
                if (userPitch > 0) {
                    const diff = Math.abs(userPitch - targetFreq);
                    if (diff < 25) {
                        document.getElementById('ai-feedback').innerText = "🔥 PERFECT! 완벽한 음정입니다!";
                        document.getElementById('ai-feedback').style.color = "#34d399";
                    } else if (diff < 50) {
                        document.getElementById('ai-feedback').innerText = "✨ GOOD! 감미로운 음색입니다.";
                        document.getElementById('ai-feedback').style.color = "#facc15";
                    } else {
                        document.getElementById('ai-feedback').innerText = "⚡ MISS! 음정이 벗어났습니다.";
                        document.getElementById('ai-feedback').style.color = "#f43f5e";
                        totalDeductions += 0.25;
                    }

                    currentScore = Math.max(50, Math.round(100 - totalDeductions));
                    document.getElementById('live-score').innerText = currentScore;
                }
            }
        }

        if (isPlaying && currentSong) {
            const elapsed = (Date.now() - startTime) / 1000;
            if (noteIdx < currentSong.notes.length) {
                const note = currentSong.notes[noteIdx];
                if (elapsed >= note.time) {
                    playMRChordAndBass(note.chord, note.freq);
                    document.getElementById('cur-lyric').innerText = note.lyric;
                    document.getElementById('next-lyric').innerText = "NEXT: " + (note.next || "");
                    noteIdx++;
                }
            } else if (elapsed > currentSong.notes[currentSong.notes.length - 1].time + 2.5) {
                isPlaying = false;
                showModal();
            }
        }

        renderer.render(scene, camera);
    }

    function showModal() {
        document.getElementById('modal').style.display = 'flex';
        document.getElementById('final-score').innerText = currentScore + " PTS";
        document.getElementById('final-eval').innerText = "AI 종합 평가: 죠지 특유의 감성을 훌륭하게 살린 가창이었습니다!";
    }

    window.closeModal = function() {
        document.getElementById('modal').style.display = 'none';
        document.getElementById('cur-lyric').innerText = "노래 시작 버튼을 누르면 MR 반주와 함께 가사가 나옵니다";
    };

    window.initAudioAndStart = initAudioAndStart;
    animate();
</script>
</body>
</html>
"""

components.html(real_karaoke_html, height=660)
