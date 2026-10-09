"""review.mermaid v1:mermaid 原始碼的輕量文字解析(不渲染)。只抽審計核對需要的結構:
sequence → 參與者與呼叫;state → 狀態與轉移事件;class → 類別;er → 實體;C4Component → 元件與 Rel;flowchart → 節點與邊。"""
import re

def kind_of(code: str) -> str:
    head = next((l.strip() for l in code.splitlines() if l.strip() and not l.strip().startswith("%%")), "")
    for k, v in (("sequenceDiagram", "sequence"), ("stateDiagram", "state"), ("classDiagram", "class"), ("erDiagram", "erd"),
                 ("C4Context", "c4-context"), ("C4Container", "c4-container"), ("C4Component", "c4-component"), ("flowchart", "flowchart"), ("graph", "flowchart")):
        if head.startswith(k): return v
    return "other"

def parse_sequence(code: str) -> dict:
    parts, actors, calls = {}, set(), []
    for line in code.splitlines():
        s = line.strip()
        m = re.match(r"^(participant|actor)\s+(\S+?)(?:\s+as\s+(.+))?$", s)
        if m:
            pid, alias = m.group(2), (m.group(3) or m.group(2)).strip()
            parts[pid] = alias
            if m.group(1) == "actor": actors.add(pid)
            continue
        m = re.match(r"^(\S+?)\s*(-{1,2}>>|-{1,2}\)|-{1,2}x|-{1,2}>)\s*([^:]+?)\s*:\s*(.*)$", s)
        if m:
            a, arrow, b, msg = m.group(1), m.group(2), m.group(3).strip(), m.group(4)
            for x in (a, b): parts.setdefault(x, x)
            calls.append({"from": a, "to": b, "msg": msg, "reply": arrow.startswith("--")})
    return {"participants": parts, "actors": actors, "calls": calls}

def parse_state(code: str) -> dict:
    states, trans = set(), []
    for line in code.splitlines():
        s = line.strip()
        if s.startswith("note") or s.startswith("stateDiagram") or not s: continue
        m = re.match(r"^(\[\*\]|[\w-]+)\s*-->\s*(\[\*\]|[\w-]+)\s*(?::\s*(.*))?$", s)
        if m:
            a, b, ev = m.group(1), m.group(2), (m.group(3) or "").strip()
            for x in (a, b):
                if x != "[*]": states.add(x)
            trans.append({"from": a, "to": b, "event": ev, "event_name": (re.match(r"[A-Za-z_][\w-]*", ev) or [None])[0] if ev else ""})
        m = re.match(r"^state\s+\"?([^\"]+)\"?\s+as\s+(\w+)", s)
        if m: states.add(m.group(2))
    return {"states": states, "transitions": trans}

def parse_class(code: str) -> dict:
    classes, rels = set(), []
    for line in code.splitlines():
        s = line.strip()
        m = re.match(r"^class\s+([A-Za-z_]\w*)", s)
        if m: classes.add(m.group(1)); continue
        m = re.match(r'^([A-Za-z_]\w*)\s*(?:"[^"]*"\s*)?(<\|--|\*--|o--|-->|--|\.\.>|\.\.\|>|\.\.)\s*(?:"[^"]*"\s*)?([A-Za-z_]\w*)', s)
        if m: classes.update([m.group(1), m.group(3)]); rels.append((m.group(1), m.group(3)))
    return {"classes": classes, "relations": rels}

def parse_er(code: str) -> dict:
    ents, rels = set(), []
    for line in code.splitlines():
        s = line.strip()
        m = re.match(r"^([A-Za-z_]\w*)\s*\{", s)
        if m: ents.add(m.group(1)); continue
        m = re.match(r"^([A-Za-z_]\w*)\s+[|}o{]{2}--[|}o{]{2}\s+([A-Za-z_]\w*)", s)
        if m: ents.update([m.group(1), m.group(2)]); rels.append((m.group(1), m.group(2)))
    return {"entities": ents, "relations": rels}

def parse_c4(code: str) -> dict:
    comps, rels = {}, []
    for m in re.finditer(r"\b(?:Component|Container|ContainerDb|System|System_Ext|Person)\(\s*(\w+)\s*,\s*\"([^\"]*)\"", code):
        comps[m.group(1)] = m.group(2)
    for m in re.finditer(r"\bRel\(\s*(\w+)\s*,\s*(\w+)", code):
        rels.append((m.group(1), m.group(2)))
    return {"components": comps, "relations": rels}

def parse_flowchart(code: str) -> dict:
    nodes, edges = {}, []
    for line in code.splitlines():
        s = line.strip()
        if not s or s.startswith(("flowchart", "graph", "subgraph", "end", "classDef", "class ", "%%", "style")): continue
        for m in re.finditer(r"\b([A-Za-z_][\w]*)\s*(?:\[\[?\"?|\(\[?\(?\"?|\{\{?\"?|\[/\"?)([^\]\)\}\"]*)", s):
            nodes.setdefault(m.group(1), m.group(2).strip())
        chain = re.split(r"\s*(?:-->|-\.->|==>|---|--[^>]*-->)\s*(?:\|[^|]*\|\s*)?", s)
        ids = [re.match(r"([A-Za-z_][\w]*)", c).group(1) for c in chain if re.match(r"([A-Za-z_][\w]*)", c)]
        for a, b in zip(ids, ids[1:]): edges.append((a, b))
    return {"nodes": nodes, "edges": edges}

PARSERS = {"sequence": parse_sequence, "state": parse_state, "class": parse_class, "erd": parse_er,
           "c4-component": parse_c4, "c4-container": parse_c4, "c4-context": parse_c4, "flowchart": parse_flowchart}

def parse(code: str) -> dict:
    k = kind_of(code)
    return {"kind": k, **(PARSERS[k](code) if k in PARSERS else {})}
