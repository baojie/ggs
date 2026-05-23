# 枪炮、病菌与钢铁 — 章节顺序

> 依据 `corpus/raw/枪炮病菌与钢铁_校勘底稿.md` 标题结构整理。
> 命名规则：`chNN-slug`（NN = 2 位数字，slug 取英文关键词或拼音）

## 书籍信息

- 书名：枪炮、病菌与钢铁：人类社会的命运
- 作者：贾雷德·戴蒙德（Jared Diamond）
- 译者：谢延光
- 语料：corpus/raw/枪炮病菌与钢铁_校勘底稿.md

## 章节列表

| # | 页面 ID | 标题 | chapter |
|---|---------|------|---------|
| 0 | `Preface` | 前言　耶利的问题 | 0 |
| 1 | `ch01-up-to-the-starting-line` | 第一章　走上起跑线 | 1 |
| 2 | `ch02-natural-experiment-of-history` | 第二章　历史的自然实验 | 2 |
| 3 | `ch03-collision-at-cajamarca` | 第三章　卡哈马卡的冲突 | 3 |
| 4 | `ch04-farmer-power` | 第四章　农民的力量 | 4 |
| 5 | `ch05-historys-haves-and-have-nots` | 第五章　历史上的穷与富 | 5 |
| 6 | `ch06-to-farm-or-not-to-farm` | 第六章　种田还是不种田 | 6 |
| 7 | `ch07-how-to-make-an-almond` | 第七章　怎样识别杏仁 | 7 |
| 8 | `ch08-apples-or-indians` | 第八章　问题在苹果还是在印第安人 | 8 |
| 9 | `ch09-zebras-unhappy-marriages-anna-karenina` | 第九章　斑马、不幸的婚姻和安娜·卡列尼娜原则 | 9 |
| 10 | `ch10-spacious-skies-tilted-axis` | 第十章　辽阔的天空与偏斜的轴线 | 10 |
| 11 | `ch11-lethal-gift-of-livestock` | 第十一章　牲畜的致命礼物 | 11 |
| 12 | `ch12-blueprints-borrowed-letters` | 第十二章　蓝图和借用字母 | 12 |
| 13 | `ch13-necessitys-mother` | 第十三章　需要之母 | 13 |
| 14 | `ch14-from-egalitarianism-to-kleptocracy` | 第十四章　从平等主义到盗贼统治 | 14 |
| 15 | `ch15-yalis-people` | 第十五章　耶利的族人 | 15 |
| 16 | `ch16-how-china-became-chinese` | 第十六章　中国是怎样成为中国人的中国的 | 16 |
| 17 | `ch17-speedboat-to-polynesia` | 第十七章　驶向波利尼西亚的快艇 | 17 |
| 18 | `ch18-collision-of-two-hemispheres` | 第十八章　两个半球的碰撞 | 18 |
| 19 | `ch19-how-africa-became-black` | 第十九章　非洲是怎样成为黑人的非洲的 | 19 |
| 20 | `Epilogue` | 后记　人类史作为一门科学的未来 | 20 |

## 各部分区间

| 部分 | 章节范围 | 章节编号 |
|------|---------|---------|
| 前言 | 耶利的问题 | 0 |
| 第一部分：从伊甸园到卡哈马卡 | 第 1–3 章 | 1–3 |
| 第二部分：粮食生产的出现和传播 | 第 4–10 章 | 4–10 |
| 第三部分：从粮食到枪炮、病菌与钢铁 | 第 11–14 章 | 11–14 |
| 第四部分：在5章中环游世界 | 第 15–19 章 | 15–19 |
| 后记 | 人类史作为一门科学的未来 | 20 |

## 验证

```bash
# 从语料提取标题数与本章节列表对比
grep -n "^第.*章\|^前言\|^后记" corpus/raw/枪炮病菌与钢铁_校勘底稿.md
# 预期：1 前言 + 19 章 + 1 后记 = 21 行
```
