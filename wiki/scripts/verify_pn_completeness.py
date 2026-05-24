#!/usr/bin/env python3
"""CHKP1: PN 完整性结构验收。

用法:
  python3 wiki/scripts/verify_pn_completeness.py           # 全量
  python3 wiki/scripts/verify_pn_completeness.py ch08      # 单章
  python3 wiki/scripts/verify_pn_completeness.py --errors  # 只看 ERROR
"""

import json, re, sys
from dataclasses import dataclass, field
from pathlib import Path

WIKI_ROOT   = Path(__file__).resolve().parent.parent.parent
PAGES_DIR   = WIKI_ROOT / 'docs/wiki/pages'
PAGES_JSON  = WIKI_ROOT / 'docs/wiki/pages.json'
CHAPTER_ORDER = WIKI_ROOT / 'ref/chapter-order.md'

SEVERITY = {'ERROR': 0, 'WARN': 1, 'INFO': 2}

@dataclass
class Issue:
    code: str
    severity: str      # ERROR / WARN / INFO
    page_id: str
    line: int
    message: str

    def __str__(self):
        loc = f'{self.page_id}:{self.line}' if self.line else self.page_id
        return f'  [{self.severity}] {self.code} {loc}: {self.message}'


def load_chapter_order() -> dict[str, str]:
    """返回 {page_id: nnn}。"""
    result = {}
    text = CHAPTER_ORDER.read_text(encoding='utf-8')
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith('|') or line.startswith('|---'):
            continue
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 3:
            nnn, pid = parts[1], parts[2]
            if re.match(r'^(P\d{2}|\d{3})$', nnn) and pid:
                result[pid] = nnn
    return result


def load_page_paths() -> dict[str, Path]:
    if not PAGES_JSON.exists():
        return {}
    data = json.load(PAGES_JSON.open(encoding='utf-8'))
    return {
        pid: PAGES_DIR / info['path']
        for pid, info in data.get('pages', {}).items()
        if info.get('path')
    }


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """返回 (frontmatter_dict, body)。"""
    if not text.startswith('---'):
        return {}, text
    m = re.match(r'^---.*?\n---\n?', text, re.DOTALL)
    if not m:
        return {}, text
    fm_text = m.group(0)
    body = text[m.end():]
    fm: dict = {}
    for kv in re.finditer(r'^(\w+):\s*"?([^"\n]+)"?', fm_text, re.MULTILINE):
        fm[kv.group(1)] = kv.group(2).strip()
    return fm, body


def check_chapter(page_id: str, fpath: Path, nnn: str) -> list[Issue]:
    issues: list[Issue] = []
    text = fpath.read_text(encoding='utf-8')
    fm, body = parse_frontmatter(text)

    # ── F2: pn_prefix 与 chapter-order 一致 ──────────────────────────────
    prefix = fm.get('pn_prefix', '').strip('"')
    if prefix and prefix != nnn:
        issues.append(Issue('F2', 'ERROR', page_id, 0,
            f'pn_prefix={prefix!r} 与 chapter-order.md NNN={nnn!r} 不符'))

    lines = body.splitlines()
    pn_nums: list[tuple[int, int]] = []   # [(line_no, ppp_int)]
    image_pn_found: list[int] = []        # 已找到 pn= 的 image block 行号
    in_fence = False

    for lineno, raw in enumerate(lines, 1):
        line = raw

        # ── 代码围栏状态跟踪 ─────────────────────────────────────────────
        if re.match(r'^```', line):
            in_fence = not in_fence

        # ── D2: frontmatter 内已在 parse_frontmatter 排除，此处检查残留 ──
        # （frontmatter 已剥离，body 不含 --- 块，跳过）

        # ── D1: 标题行不得有 PN ──────────────────────────────────────────
        if re.match(r'^#{1,6} ', line):
            if re.search(rf'\[{nnn}-\d{{3}}\]', line):
                issues.append(Issue('D1', 'ERROR', page_id, lineno,
                    f'标题行含 PN 锚点: {line.strip()[:60]!r}'))
            continue

        # ── D3: 脚注定义行不得有 PN ─────────────────────────────────────
        if re.match(r'^\[\^', line):
            if re.search(rf'\[{nnn}-\d{{3}}\]', line):
                issues.append(Issue('D3', 'ERROR', page_id, lineno,
                    f'脚注定义行含 PN 锚点: {line.strip()[:60]!r}'))
            continue

        # ── D5: blockquote 行不得有 PN 锚点 ─────────────────────────────
        if line.startswith('>'):
            if re.match(rf'^\[{nnn}-\d{{3}}\]>', line):
                issues.append(Issue('D5', 'ERROR', page_id, lineno,
                    f'blockquote 行含 PN 锚点: {line.strip()[:60]!r}'))
            continue

        # ── D4: ::: 闭合标签不得有 PN ────────────────────────────────────
        if re.match(r'^:::\s*$', line):
            if re.search(rf'\[{nnn}-\d{{3}}\]', line):
                issues.append(Issue('D4', 'ERROR', page_id, lineno,
                    f':::闭合标签含 PN: {line.strip()!r}'))
            continue

        # ── A6: ::: 后必须有空格（:::TYPE 格式，不得 :::image 无空格）──
        if re.match(r'^:::[a-zA-Z]', line):
            issues.append(Issue('A6', 'ERROR', page_id, lineno,
                f'::: 与块类型之间缺少空格: {line.strip()[:60]!r}'))
            # 仍继续后续 C1 检查

        # ── C1: 所有 ::: 语义块开启行必须有 pn= 属性（属性文法）────────
        if re.match(r'^:::', line) and not re.match(r'^:::\s*$', line):
            pn_m = re.search(rf'pn=({re.escape(nnn)}-(\d{{3}}))', line)
            if not pn_m:
                issues.append(Issue('C1', 'ERROR', page_id, lineno,
                    f'语义块开启行缺少 pn= 属性: {line.strip()[:60]!r}'))
            else:
                ppp = int(pn_m.group(2))
                pn_nums.append((lineno, ppp))
            continue

        # ── A4: 半角括号 PN ───────────────────────────────────────────────
        if re.search(r'\(\d{3}-\d{3}\)', line):
            issues.append(Issue('A4', 'ERROR', page_id, lineno,
                f'含半角括号 PN (应为方括号锚点或全角引用): {line.strip()[:60]!r}'))

        # ── 普通段落 PN 锚点检查 ──────────────────────────────────────────
        m_pn = re.match(rf'^\[({re.escape(nnn)})-(\d{{3}})\](.*)', line)
        if m_pn:
            ppp = int(m_pn.group(2))
            pn_nums.append((lineno, ppp))

            # A1: NNN 是否与 pn_prefix 一致（已由 F2 覆盖，此处检查任意 NNN）
            actual_nnn = m_pn.group(1)
            if actual_nnn != nnn:
                issues.append(Issue('A1', 'ERROR', page_id, lineno,
                    f'PN NNN={actual_nnn!r} 与 pn_prefix={nnn!r} 不符'))

            # A5: PN 后空格
            rest = m_pn.group(3)
            if rest.startswith(' '):
                issues.append(Issue('A5', 'WARN', page_id, lineno,
                    f'PN 锚点后有多余空格: {line.strip()[:60]!r}'))
        else:
            # 检查行内是否含不在行首的 PN 锚点（误格式）
            interior = re.findall(rf'(?<!^)\[{re.escape(nnn)}-\d{{3}}\]', line)
            if interior:
                issues.append(Issue('A1', 'WARN', page_id, lineno,
                    f'PN 锚点不在行首: {line.strip()[:60]!r}'))

    # ── B1/B2: 连续性检查 ────────────────────────────────────────────────
    if not pn_nums:
        issues.append(Issue('B3', 'WARN', page_id, 0,
            f'页面无任何 PN（pn_prefix={nnn}）'))
    else:
        nums_sorted = sorted(pn_nums, key=lambda x: x[1])
        ppps = [n for _, n in nums_sorted]

        # 起始
        if ppps[0] != 1:
            issues.append(Issue('B1', 'ERROR', page_id, nums_sorted[0][0],
                f'PPP 起始为 {ppps[0]:03d}，应为 001'))

        # 连续性
        seen: set[int] = set()
        for lineno, ppp in nums_sorted:
            if ppp in seen:
                issues.append(Issue('B2', 'ERROR', page_id, lineno,
                    f'重号 [{nnn}-{ppp:03d}] 出现多次'))
            seen.add(ppp)

        for i in range(1, len(ppps)):
            if ppps[i] != ppps[i-1] + 1:
                issues.append(Issue('B1', 'ERROR', page_id, nums_sorted[i][0],
                    f'跳号: {ppps[i-1]:03d} → {ppps[i]:03d}'))

    # ── E1: 连续 blockquote 块完整性 ────────────────────────────────────
    bq_runs = []
    run_start = None
    for lineno, raw in enumerate(lines, 1):
        if raw.startswith('>'):
            if run_start is None:
                run_start = lineno
        else:
            if run_start is not None:
                run_len = lineno - run_start
                bq_runs.append((run_start, run_len))
                run_start = None
    if run_start is not None:
        bq_runs.append((run_start, len(lines) - run_start + 1))

    for bq_start, bq_len in bq_runs:
        if bq_len < 4:
            continue
        # 检查引用块前一段落是否有 PN
        preceding_has_pn = False
        for j in range(max(1, bq_start - 5), bq_start):
            if re.match(rf'^\[{re.escape(nnn)}-\d{{3}}\]', lines[j - 1]):
                preceding_has_pn = True
                break
        if not preceding_has_pn:
            issues.append(Issue('E1', 'WARN', page_id, bq_start,
                f'连续 {bq_len} 行 blockquote 块，前一段落无 PN 锚点（可能漏赋导语 PN）'))

    return issues


def main():
    only_errors = '--errors' in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith('--')]

    chapter_order = load_chapter_order()
    page_paths    = load_page_paths()

    # 确定要检查的页面
    targets: list[tuple[str, str]] = []  # [(page_id, nnn)]

    if args:
        for arg in args:
            matched = False
            for pid, nnn in chapter_order.items():
                if pid == arg or pid.startswith(arg + '-') or pid.startswith(arg):
                    targets.append((pid, nnn))
                    matched = True
                    break
            if not matched:
                print(f'未找到匹配页面: {arg}')
                sys.exit(1)
    else:
        # 全量：按 chapter-order 顺序
        p_pages = [(pid, nnn) for pid, nnn in chapter_order.items()
                   if re.match(r'^P\d{2}$', nnn)]
        n_pages = [(pid, nnn) for pid, nnn in chapter_order.items()
                   if re.match(r'^\d{3}$', nnn)]
        targets = sorted(p_pages, key=lambda x: x[1]) + \
                  sorted(n_pages, key=lambda x: x[1])

    # ── F1: 覆盖检查 ─────────────────────────────────────────────────────
    all_issues: list[Issue] = []
    missing_chapters = [pid for pid, _ in targets if pid not in page_paths
                        or not page_paths[pid].exists()]
    if missing_chapters:
        for pid in missing_chapters:
            all_issues.append(Issue('F1', 'ERROR', pid, 0, '章节文件不存在'))

    # ── 逐章检查 ─────────────────────────────────────────────────────────
    results: dict[str, list[Issue]] = {}
    for pid, nnn in targets:
        fpath = page_paths.get(pid)
        if not fpath or not fpath.exists():
            continue
        chapter_issues = check_chapter(pid, fpath, nnn)
        results[pid] = chapter_issues
        all_issues.extend(chapter_issues)

    # ── 输出报告 ─────────────────────────────────────────────────────────
    from datetime import date
    print(f'CHKP1 PN 完整性检查 — {date.today()}')
    print(f'检查章节: {len(targets)}  页面路径: {len(page_paths)}')
    print()

    # 按 code 分组汇总
    groups: dict[str, list[Issue]] = {}
    for iss in all_issues:
        groups.setdefault(iss.code, []).append(iss)

    # 所有检查项定义（code, 描述, 严重度）
    ALL_CHECKS = [
        ('=== 覆盖检查 (F) ===', [
            ('F1', 'chapter-order.md 中所有章节文件存在'),
            ('F2', 'pn_prefix 与 chapter-order.md NNN 一致'),
        ]),
        ('=== 语法检查 (A) ===', [
            ('A1', '锚点格式 [NNN-PPP] 合规，NNN 与 pn_prefix 一致'),
            ('A2', '所有 :::TYPE pn=NNN-PPP 属性格式合规'),
            ('A4', '无半角括号 PN (NNN-PPP)'),
            ('A5', 'PN 锚点后无多余空格'),
            ('A6', '::: 与块类型名之间有空格（::: image 而非 :::image）'),
        ]),
        ('=== 连续性检查 (B) ===', [
            ('B1', '各章 PPP 从 001 起严格递增，无跳号'),
            ('B2', '无重号（同 NNN 下同 PPP 出现多次）'),
            ('B3', '每章至少有 1 个 PN'),
        ]),
        ('=== 特殊块检查 (C) ===', [
            ('C1', '所有 :::TYPE 语义块开启行均含 pn= 属性（属性文法）'),
        ]),
        ('=== 不当赋号检查 (D) ===', [
            ('D1', '标题行（# ## ###）无 PN 锚点'),
            ('D3', '脚注定义行（[^N]:）无 PN 锚点'),
            ('D4', ':::闭合标签无 PN 锚点'),
            ('D5', 'blockquote 行（>）无 PN 锚点'),
        ]),
        ('=== 引文完整性 (E) ===', [
            ('E1', '长 blockquote 块（≥4行）前导语段落已赋 PN'),
        ]),
    ]

    for section_title, checks in ALL_CHECKS:
        print(section_title)
        for code, desc in checks:
            issues_list = groups.get(code, [])
            errors = [i for i in issues_list if i.severity == 'ERROR']
            warns  = [i for i in issues_list if i.severity == 'WARN']
            if errors:
                print(f'✗ {code}  [{len(errors)} ERROR] {desc}')
                for iss in errors[:10]:
                    print(str(iss))
                if len(errors) > 10:
                    print(f'    ... 共 {len(errors)} 处')
            elif warns and not only_errors:
                print(f'△ {code}  [{len(warns)} WARN] {desc}')
                for iss in warns[:5]:
                    print(str(iss))
                if len(warns) > 5:
                    print(f'    ... 共 {len(warns)} 处')
            else:
                print(f'✓ {code}  {desc}')
        print()

    n_err  = sum(1 for i in all_issues if i.severity == 'ERROR')
    n_warn = sum(1 for i in all_issues if i.severity == 'WARN')
    n_info = sum(1 for i in all_issues if i.severity == 'INFO')
    print(f'--- ERROR: {n_err}  WARN: {n_warn}  INFO: {n_info} ---')
    return 1 if n_err > 0 else 0


if __name__ == '__main__':
    sys.exit(main())
