// LocalSettings.js — 枪炮、病菌与钢铁 Wiki 本地配置

export const wgSiteName = '枪炮、病菌与钢铁';

export const wgEnabledPlugins = [
  // ── localConfig: required ─────────────────────────────────────────────────
  'i18n',             // 多语言（i18n.config.js）

  // ── localConfig: no（core，始终加载）──────────────────────────────────────
  'variable',
  'recent',
  'diff',
  'browse',
  'sidebar',
  'bold-terms',

  // ── localConfig: optional ─────────────────────────────────────────────────
  'category',
  // ── localConfig: no（core）
  'page-footer',
  // ── localConfig: optional
  'chapter',          // chapter.config.js
  // ── localConfig: no（core）
  'toc',
  'infobox',
  // ── localConfig: optional
  'hero',             // hero.config.js
  // ── localConfig: no（core）
  'search',
  'home',

  // ── localConfig: no（非 core）─────────────────────────────────────────────
  'autolink',
  'pn-citation',
  'footnote',
  'backlinks',
  'sealso',
  'source-view',
  'want-button',
  'math',
  'semantic-history',
  'page-marker',
  'math-array',
  'anchor',
  'export',
];
