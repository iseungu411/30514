import streamlit as st
import streamlit.components.v1 as components
import random

# ==========================================
# 1. 시스템 설정 및 세션 상태 초기화
# ==========================================
st.set_page_config(page_title="Dark Fantasy 3D RPG", page_icon="⚔️", layout="wide")

if 'game_screen' not in st.session_state:
    st.session_state.game_screen = "home"
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'gold' not in st.session_state:
    st.session_state.gold = 1000
if 'monster_hp' not in st.session_state:
    st.session_state.monster_hp = 2000
if 'action' not in st.session_state:
    st.session_state.action = "idle"
if 'play_sfx' not in st.session_state:
    st.session_state.play_sfx = False

# ==========================================
# 2. 커스텀 CSS (다크 판타지 UI 디자인)
# ==========================================
st.markdown("""
<style>
    .stApp { background-color: #050608; color: #ffffff; }
    .top-bar {
        background: linear-gradient(135deg, #0e111a, #1a1e2e);
        border: 1px solid #2d3548;
        border-radius: 12px;
        padding: 12px 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .boss-header {
        color: #ff2a4b;
        font-size: 24px;
        font-weight: bold;
        text-shadow: 0 0 12px #ff0022;
        text-align: center;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 오디오 시스템 (BGM 및 SFX 동기화)
# ==========================================
BGM_HOME = "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3"
BGM_BATTLE = "https://cdn.pixabay.com/download/audio/2022/03/15/audio_c8c8a73232.mp3"
SFX_ATTACK = "https://cdn.pixabay.com/download/audio/2022/03/10/audio_c2f42a9b47.mp3"

bgm_target = BGM_HOME if st.session_state.game_screen == "home" else BGM_BATTLE
sfx_trigger = "true" if st.session_state.play_sfx else "false"

components.html(f"""
<audio id="bgm" loop autoplay style="display:none;"><source src="{bgm_target}" type="audio/mp3"></audio>
<audio id="sfx" style="display:none;"><source src="{SFX_ATTACK}" type="audio/mp3"></audio>
<script>
    const bgm = document.getElementById('bgm');
    const sfx = document.getElementById('sfx');
    bgm.volume = 0.25;
    sfx.volume = 0.8;
    if ({sfx_trigger}) {{
        sfx.currentTime = 0;
        sfx.play().catch(e => console.log(e));
    }}
</script>
""", height=0)

st.session_state.play_sfx = False

# ==========================================
# 4. 상단 플레이어 리소스 UI (공통)
# ==========================================
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="top-bar">💰 <b>소지금:</b> <span style="color:#ffd700;">{st.session_state.gold:,} G</span></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="top-bar">🗡️ <b>무기:</b> <span style="color:#00ffff;">+{st.session_state.level} 마법검</span></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="top-bar">💥 <b>공격력:</b> <span style="color:#ff4d4f;">{st.session_state.level * 80 + 50} ATK</span></div>', unsafe_allow_html=True)

st.write("")

# ==========================================
# 5. [화면 A] 대장간 로비 (HOME)
# ==========================================
if st.session_state.game_screen == "home":
    st.title("🔨 중앙 대장간 (Lobby)")
    st.caption("무기를 강화하고 준비를 마친 후 던전으로 출격하세요.")
    
    col_l, col_r = st.columns([1.4, 1])
    
    with col_l:
        st.code(f"""
           /| ________________________________________
    O|===|* >___  [+{st.session_state.level} 마법 강화검]  ___>
           \\|
        ✨ 무기 등급: { "신화" if st.session_state.level >= 7 else "전설" if st.session_state.level >= 4 else "일반" }
        📜 강화 성공률: {max(10, 100 - st.session_state.level * 10)}%
        """, language="text")
        
        cost = 200 + (st.session_state.level * 150)
        if st.button(f"🔨 무기 강화 시도 ({cost:,} Gold)", use_container_width=True):
            if st.session_state.gold >= cost:
                st.session_state.gold -= cost
                if random.randint(1, 100) <= max(10, 100 - st.session_state.level * 10):
                    st.session_state.level += 1
                    st.balloons()
                    st.toast(f"🎉 강화 성공! +{st.session_state.level} 달성!", icon="✨")
                else:
                    st.snow()
                    if st.session_state.level > 1:
                        st.session_state.level -= 1
                    st.toast("💔 강화 실패... 무기 단계 하강.", icon="❌")
            else:
                st.error("골드가 부족합니다!")
            st.rerun()

    with col_r:
        st.subheader("👹 토벌 대상 정보")
        st.write("**보스:** 심연의 군주 아바돈")
        st.write("**난이도:** ★★★★★")
        st.caption("3D 실시간 전투 씬과 보스전 전용 OST가 출격 시 활성화됩니다.")
        st.write("")
        st.write("")
        if st.button("⚔️ 던전 출격 (전투 시작)", type="primary", use_container_width=True):
            st.session_state.game_screen = "battle"
            st.session_state.action = "idle"
            st.rerun()

# ==========================================
# 6. [화면 B] 3D 시네마틱 전투 화면 (BATTLE)
# ==========================================
elif st.session_state.game_screen == "battle":
    st.markdown('<div class="boss-header">👹 BOSS: 심연의 군주 아바돈 (LORD ABADDON)</div>', unsafe_allow_html=True)
    st.progress(st.session_state.monster_hp / 2000, text=f"HP: {st.session_state.monster_hp} / 2000")

    # Three.js 3D 엔진 연동 코드
    three_js_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>body {{ margin: 0; overflow: hidden; background: #000; }} canvas {{ width: 100vw; height: 100vh; display: block; }}</style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    </head>
    <body>
    <script>
        const scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x050608, 0.02);

        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 3.5, 9);

        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        scene.add(new THREE.AmbientLight(0xffffff, 0.5));
        
        const pLight1 = new THREE.PointLight(0xff0044, 4, 15);
        pLight1.position.set(3, 4, 0);
        scene.add(pLight1);

        const pLight2 = new THREE.PointLight(0x00ffff, 4, 15);
        pLight2.position.set(-3, 3, 2);
        scene.add(pLight2);

        const grid = new THREE.GridHelper(40, 40, 0xff0044, 0x111625);
        grid.position.y = -1;
        scene.add(grid);

        // [3D 용사 메쉬]
        const warrior = new THREE.Group();
        const wBody = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.2, 1.5, 8), new THREE.MeshStandardMaterial({{ color: 0x1d4ed8, metalness: 0.8 }}));
        warrior.add(wBody);
        
        const sword = new THREE.Mesh(new THREE.BoxGeometry(0.12, 2.5, 0.2), new THREE.MeshBasicMaterial({{ color: 0x00ffff }}));
        sword.position.set(0.6, 0.4, -0.4);
        sword.rotation.x = Math.PI / 4;
        warrior.add(sword);
        warrior.position.set(-3.2, 0, 0);
        scene.add(warrior);

        // [3D 보스 악당 메쉬]
        const boss = new THREE.Group();
        const bBody = new THREE.Mesh(new THREE.ConeGeometry(1.3, 2.6, 6), new THREE.MeshStandardMaterial({{ color: 0x111111, roughness: 0.2, metalness: 0.9 }}));
        boss.add(bBody);

        const bAura = new THREE.Mesh(new THREE.OctahedronGeometry(1.7, 2), new THREE.MeshBasicMaterial({{ color: 0xff0044, wireframe: true }}));
        boss.add(bAura);

        const hornMat = new THREE.MeshBasicMaterial({{ color: 0xff1133 }});
        const horn1 = new THREE.Mesh(new THREE.ConeGeometry(0.2, 1.2, 4), hornMat);
        horn1.position.set(-0.6, 1.5, 0);
        horn1.rotation.z = -0.4;
        const horn2 = new THREE.Mesh(new THREE.ConeGeometry(0.2, 1.2, 4), hornMat);
        horn2.position.set(0.6, 1.5, 0);
        horn2.rotation.z = 0.4;
        boss.add(horn1);
        boss.add(horn2);

        boss.position.set(3, 0.8, 0);
        scene.add(boss);

        // [3D 파티클 폭발 이펙트]
        const pCount = 350;
        const pGeo = new THREE.BufferGeometry();
        const pPos = new Float32Array(pCount * 3);
        for(let i=0; i<pCount*3; i++) pPos[i] = (Math.random() - 0.5) * 10;
        pGeo.setAttribute('position', new THREE.BufferAttribute(pPos, 3));
        const pMat = new THREE.PointsMaterial({{ color: 0xff0044, size: 0.12, transparent: true }});
        const particles = new THREE.Points(pGeo, pMat);
        scene.add(particles);

        let action = "{st.session_state.action}";
        let timer = 0;

        function animate() {{
            requestAnimationFrame(animate);
            timer += 0.05;
            
            bAura.rotation.y += 0.03;
            bAura.rotation.x += 0.01;
            boss.position.y = 0.8 + Math.sin(timer * 2) * 0.15;
            particles.rotation.y += 0.003;

            if (action === "attack") {{
                if (warrior.position.x < 1.8) {{
                    warrior.position.x += 0.45;
                    sword.rotation.z -= 0.5;
                }} else {{
                    boss.scale.set(1.35, 1.35, 1.35);
                    pMat.color.setHex(0x00ffff);
                    camera.position.x = (Math.random() - 0.5) * 0.5;
                    camera.position.y = 3.5 + (Math.random() - 0.5) * 0.5;
                }}
            }} else {{
                warrior.position.set(-3.2, 0, 0);
                sword.rotation.set(0, 0, 0);
                boss.scale.set(1, 1, 1);
                camera.position.set(0, 3.5, 9);
                pMat.color.setHex(0xff0044);
            }}

            renderer.render(scene, camera);
        }}
        animate();
    </script>
    </body>
    </html>
    """
    
    components.html(three_js_code, height=400)
    
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("⚔️ 필살 검기 공격!", type="primary", use_container_width=True):
            st.session_state.action = "attack"
            st.session_state.play_sfx = True
            
            damage = st.session_state.level * 80 + random.randint(40, 90)
            st.session_state.monster_hp = max(0, st.session_state.monster_hp - damage)
            st.session_state.gold += 200
            
            if st.session_state.monster_hp == 0:
                st.session_state.monster_hp = 2000
                st.session_state.gold += 3000
                st.toast("🔥 보스 처치 완료! +3,000 Gold 획득!", icon="🏆")
            else:
                st.toast(f"💥 {damage} 치명타 타격!", icon="🗡️")
            st.rerun()

    with btn_col2:
        if st.button("🚪 대장간(로비) 복귀", use_container_width=True):
            st.session_state.game_screen = "home"
            st.session_state.action = "idle"
            st.rerun()
