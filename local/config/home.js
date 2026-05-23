// WIKI_LANG = zh
export const CORE_FEATURED = [];
export const PREFACE_IDS   = ['目录', 'Preface'];
export const APPENDIX_IDS  = ['Epilogue'];
export const HOME_SECTIONS = [
  { label: '核心概念', tag: null, type: 'concept', featuredOnly: false, limit: 8 },
  { label: '重要人物', tag: null, type: 'person',  featuredOnly: false, limit: 6 },
  { label: '地理区域', tag: null, type: 'place',   featuredOnly: false, limit: 6 },
  { label: '物种',     tag: null, type: 'species', featuredOnly: false, limit: 6 },
];
export const SKIP_TYPES = new Set(['chapter', 'list', 'overview']);
