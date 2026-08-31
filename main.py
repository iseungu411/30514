import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="3D Piano Rhythm Game", page_icon="🎮", layout="wide")

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
    <h2>🎮 3D 피아노 박자 맞추기 (리듬 게임)</h2>
    <p>위에서 떨어지는 노트가 판정선(건반)에 맞춰 도착할 때 키보드 또는 건반을 누르세요!</p>
</div>
""", unsafe_allow_html=True)

# 2. Three.js 기반 3D 리듬게임 HTML
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
            gap: 20px;
            z-index: 10;
            pointer-events: none;
        }
        .hud-card {
            background: rgba(17, 24, 39, 0.85);
            border: 1px solid #3b82f6;
            padding: 8px 20px;
            border-radius: 12px;
            color: #fff;
            text-align: center;
            box-shadow: 0 0 10px rgba(59, 130, 246, 0.3);
        }
        .hud-label { font-size: 11px; color: #9ca3af; text-transform: uppercase; }
        .hud-value { font-size: 20px; font-weight: bold; color: #60a5fa; }
        #feedback {
            position: absolute;
            top: 40%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 42px;
            font-weight: 900;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.1s, transform 0.1s;
            text-shadow: 0 0 20px currentColor;
        }
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
    <div class="hud-card"><div class="hud-label">SCORE</div><div id="score" class="hud-value">0</div></div>
    <div class="hud-card"><div class="hud-label">COMBO</div><div id="combo" class="hud-value">0</div></div>
</div>

<div id="feedback">PERFECT</div>
<div id="info">⌨️ 입력 키: [A] [S] [D] [F] [G] [H] [J] | 건반 직접 클릭 가능</div>

<script>
    // 1. Web Audio API (사운드 연주)
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

    // 2. 7개 레인 (도 레 미 파 솔 라 시) 데이터 설정
    const lanes = [
        { name: "C4", freq: 261.63, key: "a", color: 0x3b82f6 },
        { name: "D4", freq: 293.66, key: "s", color: 0x60a5fa },
        { name: "E4", freq: 329.63, key: "d", color: 0x93c5fd },
        { name: "F4", freq: 349.23, key: "f", color: 0xf59e0b },
        { name: "G4", freq: 392.00, key: "g", color: 0xfbbf24 },
        { name: "H4", freq: 440.00, key: "h", color: 0xfde047 },
        { name: "J4", freq: 493.88, key: "j", color: 0x10b981 }
    ];

    // 3. Three.js 씬 구축
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

    // 4. 건반(판정선) 메쉬 생성
    const keyObjects = [];
    const laneWidth = 1.1;
    const offset = (lanes.length * laneWidth) / 2 - laneWidth / 2;

    lanes.forEach((lane, i) => {
        const geo = new THREE.BoxGeometry(1.0, 0.4, 2.5);
        const mat = new THREE.MeshStandardMaterial({ color: 0x1f2937, roughness: 0.3 });
        const mesh = new THREE.Mesh(geo, mat);
        mesh.position.set(i * laneWidth - offset, 0, 1.5);
        mesh.userData = { ...lane, index: i, originalY: 0 };
        scene.add(mesh);
        keyObjects.push(mesh);

        // 레인 가이드 라인
        const lineGeo = new THREE.PlaneGeometry(1.0, 30);
        const lineMat = new THREE.MeshBasicMaterial({ color: lane.color, wireframe: true, transparent: true, opacity: 0.15 });
        const line = new THREE.Mesh(lineGeo, lineMat);
        line.rotation.x = -Math.PI / 2;
        line.position.set(i * laneWidth - offset, -0.2, -12);
        scene.add(line);
    });

    // 판정선 가이드 바
    const hitLine = new THREE.Mesh(
        new THREE.BoxGeometry(lanes.length * laneWidth, 0.05, 0.1),
        new THREE.MeshBasicMaterial({ color: 0xef4444 })
    );
    hitLine.position.set(0, 0.2, 1.5);
    scene.add(hitLine);

    // 5. 노트(생성) 시스템
    const notes = [];
    const noteSpeed = 0.22;
    const targetZ = 1.5; // 판정선 Z 위치

    function spawnNote() {
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

    // 1초마다 랜덤 노트 생성
    setInterval(spawnNote, 800);

    // 6. 점수 및 판정 시스템
    let score = 0;
    let combo = 0;

    const scoreEl = document.getElementById('score');
    const comboEl = document.getElementById('combo');
    const feedbackEl = document.getElementById('feedback');

    function showFeedback(text, color) {
        feedbackEl.innerText = text;
        feedbackEl.style.color = color;
        feedbackEl.style.opacity = '1';
        feedbackEl.style.transform = 'translate(-50%, -50%) scale(1.2)';
        
        setTimeout(() => {
            feedbackEl.style.opacity = '0';
            feedbackEl.style.transform = 'translate(-50%, -50%) scale(1.0)';
        }, 200);
    }

    function checkHit(laneIdx) {
        const keyMesh = keyObjects[laneIdx];
        
        // 건반 누름 애니메이션 및 소리
        playNote(keyMesh.userData.freq);
        keyMesh.position.y = -0.15;
        keyMesh.material.color.setHex(keyMesh.userData.color);
        setTimeout(() => {
            keyMesh.position.y = 0;
            keyMesh.material.color.setHex(0x1f2937);
        }, 120);

        // 노트 판정 확인 (판정선 근처의 노트 탐색)
        let hitFound = false;
        for (let i = 0; i < notes.length; i++) {
            const note = notes[i];
            if (note.userData.laneIndex === laneIdx && !note.userData.hit) {
                const dist = Math.abs(note.position.z - targetZ);
                
                if (dist < 1.2) { // 판정 범위 안
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
                    break;
                }
            }
        }

        if (!hitFound) {
            combo = 0;
            comboEl.innerText = combo;
        }
    }

    // 7. 입력 이벤트 (키보드 & 마우스)
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

    // 8. 게임 루프
    function animate() {
        requestAnimationFrame(animate);

        // 노트 이동 및 MISS 처리
        for (let i = notes.length - 1; i >= 0; i--) {
            const note = notes[i];
            note.position.z += noteSpeed;

            // 판정선을 지나쳐 흘러간 경우
            if (note.position.z > targetZ + 1.5 && !note.userData.hit) {
                scene.remove(note);
                notes.splice(i, 1);
                combo = 0;
                comboEl.innerText = combo;
                showFeedback("MISS", "#ef4444");
            }
        }

        renderer.render(scene, camera);
    }
    animate();
</script>
</body>
</html>
"""

components.html(rhythm_game_html, height=580)
