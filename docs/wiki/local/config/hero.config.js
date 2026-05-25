// hero.config.js — 枪炮、病菌与钢铁 Wiki hero background
// 矢量世界地图（CC0，Wikimedia Commons）：呼应书中"大陆轴线"主题。
// 地图缓慢东西向漂移，强化纬度轴线优势的视觉隐喻。

export function buildHeroBackground() {
  // hero-cosmos div 撑开 hero 高度（CSS clamp(260px,36vw,460px)）
  // hero-map-wrap 绝对定位铺满，承载世界地图
  return `
    <div class="hero-cosmos" style="background:#242933;"></div>
    <div id="hero-map-wrap" style="position:absolute;inset:0;overflow:hidden;">
      <img id="hero-worldmap"
           src="local/world-map.svg"
           alt=""
           style="position:absolute;width:118%;max-width:none;height:118%;top:-9%;left:-2%;object-fit:cover;object-position:center;opacity:0.48;">
    </div>`;
}

export function startHeroAnimation(setStop) {
  const el = document.getElementById('hero-worldmap');
  if (!el) return;

  const style = document.createElement('style');
  style.id = 'hero-worldmap-anim';
  style.textContent = `
    @keyframes map-drift {
      0%   { transform: translateX(0)   scale(1);     opacity: 0.42; }
      45%  { transform: translateX(4%)  scale(1.018); opacity: 0.52; }
      100% { transform: translateX(0)   scale(1);     opacity: 0.42; }
    }
    #hero-worldmap {
      animation: map-drift 35s ease-in-out infinite;
      will-change: transform, opacity;
    }
  `;
  document.head.appendChild(style);

  setStop(() => {
    style.remove();
    if (el) el.style.animation = '';
  });
}
