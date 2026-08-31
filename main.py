import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="3D Grand Piano (37 Keys)", page_icon="🎹", layout="wide")

# 커스텀 CSS
st.markdown("""
<style>
    .stApp { background-color: #0b0c10; color: #ffffff; }
    .title-container {
        text-align: center;
        padding: 12px;
        background: linear-gradient(135deg, #1f2833, #0b0c10);
        border-radius: 12px;
        border: 1px solid #45a29e;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="title-container">
    <h2>🎹 3D 풀레인지 그랜드 피아노 (3옥타브 / 37건반)</h2>
    <p>마우스 드래그로 3D 시점을 회전하고, 넓어진 건반을 마우스/키보드로 연주해보세요!</p>
</div>
""", unsafe_allow_html=True)

# 2. Three.js + 3옥타브 Web Audio API 연동 코드
piano_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; background: #0b0c10; font-family: sans-serif; }
        canvas { width: 100vw; height: 100vh; display: block; }
        #controls {
            position: absolute;
            top: 15px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 10px;
            z-index: 10;
        }
        .btn {
            background: #1f2833;
            color: #66fcf1;
            border: 1px solid #45a29e;
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            transition: 0.2s;
        }
        .btn:hover { background: #45a29e; color: #0b0c10; }
        #info {
            position: absolute;
            bottom: 15px;
            left: 50%;
            transform: translateX(-50%);
            color: #c5c6c7;
            font-size: 13px;
            background: rgba(0,0,0,0.7);
            padding: 6px 16px;
            border-radius: 20px;
            pointer-events: none;
        }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>

<div id="controls">
    <button class="btn" onclick="moveCamera(-8)">◀ 저음역대 (C3)</button>
    <button class="btn" onclick="moveCamera(0)">Mid 중앙 (C4)</button>
    <button class="btn" onclick="moveCamera(8)">고음역대 (C5) ▶</button>
</div>

<div id="info">🖱️ 마우스 드래그: 카메라 회전 / 클릭: 연주 | ⌨️ 중앙 옥타브 키보드: [A, W, S, E, D, F, T, G, Y, H, U, J, K]</div>

<script>
    // 1. Web Audio API 사운드 생성기
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

    function playSound(freq) {
        if (audioCtx.state === 'suspended') audioCtx.resume();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        
        gain.gain.setValueAtTime(0.6, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 1.4);
        
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        
        osc.start();
        osc.stop(audioCtx.currentTime + 1.4);
    }

    // 2. 3옥타브 (C3 ~ C6) 주파수 데이터 자동 생성 (37개 건반)
    const baseKeys = [
        { note: "C", isBlack: false, k: "a" }, { note: "C#", isBlack: true, k: "w" },
        { note: "D", isBlack: false, k: "s" }, { note: "D#", isBlack: true, k: "e" },
        { note: "E", isBlack: false, k: "d" }, { note: "F", isBlack: false, k: "f" },
        { note: "F#", isBlack: true, k: "t" }, { note: "G", isBlack: false, k: "g" },
        { note: "G#", isBlack: true, k: "y" }, { note: "A", isBlack: false, k: "h" },
        { note: "A#", isBlack: true, k: "u" }, { note: "B", isBlack: false, k: "j" }
    ];

    const notes = [];
    // 옥타브 3, 4, 5 생성
    [3, 4, 5].forEach((oct) => {
        baseKeys.forEach((item) => {
            // MIDI 노트 번호 기반 주파수 계산
            const noteIndex = baseKeys.indexOf(item);
            const midi = (oct + 1) * 12 + noteIndex;
            const freq = 440 * Math.pow(2, (midi - 69) / 12);
            notes.push({
                name: item.note + oct,
                freq: freq,
                isBlack: item.isBlack,
                key: oct === 4 ? item.k : null // 키보드는 C4 옥타브에 매핑
            });
        });
    });
    // 마지막 C6 추가
    notes.push({ name: "C6", freq: 1046.50, isBlack: false, key: "k" });

    // 3. Three.js 씬 & OrbitControls 카메라
    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x0b0c10, 0.02);

    const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 11, 14);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.shadowMap.enabled = true;
    document.body.appendChild(renderer.domElement);

    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.maxPolarAngle = Math.PI / 2.2; // 바닥 아래로 안 내려가게 제한

    // 조명
    scene.add(new THREE.AmbientLight(0xffffff, 0.7));
    const pLight = new THREE.PointLight(0x66fcf1, 2, 30);
    pLight.position.set(0, 10, 5);
    scene.add(pLight);

    // 4. 37개 건반 메쉬 생성
    const keyObjects = [];
    let whiteIndex = 0;
    const totalWhiteKeys = 22; // 3옥타브 전체 흰건반 수
    const offset = (totalWhiteKeys * 0.9) / 2;

    notes.forEach((note) => {
        let mesh;
        if (!note.isBlack) {
            const geo = new THREE.BoxGeometry(0.82, 0.6, 4.5);
            const mat = new THREE.MeshStandardMaterial({ color: 0xf0f0f0, roughness: 0.2 });
            mesh = new THREE.Mesh(geo, mat);
            mesh.position.set(whiteIndex * 0.88 - offset, 0, 0);
            whiteIndex++;
        } else {
            const geo = new THREE.BoxGeometry(0.48, 0.65, 2.7);
            const mat = new THREE.MeshStandardMaterial({ color: 0x111111, roughness: 0.1 });
            mesh = new THREE.Mesh(geo, mat);
            const posX = (whiteIndex - 1) * 0.88 - offset + 0.44;
            mesh.position.set(posX, 0.3, -0.9);
        }

        mesh.userData = { ...note, originalY: mesh.position.y };
        scene.add(mesh);
        keyObjects.push(mesh);
    });

    // 5. 건반 연동 함수
    function pressKey(keyMesh) {
        if (!keyMesh) return;
        playSound(keyMesh.userData.freq);

        keyMesh.position.y = keyMesh.userData.originalY - 0.15;
        keyMesh.rotation.x = 0.04;
        keyMesh.material.color.setHex(0x66fcf1);

        setTimeout(() => {
            keyMesh.position.y = keyMesh.userData.originalY;
            keyMesh.rotation.x = 0;
            keyMesh.material.color.setHex(keyMesh.userData.isBlack ? 0x111111 : 0xf0f0f0);
        }, 160);
    }

    // 마우스 클릭
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    window.addEventListener('pointerdown', (e) => {
        if (e.target.tagName === 'BUTTON') return;
        mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
        mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;

        raycaster.setFromCamera(mouse, camera);
        const intersects = raycaster.intersectObjects(keyObjects);
        if (intersects.length > 0) pressKey(intersects[0].object);
    });

    // 키보드 입력
    window.addEventListener('keydown', (e) => {
        const key = e.key.toLowerCase();
        const target = keyObjects.find(m => m.userData.key === key);
        if (target) pressKey(target);
    });

    // 카메라 시점 이동 버튼
    window.moveCamera = function(xPos) {
        controls.target.set(xPos, 0, 0);
        camera.position.set(xPos, 11, 14);
    };

    // 루프
    function animate() {
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
    }
    animate();
</script>
</body>
</html>
"""

# 3D 피아노 렌더링
components.html(piano_html, height=560)
