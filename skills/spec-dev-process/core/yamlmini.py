"""最小 YAML 子集解析:巢狀 map(縮排)、純量、行內 list [a, b]、行內 map {k: v}(可巢狀)、區塊 list - x、# 註解、引號字串。
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
        return [_scalar(x) for x in _split_top(inner, ",")] if inner else []
    if s.startswith("{") and s.endswith("}"):
        inner = s[1:-1].strip()
        out = {}
        for item in (_split_top(inner, ",") if inner else []):
            k, v = _split_top(item, ":", 1)
            out[_scalar(k)] = _scalar(v) if v.strip() else None
        return out
    if s in ("true", "True"): return True
    if s in ("false", "False"): return False
    if re.fullmatch(r"-?\d+", s): return int(s)
    if re.fullmatch(r"-?\d+\.\d+", s): return float(s)
    return s

def _split_top(s: str, sep: str, maxsplit: int = -1):
    """以 sep 切,但忽略引號內與 {} [] 內的 sep。maxsplit=1 時回傳 [left, right](找不到 sep 時 right='')。"""
    out, cur, q, depth = [], "", None, 0
    for ch in s:
        if q:
            cur += ch
            if ch == q: q = None
        elif ch in "\"'":
            q = ch; cur += ch
        elif ch in "[{":
            depth += 1; cur += ch
        elif ch in "]}":
            depth -= 1; cur += ch
        elif ch == sep and depth == 0 and (maxsplit < 0 or len(out) < maxsplit):
            out.append(cur); cur = ""
        else:
            cur += ch
    out.append(cur)
    if maxsplit == 1 and len(out) == 1: out.append("")
    return [x for x in out if x.strip()] if maxsplit < 0 else out

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
                rest = lines[pos][1][2:].strip()
                k, v = _split_top(rest, ":", 1)
                is_map = rest[:1] not in "[{\"'" and bool(v.strip() or (k and rest.endswith(":"))) and k.strip() != "" and (v == "" or v.startswith(" ") or rest.endswith(":"))
                if is_map:
                    lines[pos] = (indent + 2, rest)           # 把 "- key: v" 變成縮排更深的 map 第一行
                    items.append(parse_block(indent + 2))
                else:
                    items.append(_scalar(rest)); pos += 1
            return items
        obj = {}
        while pos < len(lines) and lines[pos][0] == indent:
            ind, line = lines[pos]
            key, rest = _split_top(line, ":", 1)
            if not key.strip() or (key.strip()[0] in "[{"):
                raise ValueError(f"yamlmini: 無法解析 '{line}'")
            key, rest = _scalar(key.strip()), rest.strip()
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
