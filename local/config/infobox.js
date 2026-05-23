// WIKI_LANG = zh
export const FIELD_LABELS = {
  label:       '名称',
  description: '简述',
  born:        '出生',
  died:        '逝世',
  nationality: '国籍',
  affiliation: '所属机构',
  field:       '研究领域',
  chapter:     '相关章节',
  region:      '地区',
  period:      '年代',
  taxon:       '分类',
};
export const INFOBOX_SKIP = new Set(['id', 'type', 'quality', 'tags', 'coords', 'aliases']);
export const FIELD_GROUPS = [
  { label: '基本信息', fields: ['label', 'description', 'born', 'died', 'nationality', 'region', 'period'] },
  { label: '学术信息', fields: ['affiliation', 'field', 'chapter', 'taxon'] },
];
