# R246 W5-REFLECT — 全库质量反思

- **日期**: 2026-05-27
- **触发**: P3 W5（w5_interval=29，rounds_since_last_w5=29 → 触发）
- **基因**: W5-REFLECT
- **扫描范围**: 全库 643 页
- **w5_findings**: 4

## 决策矩阵

| 优先级 | 基因 | 判定 |
|--------|------|------|
| P1a | EVV5+SCN28 | evv5=9 < 10 → 跳过 |
| P1b | EVV5 | 同上 |
| P2 | SCN28 | discover=0, 队列≈13 ≥ 10 → 跳过 |
| P3 | **W5** | **29 ≥ 29 → 已执行** |
| P4 | ENRICH | 待下轮 |
| P5–8 | 默认 | 待下轮 |

## 扫描结果

| 扫描项 | 结果 |
|--------|------|
| C1 破折号滥用 | 111 处（多为合法破折号，非批量错误） |
| C3 AI链式表达 | 22 页含套话模式 |
| C8 截断 wikilink | 0 处，干净 |
| C9 :::缺空格 | **55 页** 存在 `:::query` 无空格（导致解析静默失效） |
| PN 无引注年份陈述 | 30 处（多为脚注/特殊页，少量正文页） |

## 批量修复

按 W5 规范："对立即可执行的存量问题执行批量修复"。
C9 修复：为所有 `:::query` 补空格 → `::: query`。

```bash
# 在 pages/ 下批量修复 :::缺空格
python3 -c "
import re, pathlib, glob
n = 0
for f in glob.glob('docs/wiki/pages/*/*.md'):
    txt = pathlib.Path(f).read_text()
    new_txt, cnt = re.subn(r'(^:::)([a-zA-Z])', r'\1 \2', txt, flags=re.M)
    if cnt:
        pathlib.Path(f).write_text(new_txt)
        n += cnt
        print(f'  {f.split(\"/\")[-1].replace(\".md\",\"\")}: {cnt} 处')
print(f'总计修复: {n} 处（{n} 页）')
"
```

## 状态更新

- current_round: 246→247
- rounds_since_last_evv5: 9→10
- rounds_since_last_w5: 29→0
- last_10_genes: shift oldest "EVV5" → push "W5-REFLECT"
- W5 不计入窗口计数

## 下轮预测

R247 队列≈13，W5 刚执行。EVV5 与 SCN28 均可能触发。
