import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="3D Piano Rhythm Game - Stage Challenge", page_icon="🎮", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #050608; color: #ffffff; }
    .title-container {
        text-align: center;
        padding: 10px;
        background: linear-gradient(135deg, #111827, #050608);
        border-radius: 12px;
        border: 1px solid #3b82f6;
        margin-bottom: 10px;
    }
</style>
<div class="title-container">
    <h2>🎮 3D 피아노 박자 맞추기: 단계별 스테이지 도전</h2>
    <p>노트를 놓치면 HP가 깎입니다! 콤보를 올려 높은 단계(Stage)로 진화하세요.</p>
</div>
""", unsafe_allow_html=True)

rhythm_game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; background: #050608; font-family: 'Segoe UI', sans-serif; }
        canvas { width: 100vw; height: 100vh; display: block; }
        
        #ui-layer {
            position: absolute;
            top: 15px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 15px;
            z-index: 10;
            pointer-events: none;
        }
        .hud-card {
            background: rgba(17, 24, 39, 0.85);
            border: 1px solid #3b82f6;
            padding: 8px 16px;
            border-radius: 12px;
            color: #fff;
            text-align: center;
            box-shadow: 0 0 10px rgba(59, 130, 246, 0.3);
            min-width: 70px;
        }
        .hud-card.danger { border-color: #ef4444; box-shadow: 0 0 10px rgba(239, 68, 68, 0.3); }
        .hud-card.stage { border-color: #f59e0b; box-shadow: 0 0 10px rgba(245, 158, 11, 0.3); }
        .hud-label { font-size: 11px; color: #9ca3af; text-transform: uppercase; }
        .hud-value { font-size: 18px; font-weight: bold; color: #60a5fa; }
        .hud-card.danger .hud-value { color: #f87171; }
        .hud-card.stage .hud-value { color: #fbbf24; }

        #feedback {
            position: absolute;
            top: 35%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 40px;
            font-weight: 900;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.1s, transform 0.1s;
            text-shadow: 0 0 20px currentColor;
        }

        /* 게임 오버 / 성공 오버레이 */
        #game-over-screen {
            position: absolute;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(5, 6, 8, 0.9);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 100;
            display: none;
        }
        #game-over-screen h1 { font-size: 48px; color: #ef4444; margin-bottom: 10px; text-shadow: 0 0 20px #ef4444; }
        #game-over-screen p { font-size: 18px; color: #9ca3af; margin-bottom: 20px; }
        .restart-btn {
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            color: white;
            border: none;
            padding: 12px 28px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 0 15px rgba(37, 99, 235, 0.5);
            transition: 0.2s;
        }
        .restart-btn:hover { transform: scale(1.05); }

        #info {
            position: absolute;
            bottom: 10px;
            left: 50%;
            transform: translateX(-50%);
            color: #9ca3af;
            font-size: 12px;
            background: rgba(0,0,0,0.6);
            padding: 4px 12px;
            border-radius: 10px;
        }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

<div id="ui-layer">
    <div class="hud-card stage"><div class="hud-label">STAGE</div><div id="stage" class="hud-value">1</div></div>
    <div class="hud-card"><div class="hud-label">SCORE</div><div id="score" class="hud-value">0</div></div>
    <div class="hud-card"><div class="hud-label">COMBO</div><div id="combo" class="hud-value">0</div></div>
    <div class="hud-card danger"><div class="hud-label">HP</div><div id="hp" class="hud-value">5</div></div>
</div>

<div id="feedback">PERFECT</div>

<!-- 게임 오버 화면 -->
<div id="game-over-screen">
    <h1 id="over-title">GAME OVER</h1>
    <p id="over-desc">HP가 모두 소진되었습니다!</p>
    <button class="restart-btn" onclick="restartGame()">다시 도전하기 🔄</button>
</div>

<div id="info">⌨️ 입력 키: [A] [S] [D] [F] [G] [H] [J]</div>

<script>
    // 1. Web Audio API
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    function playNote(freq) {
        if (audioCtx.state === 'suspended') audioCtx.resume();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.5, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.8);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.8);
    }

    const lanes = [
        { name: "C4", freq: 261.63, key: "a", color: 0x3b82f6 },
        { name: "D4", freq: 293.66, key: "s", color: 0x60a5fa },
        { name: "E4", freq: 329.63, key: "d", color: 0x93c5fd },
        { name: "F4", freq: 349.23, key: "f", color: 0xf59e0b },
        { name: "G4", freq: 392.00, key: "g", color: 0xfbbf24 },
        { name: "H4", freq: 440.00, key: "h", color: 0xfde047 },
        { name: "J4", freq: 493.88, key: "j", color: 0x10b981 }
    ];

    // 2. 난이도 및 게임 상태 변수
    let score = 0;
    let combo = 0;
    let hp = 5;
    let stage = 1;
    let isGameOver = false;

    let noteSpeed = 0.20;       // 이동 속도 (단계별 상승)
    let spawnInterval = 1000;   // 노트 생성 간격 (단계별 단축)
    let spawnTimer = null;

    // 3. Three.js 씬 설정
    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x050608, 0.025);

    const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 7, 9);
    camera.lookAt(0, 0, -2);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    scene.add(new THREE.AmbientLight(0xffffff, 0.6));
    const pLight = new THREE.PointLight(0x3b82f6, 2, 20);
    pLight.position.set(0, 5, 2);
    scene.add(pLight);

    // 건반 및 레인 생성
    const keyObjects = [];
    const laneWidth = 1.1;
    const offset = (lanes.length * laneWidth) / 2 - laneWidth / 2;

    lanes.forEach((lane, i) => {
        const geo = new THREE.BoxGeometry(1.0, 0.4, 2.5);
        const mat = new THREE.MeshStandardMaterial({ color: 0x1f2937, roughness: 0.3 });
        const mesh = new THREE.Mesh(geo, mat);
        mesh.position.set(i * laneWidth - offset, 0, 1.5);
        mesh.userData = { ...lane, index: i };
        scene.add(mesh);
        keyObjects.push(mesh);

        const lineGeo = new THREE.PlaneGeometry(1.0, 30);
        const lineMat = new THREE.MeshBasicMaterial({ color: lane.color, wireframe: true, transparent: true, opacity: 0.15 });
        const line = new THREE.Mesh(lineGeo, lineMat);
        line.rotation.x = -Math.PI / 2;
        line.position.set(i * laneWidth - offset, -0.2, -12);
        scene.add(line);
    });

    const hitLine = new THREE.Mesh(
        new THREE.BoxGeometry(lanes.length * laneWidth, 0.05, 0.1),
        new THREE.MeshBasicMaterial({ color: 0xef4444 })
    );
    hitLine.position.set(0, 0.2, 1.5);
    scene.add(hitLine);

    // 4. 노트 및 루프 조작
    let notes = [];
    const targetZ = 1.5;

    function spawnNote() {
        if (isGameOver) return;
        const laneIdx = Math.floor(Math.random() * lanes.length);
        const lane = lanes[laneIdx];

        const geo = new THREE.BoxGeometry(0.9, 0.3, 0.8);
        const mat = new THREE.MeshStandardMaterial({ color: lane.color, emissive: lane.color, emissiveIntensity: 0.4 });
        const mesh = new THREE.Mesh(geo, mat);
        
        mesh.position.set(laneIdx * laneWidth - offset, 0.2, -20);
        mesh.userData = { laneIndex: laneIdx, hit: false };

        scene.add(mesh);
        notes.push(mesh);
    }

    function startSpawning() {
        if (spawnTimer) clearInterval(spawnTimer);
        spawnTimer = setInterval(spawnNote, spawnInterval);
    }

    // 5. 난이도 조절 (단계 상승)
    function updateStage() {
        // 점수 기준 stage 상승
        let newStage = Math.floor(score / 1000) + 1;
        if (newStage !== stage && newStage <= 10) {
            stage = newStage;
            document.getElementById('stage').innerText = stage;
            
            // 단계가 오를수록 더 빨라지고 촘촘하게 생성
            noteSpeed = 0.20 + (stage - 1) * 0.04;
            spawnInterval = Math.max(350, 1000 - (stage - 1) * 80);
            
            showFeedback("STAGE " + stage + "!", "#f59e0b");
            startSpawning();
        }
    }

    const scoreEl = document.getElementById('score');
    const comboEl = document.getElementById('combo');
    const hpEl = document.getElementById('hp');
    const feedbackEl = document.getElementById('feedback');

    function showFeedback(text, color) {
        feedbackEl.innerText = text;
        feedbackEl.style.color = color;
        feedbackEl.style.opacity = '1';
        feedbackEl.style.transform = 'translate(-50%, -50%) scale(1.2)';
        
        setTimeout(() => {
            feedbackEl.style.opacity = '0';
            feedbackEl.style.transform = 'translate(-50%, -50%) scale(1.0)';
        }, 220);
    }

    function checkHit(laneIdx) {
        if (isGameOver) return;
        const keyMesh = keyObjects[laneIdx];
        
        playNote(keyMesh.userData.freq);
        keyMesh.position.y = -0.15;
        keyMesh.material.color.setHex(keyMesh.userData.color);
        setTimeout(() => {
            keyMesh.position.y = 0;
            keyMesh.material.color.setHex(0x1f2937);
        }, 120);

        let hitFound = false;
        for (let i = 0; i < notes.length; i++) {
            const note = notes[i];
            if (note.userData.laneIndex === laneIdx && !note.userData.hit) {
                const dist = Math.abs(note.position.z - targetZ);
                
                if (dist < 1.3) {
                    hitFound = true;
                    note.userData.hit = true;
                    scene.remove(note);
                    
                    if (dist < 0.4) {
                        score += 300;
                        combo++;
                        showFeedback("PERFECT!", "#60a5fa");
                    } else if (dist < 0.8) {
                        score += 150;
                        combo++;
                        showFeedback("GREAT", "#fbbf24");
                    } else {
                        score += 50;
                        combo = 0;
                        showFeedback("GOOD", "#34d399");
                    }
                    
                    scoreEl.innerText = score;
                    comboEl.innerText = combo;
                    updateStage();
                    break;
                }
            }
        }

        // 헛스윙(잘못 누름)
        if (!hitFound) {
            combo = 0;
            comboEl.innerText = combo;
        }
    }

    function triggerMiss() {
        combo = 0;
        hp--;
        comboEl.innerText = combo;
        hpEl.innerText = hp;
        showFeedback("MISS", "#ef4444");

        if (hp <= 0) {
            endGame();
        }
    }

    function endGame() {
        isGameOver = true;
        clearInterval(spawnTimer);
        document.getElementById('game-over-screen').style.display = 'flex';
        document.getElementById('over-desc').innerText = "최종 점수: " + score + "점 | 달성 단계: Stage " + stage;
    }

    window.restartGame = function() {
        // 기존 노트 제거
        notes.forEach(n => scene.remove(n));
        notes = [];
        
        score = 0;
        combo = 0;
        hp = 5;
        stage = 1;
        noteSpeed = 0.20;
        spawnInterval = 1000;
        isGameOver = false;

        scoreEl.innerText = score;
        comboEl.innerText = combo;
        hpEl.innerText = hp;
        document.getElementById('stage').innerText = stage;
        document.getElementById('game-over-screen').style.display = 'none';

        startSpawning();
    }

    // 입력 처리
    window.addEventListener('keydown', (e) => {
        const key = e.key.toLowerCase();
        const laneIdx = lanes.findIndex(l => l.key === key);
        if (laneIdx !== -1) checkHit(laneIdx);
    });

    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    window.addEventListener('pointerdown', (e) => {
        mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
        mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
        raycaster.setFromCamera(mouse, camera);
        const intersects = raycaster.intersectObjects(keyObjects);
        if (intersects.length > 0) {
            checkHit(intersects[0].object.userData.index);
        }
    });

    // 6. 메인 애니메이션 루프
    function animate() {
        requestAnimationFrame(animate);

        if (!isGameOver) {
            for (let i = notes.length - 1; i >= 0; i--) {
                const note = notes[i];
                note.position.z += noteSpeed;

                if (note.position.z > targetZ + 1.5 && !note.userData.hit) {
                    scene.remove(note);
                    notes.splice(i, 1);
                    triggerMiss();
                }
            }
        }

        renderer.render(scene, camera);
    }

    startSpawning();
    animate();
</script>
</body>
</html>
"""

components.html(rhythm_game_html, height=580)
