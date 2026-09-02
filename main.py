import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="AI Voice Karaoke System", page_icon="🎙️", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #080711; color: #ffffff; }
    .title-container {
        text-align: center;
        padding: 12px;
        background: linear-gradient(135deg, #111827, #080711);
        border-radius: 12px;
        border: 1px solid #10b981;
        margin-bottom: 10px;
    }
</style>
<div class="title-container">
    <h2>🎙️ AI 마이크 음성 분석 노래방 (실제 음정 측정)</h2>
    <p>마이크 버튼을 눌러 권한을 허용한 후, 노래를 따라 불러보세요! AI가 목소리의 음정(Pitch)을 측정하여 평가합니다.</p>
</div>
""", unsafe_allow_html=True)

# 2. AI 음성 인식 + Three.js 노래방 앱 HTML
ai_karaoke_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; background: #080711; font-family: 'Segoe UI', sans-serif; }
        canvas { width: 100vw; height: 100vh; display: block; }

        #ui-layer {
            position: absolute;
            top: 15px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 12px;
            z-index: 10;
        }

        .select-box {
            background: rgba(17, 24, 39, 0.9);
            color: #10b981;
            border: 1px solid #10b981;
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: bold;
            outline: none;
            cursor: pointer;
        }

        .btn {
            background: linear-gradient(135deg, #059669, #10b981);
            color: white;
            border: none;
            padding: 8px 20px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 14px;
            cursor: pointer;
            box-shadow: 0 0 10px rgba(16, 185, 129, 0.4);
            transition: 0.2s;
        }
        .btn:hover { transform: scale(1.05); }

        /* 음정 모니터링 HUD */
        #pitch-hud {
            position: absolute;
            top: 15px;
            right: 20px;
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid #3b82f6;
            padding: 10px 18px;
            border-radius: 12px;
            color: #fff;
            text-align: center;
            z-index: 10;
            min-width: 140px;
        }
        .hud-title { font-size: 11px; color: #94a3b8; }
        .hud-val { font-size: 20px; font-weight: bold; color: #60a5fa; }

        /* 가사 및 실시간 피드백 */
        #lyrics-box {
            position: absolute;
            bottom: 25px;
            left: 50%;
            transform: translateX(-50%);
            width: 85%;
            max-width: 800px;
            background: rgba(15, 23, 42, 0.9);
            border: 2px solid #10b981;
            border-radius: 16px;
            padding: 16px 24px;
            text-align: center;
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.25);
            z-index: 10;
        }

        .lyric-cur {
            font-size: 26px;
            font-weight: bold;
            color: #34d399;
            margin-bottom: 6px;
            text-shadow: 0 0 10px rgba(52, 211, 153, 0.5);
        }

        .lyric-next { font-size: 16px; color: #9ca3af; }

        #ai-feedback {
            font-size: 14px;
            font-weight: bold;
            margin-top: 6px;
            color: #fbbf24;
            min-height: 20px;
        }

        /* 결과 화면 */
        #modal {
            position: absolute;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(5, 6, 8, 0.92);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 100;
            display: none;
        }
        #modal h1 { font-size: 54px; color: #facc15; margin: 0; text-shadow: 0 0 20px #facc15; }
        #modal p { font-size: 20px; color: #e2e8f0; margin-top: 10px; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

<div id="ui-layer">
    <select id="song-select" class="select-box">
        <option value="0">🎵 비행기 (어린이 동요)</option>
        <option value="1">🎵 학교종이 울린다</option>
        <option value="2">🎵 나비야 나비야</option>
    </select>
    <button class="btn" onclick="initAudioAndStart()">🎙️ 마우스 권한 연결 & 노래 시작</button>
</div>

<div id="pitch-hud">
    <div class="hud-title">내 목소리 음정 (Hz)</div>
    <div id="user-pitch" class="hud-val">--- Hz</div>
    <div class="hud-title" style="margin-top:5px;">AI 정밀 점수</div>
    <div id="live-score" class="hud-val" style="color:#10b981;">100</div>
</div>

<div id="lyrics-box">
    <div id="cur-lyric" class="lyric-cur">마이크 권한 연결 후 노래를 시작하세요!</div>
    <div id="next-lyric" class="lyric-next">AI가 목소리의 피치를 정밀 분석합니다.</div>
    <div id="ai-feedback">READY</div>
</div>

<div id="modal">
    <h1 id="final-score">92점!</h1>
    <p id="final-eval">AI 평가: 음정이 안정적이며 우수한 가창력입니다!</p>
    <button class="btn" style="margin-top:20px;" onclick="closeModal()">다시 부르기 🔄</button>
</div>

<script>
    // 1. 노래 데이터베이스 (확장된 곡 리스트)
    const songDB = [
        {
            title: "비행기",
            notes: [
                { time: 0.0, lyric: "프로펠러", next: "돌려라", freq: 329.63 }, // E4
                { time: 0.8, lyric: "프로펠러", next: "돌려라", freq: 293.66 }, // D4
                { time: 1.6, lyric: "프로펠러", next: "돌려라", freq: 261.63 }, // C4
                { time: 2.4, lyric: "프로펠러", next: "돌려라", freq: 293.66 }, // D4
                { time: 3.2, lyric: "돌려라", next: "위로 위로", freq: 329.63 }, // E4
                { time: 4.0, lyric: "돌려라", next: "위로 위로", freq: 329.63 }, // E4
                { time: 4.8, lyric: "위로 위로", next: "솟아라", freq: 293.66 }, // D4
                { time: 5.6, lyric: "위로 위로", next: "솟아라", freq: 293.66 }, // D4
                { time: 6.4, lyric: "솟아라", next: "비행기!", freq: 329.63 }, // E4
                { time: 7.2, lyric: "비행기!", next: "완료", freq: 392.00 }   // G4
            ]
        },
        {
            title: "학교종",
            notes: [
                { time: 0.0, lyric: "학교종이", next: "땡땡땡", freq: 392.00 }, // G4
                { time: 0.8, lyric: "학교종이", next: "땡땡땡", freq: 392.00 }, // G4
                { time: 1.6, lyric: "학교종이", next: "땡땡땡", freq: 440.00 }, // A4
                { time: 2.4, lyric: "학교종이", next: "땡땡땡", freq: 440.00 }, // A4
                { time: 3.2, lyric: "땡땡땡", next: "어서 모이자", freq: 392.00 }, // G4
                { time: 4.0, lyric: "땡땡땡", next: "어서 모이자", freq: 392.00 }, // G4
                { time: 4.8, lyric: "어서 모이자", next: "선생님이", freq: 329.63 }, // E4
                { time: 5.6, lyric: "선생님이", next: "기다리신다", freq: 293.66 }  // D4
            ]
        },
        {
            title: "나비야",
            notes: [
                { time: 0.0, lyric: "나비야", next: "나비야", freq: 392.00 },   // G4
                { time: 0.8, lyric: "나비야", next: "이리 날아오너라", freq: 329.63 }, // E4
                { time: 1.6, lyric: "이리 날아", next: "오너라", freq: 329.63 }, // E4
                { time: 2.4, lyric: "오너라", next: "노랑나비", freq: 349.23 },  // F4
                { time: 3.2, lyric: "노랑나비", next: "흰나비", freq: 293.66 }, // D4
                { time: 4.0, lyric: "흰나비", next: "춤을 추며", freq: 293.66 }  // D4
            ]
        }
    ];

    // 2. Web Audio API & 마이크 실시간 음정 감지 알고리즘 (Autocorrelation)
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
            alert("마이크 연결 실패: 브라우저 마이크 접근 허용이 필요합니다.");
        }
    }

    // 자기상관 함수 기반 피치 추정
    function autoCorrelate(buf, sampleRate) {
        let SIZE = buf.length;
        let rms = 0;
        for (let i = 0; i < SIZE; i++) {
            let val = buf[i];
            rms += val * val;
        }
        rms = Math.sqrt(rms / SIZE);
        if (rms < 0.01) return -1; // 소리가 너무 작음

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
            for (let j = 0; j < SIZE - i; j++) {
                c[i] = c[i] + buf[j] * buf[j + i];
            }
        }

        let d = 0; while (c[d] > c[d + 1]) d++;
        let maxval = -1, maxpos = -1;
        for (let i = d; i < SIZE; i++) {
            if (c[i] > maxval) { maxval = c[i]; maxpos = i; }
        }
        let T0 = maxpos;
        return sampleRate / T0;
    }

    // 3. Three.js 파형 애니메이션 무대
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 2, 8);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    scene.add(new THREE.AmbientLight(0xffffff, 0.7));

    // 파형 실시간 반응 바(Bar) 16개 생성
    const bars = [];
    for (let i = 0; i < 16; i++) {
        const geo = new THREE.BoxGeometry(0.3, 1, 0.3);
        const mat = new THREE.MeshStandardMaterial({ color: 0x10b981, roughness: 0.3 });
        const mesh = new THREE.Mesh(geo, mat);
        mesh.position.set((i - 7.5) * 0.45, 0, 0);
        scene.add(mesh);
        bars.push(mesh);
    }

    // 4. 노래 및 AI 음정 평가 루프
    let isPlaying = false;
    let currentSong = null;
    let startTime = 0;
    let noteIdx = 0;
    let currentScore = 100;
    let totalDeductions = 0;
    let sampleCount = 0;

    async function initAudioAndStart() {
        if (!isMicActive) await setupMicrophone();
        const songIdx = document.getElementById('song-select').value;
        currentSong = songDB[songIdx];

        isPlaying = true;
        noteIdx = 0;
        currentScore = 100;
        totalDeductions = 0;
        sampleCount = 0;
        startTime = Date.now();
    }

    function playMelodyNote(freq) {
        if (!audioCtx) return;
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.6);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.6);
    }

    function animate() {
        requestAnimationFrame(animate);

        // 마이크 입력 실시간 분석
        if (isMicActive && analyser) {
            const buffer = new Float32Array(analyser.fftSize);
            analyser.getFloatTimeDomainData(buffer);
            const userPitch = autoCorrelate(buffer, audioCtx.sampleRate);

            // 파형 바 스케일링
            for (let i = 0; i < bars.length; i++) {
                const val = Math.abs(buffer[i * 10] || 0) * 8 + 0.2;
                bars[i].scale.y = val;
            }

            if (userPitch > 0) {
                document.getElementById('user-pitch').innerText = Math.round(userPitch) + " Hz";
            } else {
                document.getElementById('user-pitch').innerText = "--- Hz";
            }

            // 실시간 AI 음정 판정
            if (isPlaying && currentSong && noteIdx < currentSong.notes.length) {
                const targetFreq = currentSong.notes[noteIdx].freq;
                if (userPitch > 0) {
                    const diff = Math.abs(userPitch - targetFreq);
                    sampleCount++;
                    if (diff < 25) {
                        document.getElementById('ai-feedback').innerText = "🎯 PERFECT! 정확한 음정입니다.";
                        document.getElementById('ai-feedback').style.color = "#34d399";
                    } else if (diff < 50) {
                        document.getElementById('ai-feedback').innerText = "👍 GOOD! 양호합니다.";
                        document.getElementById('ai-feedback').style.color = "#fbbf24";
                    } else {
                        document.getElementById('ai-feedback').innerText = "⚠️ MISS! 음정이 맞지 않습니다.";
                        document.getElementById('ai-feedback').style.color = "#ef4444";
                        totalDeductions += 0.3;
                    }

                    currentScore = Math.max(50, Math.round(100 - totalDeductions));
                    document.getElementById('live-score').innerText = currentScore;
                }
            }
        }

        // 노래 흐름 업데이트
        if (isPlaying && currentSong) {
            const elapsed = (Date.now() - startTime) / 1000;
            if (noteIdx < currentSong.notes.length) {
                const note = currentSong.notes[noteIdx];
                if (elapsed >= note.time) {
                    playMelodyNote(note.freq);
                    document.getElementById('cur-lyric').innerText = note.lyric;
                    document.getElementById('next-lyric').innerText = "다음: " + (note.next || "");
                    noteIdx++;
                }
            } else if (elapsed > currentSong.notes[currentSong.notes.length - 1].time + 1.5) {
                isPlaying = false;
                showModal();
            }
        }

        renderer.render(scene, camera);
    }

    function showModal() {
        document.getElementById('modal').style.display = 'flex';
        document.getElementById('final-score').innerText = currentScore + "점!";
        
        let evalText = "음정 정밀도가 대단히 뛰어납니다!";
        if (currentScore < 80) evalText = "조금 더 음정을 맞춰 부르면 높은 점수를 얻을 수 있습니다!";
        else if (currentScore < 90) evalText = "안정적인 가창력입니다. 훌륭해요!";
        
        document.getElementById('final-eval').innerText = "AI 종합 평가: " + evalText;
    }

    window.closeModal = function() {
        document.getElementById('modal').style.display = 'none';
        document.getElementById('cur-lyric').innerText = "마이크 연결 후 노래를 시작하세요!";
    };

    window.initAudioAndStart = initAudioAndStart;
    animate();
</script>
</body>
</html>
"""

components.html(ai_karaoke_html, height=600)
