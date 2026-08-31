import streamlit as st
import streamlit.components.v1 as components
import random

# 1. 페이지 및 게임 세션 상태 초기화
st.set_page_config(page_title="Dark Fantasy RPG with Audio", page_icon="⚔️", layout="wide")

if 'game_screen' not in st.session_state:
    st.session_state.game_screen = "home"
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'gold' not in st.session_state:
    st.session_state.gold = 1000
if 'monster_hp' not in st.session_state:
    st.session_state.monster_hp = 1500
if 'action' not in st.session_state:
    st.session_state.action = "idle"
if 'play_sfx' not in st.session_state:
    st.session_state.play_sfx = False

# 커스텀 CSS (다크 판타지 UI)
st.markdown("""
<style>
    .stApp { background-color: #06070c; color: #ffffff; }
    .top-bar {
        background: linear-gradient(135deg, #0d0f1b, #181b2e);
        border: 1px solid #2a2e4a;
        border-radius: 12px;
        padding: 12px 20px;
        margin-bottom: 20px;
    }
    .boss-bar-title {
        color: #ff334b;
        font-size: 22px;
        font-weight: bold;
        text-shadow: 0 0 10px #ff0022;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 사운드 시스템 (BGM & SFX 오디오 자동 재생)
# ---------------------------------------------------------
# 오디오 스트리밍 URL
BGM_HOME = "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3"  # 대장간 루프 음악
BGM_BATTLE = "https://cdn.pixabay.com/download/audio/2022/03/15/audio_c8c8a73232.mp3" # 웅장한 전투 음악
SFX_ATTACK = "https://cdn.pixabay.com/download/audio/2022/03/10/audio_c2f42a9b47.mp3" # 검 휘두르는 이펙트 음

# 화면 및 상태에 따른 오디오 스크립트 분기
bgm_target = BGM_HOME if st.session_state.game_screen == "home" else BGM_BATTLE
sfx_trigger = "true" if st.session_state.play_sfx else "false"

audio_html = f"""
<audio id="bgm" loop autoplay style="display:none;">
    <source src="{bgm_target}" type="audio/mp3">
</audio>
<audio id="sfx" style="display:none;">
    <source src="{SFX_ATTACK}" type="audio/mp3">
</audio>

<script>
    const bgm = document.getElementById('bgm');
    const sfx = document.getElementById('sfx');
    bgm.volume = 0.3;
    sfx.volume = 0.8;
    
    // SFX 재생 요청 시 검 효과음 출력
    if ({sfx_trigger}) {{
        sfx.currentTime = 0;
        sfx.play().catch(e => console.log("Audio play blocked by browser:", e));
    }}
</script>
"""
components.html(audio_html, height=0)

# SFX 플래그 초기화
st.session_state.play_sfx = False

# ---------------------------------------------------------
# 상단 리소스 바
# ---------------------------------------------------------
col_top1, col_top2, col_top3 = st.columns(3)
with col_top1:
    st.markdown(f'<div class="top-bar">💰 <b>골드:</b> <span style="color:#ffd700;">{st.session_state.gold:,} G</span></div>', unsafe_allow_html=True)
with col_top2:
    st.markdown(f'<div class="top-bar">🗡️ <b>무기:</b> <span style="color:#00ffff;">+{st.session_state.level} 각인검</span></div>', unsafe_allow_html=True)
with col_top3:
    st.markdown(f'<div class="top-bar">💥 <b>공격력:</b> <span style="color:#ff4d4f;">{st.session_state.level * 65 + 30} ATK</span></div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# [화면 1] 메인 로비 / 대장간 (HOME)
# ---------------------------------------------------------
if st.session_state.game_screen == "home":
    st.title("🔨 대장간 로비 🎵")
    st.caption("대장간 잔잔한 BGM 재생 중... 준비를 마치고 던전으로 출격하세요.")
    
    col_home1, col_home2 = st.columns([1.5, 1])
    
    with col_home1:
        st.code(f"""
           /| ________________________________________
    O|===|* >___  [+{st.session_state.level} 마법 각인검]  ___>
           \\|
        ✨ 무기 등급: { "전설" if st.session_state.level >= 5 else "희귀" if st.session_state.level >= 3 else "일반" }
        📜 강화 성공 확률: {max(15, 100 - st.session_state.level * 10)}%
        """, language="text")
        
        cost = 150 + (st.session_state.level * 100)
        if st.button(f"🔨 무기 강화하기 ({cost:,} G)", use_container_width=True):
            if st.session_state.gold >= cost:
                st.session_state.gold -= cost
                if random.randint(1, 100) <= max(15, 100 - st.session_state.level * 10):
                    st.session_state.level += 1
                    st.balloons()
                    st.toast(f"🎉 강화 성공! +{st.session_state.level} 단계 달성!", icon="✨")
                else:
                    st.snow()
                    if st.session_state.level > 1:
                        st.session_state.level -= 1
                    st.toast("💔 강화 실패... 단계가 감소했습니다.", icon="❌")
            else:
                st.error("골드가 부족합니다!")
            st.rerun()

    with col_home2:
        st.write("### 👹 던전 출격")
        st.write("보스: **심연의 군주 아바돈**")
        st.caption("전투 진입 시 긴박한 보스전 전용 OST로 전환됩니다.")
        st.write("")
        st.write("")
        if st.button("⚔️ 전투 시작 (던전 입장)", type="primary", use_container_width=True):
            st.session_state.game_screen = "battle"
            st.session_state.action = "idle"
            st.rerun()

# ---------------------------------------------------------
# [화면 2] 3D 시네마틱 전투 화면 (BATTLE)
# ---------------------------------------------------------
elif st.session_state.game_screen == "battle":
    st.markdown('<p class="boss-bar-title">👹 심연의 군주 아바돈 (LORD ABADDON) 🎵</p>', unsafe_allow_html=True)
    st.progress(st.session_state.monster_hp / 1500, text=f"BOSS HP: {st.session_state.monster_hp} / 1500")

    # Three.js 3D 실시간 전투 구현
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
        scene.fog = new THREE.FogExp2(0x06070c, 0.025);

        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 3.5, 9);

        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        scene.add(new THREE.AmbientLight(0xffffff, 0.6));
        
        const redLight = new THREE.PointLight(0xff0033, 5, 15);
        redLight.position.set(3, 4, 0);
        scene.add(redLight);

        const blueLight = new THREE.PointLight(0x00ffff, 4, 15);
        blueLight.position.set(-3, 3, 2);
        scene.add(blueLight);

        const grid = new THREE.GridHelper(40, 40, 0xff0044, 0x111322);
        grid.position.y = -1;
        scene.add(grid);

        // 3D Warrior
        const warrior = new THREE.Group();
        const wBody = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.2, 1.5, 8), new THREE.MeshStandardMaterial({{ color: 0x2563eb, metalness: 0.8 }}));
        warrior.add(wBody);
        
        const sword = new THREE.Mesh(new THREE.BoxGeometry(0.12, 2.5, 0.2), new THREE.MeshBasicMaterial({{ color: 0x00ffff }}));
        sword.position.set(0.6, 0.4, -0.4);
        sword.rotation.x = Math.PI / 4;
        warrior.add(sword);
        warrior.position.set(-3.2, 0, 0);
        scene.add(warrior);

        // 3D Boss
        const boss = new THREE.Group();
        const bBodyMat = new THREE.MeshStandardMaterial({{ color: 0x111111, roughness: 0.2, metalness: 0.9 }});
        const bBody = new THREE.Mesh(new THREE.ConeGeometry(1.2, 2.5, 6), bBodyMat);
        boss.add(bBody);

        const bAura = new THREE.Mesh(
            new THREE.OctahedronGeometry(1.6, 2),
            new THREE.MeshBasicMaterial({{ color: 0xff0044, wireframe: true }})
        );
        boss.add(bAura);

        const hornMat = new THREE.MeshBasicMaterial({{ color: 0xff1133 }});
        const horn1 = new THREE.Mesh(new THREE.ConeGeometry(0.2, 1, 4), hornMat);
        horn1.position.set(-0.6, 1.5, 0);
        horn1.rotation.z = -0.4;
        const horn2 = new THREE.Mesh(new THREE.ConeGeometry(0.2, 1, 4), hornMat);
        horn2.position.set(0.6, 1.5, 0);
        horn2.rotation.z = 0.4;
        boss.add(horn1);
        boss.add(horn2);

        boss.position.set(3, 0.8, 0);
        scene.add(boss);

        // Particles
        const pCount = 300;
        const pGeo = new THREE.BufferGeometry();
        const pPos = new Float32Array(pCount * 3);
        for(let i=0; i<pCount*3; i++) pPos[i] = (Math.random() - 0.5) * 10;
        pGeo.setAttribute('position', new THREE.BufferAttribute(pPos, 3));
        const pMat = new THREE.PointsMaterial({{ color: 0xff0044, size: 0.1, transparent: true }});
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
            particles.rotation.y += 0.002;

            if (action === "attack") {{
                if (warrior.position.x < 1.8) {{
                    warrior.position.x += 0.4;
                    sword.rotation.z -= 0.5;
                }} else {{
                    boss.scale.set(1.3, 1.3, 1.3);
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
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button("⚔️ 필살 검기 공격!", type="primary", use_container_width=True):
            st.session_state.action = "attack"
            st.session_state.play_sfx = True  # 검 효과음 동기화
            
            damage = st.session_state.level * 65 + random.randint(30, 80)
            st.session_state.monster_hp = max(0, st.session_state.monster_hp - damage)
            st.session_state.gold += 180
            
            if st.session_state.monster_hp == 0:
                st.session_state.monster_hp = 1500
                st.session_state.gold += 2000
                st.toast("🔥 보스 처치 성공! 보상 +2,000 Gold!", icon="🏆")
            else:
                st.toast(f"💥 {damage}의 치명타 데미지!", icon="🗡️")
            st.rerun()

    with col_b2:
        if st.button("🚪 대장간(홈)으로 복귀", use_container_width=True):
            st.session_state.game_screen = "home"
            st.session_state.action = "idle"
            st.rerun()
