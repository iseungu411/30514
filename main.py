import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="CYBER AI KARAOKE", page_icon="🎤", layout="wide")

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
    <div class="title-text">✨ CYBERPUNK AI VOICE KARAOKE STAGE ✨</div>
    <p style="color: #94a3b8; margin-top: 4px; font-size: 14px;">화려한 네온 무대 위에서 실제 마이크로 노래를 부르고 AI 음정 평가를 받아보세요!</p>
</div>
""", unsafe_allow_html=True)

# 2. 사이버펑크 3D 비주얼라이저 & AI 노래방 HTML
cyber_karaoke_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;900&family=Noto+Sans+KR:wght@500;800&display=swap');

        * { box-sizing: border-box; }
        body { margin: 0; overflow: hidden; background: #030014; font-family: 'Noto Sans KR', sans-serif; }
        canvas { width: 100vw; height: 100vh; display: block; }

        /* 컨트롤 상단바 */
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
            background: rgba(15, 23, 42, 0.8);
            color: #38bdf8;
            border: 2px solid #06b6d4;
            padding: 10px 20px;
            border-radius: 30px;
            font-family: 'Orbitron', sans-serif;
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

        /* 실시간 음정 / 점수 네온 패널 */
        #pitch-hud {
            position: absolute;
            top: 20px;
            right: 25px;
            background: rgba(15, 23, 42, 0.75);
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

        /* 중앙 네온 가사 디스플레이 */
        #lyrics-box {
            position: absolute;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            width: 88%;
            max-width: 850px;
            background: rgba(15, 12, 41, 0.85);
            border: 2px solid rgba(236, 72, 153, 0.7);
            border-radius: 24px;
            padding: 20px 30px;
            text-align: center;
            box-shadow: 0 0 35px rgba(236, 72, 153, 0.35);
            backdrop-filter: blur(15px);
            z-index: 10;
        }

        .lyric-cur {
            font-size: 32px;
            font-weight: 800;
            background: linear-gradient(90deg, #f43f5e, #facc15, #38bdf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
            filter: drop-shadow(0 0 12px rgba(250, 204, 21, 0.6));
        }

        .lyric-next { font-size: 18px; color: #94a3b8; font-weight: 500; }

        #ai-feedback {
            font-size: 16px;
            font-weight: 800;
            margin-top: 10px;
            color: #facc15;
            min-height: 24px;
            letter-spacing: 1px;
            text-shadow: 0 0 10px rgba(250, 204, 21, 0.5);
        }

        /* 최종 점수 모달 */
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
        <option value="0">🎵 [K-POP] 비행기 - 리믹스 ver.</option>
        <option value="1">🎵 [CLASSIC] 학교종이 울린다</option>
        <option value="2">🎵 [POP] 나비야 나비야</option>
    </select>
    <button class="btn" onclick="initAudioAndStart()">🎤 마이크 승인 & AI 스테이지 시작</button>
</div>

<div id="pitch-hud">
    <div class="hud-title">USER PITCH</div>
    <div id="user-pitch" class="hud-val">--- Hz</div>
    <div class="hud-title" style="margin-top:8px;">AI SCORE</div>
    <div id="live-score" class="hud-val" style="color:#ec4899; text-shadow: 0 0 10px #ec4899;">100</div>
</div>

<div id="lyrics-box">
    <div id="cur-lyric" class="lyric-cur">마이크 버튼을 클릭하여 콘서트 무대를 시작하세요!</div>
    <div id="next-lyric" class="lyric-next">AI가 사용자의 음성을 실시간 분석 및 수신합니다.</div>
    <div id="ai-feedback">STAGE READY</div>
</div>

<div id="modal">
    <h1 id="final-score">98 PTS</h1>
    <p id="final-eval">AI EVALUATION: 판타스틱한 음정 안정도와 완성도 높은 가창력입니다!</p>
    <button class="btn" style="margin-top:25px;" onclick="closeModal()">다시 도전하기 🔄</button>
</div>

<script>
    // 1. 곡 데이터베이스
    const songDB = [
        {
            title: "비행기",
            notes: [
                { time: 0.0, lyric: "프로펠러", next: "돌려라", freq: 329.63 },
                { time: 0.8, lyric: "프로펠러", next: "돌려라", freq: 293.66 },
                { time: 1.6, lyric: "프로펠러", next: "돌려라", freq: 261.63 },
                { time: 2.4, lyric: "프로펠러", next: "돌려라", freq: 293.66 },
                { time: 3.2, lyric: "돌려라", next: "위로 위로", freq: 329.63 },
                { time: 4.0, lyric: "돌려라", next: "위로 위로", freq: 329.63 },
                { time: 4.8, lyric: "위로 위로", next: "솟아라", freq: 293.66 },
                { time: 5.6, lyric: "위로 위로", next: "솟아라", freq: 293.66 },
                { time: 6.4, lyric: "솟아라", next: "비행기!", freq: 329.63 },
                { time: 7.2, lyric: "비행기!", next: "FINISH", freq: 392.00 }
            ]
        },
        {
            title: "학교종",
            notes: [
                { time: 0.0, lyric: "학교종이", next: "땡땡땡", freq: 392.00 },
                { time: 0.8, lyric: "학교종이", next: "땡땡땡", freq: 392.00 },
                { time: 1.6, lyric: "학교종이", next: "땡땡땡", freq: 440.00 },
                { time: 2.4, lyric: "학교종이", next: "땡땡땡", freq: 440.00 },
                { time: 3.2, lyric: "땡땡땡", next: "어서 모이자", freq: 392.00 },
                { time: 4.0, lyric: "땡땡땡", next: "어서 모이자", freq: 392.00 },
                { time: 4.8, lyric: "어서 모이자", next: "선생님이", freq: 329.63 },
                { time: 5.6, lyric: "선생님이", next: "기다리신다", freq: 293.66 }
            ]
        },
        {
            title: "나비야",
            notes: [
                { time: 0.0, lyric: "나비야", next: "나비야", freq: 392.00 },
                { time: 0.8, lyric: "나비야", next: "이리 날아오너라", freq: 329.63 },
                { time: 1.6, lyric: "이리 날아", next: "오너라", freq: 329.63 },
                { time: 2.4, lyric: "오너라", next: "노랑나비", freq: 349.23 },
                { time: 3.2, lyric: "노랑나비", next: "흰나비", freq: 293.66 },
                { time: 4.0, lyric: "흰나비", next: "춤을 추며", freq: 293.66 }
            ]
        }
    ];

    // 2. AudioContext & Pitch Detection
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
            alert("마이크 연결 실패: 브라우저 권한을 확인해주세요.");
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

    // 3. Three.js 화려한 3D 사이버 무대 연출
    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x030014, 0.05);

    const camera = new THREE.PerspectiveCamera(65, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 3, 10);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    document.body.appendChild(renderer.domElement);

    // 조명
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0xec4899, 3, 20);
    pointLight.position.set(0, 5, 0);
    scene.add(pointLight);

    // 중앙 사이버 미러볼 / 코어 링
    const coreGroup = new THREE.Group();
    const coreGeo = new THREE.IcosahedronGeometry(1.5, 2);
    const coreMat = new THREE.MeshStandardMaterial({
        color: 0x38bdf8,
        wireframe: true,
        emissive: 0x8b5cf6,
        emissiveIntensity: 0.8
    });
    const coreMesh = new THREE.Mesh(coreGeo, coreMat);
    coreGroup.add(coreMesh);
    scene.add(coreGroup);

    // 3D 네온 이퀄라이저 기둥 (32개 원형 배치)
    const bars = [];
    const barCount = 32;
    const radius = 5.5;

    for (let i = 0; i < barCount; i++) {
        const angle = (i / barCount) * Math.PI * 2;
        const geo = new THREE.CylinderGeometry(0.12, 0.12, 2, 16);
        
        // 무지개 네온 색상 계산
        const color = new THREE.Color();
        color.setHSL(i / barCount, 0.9, 0.6);
        
        const mat = new THREE.MeshStandardMaterial({
            color: color,
            emissive: color,
            emissiveIntensity: 0.6,
            roughness: 0.2
        });
        
        const mesh = new THREE.Mesh(geo, mat);
        mesh.position.set(Math.cos(angle) * radius, 0, Math.sin(angle) * radius - 2);
        scene.add(mesh);
        bars.push(mesh);
    }

    // 1000개의 우주 파티클 별빛
    const particleGeo = new THREE.BufferGeometry();
    const particleCount = 1000;
    const posArray = new Float32Array(particleCount * 3);

    for (let i = 0; i < particleCount * 3; i++) {
        posArray[i] = (Math.random() - 0.5) * 40;
    }
    particleGeo.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
    const particleMat = new THREE.PointsMaterial({
        size: 0.08,
        color: 0xf43f5e,
        transparent: true,
        opacity: 0.8
    });
    const particles = new THREE.Points(particleGeo, particleMat);
    scene.add(particles);

    // 4. 메인 애니메이션 & 게임 루프
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

        isPlaying = true;
        noteIdx = 0;
        currentScore = 100;
        totalDeductions = 0;
        startTime = Date.now();
    }

    function playMelodyNote(freq) {
        if (!audioCtx) return;
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.15, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.5);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.5);
    }

    function animate() {
        requestAnimationFrame(animate);

        // 파티클 및 중앙 코어 회전
        particles.rotation.y += 0.001;
        coreGroup.rotation.y += 0.01;
        coreGroup.rotation.x += 0.005;

        // 마이크 및 피치 처리
        if (isMicActive && analyser) {
            const buffer = new Float32Array(analyser.fftSize);
            analyser.getFloatTimeDomainData(buffer);
            const userPitch = autoCorrelate(buffer, audioCtx.sampleRate);

            // 네온 기둥 반응 애니메이션
            for (let i = 0; i < bars.length; i++) {
                const val = Math.abs(buffer[i * 8] || 0) * 12 + 0.3;
                bars[i].scale.y = val;
            }

            if (userPitch > 0) {
                document.getElementById('user-pitch').innerText = Math.round(userPitch) + " Hz";
            } else {
                document.getElementById('user-pitch').innerText = "--- Hz";
            }

            // AI 정밀 실시간 음정 채점
            if (isPlaying && currentSong && noteIdx < currentSong.notes.length) {
                const targetFreq = currentSong.notes[noteIdx].freq;
                if (userPitch > 0) {
                    const diff = Math.abs(userPitch - targetFreq);
                    if (diff < 25) {
                        document.getElementById('ai-feedback').innerText = "🔥 PERFECT! 완벽한 음정입니다!";
                        document.getElementById('ai-feedback').style.color = "#34d399";
                    } else if (diff < 50) {
                        document.getElementById('ai-feedback').innerText = "✨ GOOD! 잘하고 있어요!";
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

        // 가사 및 진행 처리
        if (isPlaying && currentSong) {
            const elapsed = (Date.now() - startTime) / 1000;
            if (noteIdx < currentSong.notes.length) {
                const note = currentSong.notes[noteIdx];
                if (elapsed >= note.time) {
                    playMelodyNote(note.freq);
                    document.getElementById('cur-lyric').innerText = note.lyric;
                    document.getElementById('next-lyric').innerText = "NEXT: " + (note.next || "");
                    noteIdx++;
                }
            } else if (elapsed > currentSong.notes[currentSong.notes.length - 1].time + 1.8) {
                isPlaying = false;
                showModal();
            }
        }

        renderer.render(scene, camera);
    }

    function showModal() {
        document.getElementById('modal').style.display = 'flex';
        document.getElementById('final-score').innerText = currentScore + " PTS";
        
        let evalText = "대단한 가창력입니다! 음정 정확도가 우수합니다.";
        if (currentScore < 80) evalText = "음정이 조금 불안정했습니다. 연습을 통해 점수를 높여보세요!";
        else if (currentScore < 92) evalText = "안정적인 실력입니다! 약간의 고음 연습을 추천합니다.";
        
        document.getElementById('final-eval').innerText = "AI 종합 평가: " + evalText;
    }

    window.closeModal = function() {
        document.getElementById('modal').style.display = 'none';
        document.getElementById('cur-lyric').innerText = "마이크 버튼을 클릭하여 콘서트 무대를 시작하세요!";
    };

    window.initAudioAndStart = initAudioAndStart;
    animate();
</script>
</body>
</html>
"""

components.html(cyber_karaoke_html, height=650)
