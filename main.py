import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="3D Interactive Piano", page_icon="🎹", layout="wide")

# 커스텀 CSS
st.markdown("""
<style>
    .stApp { background-color: #0b0c10; color: #ffffff; }
    .title-container {
        text-align: center;
        padding: 10px;
        background: linear-gradient(135deg, #1f2833, #0b0c10);
        border-radius: 12px;
        border: 1px solid #45a29e;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="title-container">
    <h1>🎹 3D 리얼타임 인터랙티브 피아노</h1>
    <p>마우스로 3D 건반을 클릭하거나 키보드(A, S, D, F, G, H, J...)를 눌러 연주해보세요!</p>
</div>
""", unsafe_allow_html=True)

# 2. Three.js + Web Audio API 기반 3D 피아노 코드
piano_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; background: #0b0c10; font-family: sans-serif; }
        canvas { width: 100vw; height: 100vh; display: block; }
        #info {
            position: absolute;
            top: 10px;
            left: 50%;
            transform: translateX(-50%);
            color: #66fcf1;
            font-size: 14px;
            pointer-events: none;
            background: rgba(0,0,0,0.6);
            padding: 8px 16px;
            border-radius: 20px;
        }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
<div id="info">⌨️ 키보드 매핑: [A, W, S, E, D, F, T, G, Y, H, U, J, K]</div>
<script>
    // 1. Web Audio API (피아노 음생성기)
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    
    // 도, 도#, 레, 레#, 미, 파, 파#, 솔, 솔#, 라, 라#, 시, 도 (옥타브 4)
    const notes = [
        { name: "C4", freq: 261.63, isBlack: false, key: "a" },
        { name: "C#4", freq: 277.18, isBlack: true, key: "w" },
        { name: "D4", freq: 293.66, isBlack: false, key: "s" },
        { name: "D#4", freq: 311.13, isBlack: true, key: "e" },
        { name: "E4", freq: 329.63, isBlack: false, key: "d" },
        { name: "F4", freq: 349.23, isBlack: false, key: "f" },
        { name: "F#4", freq: 369.99, isBlack: true, key: "t" },
        { name: "G4", freq: 392.00, isBlack: false, key: "g" },
        { name: "G#4", freq: 415.30, isBlack: true, key: "y" },
        { name: "A4", freq: 440.00, isBlack: false, key: "h" },
        { name: "A#4", freq: 466.16, isBlack: true, key: "u" },
        { name: "B4", freq: 493.88, isBlack: false, key: "j" },
        { name: "C5", freq: 523.25, isBlack: false, key: "k" }
    ];

    function playNote(freq) {
        if (audioCtx.state === 'suspended') {
            audioCtx.resume();
        }
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        
        osc.type = 'triangle'; // 피아노에 가까운 부드러운 파형
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        
        gain.gain.setValueAtTime(0.5, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 1.2);
        
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        
        osc.start();
        osc.stop(audioCtx.currentTime + 1.2);
    }

    // 2. Three.js 3D 씬 세팅
    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x0b0c10, 0.03);

    const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 8, 10);
    camera.lookAt(0, 0, 0);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.shadowMap.enabled = true;
    document.body.appendChild(renderer.domElement);

    // 조명
    scene.add(new THREE.AmbientLight(0xffffff, 0.6));
    const pLight = new THREE.PointLight(0x66fcf1, 2, 20);
    pLight.position.set(0, 6, 3);
    scene.add(pLight);

    // 3. 피아노 건반 3D 모델링 생성
    const keysGroup = new THREE.Group();
    const keyObjects = [];
    
    let whiteIndex = 0;
    
    notes.forEach((note, index) => {
        let mesh;
        if (!note.isBlack) {
            // 흰 건반
            const geo = new THREE.BoxGeometry(0.85, 0.6, 4);
            const mat = new THREE.MeshStandardMaterial({ color: 0xeeeeee, roughness: 0.2 });
            mesh = new THREE.Mesh(geo, mat);
            mesh.position.set((whiteIndex - 3.5) * 0.9, 0, 0);
            whiteIndex++;
        } else {
            // 검은 건반
            const geo = new THREE.BoxGeometry(0.5, 0.6, 2.4);
            const mat = new THREE.MeshStandardMaterial({ color: 0x111111, roughness: 0.1 });
            mesh = new THREE.Mesh(geo, mat);
            const posX = ((whiteIndex - 1) - 3.5) * 0.9 + 0.45;
            mesh.position.set(posX, 0.3, -0.8);
        }
        
        mesh.userData = { ...note, originalY: mesh.position.y, isPressed: false };
        keysGroup.add(mesh);
        keyObjects.push(mesh);
    });

    scene.add(keysGroup);

    // 건반 누름 애니메이션 및 소리 재생
    function pressKey(keyMesh) {
        if (!keyMesh) return;
        playNote(keyMesh.userData.freq);
        
        keyMesh.position.y = keyMesh.userData.originalY - 0.15;
        keyMesh.rotation.x = 0.05;
        keyMesh.material.color.setHex(0x66fcf1); // 눌렸을 때 민트색 발광

        setTimeout(() => {
            keyMesh.position.y = keyMesh.userData.originalY;
            keyMesh.rotation.x = 0;
            keyMesh.material.color.setHex(keyMesh.userData.isBlack ? 0x111111 : 0xeeeeee);
        }, 150);
    }

    // 4. 마우스 클릭 이벤트 (Raycasting)
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    window.addEventListener('pointerdown', (e) => {
        mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
        mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;

        raycaster.setFromCamera(mouse, camera);
        const intersects = raycaster.intersectObjects(keyObjects);

        if (intersects.length > 0) {
            pressKey(intersects[0].object);
        }
    });

    // 5. 키보드 연동 이벤트
    window.addEventListener('keydown', (e) => {
        const key = e.key.toLowerCase();
        const targetMesh = keyObjects.find(m => m.userData.key === key);
        if (targetMesh) {
            pressKey(targetMesh);
        }
    });

    // 6. 애니메이션 루프
    function animate() {
        requestAnimationFrame(animate);
        renderer.render(scene, camera);
    }
    animate();
</script>
</body>
</html>
"""

# 3D 피아노 캔버스 출력
components.html(piano_html, height=500)
