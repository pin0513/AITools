"""最小 YAML 子集解析:巢狀 map(2 空格縮排)、純量、行內 list [a, b]、區塊 list - x、# 註解、引號字串。
有 PyYAML 時優先用 PyYAML。只為 config.yaml 服務,不支援多行字串與錨點。"""
import re

def _scalar(s: str):
    s = s.strip()
    if s == "" or s == "~" or s == "null":
        return None
    if s[0] in "\"'" and s[-1] == s[0] and len(s) >= 2:
        return s[1:-1]
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        return [_scalar(x) for x in _split_commas(inner)] if inner else []
    if s in ("true", "True"): return True
    if s in ("false", "False"): return False
    if re.fullmatch(r"-?\d+", s): return int(s)
    if re.fullmatch(r"-?\d+\.\d+", s): return float(s)
    return s

def _split_commas(s: str):
    out, cur, q = [], "", None
    for ch in s:
        if q:
            cur += ch
            if ch == q: q = None
        elif ch in "\"'":
            q = ch; cur += ch
        elif ch == ",":
            out.append(cur); cur = ""
        else:
            cur += ch
    if cur.strip(): out.append(cur)
    return out

def _strip_comment(line: str) -> str:
    q, out = None, ""
    for i, ch in enumerate(line):
        if q:
            out += ch
            if ch == q: q = None
        elif ch in "\"'":
            q = ch; out += ch
        elif ch == "#" and (i == 0 or line[i - 1] in " \t"):
            break
        else:
            out += ch
    return out.rstrip()

def loads(text: str):
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text)
    except ImportError:
        pass
    lines = []
    for raw in text.splitlines():
        line = _strip_comment(raw)
        if line.strip():
            lines.append((len(line) - len(line.lstrip(" ")), line.strip()))
    pos = 0

    def parse_block(indent):
        nonlocal pos
        if pos < len(lines) and lines[pos][1].startswith("- "):
            items = []
            while pos < len(lines) and lines[pos][0] == indent and lines[pos][1].startswith("- "):
                items.append(_scalar(lines[pos][1][2:])); pos += 1
            return items
        obj = {}
        while pos < len(lines) and lines[pos][0] == indent:
            ind, line = lines[pos]
            m = re.match(r"^([^:]+):(.*)$", line)
            if not m:
                raise ValueError(f"yamlmini: 無法解析 '{line}'")
            key, rest = m.group(1).strip(), m.group(2).strip()
            pos += 1
            if rest == "":
                if pos < len(lines) and lines[pos][0] > indent:
                    obj[key] = parse_block(lines[pos][0])
                else:
                    obj[key] = None
            else:
                obj[key] = _scalar(rest)
        return obj

    return parse_block(lines[0][0]) if lines else {}

def load(path):
    with open(path, encoding="utf-8") as f:
        return loads(f.read())
