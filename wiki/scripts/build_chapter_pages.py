#!/usr/bin/env python3
"""Build chapter pages from doc_final.md for ggs wiki.

Splits corpus by H2 headings (preface, chapters, epilogue),
writes each to docs/wiki/pages/ with proper frontmatter,
updates pages.json and pages.lite.json."""
import json, os, re, sys
from pathlib import Path

# YAML frontmatter serialization (lightweight, no dependency on PyYAML for output)
def _yaml_fm(fm: dict) -> str:
    """Serialize frontmatter dict to YAML string (subset of YAML, frontmatter-safe)."""
    lines = []
    key_order = ['id', 'type', 'label', 'aliases', 'tags', 'chapter', 'description']
    for key in key_order:
        if key not in fm:
            continue
        val = fm[key]
        if val is None:
            continue
        if isinstance(val, str):
            # Quote if contains special chars
            if any(c in val for c in ':#{}[]&*!|>%@`,'):
                escaped = val.replace('"', '\\"')
                lines.append(f'{key}: "{escaped}"')
            else:
                lines.append(f'{key}: {val}')
        elif isinstance(val, bool):
            lines.append(f'{key}: {"true" if val else "false"}')
        elif isinstance(val, int):
            lines.append(f'{key}: {val}')
        elif isinstance(val, (list, tuple)):
            items = []
            for item in val:
                if isinstance(item, str):
                    items.append(f'"{item}"')
                else:
                    items.append(str(item))
            lines.append(f'{key}: [{", ".join(items)}]')
        elif isinstance(val, dict):
            lines.append(f'{key}:')
            for k, v in val.items():
                lines.append(f'  {k}: {v}')
    return '\n'.join(lines)

WIKI_ROOT = Path(os.environ.get('WIKI_ROOT', os.getcwd()))
CORPUS = WIKI_ROOT / 'corpus/raw/doc_final.md'
PAGES_DIR = WIKI_ROOT / 'docs/wiki/pages'
PAGES_JSON = WIKI_ROOT / 'docs/wiki/pages.json'
PAGES_LITE_JSON = WIKI_ROOT / 'docs/wiki/pages.lite.json'

# (chapter_num, page_id, label)
CHAPTERS = [
    (0,    'Preface',        '前言　耶利的问题'),
    (1,    'ch01-up-to-the-starting-line',
                              '第一章　走上起跑线'),
    (2,    'ch02-natural-experiment-of-history',
                              '第二章　历史的自然实验'),
    (3,    'ch03-collision-at-cajamarca',
                              '第三章　卡哈马卡的冲突'),
    (4,    'ch04-farmer-power',
                              '第四章　农民的力量'),
    (5,    'ch05-historys-haves-and-have-nots',
                              '第五章　历史上的穷与富'),
    (6,    'ch06-to-farm-or-not-to-farm',
                              '第六章　种田还是不种田'),
    (7,    'ch07-how-to-make-an-almond',
                              '第七章　怎样识别杏仁'),
    (8,    'ch08-apples-or-indians',
                              '第八章　问题在苹果还是在印第安人'),
    (9,    'ch09-zebras-unhappy-marriages-anna-karenina',
                              '第九章　斑马、不幸的婚姻和安娜·卡列尼娜原则'),
    (10,   'ch10-spacious-skies-tilted-axis',
                              '第十章　辽阔的天空与偏斜的轴线'),
    (11,   'ch11-lethal-gift-of-livestock',
                              '第十一章　牲畜的致命礼物'),
    (12,   'ch12-blueprints-borrowed-letters',
                              '第十二章　蓝图和借用字母'),
    (13,   'ch13-necessitys-mother',
                              '第十三章　需要之母'),
    (14,   'ch14-from-egalitarianism-to-kleptocracy',
                              '第十四章　从平等主义到盗贼统治'),
    (15,   'ch15-yalis-people',
                              '第十五章　耶利的族人'),
    (16,   'ch16-how-china-became-chinese',
                              '第十六章　中国是怎样成为中国人的中国的'),
    (17,   'ch17-speedboat-to-polynesia',
                              '第十七章　驶向波利尼西亚的快艇'),
    (18,   'ch18-collision-of-two-hemispheres',
                              '第十八章　两个半球的碰撞'),
    (19,   'ch19-how-africa-became-black',
                              '第十九章　非洲是怎样成为黑人的非洲的'),
    (20,   'Epilogue',       '后记　人类史作为一门科学的未来'),
]

# Build heading → (num, pid, label) lookup
H2_PATTERN = re.compile(r'^##\s+(.+)$')
HEADING_MAP = {}
for num, pid, label in CHAPTERS:
    HEADING_MAP[label] = (num, pid, label)


def split_sections(text: str):
    """Split corpus into sections by H2 headings.

    Returns list of (heading_text_or_None, content_lines).
    First section (before any H2) uses heading_text=None (includes colophon)."""
    lines = text.splitlines()
    sections = []

    # ── content before the first H2 (colophon / book metadata) ──
    i = 0
    while i < len(lines) and not H2_PATTERN.match(lines[i]):
        i += 1
    if i > 2:  # more than just the H1 title
        sections.append((None, lines[:i]))

    # ── split on H2 ──
    while i < len(lines):
        m = H2_PATTERN.match(lines[i])
        if m:
            start = i
            i += 1
            while i < len(lines) and not H2_PATTERN.match(lines[i]):
                i += 1
            sections.append((m.group(1), lines[start:i]))
        else:
            i += 1

    return sections


def make_frontmatter(num, pid, label):
    """Build frontmatter dict for a chapter page."""
    fm = {
        'id': pid,
        'type': 'chapter',
        'label': label,
        'tags': ['chapter'],
    }
    if num is not None:
        fm['chapter'] = num
    return fm


def main():
    text = CORPUS.read_text(encoding='utf-8')
    sections = split_sections(text)

    written = []
    unmatched_heading = None

    for heading, content in sections:
        if heading is None:
            # Colophon section — prepend to the Preface page
            unmatched_heading = content
            continue

        # Match heading → chapter entry
        match = HEADING_MAP.get(heading)
        if match is None:
            print(f"  ⚠  unmapped heading: {heading}", file=sys.stderr)
            continue

        num, pid, label = match

        # Build body: keep H2 heading, prepend colophon if this is Preface
        body_lines = list(content)
        if pid == 'Preface' and unmatched_heading is not None:
            body_lines = list(unmatched_heading) + [''] + body_lines

        body = '\n'.join(body_lines).strip()

        # Build page content
        fm = make_frontmatter(num, pid, label)
        page_text = f"---\n{_yaml_fm(fm)}\n---\n\n{body}\n"

        # Write to bucket directory
        prefix = pid[:2].lower()
        out_dir = PAGES_DIR / prefix
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f'{pid}.md'
        out_file.write_text(page_text, encoding='utf-8')
        written.append((pid, fm))
        print(f"  ✓ {out_file.relative_to(WIKI_ROOT)}")

    # ── Update pages.json / pages.lite.json ──
    if written:
        _update_registries(written)
        print(f"\n  ✓ pages.json / pages.lite.json updated ({len(written)} pages)")
    else:
        print("\n  No pages written — nothing to register")


def _update_registries(written):
    """Append new chapter entries to pages.json and pages.lite.json."""
    for reg_path in [PAGES_JSON, PAGES_LITE_JSON]:
        if reg_path.exists():
            reg = json.loads(reg_path.read_text(encoding='utf-8'))
        else:
            reg = {'pages': {}}

        for pid, fm in written:
            if pid not in reg['pages']:
                entry = {
                    'id': pid,
                    'type': fm['type'],
                    'label': fm['label'],
                    'tags': fm['tags'],
                }
                if 'chapter' in fm:
                    entry['chapter'] = fm['chapter']
                reg['pages'][pid] = entry

        reg_path.write_text(
            json.dumps(reg, ensure_ascii=False, indent=2) + '\n',
            encoding='utf-8',
        )


if __name__ == '__main__':
    main()
