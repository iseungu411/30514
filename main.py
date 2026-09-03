import streamlit as st
import streamlit.components.v1 as components
import random
import time

st.set_page_config(page_title="NEON RPG: OVERDRIVE BATTLE", page_icon="⚔️", layout="centered")

# --- 🎨 Cyberpunk & Neon Design CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=Noto+Sans+KR:wght@500;700;900&display=swap');

    .stApp {
        background: 
            radial-gradient(circle at 50% 30%, rgba(255, 0, 127, 0.15) 0%, transparent 60%),
            radial-gradient(circle at 80% 80%, rgba(0, 240, 255, 0.15) 0%, transparent 60%),
            linear-gradient(180deg, #120326 0%, #030008 100%);
        color: #ffffff;
        font-family: 'Noto Sans KR', sans-serif;
    }

    .game-title {
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        font-size: 2.8rem;
        font-weight: 900;
        letter-spacing: 3px;
        background: linear-gradient(180deg, #00f0ff 0%, #ff007f 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(0, 240, 255, 0.8), 0 0 10px rgba(255, 0, 127, 0.5);
        margin-bottom: 20px;
    }

    .profile-card, .weapon-card-glow {
        background: rgba(18, 8, 38, 0.75);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(0, 240, 255, 0.6);
        border-radius: 20px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.25), inset 0 0 15px rgba(0, 240, 255, 0.1);
    }
    .weapon-card-glow { 
        border-color: rgba(255, 0, 127, 0.8); 
        box-shadow: 0 0 20px rgba(255, 0, 127, 0.3), inset 0 0 15px rgba(255, 0, 127, 0.15);
    }

    .svg-container {
        width: 100%; height: 135px;
        display: flex; justify-content: center; align-items: center;
        background: radial-gradient(circle, rgba(0, 240, 255, 0.1) 0%, rgba(0,0,0,0.6) 100%);
        border-radius: 14px; margin-bottom: 12px;
        border: 1px solid rgba(255,255,255,0.08);
    }
    
    .battle-arena {
        background: radial-gradient(circle at center, rgba(35, 10, 55, 0.95) 0%, rgba(5, 1, 15, 0.98) 100%);
        border: 2px solid #ff007f;
        box-shadow: 0 0 40px rgba(255, 0, 127, 0.5), inset 0 0 20px rgba(0, 240, 255, 0.2);
        border-radius: 24px;
        padding: 22px;
        margin-top: 15px;
    }

    .battle-log-text {
        font-family: 'Orbitron', 'Noto Sans KR', sans-serif;
        font-size: 0.95rem;
        line-height: 1.7;
        background: rgba(0, 0, 0, 0.6);
        padding: 12px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    div.stButton > button {
        width: 100% !important; height: 55px !important; border-radius: 14px !important;
        font-weight: 900 !important; font-size: 1.15rem !important;
        background: linear-gradient(135deg, #ff007f 0%, #7928ca 50%, #00f0ff 100%) !important;
        color: #ffffff !important; border: none !important;
        box-shadow: 0 0 20px rgba(255, 0, 127, 0.5) !important;
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.9) !important;
    }
    </style>
""", unsafe_allow_html=True)

def safe_rerun():
    if hasattr(st, "rerun"): st.rerun()
    elif hasattr(st, "experimental_rerun"): st.experimental_rerun()

# --- 🎨 SVG Graphic Elements ---
HERO_SVGS = [
    '''<svg width="100" height="100" viewBox="0 0 100 100"><circle cx="50" cy="35" r="20" fill="#ffcc99"/><path d="M 20 90 Q 50 50 80 90" fill="#78909C"/><circle cx="43" cy="32" r="3" fill="#000"/><circle cx="57" cy="32" r="3" fill="#000"/></svg>''',
    '''<svg width="100" height="100" viewBox="0 0 100 100"><path d="M 25 20 L 75 20 L 70 85 L 50 95 L 30 85 Z" fill="#37474F" stroke="#00f0ff" stroke-width="2"/><rect x="35" y="35" width="30" height="8" fill="#00f0ff"/></svg>''',
    '''<svg width="100" height="100" viewBox="0 0 100 100"><circle cx="50" cy="50" r="45" fill="none" stroke="#ff007f" stroke-width="3"/><path d="M 20 25 L 80 25 L 75 85 L 50 100 L 25 85 Z" fill="#1A237E" stroke="#00f0ff" stroke-width="3"/><polygon points="50,15 60,35 40,35" fill="#ffd700"/></svg>'''
]

WEAPON_SVGS = [
    '''<svg width="100" height="100" viewBox="0 0 100 100"><rect x="47" y="20" width="6" height="50" fill="#8D6E63"/><rect x="35" y="70" width="30" height="6" fill="#5D4037"/><rect x="47" y="76" width="6" height="15" fill="#3E2723"/></svg>''',
    '''<svg width="100" height="100" viewBox="0 0 100 100"><path d="M 46 15 L 50 5 L 54 15 L 53 65 L 47 65 Z" fill="#B0BEC5" stroke="#37474F" stroke-width="2"/><rect x="35" y="65" width="30" height="6" fill="#455A64"/></svg>''',
    '''<svg width="100" height="100" viewBox="0 0 100 100"><path d="M 45 15 L 50 5 L 55 15 L 53 65 L 47 65 Z" fill="#7E57C2" stroke="#00f0ff" stroke-width="2"/><circle cx="50" cy="40" r="4" fill="#00f0ff"/></svg>''',
    '''<svg width="100" height="100" viewBox="0 0 100 100"><path d="M 46 10 L 50 2 L 54 10 L 53 65 L 47 65 Z" fill="#66BB6A" stroke="#2E7D32" stroke-width="2"/><polygon points="40,65 60,65 50,72" fill="#A5D6A7"/></svg>''',
    '''<svg width="100" height="100" viewBox="0 0 100 100"><path d="M 46 15 L 50 5 L 54 15 L 53 65 L 47 65 Z" fill="#ECEFF1" stroke="#FFD700" stroke-width="2"/><path d="M 30 65 L 70 65 L 50 72 Z" fill="#FFD700"/></svg>''',
    '''<svg width="100" height="100" viewBox="0 0 100 100"><path d="M 40 10 L 50 0 L 60 10 L 56 65 L 44 65 Z" fill="#FF5722" stroke="#BF360C" stroke-width="2"/><rect x="30" y="65" width="40" height="8" fill="#D84315"/></svg>''',
    '''<svg width="100" height="100" viewBox="0 0 100 100"><path d="M 45 10 L 50 0 L 55 10 L 54 60 L 46 60 Z" fill="#00f0ff" filter="drop-shadow(0 0 8px #00f0ff)"/><path d="M 25 60 L 75 60 L 50 70 Z" fill="#ff007f"/></svg>''',
    '''<svg width="100" height="100" viewBox="0 0 100 100"><path d="M 42 5 L 50 -5 L 58 5 L 55 65 L 45 65 Z" fill="#FF007F" filter="drop-shadow(0 0 12px #FF007F)"/><polygon points="30,65 70,65 50,75" fill="#FFD700"/></svg>'''
]

MONSTER_SVGS = [
    '''<svg width="120" height="120" viewBox="0 0 100 100"><path d="M 20 80 Q 10 40 50 30 Q 90 40 80 80 Q 50 95 20 80 Z" fill="#00E676"/><circle cx="40" cy="55" r="5" fill="#fff"/><circle cx="60" cy="55" r="5" fill="#fff"/></svg>''',
    '''<svg width="120" height="120" viewBox="0 0 100 100"><circle cx="50" cy="50" r="35" fill="#8D6E63"/><polygon points="30,20 40,35 20,35" fill="#5D4037"/><polygon points="70,20 80,35 60,35" fill="#5D4037"/></svg>''',
    '''<svg width="120" height="120" viewBox="0 0 100 100"><path d="M 25 30 L 75 30 L 70 85 L 30 85 Z" fill="#78909C"/><ellipse cx="50" cy="45" rx="15" ry="8" fill="#FF1744"/></svg>''',
    '''<svg width="120" height="120" viewBox="0 0 100 100"><path d="M 20 20 L 80 20 L 70 90 L 30 90 Z" fill="#3E2723"/><line x1="30" y1="40" x2="70" y2="40" stroke="#FFD54F" stroke-width="4"/></svg>''',
    '''<svg width="120" height="120" viewBox="0 0 100 100"><path d="M 30 30 L 70 30 L 85 60 L 50 90 L 15 60 Z" fill="#D50000"/><polygon points="50,10 35,30 65,30" fill="#FF6D00"/></svg>''',
    '''<svg width="120" height="120" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="#29B6F6"/><path d="M 20 50 Q 50 20 80 50 Q 50 80 20 50 Z" fill="#0288D1"/></svg>''',
    '''<svg width="120" height="120" viewBox="0 0 100 100"><path d="M 20 30 L 50 10 L 80 30 L 90 85 L 50 95 L 10 85 Z" fill="#311B92" stroke="#ff007f" stroke-width="2"/><ellipse cx="50" cy="50" rx="15" ry="8" fill="#ff007f"/></svg>''',
    '''<svg width="120" height="120" viewBox="0 0 100 100"><polygon points="50,5 90,30 80,85 20,85 10,30" fill="#1A237E" stroke="#00f0ff" stroke-width="3"/><circle cx="50" cy="50" r="15" fill="#FF007F"/></svg>'''
]

HERO_TIERS = [{"title": "초보 모험가", "svg": HERO_SVGS[0]}, {"title": "영웅 기사", "svg": HERO_SVGS[1]}, {"title": "신화의 오버로드", "svg": HERO_SVGS[2]}]

WEAPON_TIERS = [
    {"name": "낡은 수련검", "base": 25, "svg": WEAPON_SVGS[0]},
    {"name": "강철 장검", "base": 60, "svg": WEAPON_SVGS[1]},
    {"name": "룬 각인 검", "base": 110, "svg": WEAPON_SVGS[2]},
    {"name": "엘프의 명검", "base": 180, "svg": WEAPON_SVGS[3]},
    {"name": "영웅의 성검", "base": 280, "svg": WEAPON_SVGS[4]},
    {"name": "용살자의 대검", "base": 420, "svg": WEAPON_SVGS[5]},
    {"name": "차원 파괴검", "base": 600, "svg": WEAPON_SVGS[6]},
    {"name": "신화의 오버로드 블레이드", "base": 1000, "svg": WEAPON_SVGS[7]}
]

MONSTERS = [
    {"name": "말랑 슬라임", "hp": 150, "atk": 15, "skill": "💦 액체 체벌", "reward": 250, "svg": MONSTER_SVGS[0]},
    {"name": "고블린 족장", "hp": 320, "atk": 35, "skill": "🪓 몽둥이 난타", "reward": 600, "svg": MONSTER_SVGS[1]},
    {"name": "저주받은 골렘", "hp": 700, "atk": 65, "skill": "🪨 암석 내려찍기", "reward": 1400, "svg": MONSTER_SVGS[2]},
    {"name": "지옥 미노타우로스", "hp": 1300, "atk": 120, "skill": "🐂 붉은 뿔 돌진", "reward": 3000, "svg": MONSTER_SVGS[3]},
    {"name": "지옥 화염 드래곤", "hp": 2400, "atk": 200, "skill": "🔥 브레스 대폭발", "reward": 6000, "svg": MONSTER_SVGS[4]},
    {"name": "심연의 크라켄", "hp": 4000, "atk": 280, "skill": "🐙 해일 해저 조르기", "reward": 10000, "svg": MONSTER_SVGS[5]},
    {"name": "세계뱀 요르문간드", "hp": 7000, "atk": 420, "skill": "🐍 맹독 차원 소용돌이", "reward": 20000, "svg": MONSTER_SVGS[6]},
    {"name": "종말의 신 파괴자", "hp": 13000, "atk": 680, "skill": "⚡ 우주 멸망 일격", "reward": 45000, "svg": MONSTER_SVGS[7]}
]

if "gold" not in st.session_state:
    st.session_state.hero_name = "용사님"
    st.session_state.hero_level = 1
    st.session_state.gold = 3000
    st.session_state.weapon_lvl = 0
    st.session_state.protection_scrolls = 1
    st.session_state.log = ["✨ 광활한 네온 세계의 모험이 시작되었습니다!"]

def get_hero_tier_idx(): return 2 if st.session_state.hero_level >= 15 else (1 if st.session_state.hero_level >= 7 else 0)
def get_weapon_tier_idx(): return min(st.session_state.weapon_lvl // 3, len(WEAPON_TIERS) - 1)
def get_hero_atk(): return st.session_state.hero_level * 35
def get_weapon_atk(): return WEAPON_TIERS[get_weapon_tier_idx()]["base"] + (st.session_state.weapon_lvl * 30)
def get_total_atk(): return get_hero_atk() + get_weapon_atk()
def get_max_hp(): return 250 + (st.session_state.hero_level * 90)
def get_w_cost(): return (st.session_state.weapon_lvl + 1) * 350
def get_h_cost(): return st.session_state.hero_level * 400
def get_w_rate(): return max(10, 100 - (st.session_state.weapon_lvl * 4))

def enhance_weapon():
    if st.session_state.gold < get_w_cost():
        st.toast("⚠️ 골드가 부족합니다!", icon="💰")
        return
    st.session_state.gold -= get_w_cost()
    if random.randint(1, 100) <= get_w_rate():
        st.session_state.weapon_lvl += 1
        st.toast(f"⚔️ 무기 강화 성공! (+{st.session_state.weapon_lvl})", icon="✨")
    else:
        if st.session_state.protection_scrolls > 0 and st.session_state.weapon_lvl >= 5:
            st.session_state.protection_scrolls -= 1
            st.toast("🛡️ 파괴 방지권 사용으로 등급 유지!", icon="🛡️")
        else:
            st.session_state.weapon_lvl = max(0, st.session_state.weapon_lvl - 1)
            st.toast("❌ 강화 실패...", icon="💀")
    safe_rerun()

def enhance_hero():
    if st.session_state.gold < get_h_cost():
        st.toast("⚠️ 골드가 부족합니다!", icon="💰")
        return
    st.session_state.gold -= get_h_cost()
    st.session_state.hero_level += 1
    st.toast(f"🦸 레벨 업! (Lv.{st.session_state.hero_level})", icon="💪")
    safe_rerun()

# 🎨 [동적 고품질 Canvas 애니메이션 엔진]
def render_canvas_battle(hero_name, monster_name, monster_tier, is_ultimate, damage, is_hero_turn, hero_level):
    is_boss = (monster_tier >= 3)  # 4단계 이상부터 고난도 보스 이펙트 적용
    is_high_hero = (hero_level >= 7)

    html_code = f"""
    <div style="text-align: center;">
        <canvas id="battleCanvas" width="600" height="230" style="border-radius:15px; border:2px solid { "#ff0055" if is_boss else "#00f0ff" }; background: linear-gradient(180deg, #10002b 0%, #030008 100%); box-shadow: 0 0 25px { "rgba(255, 0, 85, 0.6)" if is_boss else "rgba(0, 240, 255, 0.4)" };"></canvas>
    </div>
    <script>
    (function() {{
        const canvas = document.getElementById('battleCanvas');
        const ctx = canvas.getContext('2d');
        let frame = 0;
        
        let heroX = 90;
        let monsterX = 470;
        let isBoss = { 'true' if is_boss else 'false' };
        let isHighHero = { 'true' if is_high_hero else 'false' };
        let monsterTier = {monster_tier};
        
        function animate() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // 🌌 배경 사이버네틱 그리드 연출
            ctx.strokeStyle = isBoss ? 'rgba(255, 0, 100, 0.15)' : 'rgba(0, 240, 255, 0.12)';
            ctx.lineWidth = 1;
            for(let x=0; x<canvas.width; x+=30) {{ ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,canvas.height); ctx.stroke(); }}
            for(let y=0; y<canvas.height; y+=30) {{ ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(canvas.width,y); ctx.stroke(); }}
            
            let hX = heroX;
            let mX = monsterX;
            let strike = false;
            
            // 이동 애니메이션 계산
            if ({ 'true' if is_hero_turn else 'false' }) {{
                if (frame < 12) hX += frame * 17;
                else if (frame < 22) {{ hX = 370; strike = true; mX += Math.sin(frame)*12; }}
                else hX -= (frame - 22) * 17;
            }} else {{
                if (frame < 12) mX -= frame * 17;
                else if (frame < 22) {{ mX = 190; strike = true; hX += Math.sin(frame)*12; }}
                else mX += (frame - 22) * 17;
            }}
            
            // 🦸 1. 용사 캐릭터 연출 (티어에 따른 오라 차이)
            ctx.save();
            if (isHighHero) {{
                // 영웅/신화 티어: 황금빛 아우라
                ctx.strokeStyle = '#ffd700'; ctx.lineWidth = 3; ctx.shadowColor = '#ffd700'; ctx.shadowBlur = 20;
                ctx.beginPath(); ctx.arc(hX, 120, 32 + Math.sin(frame*0.3)*3, 0, Math.PI*2); ctx.stroke();
            }}
            ctx.fillStyle = isHighHero ? '#00ffff' : '#00f0ff';
            ctx.shadowColor = '#00f0ff'; ctx.shadowBlur = 15;
            ctx.beginPath(); ctx.arc(hX, 120, 24, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = '#fff'; ctx.font = 'bold 12px Orbitron'; ctx.fillText('{hero_name}', hX - 25, 168);
            ctx.restore();
            
            // 👹 2. 몬스터 캐릭터 연출 (강한 몬스터일수록 웅장한 아우라 및 회전 마법진)
            ctx.save();
            if (isBoss) {{
                // 🔴 보스급: 회전하는 멸망의 마법진 & 거대 붉은 아우라
                let auraSize = 35 + monsterTier * 3;
                ctx.strokeStyle = '#ff0055'; ctx.lineWidth = 3; ctx.shadowColor = '#ff0055'; ctx.shadowBlur = 25;
                ctx.beginPath(); ctx.arc(mX, 120, auraSize + Math.sin(frame*0.4)*5, 0, Math.PI*2); ctx.stroke();
                
                // 마법진 오각성 회전
                ctx.strokeStyle = 'rgba(255, 0, 100, 0.4)';
                ctx.beginPath();
                for(let i=0; i<5; i++) {{
                    let ang = (frame*0.05) + (i * Math.PI * 2 / 5);
                    let rx = mX + Math.cos(ang) * (auraSize + 10);
                    let ry = 120 + Math.sin(ang) * (auraSize + 10);
                    if(i===0) ctx.moveTo(rx, ry); else ctx.lineTo(rx, ry);
                }}
                ctx.closePath(); ctx.stroke();
            }}
            
            // 몬스터 본체
            ctx.fillStyle = isBoss ? '#ff0055' : '#a100ff';
            ctx.shadowColor = isBoss ? '#ff0055' : '#a100ff'; ctx.shadowBlur = 15;
            let boxSize = 46 + monsterTier * 2;
            ctx.fillRect(mX - boxSize/2, 120 - boxSize/2, boxSize, boxSize);
            ctx.fillStyle = '#fff'; ctx.font = 'bold 12px Orbitron'; ctx.fillText('{monster_name}', mX - 30, 168);
            ctx.restore();
            
            // ⚔️ 3. 공격 & 타격 스킬 화려한 이펙트 연출
            if (strike) {{
                ctx.save();
                if ({ 'true' if is_hero_turn else 'false' }) {{
                    // 용사의 공격
                    if ({ 'true' if is_ultimate else 'false' }) {{
                        // 🔥 4번째 턴 [필살 차원참]: 3중 네온 십자 검격 & 화면 붉은 섬광
                        ctx.strokeStyle = '#ff007f'; ctx.shadowColor = '#ff007f'; ctx.shadowBlur = 30; ctx.lineWidth = 9;
                        ctx.beginPath(); ctx.moveTo(mX - 50, 70); ctx.lineTo(mX + 50, 170); ctx.stroke();
                        ctx.beginPath(); ctx.moveTo(mX + 50, 70); ctx.lineTo(mX - 50, 170); ctx.stroke();
                        ctx.strokeStyle = '#00f0ff'; ctx.lineWidth = 5;
                        ctx.beginPath(); ctx.moveTo(mX - 60, 120); ctx.lineTo(mX + 60, 120); ctx.stroke();
                    }} else {{
                        // 일반 검격
                        ctx.strokeStyle = '#00f0ff'; ctx.shadowColor = '#00f0ff'; ctx.shadowBlur = 15; ctx.lineWidth = 5;
                        ctx.beginPath(); ctx.moveTo(mX - 40, 80); ctx.lineTo(mX + 40, 160); ctx.stroke();
                    }}
                }} else {{
                    // 몬스터의 공격 (강한 몬스터일수록 거대한 폭발 이펙트)
                    if (isBoss) {{
                        ctx.strokeStyle = '#ff0000'; ctx.shadowColor = '#ff0000'; ctx.shadowBlur = 35; ctx.lineWidth = 10;
                        ctx.beginPath(); ctx.arc(hX, 120, 45, 0, Math.PI*2); ctx.stroke();
                        ctx.fillStyle = 'rgba(255,0,0,0.3)'; ctx.fill();
                    }} else {{
                        ctx.strokeStyle = '#ff007f'; ctx.shadowColor = '#ff007f'; ctx.shadowBlur = 15; ctx.lineWidth = 5;
                        ctx.beginPath(); ctx.moveTo(hX + 30, 80); ctx.lineTo(hX - 30, 160); ctx.stroke();
                    }}
                }}
                
                // 데미지 폰트 텍스트 연출
                ctx.fillStyle = isBoss && !{ 'true' if is_hero_turn else 'false' } ? '#ff0000' : '#ffff00';
                ctx.font = 'bold 26px Orbitron';
                let txtX = { 'mX' if is_hero_turn else 'hX' };
                ctx.fillText('-{damage:,}', txtX - 25, 55);
                ctx.restore();
            }}
            
            frame++;
            if (frame < 30) requestAnimationFrame(animate);
        }}
        animate();
    }})();
    </script>
    """
    return html_code

# --- 🖥️ UI Layout ---
st.markdown("<h1 class='game-title'>⚔️ OVERDRIVE BATTLE ⚔️</h1>", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
m1.metric("💰 골드", f"{st.session_state.gold:,} G")
m2.metric("⚡ 총 공격력", f"{get_total_atk():,} ATK")
m3.metric("🦸 히어로", f"Lv.{st.session_state.hero_level}")
m4.metric("🛡️ 무기 강화", f"+{st.session_state.weapon_lvl}")

st.markdown("---")

col_hero, col_weapon = st.columns(2)
hero_info = HERO_TIERS[get_hero_tier_idx()]
weapon_info = WEAPON_TIERS[get_weapon_tier_idx()]

with col_hero:
    st.markdown(f"<div class='profile-card'><div class='svg-container'>{hero_info['svg']}</div><b>[{hero_info['title']}] {st.session_state.hero_name}</b><br>HP: {get_max_hp():,} | ATK: {get_hero_atk():,}</div>", unsafe_allow_html=True)
    st.write("")
    if st.button("💪 히어로 훈련 (+Level)"): enhance_hero()

with col_weapon:
    st.markdown(f"<div class='weapon-card-glow'><div class='svg-container'>{weapon_info['svg']}</div><b>+{st.session_state.weapon_lvl} {weapon_info['name']}</b><br>ATK: {get_weapon_atk():,} | 성공률: {get_w_rate()}%</div>", unsafe_allow_html=True)
    st.write("")
    if st.button("🔨 명검 강화 (+Forge)"): enhance_weapon()

st.markdown("---")

# --- 👹 2D CANVAS 실시간 격투 아레나 ---
st.subheader("⚔️ 괴물 실시간 격투 아레나")
st.info("🔥 **티어 비주얼 연출**: 고단 보스 몬스터일수록 **회전 마법진과 거대 아우라**가 발동하며, 용사 레벨 상승 시 **황금 오라 및 필살 3중 차원참 연출**이 펼쳐집니다!")

skip_battle = st.checkbox("⏩ 전투 연출 SKIP (결과 즉시 계산)", value=False)

m_idx = st.selectbox(
    "🎯 사냥할 괴물 선택", 
    range(len(MONSTERS)), 
    format_func=lambda x: f"[{x+1}단계] {MONSTERS[x]['name']} (권장 ATK: {MONSTERS[x]['hp']//3})"
)
monster = MONSTERS[m_idx]

# 전투 개시
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
            atk_mult = 2.5
            skill_name = "💥 **[필살 3중 차원참]**"
            if not skip_battle: status_display.markdown("<h3 style='text-align:center; color:#ff007f;'>🔥 [4번째 턴] 필살 차원참 장전 및 십자 격파!!</h3>", unsafe_allow_html=True)
        else:
            atk_mult = 1.0
            skill_name = "🗡️ **[기본 검격]**"
            if not skip_battle: status_display.markdown(f"<h4 style='text-align:center; color:#00f0ff;'>🗡️ [{turn % 4}/3번째 턴] 용사의 기본 공격!</h4>", unsafe_allow_html=True)
        
        is_crit = random.random() < 0.25
        crit_mult = 1.5 if is_crit else 1.0
        damage_to_monster = int(base_atk * atk_mult * crit_mult * random.uniform(0.9, 1.1))
        monster_hp = max(0, monster_hp - damage_to_monster)
        
        crit_text = "✨ **CRITICAL!** " if is_crit else ""
        battle_logs.append(f"<span style='color:#00f0ff;'>[Turn {turn}] 용사의 {skill_name}! {crit_text}<b>{damage_to_monster:,}</b> 피해!</span>")
        
        if not skip_battle:
            monster_bar.progress(monster_hp / monster['hp'], text=f"HP: {monster_hp:,} / {monster['hp']:,}")
            with canvas_box:
                components.html(render_canvas_battle(st.session_state.hero_name, monster['name'], m_idx, is_ultimate, damage_to_monster, True, st.session_state.hero_level), height=240)
            battle_log_box.markdown("<div class='battle-log-text'>" + "<br>".join(battle_logs[-4:]) + "</div>", unsafe_allow_html=True)
            time.sleep(0.85)
            
        if monster_hp <= 0:
            break
            
        # 2. 몬스터의 공격
        is_m_skill = random.random() < 0.35
        m_atk_mult = 1.7 if is_m_skill else random.uniform(0.8, 1.1)
        damage_to_hero = int(monster["atk"] * m_atk_mult)
        hero_hp = max(0, hero_hp - damage_to_hero)
        
        m_skill_text = f"☠️ <b>[{monster['skill']}]</b>" if is_m_skill else "🐾 <b>[일반 반격]</b>"
        battle_logs.append(f"<span style='color:#ff007f;'>[Turn {turn}] {monster['name']}의 {m_skill_text}! 용사에게 <b>{damage_to_hero:,}</b> 피해!</span>")
        
        if not skip_battle:
            hero_bar.progress(hero_hp / get_max_hp(), text=f"HP: {hero_hp:,} / {get_max_hp():,}")
            with canvas_box:
                components.html(render_canvas_battle(st.session_state.hero_name, monster['name'], m_idx, False, damage_to_hero, False, st.session_state.hero_level), height=240)
            battle_log_box.markdown("<div class='battle-log-text'>" + "<br>".join(battle_logs[-4:]) + "</div>", unsafe_allow_html=True)
            time.sleep(0.85)
            
        turn += 1

    # SKIP 모드 시 최종 결과 및 로그 일괄 출력
    if skip_battle:
        hero_bar.progress(hero_hp / get_max_hp(), text=f"HP: {hero_hp:,} / {get_max_hp():,}")
        monster_bar.progress(monster_hp / monster['hp'], text=f"HP: {monster_hp:,} / {monster['hp']:,}")
        status_display.markdown("<h3 style='text-align:center; color:#ff007f;'>⚡ 전투 즉시 완료!</h3>", unsafe_allow_html=True)
        battle_log_box.markdown("<div class='battle-log-text'>" + "<br>".join(battle_logs[-5:]) + "</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # 🏆 보상 / 패배 판정
    if monster_hp <= 0:
        reward = monster['reward'] + random.randint(100, 1000)
        st.session_state.gold += reward
        st.balloons()
        st.success(f"🎉 **토벌 완료!** [{monster['name']}]을(를) 물리치고 **{reward:,} Gold**를 획득했습니다!")
        st.session_state.log.append(f"🏆 [{monster['name']}] 토벌 성공 (+{reward:,} G)")
    else:
        penalty = random.randint(400, 1500)
        st.session_state.gold = max(0, st.session_state.gold - penalty)
        st.error(f"☠️ **전투 패배...** 괴물의 공격에 패배하여 치료비로 {penalty:,} Gold를 지불했습니다.")
        st.session_state.log.append(f"💀 [{monster['name']}] 사냥 실패 (-{penalty:,} G)")

st.markdown("---")
with st.expander("📜 최근 모험 기록"):
    for log in reversed(st.session_state.log[-5:]):
        st.write(log)
