// plugins.config.js — 枪炮、病菌与钢铁统一插件配置
// 引擎自动加载此文件，所有插件配置集中于此。
// 旧版单文件（config/*.config.js）保留做降级回退。

// ── hero 动画函数 ──────────────────────────────────────

function buildHeroBackground() {
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

function startHeroAnimation(setStop) {
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

// ── 统一配置表 ──────────────────────────────────────────

export const configs = {

  // ── 引擎加载型（engine → plugin.init(core, localConfig)）──

  i18n: {
    defaultLang: 'zh',
  },

  chapter: {
    TOC_PAGE_ID: '目录',
  },

  hero: {
    buildHeroBackground,
    startHeroAnimation,
  },

};
