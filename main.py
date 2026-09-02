import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="Streamlit 3D Karaoke", page_icon="🎤", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #080711; color: #ffffff; }
    .title-container {
        text-align: center;
        padding: 10px;
        background: linear-gradient(135deg, #2b1055, #080711);
        border-radius: 12px;
        border: 1px solid #755135;
        margin-bottom: 10px;
    }
</style>
<div class="title-container">
    <h2>🎤 스트림릿 3D 노래방 (Karaoke Stage)</h2>
    <p>곡을 선택하고 시작 버튼을 누르면 3D 무대 조명과 함께 가사 반주가 시작됩니다!</p>
</div>
""", unsafe_allow_html=True)

# 2. Three.js + Web Audio API 노래방 HTML 코드
karaoke_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; background: #080711; font-family: 'Segoe UI', sans-serif; }
        canvas { width: 100vw; height: 100vh; display: block; }

        /* UI 레이어 */
        #ui-layer {
            position: absolute;
            top: 15px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 15px;
            z-index: 10;
        }

        .select-box {
            background: rgba(30, 20, 60, 0.85);
            color: #ff6b6b;
            border: 1px solid #ff6b6b;
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 15px;
            font-weight: bold;
            outline: none;
            cursor: pointer;
        }

        .action-btn {
            background: linear-gradient(135deg, #ff007f, #7928ca);
            color: white;
            border: none;
            padding: 8px 24px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 15px;
            cursor: pointer;
            box-shadow: 0 0 12px rgba(255, 0, 127, 0.5);
            transition: 0.2s;
        }
        .action-btn:hover { transform: scale(1.05); }

        #score-board {
            position: absolute;
            top: 15px;
            right: 20px;
            background: rgba(0,0,0,0.6);
            border: 1px solid #facc15;
            padding: 8px 18px;
            border-radius: 10px;
            color: #facc15;
            font-size: 20px;
            font-weight: bold;
            z-index: 10;
        }

        /* 가사 모니터 박스 */
        #lyrics-container {
            position: absolute;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            width: 80%;
            max-width: 800px;
            background: rgba(10, 10, 25, 0.85);
            border: 2px solid #00f2fe;
            border-radius: 16px;
            padding: 20px 30px;
            text-align: center;
            box-shadow: 0 0 20px rgba(0, 242, 254, 0.3);
            z-index: 10;
        }

        .lyric-current {
            font-size: 28px;
            font-weight: bold;
            color: #00f2fe;
            margin-bottom: 8px;
            text-shadow: 0 0 10px #00f2fe;
            min-height: 38px;
        }

        .lyric-next {
            font-size: 18px;
            color: #94a3b8;
            min-height: 24px;
        }

        /* 점수 모달 */
        #result-modal {
            position: absolute;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(0,0,0,0.85);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 100;
            display: none;
        }
        #result-modal h1 { font-size: 60px; color: #facc15; margin: 0; text-shadow: 0 0 30px #facc15; }
        #result-modal p { font-size: 24px; color: #fff; margin-top: 10px; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

<div id="ui-layer">
    <select id="song-select" class="select-box">
        <option value="0">🎵 비행기 (어린이 동요)</option>
        <option value="1">🎵 학교종이 울린다</option>
        <option value="2">🎵 반짝반짝 작은 별</option>
    </select>
    <button class="action-btn" onclick="startKaraoke()">🎤 노래 시작</button>
</div>

<div id="score-board">SCORE: <span id="score-val">100</span></div>

<div id="lyrics-container">
    <div id="cur-lyric" class="lyric-current">노래 시작 버튼을 눌러주세요!</div>
    <div id="next-lyric" class="lyric-next">준비되셨나요?</div>
</div>

<!-- 결과 화면 -->
<div id="result-modal">
    <h1 id="final-score">98점!</h1>
    <p id="final-msg">완벽한 가창력이네요! 🎉</p>
    <button class="action-btn" style="margin-top:20px;" onclick="closeModal()">확인</button>
</div>

<script>
    // 1. 노래 데이터베이스 (가사 및 멜로디 주파수 데이터)
    const songDB = [
        {
            title: "비행기",
            bpm: 120,
            notes: [
                { time: 0, lyric: "프로펠러", next: "돌려라", freq: 329.63, duration: 0.4 }, // 미
                { time: 0.5, lyric: "프로펠러", next: "돌려라", freq: 293.66, duration: 0.4 }, // 레
                { time: 1.0, lyric: "프로펠러", next: "돌려라", freq: 261.63, duration: 0.4 }, // 도
                { time: 1.5, lyric: "프로펠러", next: "돌려라", freq: 293.66, duration: 0.4 }, // 레
                { time: 2.0, lyric: "돌려라", next: "위로 위로", freq: 329.63, duration: 0.4 }, // 미
                { time: 2.5, lyric: "돌려라", next: "위로 위로", freq: 329.63, duration: 0.4 }, // 미
                { time: 3.0, lyric: "돌려라", next: "위로 위로", freq: 329.63, duration: 0.8 }, // 미
                { time: 4.0, lyric: "위로 위로", next: "솟아라", freq: 293.66, duration: 0.4 }, // 레
                { time: 4.5, lyric: "위로 위로", next: "솟아라", freq: 293.66, duration: 0.4 }, // 레
                { time: 5.0, lyric: "위로 위로", next: "솟아라", freq: 293.66, duration: 0.8 }, // 레
                { time: 6.0, lyric: "솟아라", next: "비행기!", freq: 329.63, duration: 0.4 }, // 미
                { time: 6.5, lyric: "솟아라", next: "비행기!", freq: 392.00, duration: 0.4 }, // 솔
                { time: 7.0, lyric: "솟아라", next: "비행기!", freq: 392.00, duration: 0.8 }, // 솔
                { time: 8.0, lyric: "비행기!", next: "수고하셨습니다!", freq: 261.63, duration: 1.2 }  // 도
            ]
        },
        {
            title: "학교종",
            bpm: 110,
            notes: [
                { time: 0, lyric: "학교종이", next: "땡땡땡", freq: 392.00, duration: 0.4 }, // 솔
                { time: 0.5, lyric: "학교종이", next: "땡땡땡", freq: 392.00, duration: 0.4 }, // 솔
                { time: 1.0, lyric: "학교종이", next: "땡땡땡", freq: 440.00, duration: 0.4 }, // 라
                { time: 1.5, lyric: "학교종이", next: "땡땡땡", freq: 440.00, duration: 0.4 }, // 라
                { time: 2.0, lyric: "땡땡땡", next: "어서 모이자", freq: 392.00, duration: 0.4 }, // 솔
                { time: 2.5, lyric: "땡땡땡", next: "어서 모이자", freq: 392.00, duration: 0.4 }, // 솔
                { time: 3.0, lyric: "땡땡땡", next: "어서 모이자", freq: 329.63, duration: 0.8 }, // 미
                { time: 4.0, lyric: "어서 모이자", next: "선생님이", freq: 392.00, duration: 0.4 }, // 솔
                { time: 4.5, lyric: "어서 모이자", next: "선생님이", freq: 392.00, duration: 0.4 }, // 솔
                { time: 5.0, lyric: "어서 모이자", next: "선생님이", freq: 329.63, duration: 0.4 }, // 미
                { time: 5.5, lyric: "어서 모이자", next: "선생님이", freq: 329.63, duration: 0.4 }, // 미
                { time: 6.0, lyric: "선생님이", next: "기다리신다", freq: 293.66, duration: 1.2 }  // 레
            ]
        }
    ];

    // 2. Web Audio API 반주 생성기
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    function playMelodyNote(freq, duration) {
        if (audioCtx.state === 'suspended') audioCtx.resume();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        
        gain.gain.setValueAtTime(0.4, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
        
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        
        osc.start();
        osc.stop(audioCtx.currentTime + duration);
    }

    // 3. Three.js 3D 무대 및 미러볼 조명
    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x080711, 0.03);

    const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 3, 10);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    // 미러볼 구체
    const mirrorBallGeo = new THREE.SphereGeometry(1.5, 16, 16);
    const mirrorBallMat = new THREE.MeshStandardMaterial({
        color: 0xffffff, roughness: 0.1, metalness: 0.9, wireframe: true
    });
    const mirrorBall = new THREE.Mesh(mirrorBallGeo, mirrorBallMat);
    mirrorBall.position.set(0, 5, 0);
    scene.add(mirrorBall);

    // 화려한 컬러 스포트라이트 3개
    const spotLights = [];
    const colors = [0xff007f, 0x00f2fe, 0xfacc15];
    colors.forEach((col, i) => {
        const light = new THREE.SpotLight(col, 5);
        light.position.set((i - 1) * 6, 8, -2);
        light.angle = Math.PI / 6;
        light.penumbra = 0.8;
        scene.add(light);
        spotLights.push(light);
    });

    scene.add(new THREE.AmbientLight(0x222233));

    // 바닥 입체 무대
    const stageGeo = new THREE.CylinderGeometry(8, 9, 1, 32);
    const stageMat = new THREE.MeshStandardMaterial({ color: 0x111827, roughness: 0.5 });
    const stage = new THREE.Mesh(stageGeo, stageMat);
    stage.position.set(0, -2, 0);
    scene.add(stage);

    // 4. 노래 재생 제어 변수
    let isPlaying = false;
    let currentSong = null;
    let songStartTime = 0;
    let nextNoteIndex = 0;

    window.startKaraoke = function() {
        const songIdx = document.getElementById('song-select').value;
        currentSong = songDB[songIdx] || songDB[0];
        
        isPlaying = true;
        nextNoteIndex = 0;
        songStartTime = Date.now();
        
        document.getElementById('cur-lyric').innerText = "🎵 반주 준비 중...";
        document.getElementById('next-lyric').innerText = currentSong.notes[0].lyric;
    };

    function finishSong() {
        isPlaying = false;
        const finalScore = Math.floor(Math.random() * 11) + 90; // 90~100점 무작위
        document.getElementById('final-score').innerText = finalScore + "점! 🏆";
        document.getElementById('result-modal').style.display = 'flex';
    }

    window.closeModal = function() {
        document.getElementById('result-modal').style.display = 'none';
        document.getElementById('cur-lyric').innerText = "곡을 선택하고 시작하세요!";
        document.getElementById('next-lyric').innerText = "";
    };

    // 5. 실시간 애니메이션 및 오디오 루프
    function animate() {
        requestAnimationFrame(animate);

        // 미러볼 회전
        mirrorBall.rotation.y += 0.01;

        // 조명 조명 무빙 효과
        const time = Date.now() * 0.003;
        spotLights.forEach((light, i) => {
            light.position.x = Math.sin(time + i) * 5;
        });

        // 가사 및 반주 동기화
        if (isPlaying && currentSong) {
            const elapsed = (Date.now() - songStartTime) / 1000;

            if (nextNoteIndex < currentSong.notes.length) {
                const note = currentSong.notes[nextNoteIndex];
                if (elapsed >= note.time) {
                    playMelodyNote(note.freq, note.duration);
                    document.getElementById('cur-lyric').innerText = note.lyric;
                    document.getElementById('next-lyric').innerText = "다음: " + (note.next || "");
                    nextNoteIndex++;
                }
            } else if (elapsed > currentSong.notes[currentSong.notes.length - 1].time + 2.0) {
                finishSong();
            }
        }

        renderer.render(scene, camera);
    }

    animate();
</script>
</body>
</html>
"""

components.html(karaoke_html, height=580)
