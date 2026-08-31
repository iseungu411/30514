import streamlit as st
import streamlit.components.v1 as components
import random

# 1. 페이지 기본 설정
st.set_page_config(page_title="3D RPG: 검 강화하기", page_icon="⚔️", layout="wide")

# 세션 상태 초기화
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'gold' not in st.session_state:
    st.session_state.gold = 1000
if 'monster_hp' not in st.session_state:
    st.session_state.monster_hp = 1000
if 'action' not in st.session_state:
    st.session_state.action = "idle"  # idle, attack, fail

# 2. 커스텀 CSS (네온 UI)
st.markdown("""
<style>
    .stApp { background-color: #05050a; color: #ffffff; }
    .stat-card {
        background: linear-gradient(135deg, #12131c, #1a1c2e);
        border: 1px solid #2d3250;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 0 15px rgba(0,150,255,0.1);
    }
</style>
""", unsafe_allow_html=True)

st.title("⚔️ 3D 다크 판타지: 시네마틱 검 강화 & 전투")

# 상단 UI
col_ui1, col_ui2, col_ui3 = st.columns(3)
with col_ui1:
    st.markdown(f'<div class="stat-card"><b>💰 보유 골드</b><br><h3 style="color:#ffd700; margin:0;">{st.session_state.gold:,} G</h3></div>', unsafe_allow_html=True)
with col_ui2:
    st.markdown(f'<div class="stat-card"><b>🗡️ 현재 무기</b><br><h3 style="color:#00ffff; margin:0;">+{st.session_state.level} 강화검</h3></div>', unsafe_allow_html=True)
with col_ui3:
    st.markdown(f'<div class="stat-card"><b>👹 몬스터 HP</b><br><h3 style="color:#ff4d4f; margin:0;">{st.session_state.monster_hp} / 1000</h3></div>', unsafe_allow_html=True)

st.write("")

# ---------------------------------------------------------
# 3. Three.js 기반 3D 전투 씬 (Canvas HTML/JS)
# ---------------------------------------------------------
three_js_code = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ margin: 0; overflow: hidden; background-color: #000; }}
        canvas {{ width: 100vw; height: 100vh; display: block; }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
<script>
    // 1. Scene, Camera, Renderer 설정
    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x05050a, 0.03);

    const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 3, 10);

    const renderer = new THREE.WebGLRenderer({{ antialias: true }});
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    document.body.appendChild(renderer.domElement);

    // 2. 조명 (Lighting)
    const ambientLight = new THREE.AmbientLight(0x404040, 2);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0x00ffff, 3, 20);
    pointLight.position.set(0, 4, 2);
    scene.add(pointLight);

    const monsterLight = new THREE.PointLight(0xff0055, 3, 20);
    monsterLight.position.set(3, 3, -2);
    scene.add(monsterLight);

    // 3. 바닥 (Floor)
    const gridHelper = new THREE.GridHelper(40, 40, 0x00ffff, 0x222244);
    gridHelper.position.y = -1;
    scene.add(gridHelper);

    // 4. [전사 3D 모델링 - 기하학 형태]
    const warriorGroup = new THREE.Group();
    const bodyGeo = new THREE.CylinderGeometry(0.5, 0.3, 1.5, 8);
    const bodyMat = new THREE.MeshStandardMaterial({{ color: 0x2a3b5c, metalness: 0.8, roughness: 0.2 }});
    const warriorBody = new THREE.Mesh(bodyGeo, bodyMat);
    warriorGroup.add(warriorBody);

    // 검 (Sword)
    const swordGeo = new THREE.BoxGeometry(0.1, 2.5, 0.2);
    const swordMat = new THREE.MeshStandardMaterial({{ color: 0x00ffff, emissive: 0x00aaaa, emissiveIntensity: 0.8 }});
    const sword = new THREE.Mesh(swordGeo, swordMat);
    sword.position.set(0.6, 0.5, -0.5);
    sword.rotation.x = Math.PI / 4;
    warriorGroup.add(sword);

    warriorGroup.position.set(-3, 0, 0);
    scene.add(warriorGroup);

    // 5. [몬스터 3D 모델링]
    const monsterGroup = new THREE.Group();
    const mGeo = new THREE.DodecahedronGeometry(1.3, 1);
    const mMat = new THREE.MeshStandardMaterial({{ color: 0xff1133, roughness: 0.4, wireframe: true }});
    const monster = new THREE.Mesh(mGeo, mMat);
    monsterGroup.add(monster);
    monsterGroup.position.set(3, 0.5, 0);
    scene.add(monsterGroup);

    // 6. 파티클 이펙트 (검기/폭발)
    const particleCount = 150;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    for(let i=0; i<particleCount*3; i++) {{
        positions[i] = (Math.random() - 0.5) * 10;
    }}
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    const pMaterial = new THREE.PointsMaterial({{ color: 0x00ffff, size: 0.15, transparent: true, opacity: 0.8 }});
    const particles = new THREE.Points(geometry, pMaterial);
    scene.add(particles);

    // 7. 애니메이션 로직
    let action = "{st.session_state.action}";
    let frame = 0;

    function animate() {{
        requestAnimationFrame(animate);
        frame += 0.05;

        // 대기 애니메이션 (Floating)
        monsterGroup.rotation.y += 0.02;
        monsterGroup.position.y = 0.5 + Math.sin(frame) * 0.2;

        particles.rotation.y += 0.005;

        // 공격 액션 연출
        if (action === "attack") {{
            if (warriorGroup.position.x < 1.5) {{
                warriorGroup.position.x += 0.3; // 돌진
                sword.rotation.z -= 0.3;
            }} else {{
                // 타격 시 이펙트 폭발
                monsterGroup.scale.set(1.3, 1.3, 1.3);
                pMaterial.color.setHex(0xff0055);
                camera.position.x = (Math.random() - 0.5) * 0.3; // 화면 흔들림
                camera.position.y = 3 + (Math.random() - 0.5) * 0.3;
            }}
        }} else {{
            warriorGroup.position.set(-3, 0, 0);
            sword.rotation.set(0, 0, 0);
            monsterGroup.scale.set(1, 1, 1);
            camera.position.set(0, 3, 10);
            pMaterial.color.setHex(0x00ffff);
        }}

        renderer.render(scene, camera);
    }}

    animate();
</script>
</body>
</html>
"""

# 3D 캔버스 렌더링 (Height: 400px)
components.html(three_js_code, height=420)

st.divider()

# ---------------------------------------------------------
# 4. 게임 조작 버튼 및 로직
# ---------------------------------------------------------
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    if st.button("⚔️ 3D 시네마틱 공격 실행!", type="primary", use_container_width=True):
        st.session_state.action = "attack"
        
        # 데미지 계산 및 HP 차감
        damage = st.session_state.level * 45 + random.randint(10, 50)
        st.session_state.monster_hp = max(0, st.session_state.monster_hp - damage)
        
        # 골드 획득
        st.session_state.gold += 150
        
        if st.session_state.monster_hp == 0:
            st.balloons()
            st.session_state.monster_hp = 1000
            st.session_state.gold += 1000
            st.toast("🔥 몬스터 처치 성공! 보너스 +1,000 Gold!", icon="🏆")
            
        st.rerun()

with col_btn2:
    if st.button("🔨 대장간 무기 강화하기 (비용: 300G)", use_container_width=True):
        if st.session_state.gold >= 300:
            st.session_state.gold -= 300
            st.session_state.action = "idle"
            
            # 확률 판정
            if random.random() < 0.65:
                st.session_state.level += 1
                st.toast(f"✨ 강화 성공! +{st.session_state.level} 단계 달성!", icon="🎉")
            else:
                st.toast("💔 강화 실패... 검의 기운이 불안정합니다.", icon="❌")
        else:
            st.error("골드가 부족합니다!")
            
        st.rerun()
