import streamlit as st
import streamlit.components.v1 as components
import random
import time

st.set_page_config(page_title="NEON RPG: OVERDRIVE 50", page_icon="⚔️", layout="centered")

# --- 🎨 Cyberpunk & High-End Neon Design CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=Noto+Sans+KR:wght@500;700;900&display=swap');

    .stApp {
        background: 
            radial-gradient(circle at 50% 20%, rgba(255, 0, 127, 0.25) 0%, transparent 60%),
            radial-gradient(circle at 80% 80%, rgba(0, 240, 255, 0.2) 0%, transparent 60%),
            linear-gradient(180deg, #090214 0%, #020005 100%);
        color: #ffffff;
        font-family: 'Noto Sans KR', sans-serif;
    }

    .game-title {
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        font-size: 2.6rem;
        font-weight: 900;
        letter-spacing: 4px;
        background: linear-gradient(180deg, #fff 0%, #00f0ff 50%, #ff007f 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(0, 240, 255, 0.8), 0 0 15px rgba(255, 0, 127, 0.6);
        margin-bottom: 25px;
    }

    .profile-card, .weapon-card-glow {
        background: rgba(15, 5, 30, 0.85);
        backdrop-filter: blur(12px);
        border: 2px solid rgba(0, 240, 255, 0.7);
        border-radius: 20px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.3), inset 0 0 15px rgba(0, 240, 255, 0.15);
    }
    .weapon-card-glow { 
        border-color: rgba(255, 0, 127, 0.9); 
        box-shadow: 0 0 30px rgba(255, 0, 127, 0.4), inset 0 0 20px rgba(255, 0, 127, 0.2);
    }

    .svg-container {
        width: 100%; height: 130px;
        display: flex; justify-content: center; align-items: center;
        background: radial-gradient(circle, rgba(0, 240, 255, 0.15) 0%, rgba(0,0,0,0.8) 100%);
        border-radius: 14px; margin-bottom: 12px;
        border: 1px solid rgba(255,255,255,0.12);
    }
    
    .battle-arena {
        background: radial-gradient(circle at center, rgba(40, 5, 60, 0.95) 0%, rgba(3, 0, 10, 0.98) 100%);
        border: 2px solid #ff007f;
        box-shadow: 0 0 45px rgba(255, 0, 127, 0.6), inset 0 0 25px rgba(0, 240, 255, 0.25);
        border-radius: 24px;
        padding: 22px;
        margin-top: 15px;
    }

    .battle-log-text {
        font-family: 'Orbitron', 'Noto Sans KR', sans-serif;
        font-size: 0.9rem;
        line-height: 1.6;
        background: rgba(0, 0, 0, 0.75);
        padding: 12px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    div.stButton > button {
        width: 100% !important; height: 50px !important; border-radius: 14px !important;
        font-weight: 900 !important; font-size: 1.1rem !important;
        background: linear-gradient(135deg, #ff007f 0%, #7928ca 50%, #00f0ff 100%) !important;
        color: #ffffff !important; border: none !important;
        box-shadow: 0 0 20px rgba(255, 0, 127, 0.5) !important;
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 0 35px rgba(0, 240, 255, 0.95) !important;
    }
    </style>
""", unsafe_allow_html=True)

def safe_rerun():
    if hasattr(st, "rerun"): st.rerun()
    elif hasattr(st, "experimental_rerun"): st.experimental_rerun()

# --- ⚔️ 진화 검 SVG 라이브러리 ---
WEAPON_SVGS = [
    '''<svg width="110" height="110" viewBox="0 0 100 100"><rect x="47" y="25" width="6" height="45" fill="#8D6E63"/><polygon points="45,25 50,15 55,25" fill="#A1887F"/><rect x="35" y="70" width="30" height="6" fill="#5D4037"/></svg>''',
    '''<svg width="110" height="110" viewBox="0 0 100 100"><path d="M 46 15 L 50 5 L 54 15 L 53 65 L 47 65 Z" fill="#CFD8DC" stroke="#37474F" stroke-width="2"/><line x1="50" y1="15" x2="50" y2="60" stroke="#90A4AE" stroke-width="1.5"/></svg>''',
    '''<svg width="110" height="110" viewBox="0 0 100 100"><path d="M 45 15 L 50 2 L 55 15 L 53 65 L 47 65 Z" fill="#9C27B0" stroke="#00f0ff" stroke-width="2"/><circle cx="50" cy="35" r="5" fill="#00f0ff" filter="drop-shadow(0 0 5px #00f0ff)"/></svg>''',
    '''<svg width="110" height="110" viewBox="0 0 100 100"><path d="M 44 10 L 50 0 L 56 10 L 54 65 L 46 65 Z" fill="#4CAF50" stroke="#1B5E20" stroke-width="2"/><circle cx="50" cy="25" r="4" fill="#A5D6A7"/></svg>''',
    '''<svg width="110" height="110" viewBox="0 0 100 100"><path d="M 44 12 L 50 0 L 56 12 L 54 65 L 46 65 Z" fill="#FFF9C4" stroke="#FFD700" stroke-width="2.5"/><polygon points="25,65 75,65 50,75" fill="#FFD700"/></svg>''',
    '''<svg width="110" height="110" viewBox="0 0 100 100"><path d="M 42 8 L 50 -5 L 58 8 L 55 65 L 45 65 Z" fill="#FF3D00" stroke="#BF360C" stroke-width="2.5" filter="drop-shadow(0 0 6px #FF3D00)"/></svg>''',
    '''<svg width="110" height="110" viewBox="0 0 100 100"><path d="M 43 5 L 50 -10 L 57 5 L 54 62 L 46 62 Z" fill="#00f0ff" filter="drop-shadow(0 0 12px #00f0ff)"/></svg>''',
    '''<svg width="110" height="110" viewBox="0 0 100 100"><path d="M 40 -8 L 50 -20 L 60 -8 L 56 65 L 44 65 Z" fill="#FF007F" filter="drop-shadow(0 0 18px #FF007F)"/><polygon points="15,65 85,65 50,82" fill="#FFD700" filter="drop-shadow(0 0 10px #FFD700)"/><circle cx="50" cy="20" r="8" fill="#00f0ff" filter="drop-shadow(0 0 12px #00f0ff)"/></svg>'''
]

def get_hero_title(lvl):
    if lvl < 10: return "초보 모험가"
    elif lvl < 20: return "숙련된 기사"
    elif lvl < 30: return "영웅 챔피언"
    elif lvl < 40: return "전설의 마스터"
    elif lvl < 50: return "신화의 오버로드"
    else: return "🌌 차원 절대신"

def get_weapon_info(lvl):
    names = [
        "녹슨 단검", "강철 장검", "룬 각인 검", "엘프의 명검", 
        "영웅의 성검", "용살자의 대검", "차원 파괴검", "🌌 신멸의 절망검"
    ]
    idx = min(lvl // 7, len(names) - 1)
    return {"name": names[idx], "svg": WEAPON_SVGS[idx]}

# 💥 50단계 보스 극악 난이도 재설계
def get_monster_info(step):
    prefix = ["말랑", "흉폭한", "저주받은", "심연의", "지옥의", "우주의", "멸망의", "절대"]
    base_names = ["슬라임", "고블린", "골렘", "미노타우로스", "드래곤", "크라켄", "요르문간드", "파괴자"]
    
    if step == 50:
        # 용사 50렙 + 검 50렙 총 스탯(HP: 18,000 / ATK: 300,000)을 보유해야 겨우 잡도록 밸런싱
        return {
            "name": "👑 [FINAL BOSS] 종말의 창조신 파괴자",
            "hp": 2200000,
            "atk": 2800,
            "skill": "⚡ 우주 멸망 소멸 포격",
            "reward": 1000000
        }
    
    p_idx = min((step - 1) // 7, len(prefix) - 1)
    b_idx = min((step - 1) // 7, len(base_names) - 1)
    
    name = f"{prefix[p_idx]} {base_names[b_idx]} (Lv.{step})"
    hp = int(300 * (1.20 ** step))
    atk = int(20 * (1.11 ** step))
    reward = int(400 * (1.20 ** step))
    
    return {"name": name, "hp": hp, "atk": atk, "skill": "💥 강격 파동", "reward": reward}

# --- 💾 Session State 초기화 ---
if "gold" not in st.session_state:
    st.session_state.hero_name = "용사님"
    st.session_state.hero_level = 1
    st.session_state.gold = 10000
    st.session_state.weapon_lvl = 0
    st.session_state.log = ["✨ 50단계 신화 모험이 시작되었습니다!"]

def get_hero_atk(): return st.session_state.hero_level * 1000

# 검 공격력 지수 증가 (50단계 도달 시 250,000 ATK 달성)
def get_weapon_atk(): 
    if st.session_state.weapon_lvl == 0: return 0
    return int(800 * (1.123 ** st.session_state.weapon_lvl))

def get_total_atk(): return get_hero_atk() + get_weapon_atk()
def get_max_hp(): return 800 + (st.session_state.hero_level * 344)

def get_w_cost(): return int(350 * (1.18 ** st.session_state.weapon_lvl))
def get_h_cost(): return int(400 * (1.15 ** st.session_state.hero_level))

def get_w_rate(): 
    return max(10.0, 100.0 - (st.session_state.weapon_lvl * 1.8))

def enhance_weapon():
    if st.session_state.weapon_lvl >= 50:
        st.toast("👑 검이 이미 최고 단계(50단계)에 도달했습니다!", icon="⭐")
        return
    if st.session_state.gold < get_w_cost():
        st.toast("⚠️ 골드가 부족합니다!", icon="💰")
        return
    st.session_state.gold -= get_w_cost()
    if random.uniform(0, 100) <= get_w_rate():
        st.session_state.weapon_lvl += 1
        st.toast(f"⚔️ 무기 강화 성공! (+{st.session_state.weapon_lvl})", icon="✨")
    else:
        st.toast("❌ 강화 실패! (등급 유지)", icon="🛡️")
    safe_rerun()

def enhance_hero():
    if st.session_state.hero_level >= 50:
        st.toast("👑 용사가 이미 최고 레벨(50단계)에 도달했습니다!", icon="⭐")
        return
    if st.session_state.gold < get_h_cost():
        st.toast("⚠️ 골드가 부족합니다!", icon="💰")
        return
    st.session_state.gold -= get_h_cost()
    st.session_state.hero_level += 1
    st.toast(f"🦸 레벨 업! (Lv.{st.session_state.hero_level})", icon="💪")
    safe_rerun()

# --- 🎨 화려해진 2D Canvas 렌더링 엔진 ---
def render_canvas_battle(hero_name, monster_name, monster_step, is_ultimate, damage, is_hero_turn, hero_level, render_id):
    is_final_boss = (monster_step == 50)
    
    html_code = f"""
    <div style="text-align: center;">
        <canvas id="battleCanvas_{render_id}" width="600" height="230" style="border-radius:15px; border:2px solid { "#ff007f" if is_final_boss else "#00f0ff" }; background: linear-gradient(180deg, #10002b 0%, #030008 100%); box-shadow: 0 0 25px { "rgba(255, 0, 127, 0.8)" if is_final_boss else "rgba(0, 240, 255, 0.4)" };"></canvas>
    </div>
    <script>
    (function() {{
        const canvas = document.getElementById('battleCanvas_{render_id}');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        let frame = 0;
        
        let heroX = 90;
        let monsterX = 470;
        let isFinalBoss = { 'true' if is_final_boss else 'false' };
        let mStep = {monster_step};
        let hLvl = {hero_level};
        let isUlt = { 'true' if is_ultimate else 'false' };
        let isHeroTurn = { 'true' if is_hero_turn else 'false' };

        function animate() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            if (isUlt && isHeroTurn && frame >= 10 && frame <= 20) {{
                let shakeX = (Math.random() - 0.5) * 14;
                let shakeY = (Math.random() - 0.5) * 14;
                ctx.setTransform(1, 0, 0, 1, shakeX, shakeY);
            }} else {{
                ctx.setTransform(1, 0, 0, 1, 0, 0);
            }}

            ctx.strokeStyle = isFinalBoss ? 'rgba(255, 0, 127, 0.25)' : 'rgba(0, 240, 255, 0.12)';
            ctx.lineWidth = 1;
            for(let x=0; x<canvas.width; x+=30) {{ ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,canvas.height); ctx.stroke(); }}
            for(let y=0; y<canvas.height; y+=30) {{ ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(canvas.width,y); ctx.stroke(); }}
            
            let hX = heroX;
            let mX = monsterX;
            let strike = false;
            
            if (isHeroTurn) {{
                if (frame < 10) hX += frame * 18;
                else if (frame < 20) {{ hX = 370; strike = true; mX += Math.sin(frame)*12; }}
                else hX -= (frame - 20) * 18;
            }} else {{
                if (frame < 10) mX -= frame * 18;
                else if (frame < 20) {{ mX = 190; strike = true; hX += Math.sin(frame)*12; }}
                else mX += (frame - 20) * 18;
            }}
            
            // 🦸 초화려 용사 비주얼 (날개 + 왕관 + 회전 차원 아우라)
            ctx.save();
            
            // 1. 차원 날개 연출
            ctx.fillStyle = 'rgba(0, 240, 255, 0.4)';
            ctx.shadowColor = '#00f0ff';
            ctx.shadowBlur = 15;
            ctx.beginPath();
            ctx.moveTo(hX, 115); ctx.lineTo(hX - 35, 80); ctx.lineTo(hX - 20, 115);
            ctx.moveTo(hX, 115); ctx.lineTo(hX + 35, 80); ctx.lineTo(hX + 20, 115);
            ctx.fill();

            // 2. 맥동하는 코어 아우라
            ctx.shadowBlur = 25 + Math.sin(frame*0.2)*10;
            ctx.fillStyle = '#00f0ff';
            ctx.beginPath(); ctx.arc(hX, 115, 25, 0, Math.PI*2); ctx.fill();
            
            // 3. 황금 왕관
            ctx.fillStyle = '#ffd700'; ctx.shadowColor = '#ffd700'; ctx.shadowBlur = 10;
            ctx.beginPath();
            ctx.moveTo(hX - 18, 98); ctx.lineTo(hX - 9, 82); ctx.lineTo(hX, 93); ctx.lineTo(hX + 9, 82); ctx.lineTo(hX + 18, 98);
            ctx.closePath(); ctx.fill();
            
            ctx.fillStyle = '#fff'; ctx.font = 'bold 12px Orbitron'; ctx.fillText('{hero_name}', hX - 25, 160);
            ctx.restore();
            
            // 👹 몬스터 비주얼
            ctx.save();
            if (isFinalBoss) {{
                let size = 52 + Math.sin(frame*0.2)*8;
                ctx.strokeStyle = '#ff0055'; ctx.lineWidth = 5; ctx.shadowColor = '#ff0055'; ctx.shadowBlur = 40;
                ctx.beginPath(); ctx.arc(mX, 115, size, 0, Math.PI*2); ctx.stroke();
                
                ctx.strokeStyle = '#ffd700'; ctx.lineWidth = 2;
                ctx.beginPath();
                for(let i=0; i<3; i++) {{
                    let ang = (frame*0.05) + (i * Math.PI * 2 / 3);
                    let rx = mX + Math.cos(ang) * (size + 15);
                    let ry = 115 + Math.sin(ang) * (size + 15);
                    if(i===0) ctx.moveTo(rx, ry); else ctx.lineTo(rx, ry);
                }}
                ctx.closePath(); ctx.stroke();
                
                ctx.fillStyle = '#110022'; ctx.fillRect(mX - 30, 115 - 30, 60, 60);
                ctx.fillStyle = '#ff0055'; ctx.beginPath(); ctx.arc(mX, 115, 15, 0, Math.PI*2); ctx.fill();
            }} else {{
                ctx.fillStyle = mStep >= 25 ? '#ff007f' : '#a100ff';
                ctx.shadowColor = '#a100ff'; ctx.shadowBlur = 15;
                let boxSize = 38 + Math.min(mStep, 50) * 0.4;
                ctx.fillRect(mX - boxSize/2, 115 - boxSize/2, boxSize, boxSize);
            }}
            ctx.fillStyle = '#fff'; ctx.font = 'bold 12px Orbitron'; ctx.fillText('{monster_name}', mX - 40, 165);
            ctx.restore();
            
            // ⚔️ 이펙트 연출
            if (strike) {{
                ctx.save();
                if (isHeroTurn) {{
                    if (isUlt) {{
                        ctx.strokeStyle = '#ffd700'; ctx.shadowColor = '#ffd700'; ctx.shadowBlur = 35; ctx.lineWidth = 10;
                        ctx.beginPath(); ctx.moveTo(mX - 60, 55); ctx.lineTo(mX + 60, 175); ctx.stroke();
                        ctx.beginPath(); ctx.moveTo(mX + 60, 55); ctx.lineTo(mX - 60, 175); ctx.stroke();
                        
                        ctx.strokeStyle = '#ff007f'; ctx.lineWidth = 6;
                        ctx.beginPath(); ctx.moveTo(mX - 70, 115); ctx.lineTo(mX + 70, 115); ctx.stroke();
                        
                        ctx.strokeStyle = '#00f0ff'; ctx.lineWidth = 3;
                        ctx.beginPath(); ctx.arc(mX, 115, 45 + (frame-10)*3, 0, Math.PI*2); ctx.stroke();
                    }} else {{
                        ctx.strokeStyle = '#00f0ff'; ctx.shadowColor = '#00f0ff'; ctx.shadowBlur = 20; ctx.lineWidth = 6;
                        ctx.beginPath(); ctx.moveTo(mX - 40, 70); ctx.lineTo(mX + 40, 160); ctx.stroke();
                    }}
                }} else {{
                    if (isFinalBoss) {{
                        ctx.strokeStyle = '#ff0055'; ctx.shadowColor = '#ff0055'; ctx.shadowBlur = 45; ctx.lineWidth = 18;
                        ctx.beginPath(); ctx.moveTo(mX, 115); ctx.lineTo(hX, 115); ctx.stroke();
                    }} else {{
                        ctx.strokeStyle = '#ff007f'; ctx.shadowColor = '#ff007f'; ctx.shadowBlur = 18; ctx.lineWidth = 6;
                        ctx.beginPath(); ctx.moveTo(hX + 35, 70); ctx.lineTo(hX - 35, 160); ctx.stroke();
                    }}
                }}
                
                ctx.fillStyle = isUlt ? '#ffd700' : '#ffff00';
                ctx.font = '900 28px Orbitron';
                let txtX = isHeroTurn ? mX : hX;
                ctx.fillText('-' + damage.toLocaleString(), txtX - 30, 45);
                ctx.restore();
            }}
            
            frame++;
            if (frame < 28) requestAnimationFrame(animate);
        }}
        animate();
    }})();
    </script>
    """
    return html_code

# --- 🖥️ UI Layout ---
st.markdown("<h1 class='game-title'>⚔️ OVERDRIVE BATTLE 50 ⚔️</h1>", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
m1.metric("💰 골드", f"{st.session_state.gold:,} G")
m2.metric("⚡ 총 공격력", f"{get_total_atk():,} ATK")
m3.metric("🦸 용사 단계", f"Lv.{st.session_state.hero_level} / 50")
m4.metric("🛡️ 검 단계", f"+{st.session_state.weapon_lvl} / 50")

st.markdown("---")

col_hero, col_weapon = st.columns(2)
w_info = get_weapon_info(st.session_state.weapon_lvl)

with col_hero:
    st.markdown(f"""
    <div class='profile-card'>
        <div class='svg-container'>
            <svg width="100" height="100" viewBox="0 0 100 100">
                <path d="M 15 50 Q 0 20 30 30 Z" fill="rgba(0,240,255,0.5)"/>
                <path d="M 85 50 Q 100 20 70 30 Z" fill="rgba(0,240,255,0.5)"/>
                <circle cx="50" cy="50" r="30" fill="#00f0ff" filter="drop-shadow(0 0 12px #00f0ff)"/>
                <polygon points="30,35 40,15 50,28 60,15 70,35" fill="#ffd700" filter="drop-shadow(0 0 8px #ffd700)"/>
            </svg>
        </div>
        <b>[{get_hero_title(st.session_state.hero_level)}] {st.session_state.hero_name}</b><br>
        HP: {get_max_hp():,} | ATK: {get_hero_atk():,}
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button(f"💪 용사 훈련 (비용: {get_h_cost():,}G)"): enhance_hero()

with col_weapon:
    st.markdown(f"""
    <div class='weapon-card-glow'>
        <div class='svg-container'>
            {w_info['svg']}
        </div>
        <b>+{st.session_state.weapon_lvl} {w_info['name']}</b><br>
        ATK: {get_weapon_atk():,} | 성공률: {get_w_rate():.1f}%
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button(f"🔨 검 강화 (비용: {get_w_cost():,}G)"): enhance_weapon()

st.markdown("---")

# --- 👹 전투 아레나 ---
st.subheader("⚔️ 50단계 실시간 격투 아레나")

skip_battle = st.checkbox("⏩ 전투 연출 SKIP (즉시 계산)", value=False)

m_step = st.slider("🎯 사냥할 괴물 단계 선택 (1 ~ 50단계)", 1, 50, st.session_state.hero_level)
monster = get_monster_info(m_step)

st.markdown(f"**상대 Monster**: <span style='color:#ff007f; font-weight:bold;'>{monster['name']}</span> | HP: {monster['hp']:,} | ATK: {monster['atk']:,}", unsafe_allow_html=True)

if st.button("⚡ 전투 개시!", use_container_width=True):
    hero_hp = get_max_hp()
    monster_hp = monster["hp"]
    base_atk = get_total_atk()
    
    st.markdown("<div class='battle-arena'>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"<h4 style='color:#00f0ff; text-align:center;'>🦸 {st.session_state.hero_name}</h4>", unsafe_allow_html=True)
        hero_bar = st.progress(1.0, text=f"HP: {hero_hp:,} / {get_max_hp():,}")
    with col_b:
        st.markdown(f"<h4 style='color:#ff007f; text-align:center;'>👹 {monster['name']}</h4>", unsafe_allow_html=True)
        monster_bar = st.progress(1.0, text=f"HP: {monster_hp:,} / {monster['hp']:,}")
    
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin:10px 0;'>", unsafe_allow_html=True)
    
    canvas_box = st.empty()
    status_display = st.empty()
    battle_log_box = st.empty()
    
    battle_logs = []
    turn = 1
    
    while hero_hp > 0 and monster_hp > 0:
        is_ultimate = (turn % 4 == 0)
        
        # 1. 용사의 공격
        if is_ultimate:
            atk_mult = 3.0
            skill_name = "💥 **[필살 차원 종말참]**"
            if not skip_battle: status_display.markdown("<h3 style='text-align:center; color:#ffd700;'>🔥 [4번째 턴] 필살 차원 참격 대폭발!!</h3>", unsafe_allow_html=True)
        else:
            atk_mult = 1.0
            skill_name = "🗡️ **[기본 검격]**"
            if not skip_battle: status_display.markdown(f"<h4 style='text-align:center; color:#00f0ff;'>🗡️ [{turn % 4}/3번째 턴] 용사의 검격!</h4>", unsafe_allow_html=True)
        
        is_crit = random.random() < 0.25
        crit_mult = 1.5 if is_crit else 1.0
        damage_to_monster = int(base_atk * atk_mult * crit_mult * random.uniform(0.9, 1.1))
        monster_hp = max(0, monster_hp - damage_to_monster)
        
        crit_text = "✨ **CRITICAL!** " if is_crit else ""
        battle_logs.append(f"<span style='color:#00f0ff;'>[Turn {turn}] 용사의 {skill_name}! {crit_text}<b>{damage_to_monster:,}</b> 피해!</span>")
        
        if not skip_battle:
            monster_bar.progress(monster_hp / monster['hp'], text=f"HP: {monster_hp:,} / {monster['hp']:,}")
            with canvas_box:
                components.html(render_canvas_battle(st.session_state.hero_name, monster['name'], m_step, is_ultimate, damage_to_monster, True, st.session_state.hero_level, f"h_{turn}_{time.time()}"), height=240)
            battle_log_box.markdown("<div class='battle-log-text'>" + "<br>".join(battle_logs[-4:]) + "</div>", unsafe_allow_html=True)
            time.sleep(0.8)
            
        if monster_hp <= 0:
            break
            
        # 2. 몬스터의 공격
        is_m_skill = random.random() < 0.35
        m_atk_mult = 1.8 if is_m_skill else random.uniform(0.9, 1.2)
        damage_to_hero = int(monster["atk"] * m_atk_mult)
        hero_hp = max(0, hero_hp - damage_to_hero)
        
        m_skill_text = f"☠️ <b>[{monster['skill']}]</b>" if is_m_skill else "🐾 <b>[일반 반격]</b>"
        battle_logs.append(f"<span style='color:#ff007f;'>[Turn {turn}] {monster['name']}의 {m_skill_text}! 용사에게 <b>{damage_to_hero:,}</b> 피해!</span>")
        
        if not skip_battle:
            hero_bar.progress(hero_hp / get_max_hp(), text=f"HP: {hero_hp:,} / {get_max_hp():,}")
            with canvas_box:
                components.html(render_canvas_battle(st.session_state.hero_name, monster['name'], m_step, False, damage_to_hero, False, st.session_state.hero_level, f"m_{turn}_{time.time()}"), height=240)
            battle_log_box.markdown("<div class='battle-log-text'>" + "<br>".join(battle_logs[-4:]) + "</div>", unsafe_allow_html=True)
            time.sleep(0.8)
            
        turn += 1

    if skip_battle:
        hero_bar.progress(hero_hp / get_max_hp(), text=f"HP: {hero_hp:,} / {get_max_hp():,}")
        monster_bar.progress(monster_hp / monster['hp'], text=f"HP: {monster_hp:,} / {monster['hp']:,}")
        status_display.markdown("<h3 style='text-align:center; color:#ff007f;'>⚡ 전투 즉시 완료!</h3>", unsafe_allow_html=True)
        battle_log_box.markdown("<div class='battle-log-text'>" + "<br>".join(battle_logs[-5:]) + "</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    if monster_hp <= 0:
        reward = monster['reward']
        st.session_state.gold += reward
        st.balloons()
        st.success(f"🎉 **토벌 완료!** [{monster['name']}]을(를) 물리치고 **{reward:,} Gold**를 획득했습니다!")
        st.session_state.log.append(f"🏆 [{monster['name']}] 토벌 성공 (+{reward:,} G)")
    else:
        penalty = int(monster['reward'] * 0.1)
        st.session_state.gold = max(0, st.session_state.gold - penalty)
        st.error(f"☠️ **전투 패배...** 괴물의 막강한 공격에 패배하여 {penalty:,} Gold를 잃었습니다.")
        st.session_state.log.append(f"💀 [{monster['name']}] 사냥 실패 (-{penalty:,} G)")

st.markdown("---")
with st.expander("📜 최근 모험 기록"):
    for log in reversed(st.session_state.log[-5:]):
        st.write(log)
