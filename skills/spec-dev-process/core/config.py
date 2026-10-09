"""載入套件設定、專案覆寫、規則、流程、契約、工具登錄。所有 YAML 都經 core.yamlmini。"""
import importlib, pathlib
from . import yamlmini

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATHS = {
    "config": ROOT / "config.yaml",
    "pipeline": ROOT / "process" / "pipeline.yaml",
    "contracts": ROOT / "process" / "io-contracts.yaml",
    "registry": ROOT / "tools" / "registry.yaml",
    "rulesets": ROOT / "rules" / "rulesets.yaml",
    "rules_dir": ROOT / "rules",
    "templates": ROOT / "process" / "templates",
    "vendor_mermaid": ROOT / "vendor" / "mermaid.min.js",
}

def _merge(base: dict, over: dict) -> dict:
    out = dict(base)
    for k, v in (over or {}).items():
        out[k] = _merge(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out

def find_override(d: pathlib.Path):
    for p in [d, *d.parents]:
        c = p / ".spec-dev.yaml"
        if c.exists():
            return c
    return None

def load_config(d: pathlib.Path, explicit=None) -> dict:
    cfg = yamlmini.load(PATHS["config"]) or {}
    src = pathlib.Path(explicit) if explicit else find_override(d)
    if src and src.exists():
        cfg = _merge(cfg, yamlmini.load(src) or {})
        cfg["_config_override"] = str(src)
    return cfg

def load_rules(cfg: dict) -> dict:
    """回傳 {id: rule};已套用 rulesets 順序、專案 disable / overrides。rule 多一個 '_order' 欄。"""
    rs = yamlmini.load(PATHS["rulesets"])
    proj = (cfg.get("rules") or {})
    disabled = set(proj.get("disable") or [])
    overrides = proj.get("overrides") or {}
    rules, order = {}, 0
    for cat in ("boundary", "gates"):
        for rid in rs["default"][cat]:
            if rid in disabled:
                continue
            p = PATHS["rules_dir"] / cat / f"{rid}.yaml"
            if not p.exists():
                raise FileNotFoundError(f"rulesets 引用的規則檔不存在:{p}")
            rule = yamlmini.load(p)
            if rule["id"] != rid:
                raise ValueError(f"{p} 的 id '{rule['id']}' 與檔名不符")
            if rid in overrides:
                rule = _merge(rule, overrides[rid])
            rule["_order"] = order; order += 1
            rules[rid] = rule
    return rules

def load_methodology(name: str) -> dict:
    p = PATHS["rules_dir"] / "methodology" / "sa" / f"{name}.yaml"
    if not p.exists():
        raise FileNotFoundError(f"SA 方法論 {name} 不存在:{p}(可用:{[x.stem for x in p.parent.glob('*.yaml')]})")
    return yamlmini.load(p)

def load_pipeline() -> dict:
    return yamlmini.load(PATHS["pipeline"])

def load_contracts() -> dict:
    return yamlmini.load(PATHS["contracts"])

def load_registry() -> dict:
    return yamlmini.load(PATHS["registry"])

def resolve_tool(ref: str, registry: dict):
    """'analyze.extract@1' / 'analyze.extract' → (callable, version)。模組路徑 'pkg.mod' 取 run,'pkg.mod:fn' 取 fn。"""
    name, _, ver = ref.partition("@")
    entry = registry["tools"].get(name)
    if not entry:
        raise KeyError(f"registry 沒有工具 {name}")
    ver = int(ver) if ver else int(entry["latest"])
    target = entry["versions"].get(ver) or entry["versions"].get(str(ver))
    if not target:
        raise KeyError(f"工具 {name} 沒有版本 {ver}(有:{sorted(entry['versions'])})")
    modpath, _, fn = str(target).partition(":")
    mod = importlib.import_module(modpath)
    return getattr(mod, fn or "run"), ver
