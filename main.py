<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>전설의 검 강화 시뮬레이터 v2.5</title>
  <style>
    /* 🎨 Cyberpunk & RPG Dark UI Styling */
    body {
      background: #0f172a;
      color: #f8fafc;
      font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      margin: 0;
    }

    .card {
      background: #1e293b;
      border-radius: 16px;
      padding: 28px;
      width: 340px;
      box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.5);
      border: 1px solid #334155;
      text-align: center;
    }

    .title {
      font-size: 1.1rem;
      color: #94a3b8;
      margin-bottom: 8px;
      font-weight: 600;
      letter-spacing: 1px;
    }

    .gold-box {
      font-size: 1.1rem;
      color: #facc15;
      font-weight: bold;
      margin-bottom: 16px;
    }

    .weapon-name {
      font-size: 2rem;
      font-weight: 800;
      color: #38bdf8;
      min-height: 2.5rem;
      transition: all 0.3s ease;
      margin-bottom: 16px;
    }

    .stats-box {
      background: #0f172a;
      border-radius: 8px;
      padding: 14px;
      margin-bottom: 16px;
      font-size: 0.95rem;
    }

    .stat-row {
      display: flex;
      justify-content: space-between;
      margin-bottom: 8px;
    }

    .stat-row:last-child {
      margin-bottom: 0;
    }

    .stat-label {
      color: #64748b;
    }

    .controls-box {
      margin-bottom: 16px;
      font-size: 0.9rem;
    }

    .controls-box label {
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
    }

    .btn {
      background: linear-gradient(135deg, #2563eb, #1d4ed8);
      color: white;
      border: none;
      padding: 14px;
      font-size: 1.1rem;
      font-weight: bold;
      border-radius: 8px;
      cursor: pointer;
      width: 100%;
      transition: all 0.2s ease;
    }

    .btn:hover:not(:disabled) {
      background: linear-gradient(135deg, #3b82f6, #2563eb);
      transform: translateY(-1px);
    }

    .btn:disabled {
      background: #475569;
      cursor: not-allowed;
      opacity: 0.7;
    }

    .log-box {
      margin-top: 14px;
      font-size: 0.9rem;
      height: 20px;
      font-weight: 600;
    }

    /* 🔥 Effect Animations */
    @keyframes pulse {
      0% { transform: scale(1); }
      50% { transform: scale(1.08); }
      100% { transform: scale(1); }
    }

    .success-anim {
      animation: pulse 0.4s ease-in-out;
    }
  </style>
</head>
<body>

<div class="card">
  <div class="title">⚔️ SWORD ENHANCE</div>
  <div class="gold-box">💰 <span id="goldValue">500</span> G <span style="font-size:0.75rem; color:#64748b; font-weight:normal;">(+15G/s)</span></div>
  
  <div class="weapon-name" id="weaponName">+0 롱소드</div>

  <div class="stats-box">
    <div class="stat-row">
      <span class="stat-label">공격력</span>
      <span id="atkValue" style="font-weight:600;">100</span>
    </div>
    <div class="stat-row">
      <span class="stat-label">강화 비용</span>
      <span id="costValue" style="color:#facc15; font-weight:600;">50 G</span>
    </div>
    <div class="stat-row">
      <span class="stat-label">성공 확률</span>
      <span id="rateValue" style="color:#4ade80; font-weight:600;">95%</span>
    </div>
    <div class="stat-row">
      <span class="stat-label">파괴 확률</span>
      <span id="destroyRateValue" style="color:#ef4444; font-weight:600;">0%</span>
    </div>
  </div>

  <div class="controls-box">
    <label><input type="checkbox" id="guardCheck" onchange="updateUI()"> 🛡️ 파괴 방지권 (비용 5배)</label>
  </div>

  <button class="btn" id="enhanceBtn" onclick="enhance()">강화하기</button>
  <div class="log-box" id="log">강화를 시작하세요!</div>
</div>

<script>
  let level = 0;
  let gold = 500;
  let isEnhancing = false;
  let isDestroyed = false;

  // 레벨별 정확한 확률 데이터
  const rates = [
    { rate: 95, destroy: 0 },
    { rate: 85, destroy: 0 },
    { rate: 75, destroy: 0 },
    { rate: 60, destroy: 0 },
    { rate: 50, destroy: 0 },
    { rate: 40, destroy: 1 },
    { rate: 30, destroy: 3 },
    { rate: 20, destroy: 5 },
    { rate: 10, destroy: 10 },
    { rate: 5,  destroy: 25 }
  ];

  // 1초마다 자동 골드 수급 (파밍 자동화)
  setInterval(() => {
    if (!isDestroyed) {
      gold += 15;
      updateUI();
    }
  }, 1000);

  function getActualCost() {
    const baseCost = 50 + (level * 25);
    return baseCost * (document.getElementById('guardCheck').checked ? 5 : 1);
  }

  function getCurrentRate() {
    return level >= rates.length ? { rate: 3, destroy: 50 } : rates[level];
  }

  function updateUI() {
    document.getElementById('goldValue').innerText = gold.toLocaleString();
    if (isDestroyed) return;

    const cost = getActualCost();
    const currentRate = getCurrentRate();
    const wName = document.getElementById('weaponName');
    
    wName.innerText = `+${level} 롱소드`;
    wName.style.color = level >= 7 ? "#f59e0b" : (level >= 4 ? "#a78bfa" : "#38bdf8");

    document.getElementById('atkValue').innerText = (100 + (level * 25)).toLocaleString();
    document.getElementById('costValue').innerText = `${cost.toLocaleString()} G`;
    document.getElementById('rateValue').innerText = `${currentRate.rate}%`;
    document.getElementById('destroyRateValue').innerText = `${currentRate.destroy}%`;

    const btn = document.getElementById('enhanceBtn');
    btn.disabled = isEnhancing || gold < cost;
    btn.innerText = isEnhancing ? "강화 중..." : (gold < cost ? "골드 부족" : "강화하기");
  }

  function enhance() {
    const cost = getActualCost();
    if (isEnhancing || isDestroyed || gold < cost) return;

    isEnhancing = true;
    gold -= cost;
    updateUI();

    const currentRate = getCurrentRate();
    const roll = Math.random() * 100; // 60% 지정 시 정확히 60% 확률 판정
    const guardActive = document.getElementById('guardCheck').checked;
    const logEl = document.getElementById('log');
    const wName = document.getElementById('weaponName');
    
    logEl.innerText = "망치질 중...";
    logEl.style.color = "#f8fafc";

    setTimeout(() => {
      wName.classList.remove('success-anim');

      if (roll < currentRate.rate) {
        // 성공
        level++;
        wName.classList.add('success-anim');
        logEl.innerText = `✨ 성공! (+${level} 달성)`;
        logEl.style.color = "#4ade80";
      } else {
        // 실패
        if (!guardActive && roll < (currentRate.rate + currentRate.destroy)) {
          // 파괴
          isDestroyed = true;
          wName.innerText = "💥 [파괴됨]";
          wName.style.color = "#ef4444";
          document.getElementById('enhanceBtn').disabled = true;
          document.getElementById('enhanceBtn').innerText = "강화 불가";
          logEl.innerText = "무기가 파괴되었습니다!";
          logEl.style.color = "#ef4444";
        } else {
          // 실패 (단계 하락 및 유지)
          if (level > 0 && level % 3 === 0) level--;
          logEl.innerText = "❌ 강화 실패 (단계 하락)";
          logEl.style.color = "#f87171";
        }
      }

      isEnhancing = false;
      updateUI();
    }, 800);
  }

  updateUI();
</script>

</body>
</html>
