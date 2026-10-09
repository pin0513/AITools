"""Markdown 解析:表格(以表頭簽名分類)、mermaid 區塊(掛到最近的 h3)、h2/h3 章節。"""
import re
from dataclasses import dataclass, field

@dataclass
class Table:
    file: str
    section: str          # 最近的 h2
    header: list
    rows: list            # list[dict] 以 header 為鍵
    line: int

@dataclass
class Mermaid:
    file: str
    heading: str          # 最近的 h3(或 h2)
    code: str
    line: int

@dataclass
class Doc:
    file: str
    h2: list = field(default_factory=list)
    h3: list = field(default_factory=list)
    tables: list = field(default_factory=list)
    mermaid: list = field(default_factory=list)
    text: str = ""

_SEP = re.compile(r"^\s*:?-+:?\s*$")

def _cells(line: str):
    return [c.strip() for c in line.strip().strip("|").split("|")]

def parse(path, text: str) -> Doc:
    d = Doc(file=str(path), text=text)
    lines = text.splitlines()
    i, cur_h2, cur_h3 = 0, "", ""
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            lang = line[3:].strip(); j = i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                j += 1
            if lang == "mermaid":
                d.mermaid.append(Mermaid(d.file, cur_h3 or cur_h2, "\n".join(lines[i + 1:j]), i + 1))
            i = j + 1
            continue
        m = re.match(r"^(#{2,3})\s+(.*)", line)
        if m:
            if len(m.group(1)) == 2:
                cur_h2, cur_h3 = m.group(2).strip(), ""
                d.h2.append(cur_h2)
            else:
                cur_h3 = m.group(2).strip(); d.h3.append(cur_h3)
            i += 1
            continue
        if line.lstrip().startswith("|"):
            start = i; block = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                block.append(lines[i]); i += 1
            cells = [_cells(b) for b in block]
            if len(cells) >= 2 and all(_SEP.match(c) for c in cells[1]):
                header = cells[0]
                rows = []
                for r in cells[2:]:
                    r = r + [""] * (len(header) - len(r))
                    if any(c for c in r):
                        rows.append(dict(zip(header, r)))
                d.tables.append(Table(d.file, cur_h2, header, rows, start + 1))
            continue
        i += 1
    return d

# 表頭簽名:前綴比對(忽略大小寫與全形/半形空白)
SIGNATURES = {
    "requirements":  ("ID", "需求", "型態"),
    "nfr":           ("ID", "刺激"),
    "components":    ("ID", "名稱", "Layer"),
    "ac_links":      ("AC", "CMP"),
    "apis":          ("ID", "Method"),
    "failure_modes": ("外部系統", "呼叫點 CMP"),
    "ownership":     ("表", "Owner Context"),
    "tests":         ("ID", "名稱", "kind"),
    "fitness":       ("NFR", "量測方式"),
    "io_map":        ("PM 來源", "RD 產物"),
    "gaps":          ("#", "問題"),
    "glossary":      ("名詞", "定義"),
}

def classify(t: Table):
    norm = [h.replace("　", " ").strip() for h in t.header]
    for name, sig in SIGNATURES.items():
        if tuple(norm[:len(sig)]) == sig:
            return name
    return None

def split_ids(cell: str):
    """'CMP-001, CMP-002' / 'CMP-001 (via IFoo)' → ['CMP-001','CMP-002']"""
    return re.findall(r"\b(?:REQ|NFR|AC|CMP|TST|API|UC|STM|SEQ)-[0-9A-Za-z-]+", cell or "")
