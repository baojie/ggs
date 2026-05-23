// hero.config.js — 枪炮、病菌与钢铁 Wiki hero background
// 大地色系漂流粒子：象征作物、牲畜、病菌在大陆间扩散的历史过程。
// 粒子沿「轴线」方向（东西向，呼应书中"轴线假说"）缓慢漂移，偶尔分裂繁殖。

export function buildHeroBackground() {
  return '<canvas id="hero-canvas" class="hero-cosmos" style="pointer-events:none;opacity:0.55;"></canvas>';
}

export function startHeroAnimation(setStop) {
  const canvas = document.getElementById('hero-canvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');

  // 大地色调：小麦黄 / 苔绿 / 赭红 / 沙棕
  const PALETTE = [
    'rgba(212, 168, 83,',   // 小麦
    'rgba(139, 154, 90,',   // 苔绿
    'rgba(196, 120, 74,',   // 赭红
    'rgba(180, 150, 110,',  // 沙棕
    'rgba(90, 130, 80,',    // 深绿
  ];
  const MAX_PARTICLES = 90;
  const AXIS_DRIFT    = 0.28;  // 东西轴漂移速度（呼应书中"纬度轴线"优势）
  const CROSS_DRIFT   = 0.06;  // 南北轻微漂移
  const SPAWN_RATE    = 0.004; // 每帧分裂概率

  let particles = [];
  let animId;

  function resize() {
    canvas.width  = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
  }

  function mkParticle(x, y) {
    const colorBase = PALETTE[Math.floor(Math.random() * PALETTE.length)];
    return {
      x:    x ?? Math.random() * canvas.width,
      y:    y ?? Math.random() * canvas.height,
      vx:   (Math.random() * 0.6 + 0.6) * (Math.random() > 0.15 ? 1 : -1) * AXIS_DRIFT,
      vy:   (Math.random() - 0.5) * 2 * CROSS_DRIFT,
      r:    Math.random() * 2.2 + 0.8,
      life: Math.random() * 300 + 200,
      age:  0,
      color: colorBase,
    };
  }

  function init() {
    resize();
    particles = Array.from({ length: 60 }, () => mkParticle());
    // 随机分散初始年龄，避免所有粒子同时消亡
    for (const p of particles) p.age = Math.random() * p.life;
  }

  function frame() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const toAdd = [];
    const toKeep = [];

    for (const p of particles) {
      p.x  += p.vx;
      p.y  += p.vy;
      p.age += 1;

      // 寿命计算：淡入淡出
      const progress = p.age / p.life;
      const alpha = progress < 0.15
        ? progress / 0.15
        : progress > 0.8
          ? (1 - progress) / 0.2
          : 1;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = p.color + (alpha * 0.85) + ')';
      ctx.fill();

      // 偶尔分裂（模拟物种扩散）
      if (p.age > 50 && Math.random() < SPAWN_RATE && particles.length + toAdd.length < MAX_PARTICLES) {
        toAdd.push(mkParticle(
          p.x + (Math.random() - 0.5) * 8,
          p.y + (Math.random() - 0.5) * 8
        ));
      }

      // 超出边界时从对侧重新进入（循环大陆）
      if (p.x > canvas.width + 10)  p.x = -10;
      if (p.x < -10)                 p.x = canvas.width + 10;
      if (p.y > canvas.height + 10 || p.y < -10) {
        p.y = Math.random() * canvas.height;
        p.x = Math.random() * canvas.width;
      }

      if (p.age < p.life) toKeep.push(p);
      else toKeep.push(mkParticle()); // 死亡后补充新粒子
    }

    particles = [...toKeep, ...toAdd].slice(0, MAX_PARTICLES);
    animId = requestAnimationFrame(frame);
  }

  function onResize() {
    resize();
  }

  init();
  frame();
  window.addEventListener('resize', onResize);

  setStop(() => {
    cancelAnimationFrame(animId);
    window.removeEventListener('resize', onResize);
  });
}
