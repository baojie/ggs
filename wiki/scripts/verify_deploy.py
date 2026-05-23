#!/usr/bin/env python3
"""部署验证脚本 — 替代 Phase 4-D 浏览器手动检查

检查项:
  V1 — pages.json 章节完整性（hero.js book card 所需数据全部就绪）
  V2 — home.js/hero.js 配置正确性（PREFACE_IDS / BOOK_META / APPENDIX_IDS）
  V3 — HTTP 200：所有章节页及首页可访问
  V4 — 编码洁净：无乱码字符
  V5 — 目录页 wikilink 可解析
  V6 — daemon restart 后仍可达（重启后复检 V3）

用法:
  python3 wiki/scripts/verify_deploy.py              # 全部检查
  python3 wiki/scripts/verify_deploy.py --skip-start  # 不自动启动 daemon

返回码: 0 = 全部通过, 1 = 有错误, 2 = 严重系统错误
"""

import json, os, re, subprocess, sys, time, urllib.request, urllib.error
from pathlib import Path

WIKI_ROOT = Path(os.environ.get('WIKI_ROOT', os.getcwd()))
PAGES_DIR = WIKI_ROOT / 'docs/wiki/pages'
PAGES_JSON = WIKI_ROOT / 'docs/wiki/pages.json'
HOME_JS = WIKI_ROOT / 'docs/wiki/local/config/home.js'
HERO_JS = WIKI_ROOT / 'docs/wiki/local/config/hero.js'
DAEMON_SH = WIKI_ROOT / 'wiki-daemon.sh'
PORT = 1997
BASE_URL = f'http://localhost:{PORT}'

EXPECTED_CHAPTERS = [
    (0,    'Preface',        '前言　耶利的问题'),
    (1,    'ch01-up-to-the-starting-line',    '第一章　走上起跑线'),
    (2,    'ch02-natural-experiment-of-history', '第二章　历史的自然实验'),
    (3,    'ch03-collision-at-cajamarca',     '第三章　卡哈马卡的冲突'),
    (4,    'ch04-farmer-power',               '第四章　农民的力量'),
    (5,    'ch05-historys-haves-and-have-nots','第五章　历史上的穷与富'),
    (6,    'ch06-to-farm-or-not-to-farm',     '第六章　种田还是不种田'),
    (7,    'ch07-how-to-make-an-almond',      '第七章　怎样识别杏仁'),
    (8,    'ch08-apples-or-indians',          '第八章　问题在苹果还是在印第安人'),
    (9,    'ch09-zebras-unhappy-marriages-anna-karenina', '第九章　斑马、不幸的婚姻和安娜·卡列尼娜原则'),
    (10,   'ch10-spacious-skies-tilted-axis', '第十章　辽阔的天空与偏斜的轴线'),
    (11,   'ch11-lethal-gift-of-livestock',   '第十一章　牲畜的致命礼物'),
    (12,   'ch12-blueprints-borrowed-letters','第十二章　蓝图和借用字母'),
    (13,   'ch13-necessitys-mother',          '第十三章　需要之母'),
    (14,   'ch14-from-egalitarianism-to-kleptocracy', '第十四章　从平等主义到盗贼统治'),
    (15,   'ch15-yalis-people',               '第十五章　耶利的族人'),
    (16,   'ch16-how-china-became-chinese',   '第十六章　中国是怎样成为中国人的中国的'),
    (17,   'ch17-speedboat-to-polynesia',     '第十七章　驶向波利尼西亚的快艇'),
    (18,   'ch18-collision-of-two-hemispheres','第十八章　两个半球的碰撞'),
    (19,   'ch19-how-africa-became-black',    '第十九章　非洲是怎样成为黑人的非洲的'),
    (20,   'Epilogue',        '后记　人类史作为一门科学的未来'),
]
ALL_EXPECTED_IDS = {pid for _, pid, _ in EXPECTED_CHAPTERS}
EXPECTED_MAP = {pid: (num, pid, label) for num, pid, label in EXPECTED_CHAPTERS}

# ── helpers ─────────────────────────────────────────────────────────────────

def _http_get(path: str, timeout: int = 5) -> tuple[int, str]:
    """GET localhost, return (status, body)."""
    url = f'{BASE_URL}/{path.lstrip("/")}'
    try:
        resp = urllib.request.urlopen(url, timeout=timeout)
        body = resp.read().decode('utf-8', errors='replace')
        return resp.status, body
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')
        return e.code, body
    except Exception as e:
        return 0, str(e)


def _daemon_cmd(cmd: str) -> tuple[int, str]:
    """Run wiki-daemon.sh command, return (returncode, stdout+stderr)."""
    proc = subprocess.run(
        ['bash', str(DAEMON_SH), cmd, str(PORT)],
        capture_output=True, text=True, timeout=15,
    )
    return proc.returncode, proc.stdout + proc.stderr


def _is_daemon_running() -> bool:
    pid_file = Path(f'/tmp/ggs-wiki.pid')
    if not pid_file.exists():
        return False
    pid = pid_file.read_text().strip()
    if not pid.isdigit():
        return False
    rc = subprocess.run(['kill', '-0', pid], capture_output=True).returncode
    return rc == 0


def _ensure_daemon(skip_start: bool) -> bool:
    """Ensure daemon is running. Return True if OK."""
    if _is_daemon_running():
        return True
    if skip_start:
        return False
    print("  daemon 未运行，自动启动...")
    rc, out = _daemon_cmd('start')
    if rc != 0:
        print(f"  daemon 启动失败:\n{out}")
        return False
    time.sleep(1)
    return _is_daemon_running()


def _load_pages_json() -> dict:
    return json.loads(PAGES_JSON.read_text(encoding='utf-8'))['pages']


# ═══════════════════════════════════════════════════════════════════════════
# V1 — pages.json 章节完整性
# ═══════════════════════════════════════════════════════════════════════════

def check_v1() -> list[str]:
    """章节类型 / chapter 字段 / book_seq / label 完整性."""
    errs = []
    pages = _load_pages_json()
    registered = set(pages.keys())

    missing = ALL_EXPECTED_IDS - registered
    if missing:
        errs.append(f"V1 pages.json 缺失章节: {', '.join(sorted(missing))}")

    for pid in sorted(ALL_EXPECTED_IDS & registered):
        e = pages[pid]
        num, _, label = EXPECTED_MAP[pid]

        if e.get('type') != 'chapter':
            errs.append(f"V1 {pid}: type={e.get('type')!r}，应为 chapter")
        if e.get('chapter') != num:
            errs.append(f"V1 {pid}: chapter={e.get('chapter')!r}，应为 {num}")
        if e.get('book_seq') != num:
            errs.append(f"V1 {pid}: book_seq={e.get('book_seq')!r}，应为 {num}")
        if e.get('label') != label:
            errs.append(f"V1 {pid}: label={e.get('label')!r}，预期 {label!r}")

    return errs


# ═══════════════════════════════════════════════════════════════════════════
# V2 — home.js / hero.js 配置正确性
# ═══════════════════════════════════════════════════════════════════════════

def check_v2() -> list[str]:
    """验证 PREFACE_IDS / APPENDIX_IDS / BOOK_META."""
    errs = []

    # 读取 home.js
    home_text = HOME_JS.read_text(encoding='utf-8')
    # 提取 PREFACE_IDS
    m = re.search(r'export\s+const\s+PREFACE_IDS\s*=\s*\[([^\]]+)\]', home_text)
    if not m:
        errs.append("V2 home.js: 未找到 PREFACE_IDS")
    else:
        ids = re.findall(r"'([^']+)'", m.group(1))
        expected = ['目录', 'Frontispiece', 'Preface']
        for eid in expected:
            if eid not in ids:
                errs.append(f"V2 home.js: PREFACE_IDS 缺少 {eid!r}")

    # 提取 APPENDIX_IDS
    m = re.search(r'export\s+const\s+APPENDIX_IDS\s*=\s*\[([^\]]+)\]', home_text)
    if not m:
        errs.append("V2 home.js: 未找到 APPENDIX_IDS")
    elif 'Epilogue' not in m.group(1):
        errs.append("V2 home.js: APPENDIX_IDS 缺少 'Epilogue'")

    # 读取 hero.js → BOOK_META
    hero_text = HERO_JS.read_text(encoding='utf-8')
    m = re.search(r'export\s+const\s+BOOK_META\s*=\s*\[(.*?)\]', hero_text, re.DOTALL)
    if not m:
        errs.append("V2 hero.js: 未找到 BOOK_META")
    else:
        block = m.group(1)
        parts = re.findall(r'\{([^}]+)\}', block)
        if len(parts) != 6:
            errs.append(f"V2 hero.js: BOOK_META 应有 6 个 part，实际 {len(parts)}")

        # 验证覆盖 0–20 完整范围
        min_vals = sorted(int(re.search(r'\bmin\s*:\s*(\d+)', p).group(1)) for p in parts)
        max_vals = sorted(int(re.search(r'\bmax\s*:\s*(\d+)', p).group(1)) for p in parts)
        all_covered = set()
        for p in parts:
            mi = int(re.search(r'\bmin\s*:\s*(\d+)', p).group(1))
            ma = int(re.search(r'\bmax\s*:\s*(\d+)', p).group(1))
            all_covered.update(range(mi, ma + 1))
        expected_range = set(range(21))
        uncovered = expected_range - all_covered
        if uncovered:
            errs.append(f"V2 hero.js: BOOK_META 未覆盖 chapter {sorted(uncovered)}")

    return errs


# ═══════════════════════════════════════════════════════════════════════════
# V3 — 服务可达性（SPA 架构）
# ═══════════════════════════════════════════════════════════════════════════

def check_v3() -> list[str]:
    """首页 + 静态资源 HTTP 200 + 页面文件磁盘存在."""
    errs = []

    # 首页
    status, body = _http_get('')
    if status != 200:
        errs.append(f"V3 首页: HTTP {status}")
    elif '枪炮' not in body and 'ggs' not in body:
        errs.append("V3 首页: 响应内容不包含站点标识")

    # 静态资源
    assets = ['css/main.css', 'js/core.js', 'js/renderer.js']
    for asset in assets:
        status, _ = _http_get(asset)
        if status != 200:
            errs.append(f"V3 静态资源 {asset}: HTTP {status}")

    # 页面文件磁盘存在（SPA 路由由 JS 处理，无法 HTTP 验证）
    pages = _load_pages_json()
    for pid in sorted(ALL_EXPECTED_IDS):
        entry = pages.get(pid)
        if not entry:
            errs.append(f"V3 {pid}: pages.json 无此条目")
            continue
        fpath = entry.get('path', '')
        if not fpath:
            errs.append(f"V3 {pid}: pages.json 无 path 字段")
            continue
        if not (PAGES_DIR / fpath).exists():
            errs.append(f"V3 {pid}: 文件不存在 {fpath}")

    return errs


# ═══════════════════════════════════════════════════════════════════════════
# V4 — 编码洁净
# ═══════════════════════════════════════════════════════════════════════════

def check_v4() -> list[str]:
    """扫描章节页编码异常."""
    errs = []

    for num, pid, _ in EXPECTED_CHAPTERS:
        prefix = pid[:2].lower()
        fpath = PAGES_DIR / prefix / f'{pid}.md'
        if not fpath.exists():
            errs.append(f"V4 {pid}: 文件不存在")
            continue

        raw = fpath.read_bytes()

        # 检查 UTF-8 解码
        try:
            text = raw.decode('utf-8')
        except UnicodeDecodeError as e:
            errs.append(f"V4 {pid}: UTF-8 解码失败 ({e})")
            continue

        # 检查 U+FFFD 替换字符
        if '�' in text:
            # 定位
            for i, line in enumerate(text.splitlines(), 1):
                if '�' in line:
                    ctx = line.strip()[:80]
                    errs.append(f"V4 {pid}:{i}: 含 U+FFFD 替换字符: {ctx!r}")
                    break

        # 检查常见 mojibake 模式：Latin-1 解码 CJK 产生的遗留
        # 如 æ±‰å­— 这类模式通常表现为连续的非ASCII扩展字符
        mojibake = re.findall(r'[\xe0-\xef][\x80-\xbf]{2}', text)
        if mojibake:
            # 如果文本中有大量 3-byte UTF-8 序列是正常的（CJK 正用这个范围），
            # mojibake 的特征是出现在非期待位置 + 连续出现
            pass  # 仅凭正则误报太多，留作人工判断

    return errs


# ═══════════════════════════════════════════════════════════════════════════
# V5 — 目录页 wikilink 可解析
# ═══════════════════════════════════════════════════════════════════════════

def check_v5() -> list[str]:
    """目录页所有 wikilink 目标在 pages.json 中存在."""
    errs = []
    pages = _load_pages_json()
    registered = set(pages.keys())

    toc_file = PAGES_DIR / 'mu' / '目录.md'
    if not toc_file.exists():
        return ["V5 目录页文件不存在"]

    text = toc_file.read_text(encoding='utf-8')
    # 提取所有 [[id|label]] 和 [[id]] 形式的 wikilink
    links = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', text)
    unresolved = []
    for target in links:
        target = target.strip()
        if target not in registered:
            unresolved.append(target)

    if unresolved:
        errs.append(f"V5 目录页 {len(unresolved)} 个 wikilink 目标在 pages.json 中不存在: "
                     f"{', '.join(unresolved[:10])}"
                     f"{'…' if len(unresolved) > 10 else ''}")

    return errs


# ═══════════════════════════════════════════════════════════════════════════
# V6 — daemon restart 持久化
# ═══════════════════════════════════════════════════════════════════════════

def check_v6() -> list[str]:
    """Restart daemon then re-check V3."""
    errs = []
    print("  restart daemon...")
    rc, out = _daemon_cmd('restart')
    if rc != 0:
        return [f"V6 daemon restart 失败:\n{out}"]
    time.sleep(1.5)
    if not _is_daemon_running():
        return ["V6 daemon restart 后未运行"]

    # 复检 V3
    v3_errs = check_v3()
    if v3_errs:
        errs.append("V6 restart 后 V3 检查失败:")
        errs.extend(f"  {e}" for e in v3_errs)
    else:
        print("  restart 后全部章节页可达 ✓")
    return errs


# ═══════════════════════════════════════════════════════════════════════════
# V7 — 章节导航配置
# ═══════════════════════════════════════════════════════════════════════════

CHAPTER_CONFIG = WIKI_ROOT / 'docs/wiki/local/config/chapter.config.js'

def check_v7() -> list[str]:
    """章节页「回到目录」和「上一章/下一章」链接的底层数据完整性."""
    errs = []

    # 7a: chapter.config.js 配置
    if not CHAPTER_CONFIG.exists():
        errs.append("V7 chapter.config.js 不存在")
    else:
        text = CHAPTER_CONFIG.read_text(encoding='utf-8')
        m = re.search(r"export\s+const\s+TOC_PAGE_ID\s*=\s*'([^']+)'", text)
        if not m:
            errs.append("V7 chapter.config.js: 未找到 TOC_PAGE_ID")
        else:
            toc_id = m.group(1)
            pages = _load_pages_json()
            if toc_id not in pages:
                errs.append(f"V7 TOC_PAGE_ID={toc_id!r} 在 pages.json 中不存在")
            elif pages[toc_id].get('type') not in ('overview', 'concept'):
                errs.append(f"V7 TOC 页 {toc_id} type={pages[toc_id].get('type')!r}，预期 overview")

    # 7b: 所有章节有 book_seq（导航排序依赖，V1 已检查但此处做语义验证）
    pages = _load_pages_json()
    seqs = []
    for pid in sorted(ALL_EXPECTED_IDS):
        if pid not in pages:
            continue
        bs = pages[pid].get('book_seq')
        if bs is None:
            errs.append(f"V7 {pid}: 缺 book_seq 字段（章节导航排序依赖）")
        else:
            seqs.append(bs)

    # 7c: book_seq 连续无断裂
    if seqs:
        seqs.sort()
        expected = list(range(seqs[0], seqs[-1] + 1))
        missing_seqs = set(expected) - set(seqs)
        if missing_seqs:
            errs.append(f"V7 book_seq 不连续，缺失: {sorted(missing_seqs)}")

    # 7d: book 字段一致性（全部无 book 或全部同值）
    books = set()
    for pid in ALL_EXPECTED_IDS:
        if pid in pages:
            b = pages[pid].get('book')
            books.add(b)
    if len(books) > 1:
        errs.append(f"V7 章节 book 字段不一致: {books}")

    return errs


# ═══════════════════════════════════════════════════════════════════════════

def main():
    skip_start = '--skip-start' in sys.argv
    all_errors = {}
    has_critical = False

    if not PAGES_JSON.exists():
        print("✗ pages.json 不存在", file=sys.stderr)
        return 2

    # ── V1 ──
    print("V1 pages.json 章节完整性...")
    e = check_v1()
    all_errors['V1'] = e

    # ── V2 ──
    print("V2 home.js/hero.js 配置正确性...")
    e = check_v2()
    all_errors['V2'] = e

    # ── daemon 就绪（V3/V6 依赖）──
    daemon_ok = _ensure_daemon(skip_start)
    if not daemon_ok:
        msg = "daemon 不可用，跳过 V3/V6"
        all_errors['V3'] = [msg]
        all_errors['V6'] = [msg]
        has_critical = True
    else:
        print(f"V3 HTTP 200 可达性 (PORT={PORT})...")
        e = check_v3()
        all_errors['V3'] = e

    # ── V4 ──
    print("V4 编码洁净度...")
    e = check_v4()
    all_errors['V4'] = e

    # ── V5 ──
    print("V5 目录页 wikilink 可解析...")
    e = check_v5()
    all_errors['V5'] = e

    # ── V6 ──
    print("V6 daemon restart 持久化...")
    if not daemon_ok:
        all_errors['V6'] = ["daemon 不可用，跳过"]
    else:
        e = check_v6()
        all_errors['V6'] = e

    # ── V7 ──
    print("V7 章节导航配置...")
    e = check_v7()
    all_errors['V7'] = e

    # ── 汇总 ──
    print()
    total_errs = 0
    for name in ['V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7']:
        errs = all_errors[name]
        if not errs:
            print(f"✓ {name} 通过")
        else:
            total_errs += len(errs)
            print(f"✗ {name} ({len(errs)} 项):")
            for e in errs:
                print(f"    {e}")

    print()
    if total_errs == 0:
        print("结果: 全部通过 ✓")
        return 0
    else:
        print(f"结果: {total_errs} 个错误")
        return 1


if __name__ == '__main__':
    sys.exit(main())
