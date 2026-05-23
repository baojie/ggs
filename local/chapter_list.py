# ggs wiki 章节列表 — 供 wiki/scripts/chapter_integrity.py（CHK12）使用
# 格式：(book_seq, page_id, label)

EXPECTED_CHAPTERS = [
    (0,    'Preface',        '前言　耶利的问题'),
    (1,    'ch01-up-to-the-starting-line',          '第一章　走上起跑线'),
    (2,    'ch02-natural-experiment-of-history',     '第二章　历史的自然实验'),
    (3,    'ch03-collision-at-cajamarca',            '第三章　卡哈马卡的冲突'),
    (4,    'ch04-farmer-power',                      '第四章　农民的力量'),
    (5,    'ch05-historys-haves-and-have-nots',      '第五章　历史上的穷与富'),
    (6,    'ch06-to-farm-or-not-to-farm',            '第六章　种田还是不种田'),
    (7,    'ch07-how-to-make-an-almond',             '第七章　怎样识别杏仁'),
    (8,    'ch08-apples-or-indians',                 '第八章　问题在苹果还是在印第安人'),
    (9,    'ch09-zebras-unhappy-marriages-anna-karenina',
                                                     '第九章　斑马、不幸的婚姻和安娜·卡列尼娜原则'),
    (10,   'ch10-spacious-skies-tilted-axis',        '第十章　辽阔的天空与偏斜的轴线'),
    (11,   'ch11-lethal-gift-of-livestock',          '第十一章　牲畜的致命礼物'),
    (12,   'ch12-blueprints-borrowed-letters',       '第十二章　蓝图和借用字母'),
    (13,   'ch13-necessitys-mother',                 '第十三章　需要之母'),
    (14,   'ch14-from-egalitarianism-to-kleptocracy','第十四章　从平等主义到盗贼统治'),
    (15,   'ch15-yalis-people',                      '第十五章　耶利的族人'),
    (16,   'ch16-how-china-became-chinese',          '第十六章　中国是怎样成为中国人的中国的'),
    (17,   'ch17-speedboat-to-polynesia',            '第十七章　驶向波利尼西亚的快艇'),
    (18,   'ch18-collision-of-two-hemispheres',      '第十八章　两个半球的碰撞'),
    (19,   'ch19-how-africa-became-black',           '第十九章　非洲是怎样成为黑人的非洲的'),
    (20,   'Epilogue',       '后记　人类史作为一门科学的未来'),
]

NON_CHAPTER_PAGES = {'Frontispiece', 'About', '目录'}
