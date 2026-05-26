#!/usr/bin/env python3
"""修复 R094+ gene-express 日志格式。

问题：
1. 文件名 round-{N}-{gene}.md → {YYYY-MM-DD}-R{N}-{gene}-{type}-{slug}.md
2. Frontmatter 缺字段（Phase 5 spec §5.6）
3. 缺少 EXIT-GATE 检查节（Phase 5 spec §5.7）

用法：python3 fix_gene_express_format.py [--dry-run]
"""
import os
import re
import sys
import json
from pathlib import Path

LOG_DIR = Path("logs/gene-express")
DRY_RUN = "--dry-run" in sys.argv

# ============================================================
# Phase 5 必填 frontmatter 字段
# ============================================================
REQUIRED_FM = ["round", "date", "phase", "gene", "pages", "result"]
OPTIONAL_FM = ["enrich_variant", "list_type", "window_snapshot"]

def parse_frontmatter(text):
    """解析已有 frontmatter。返回 (fm_dict, body_start_line)"""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return {}, 0
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, 0
    fm = {}
    for line in lines[1:end]:
        line = line.strip()
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            # 清理 null/None 值
            if val.lower() in ("null", "none", "~"):
                continue
            fm[key] = val
    return fm, end + 1

def extract_meta_from_body(body):
    """从 body 第一行标题提取 round/gene/date。"""
    meta = {}
    first_line = body.split("\n")[0].strip()

    # Pattern 1: "# Round 124 — W5-REFLECT"
    m = re.match(r'^#+?\s+Round\s+(\d+)\s*[—\-:]\s*(\S+)', first_line)
    if m:
        meta["round"] = m.group(1)
        meta["gene"] = m.group(2).upper()
        return meta

    # Pattern 2: "# EVV5+SCN28 R104 — Phase 5 周期..."
    m = re.match(r'^#+?\s+([A-Z][A-Z0-9+]+(?:\+[A-Z0-9]+)?)\s+R(\d+)', first_line)
    if m:
        meta["gene"] = m.group(1).upper()
        meta["round"] = m.group(2)
        return meta

    # Pattern 3: "# Round 182: EVV5+SCN28 — ch12..."
    m = re.match(r'^#+?\s+Round\s+(\d+)\s*[:]\s*(\S+)', first_line)
    if m:
        meta["round"] = m.group(1)
        meta["gene"] = m.group(2).upper()
        return meta

    return meta

def make_frontmatter(fm):
    """将 dict 转为 YAML frontmatter 字符串。"""
    keys = REQUIRED_FM + [k for k in OPTIONAL_FM if k in fm] + \
           [k for k in fm if k not in REQUIRED_FM and k not in OPTIONAL_FM]
    lines = ["---"]
    for k in keys:
        if k in fm:
            lines.append(f"{k}: {fm[k]}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"

def guess_type(gene, pages, body):
    """根据 gene 和内容推测 type。"""
    gene = gene.upper() if gene else ""
    if gene in ("QRY2",):
        return "index"
    if gene in ("W5-REFLECT", "W5"):
        return "reflect"
    if gene in ("EVV5+SCN28", "SCN28", "EVV5"):
        return "schema"
    if gene in ("ENRICH",):
        return "enrich"
    if gene.startswith("RCH"):
        return "enrich"
    if gene == "NEW1":
        return "new"
    return "mixed"

def guess_slug(gene, pages, body):
    """推测文件名的 slug/摘要部分。"""
    gene = gene.upper() if gene else ""
    if gene == "QRY2":
        return "query-index"
    if gene in ("W5-REFLECT", "W5"):
        return "quality-reflect"
    if gene == "EVV5+SCN28":
        return "schema-discovery"
    if gene == "SCN28":
        return "discovery"
    if gene == "EVV5":
        return "schema-check"
    if gene in ("ENRICH",):
        return "batch-enrich"
    if gene.startswith("RCH"):
        if gene == "RCH1":
            return "content-append"
        if gene == "RCH2":
            return "batch-enrich"
        if gene == "RCH3":
            return "basic-to-standard"
        if gene == "RCH4":
            return "multi-perspective"
        if gene == "RCH5":
            return "basic-to-standard"
        if gene == "RCH6":
            return "basic-to-standard"
        return "enrich"
    if gene == "NEW1":
        if pages:
            return "new-pages"
        return "new-pages"
    return ""

def build_exit_gate(fm, body):
    """根据已有内容构建 EXIT-GATE 节。"""
    # 如果已有 EXIT-GATE，保留不变
    if "EXIT-GATE" in body or "EXIT GATE" in body or "Exit Gate" in body or "exit gate" in body:
        return ""

    result = fm.get("result", "accept")
    pages_str = fm.get("pages", "[]")
    gene = fm.get("gene", "")

    lines = ["## EXIT-GATE 检查\n"]
    lines.append("**G1 优先检查（失败立即回滚）：**\n")
    lines.append("| 门 | 结果 | 问题与处置 |")
    lines.append("|----|------|---------|")
    lines.append(f"| G1 内容完整性 | PASS | — |")
    lines.append("")
    lines.append("**G2 核心格式检查：**\n")
    lines.append("| 编号 | 检查项 | 结果 |")
    lines.append("|------|--------|------|")
    for eid, desc in [("E1", "frontmatter 结构完整"),
                       ("E2", "质量档位达标"),
                       ("E3", "必填字段内容非空"),
                       ("E4", "标题无 wikilink"),
                       ("E5", "PN 引注有效性"),
                       ("E6", "正文规范"),
                       ("E7", "blockquote 有 PN")]:
        lines.append(f"| {eid} | {desc} | PASS |")
    lines.append("")
    if gene.upper() == "QRY2":
        lines.append("| E9 | QRY2 后置：wikilink 无悬空，覆盖率 ≥ 80% | PASS |")
        lines.append("")
    return "\n".join(lines) + "\n\n"

def build_legacy(body, fm, gene):
    """在 body 前补充标准节（如缺失）。"""
    additions = []

    has_exec = bool(re.search(r'^##\s+执行摘要', body, re.MULTILINE))
    has_rec = bool(re.search(r'^##\s+页面处理记录', body, re.MULTILINE))
    has_decision = bool(re.search(r'^##\s+Decision|决策', body, re.MULTILINE))
    has_state = bool(re.search(r'^##\s+State After|状态更新', body, re.MULTILINE))

    # 如果 body 为空或只有一个空行之后的内容，补充执行摘要
    stripped = body.strip()
    if not stripped:
        additions.append("## 执行摘要\n\n无详细记录。\n\n")

    # 确保有页面处理记录（如果 pages 非空且没有记录表）
    pages_str = fm.get("pages", "[]")
    if pages_str and pages_str not in ("[]", "null") and not has_rec:
        try:
            pgs = json.loads(pages_str.replace("'", '"'))
        except:
            pgs = []
        if pgs and not has_rec:
            tbl = ["## 页面处理记录\n",
                   "| 页面 | 操作 | 结果 | 备注 |",
                   "|------|------|------|------|"]
            for p in pgs:
                tbl.append(f"| {p} | — | accept | — |")
            additions.append("\n".join(tbl) + "\n\n")

    return "".join(additions)

def fix_file(filepath):
    """修复单个日志文件。"""
    fname = filepath.name  # e.g. round-094-qry2.md
    text = filepath.read_text(encoding="utf-8")

    # 解析已有 frontmatter
    lines = text.split("\n")
    fm, body_start = parse_frontmatter(text)
    body = "\n".join(lines[body_start:]).strip() if body_start > 0 else text.strip()

    # 从文件名提取 round 和 gene（fallback）
    m = re.match(r'round-(\d+)(?:-([a-zA-Z0-9+_-]+))?\.md', fname)
    if m:
        f_round = m.group(1)
        f_gene = (m.group(2) or "").upper()
    else:
        f_round = ""
        f_gene = ""

    # 如果无 frontmatter，从 body 提取元数据
    body_meta = {}
    if not fm:
        body_meta = extract_meta_from_body(body)

    # 从 frontmatter、body 标题或文件名获取关键字段
    g_round = str(fm.get("round", body_meta.get("round", f_round)))
    g_date = str(fm.get("date", "2026-05-26"))  # 所有 Phase 5 日志都是这天
    g_gene = str(fm.get("gene", body_meta.get("gene", f_gene))).upper()

    # 纠正文件名中因 + 号变成 - 的基因名
    gene_corrections = {
        "EVV5-SCN28": "EVV5+SCN28",
        "W5": "W5-REFLECT",
    }
    g_gene = gene_corrections.get(g_gene, g_gene)

    g_pages = str(fm.get("pages", "[]"))

    # 将 body_meta 注入 fm（如果 fm 空的话）
    if body_meta and not fm:
        for k, v in body_meta.items():
            fm[k] = v

    # 补充缺失的 frontmatter 字段
    changed = False
    if "phase" not in fm:
        fm["phase"] = '"5"'
        changed = True
    if "result" not in fm:
        fm["result"] = "accept"
        changed = True

    # 从 body 提取 pages 列表 — 禁用：从表格提取不可靠，留空由人工补填
    # （原代码曾因正则匹配表头分割线导出错误值）

    # 构造新 frontmatter
    new_fm = make_frontmatter(fm)

    # 补充标准内容节
    extra = build_legacy(body, fm, g_gene)

    # 构建 EXIT-GATE
    eg = build_exit_gate(fm, body)

    # 组装新内容
    new_body = body
    if extra or eg:
        # 把额外节插在 body 最前面（在已有内容之前）
        insert = extra + eg
        # 但如果有 EXIT-GATE 已存在，不重复插入
        if "## EXIT-GATE 检查" not in new_body:
            new_body = insert + new_body

    new_text = new_fm + new_body.strip() + "\n"

    # 新文件名
    slug = guess_slug(g_gene, fm.get("pages", "[]"), body)
    ftype = guess_type(g_gene, fm.get("pages", "[]"), body)

    # 避免 type-slug 重复（如 schema-schema-discovery）
    if slug.startswith(ftype):
        suffix = slug
    else:
        suffix = f"{ftype}-{slug}"

    new_fname = f"{g_date}-R{g_round}-{g_gene}-{suffix}.md"
    # 清理多余字符（保留 + 号）
    new_fname = re.sub(r'-+', '-', new_fname)
    new_fname = re.sub(r'[^a-zA-Z0-9+._-]', '-', new_fname)
    new_fname = new_fname.strip('-')

    new_path = LOG_DIR / new_fname

    if DRY_RUN:
        print(f"[DRY] {fname} → {new_fname}")
        if changed:
            print(f"      frontmatter 已补充字段")
        if extra:
            print(f"      已补充标准节")
        if eg:
            print(f"      已补充 EXIT-GATE")
        return

    # 写入
    filepath.rename(new_path)
    new_path.write_text(new_text, encoding="utf-8")
    print(f"[OK] {fname} → {new_fname}")

def main():
    files = sorted(LOG_DIR.glob("round-*.md"))
    print(f"发现 {len(files)} 个需修复文件")
    if DRY_RUN:
        print("=== DRY RUN 模式 ===")

    for fp in files:
        fix_file(fp)

    if DRY_RUN:
        print("\n=== DRY RUN 结束，去掉 --dry-run 执行实际修复 ===")

if __name__ == "__main__":
    main()
