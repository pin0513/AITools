"""review.serve v1:一站式審查站台。同一張看板(check-panel.html),PM / QA / RD 打開同一個網址:
做確認事項(以事情區分,不以人區分;跨職能的同一個人可一次做完)、互相提問與回答、點「檔:行」直接看原文,不切畫面、不落快照。

為什麼是伺服器而不是靜態檔:靜態看板是快照,人的判斷只能留在各自瀏覽器(localStorage)再手抄成指令;
三個角色要共同核對,判斷必須寫回同一份 SSOT(audit/signoff.md、audit/threads.md),而且畫面要反映最新的 md。

邊界(刻意的):
- 只用標準庫。spec 與 codebase 一律唯讀;唯一的寫入是 review_dir/audit/ 下的 signoff.md 與 threads.md(白名單)。
- 讀檔走 safe_join:解析後逃出專案根目錄 → 與「不存在」同一句話(那個差異只對攻擊者有意義)。
- 拒絕(hash 不符、事項不屬於這張圖、退回或不需要沒寫理由)回 200 + error;body 不是 JSON 物件回 400;未知路徑回 404。
- 沒有認證:預設只綁 127.0.0.1。要給團隊用,綁內網 IP,審核者名字是自報的(signoff.md 的 git 歷史才是稽核依據)。
- 重建時不跑瀏覽器渲染檢查(看板本身就在瀏覽器裡);要正式驗證請跑 spec-dev.py review。"""
import http.server, json, pathlib, socketserver, threading, urllib.parse
from core import config as C

WATCH_SUFFIX = {".md", ".jsonl", ".yaml", ".yml", ".html", ".png", ".jpg", ".svg"}
GENERATED = {"check-panel.html", "90-traceability.md", "boundary-report.md", "survey-candidates.md", "traceability.json"}
MAX_READ = 400_000

def safe_join(root: pathlib.Path, rel: str):
    try: p = (root / rel.lstrip("/")).resolve()
    except (OSError, ValueError): return None
    return p if p.is_relative_to(root) and p.is_file() else None

class Site:
    def __init__(self, spec_dir: pathlib.Path, cfg: dict, offline: bool):
        from tools.execute import runner_v1 as R
        self.R = R; self.cfg = dict(cfg); self.cfg["reviewer"] = {**(cfg.get("reviewer") or {}), "render_check": "off"}
        self.spec_dir = spec_dir.resolve(); self.offline = offline
        ctx = R.make_ctx(self.spec_dir, self.cfg, offline)
        self.review = ctx["review_dir"]; self.audit_dir = self.review / "audit"
        self.root = _common(ctx["project_root"], self.spec_dir, self.review)
        self.lock = threading.RLock(); self.sig = None; self.html = ""; self.last = {}; self.tracked = []

    def signature(self):
        h = []
        for base in {self.spec_dir, self.review}:
            for p in base.rglob("*"):
                if p.is_file() and p.suffix in WATCH_SUFFIX and p.name not in GENERATED and "html" not in p.relative_to(base).parts[:1]:
                    h.append((str(p), p.stat().st_mtime_ns))
        for p in self.tracked:   # 版本追蹤的文件(PM spec、mock、參考文件、名詞表…常在 spec 目錄之外)
            if p.is_file(): h.append((str(p), p.stat().st_mtime_ns))
        return hash(tuple(sorted(h)))

    def rebuild(self, force=False):
        with self.lock:
            sig = self.signature()
            if not force and sig == self.sig: return False
            ctx = self.R.make_ctx(self.spec_dir, self.cfg, self.offline)
            ctx = self.R.run_pipeline(ctx, to="S6", no_stop=True)
            gate = ctx.get("gate") or []; rules = {}
            for g in gate:
                if g["level"] != "INFO": rules[g["rule"]] = rules.get(g["rule"], 0) + 1
            self.last = {"fail": sum(1 for g in gate if g["level"] == "FAIL"), "rules": rules, "audit": (ctx.get("data") or {}).get("audit", {}).get("summary")}
            self.html = (self.review / "check-panel.html").read_text(encoding="utf-8")
            self.tracked = [self.root / d["path"] for d in ((ctx.get("data") or {}).get("versions") or {}).get("docs") or []]
            self.sig = self.signature()   # 重建本身會寫 signoff.md / threads 以外的產生物;重算以免下次又重建
            return True

    def page(self):
        self.rebuild()
        boot = json.dumps({"serve": True, "version": str(self.sig), "spec_dir": str(self.spec_dir.relative_to(self.root)) if self.spec_dir.is_relative_to(self.root) else str(self.spec_dir)}, ensure_ascii=False)
        html = self.html.replace("https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js", "/vendor/mermaid.min.js")
        return html.replace("</head>", f"<script>window.__SERVE__={boot}</script></head>", 1)

def resolve(site, rel: str):
    """看板上的「檔:行」寫法不一:專案根相對、spec 目錄相對、review 目錄相對、只有檔名、或 2 位數簡寫(30 = 30-*.md)。依序試,全部受 safe_join 限制。"""
    rel = (rel or "").strip()
    if not rel or "\x00" in rel: return None
    for base in (site.root, site.spec_dir, site.review):
        p = safe_join(site.root, str((base / rel).relative_to(site.root))) if (base / rel).resolve().is_relative_to(site.root) else None
        if p: return p
    if "/" not in rel and ".." not in rel:
        pat = f"{rel}-*.md" if rel.isdigit() and len(rel) == 2 else rel
        for base in (site.spec_dir, site.review):
            for p in sorted(base.rglob(pat)):
                if p.is_file() and p.resolve().is_relative_to(site.root): return p.resolve()
    return None

def _common(*paths):
    parts = [pathlib.Path(p).resolve().parts for p in paths]; out = []
    for xs in zip(*parts):
        if len(set(xs)) != 1: break
        out.append(xs[0])
    return pathlib.Path(*out)

def make_handler(site: Site):
    from tools.review import signoff_v1 as SO, threads_v1 as TH

    class H(http.server.BaseHTTPRequestHandler):
        server_version = "spec-review/1"
        def log_message(self, fmt, *a): pass

        def _send(self, code, body, ctype="application/json; charset=utf-8"):
            b = body if isinstance(body, bytes) else (json.dumps(body, ensure_ascii=False) if not isinstance(body, str) else body).encode("utf-8")
            self.send_response(code); self.send_header("Content-Type", ctype); self.send_header("Content-Length", str(len(b)))
            self.send_header("Cache-Control", "no-store"); self.send_header("X-Content-Type-Options", "nosniff"); self.end_headers(); self.wfile.write(b)

        def do_GET(self):
            u = urllib.parse.urlparse(self.path); q = urllib.parse.parse_qs(u.query)
            if u.path in ("/", "/index.html"): return self._send(200, site.page(), "text/html; charset=utf-8")
            if u.path == "/vendor/mermaid.min.js": return self._send(200, C.PATHS["vendor_mermaid"].read_bytes(), "application/javascript")
            if u.path == "/api/health": return self._send(200, {"ok": True, "spec": str(site.spec_dir), "root": str(site.root)})
            if u.path == "/api/state":
                changed = site.signature() != site.sig
                return self._send(200, {"version": str(site.sig), "changed": changed, **site.last})
            if u.path == "/api/read":
                p = resolve(site, (q.get("p") or [""])[0])
                if not p: return self._send(200, {"error": "檔案不存在"})
                if p.stat().st_size > MAX_READ: return self._send(200, {"error": f"檔案太大(>{MAX_READ // 1000} KB),請在編輯器開"})
                try: text = p.read_text(encoding="utf-8")
                except UnicodeDecodeError: return self._send(200, {"error": "不是文字檔"})
                return self._send(200, {"path": str(p.relative_to(site.root)), "text": text})
            return self._send(404, {"error": "not found"})

        def do_POST(self):
            u = urllib.parse.urlparse(self.path)
            if u.path not in ("/api/signoff", "/api/ask", "/api/answer", "/api/rebuild"): return self._send(404, {"error": "not found"})
            try:
                n = int(self.headers.get("Content-Length") or 0); body = json.loads(self.rfile.read(n).decode("utf-8") or "{}")
                if not isinstance(body, dict): raise ValueError
            except (ValueError, UnicodeDecodeError): return self._send(400, {"error": "body 必須是 JSON 物件"})
            s = lambda k: str(body.get(k) or "").strip()
            try:
                with site.lock:
                    if u.path == "/api/signoff":
                        dus = body.get("duties") or [s("duty")]
                        if not isinstance(dus, list) or not dus: raise ValueError("duties 必須是清單")
                        msg = " · ".join(SO.apply(site.review, s("id"), s("by"), s("decision"), s("hash"), s("note"), str(du)) for du in dus)
                    elif u.path == "/api/ask":
                        if s("to") not in ("", "PM", "QA", "RD"): raise ValueError("「給」只能是 PM / QA / RD 或留空(任何人)")
                        if not s("by"): raise ValueError("要寫你的名字")
                        msg = f"Q{TH.ask(site.audit_dir / 'threads.md', s('item'), s('by'), s('to') or '任何人', s('text'))} 已送出"
                    elif u.path == "/api/answer":
                        if not s("by"): raise ValueError("要寫你的名字")
                        r = TH.answer(site.audit_dir / "threads.md", s("n") or 0, s("by"), s("text"), body.get("close", True) is not False)
                        msg = f"Q{r['n']} {'已結案' if r['status'] == 'closed' else '已回覆'}"
                    else: msg = "已重建"
                    site.rebuild(force=True)
                return self._send(200, {"ok": True, "msg": msg, "version": str(site.sig), **site.last})
            except (SO.Refused, ValueError) as e:
                return self._send(200, {"error": str(e)})

    return H

class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True; allow_reuse_address = True

def start(spec_dir, cfg, offline=False, bind="127.0.0.1", port=8110):
    site = Site(pathlib.Path(spec_dir), cfg, offline); site.rebuild(force=True)
    srv = Server((bind, port), make_handler(site)); return srv, site

def serve(spec_dir, cfg, offline=False, bind="127.0.0.1", port=8110):
    srv, site = start(spec_dir, cfg, offline, bind, port)
    print(f"spec review 站台:http://{bind}:{srv.server_address[1]}/  (spec {site.spec_dir})")
    print(f"  寫入只會到 {site.audit_dir}/signoff.md、threads.md;讀檔範圍 {site.root}")
    if bind not in ("127.0.0.1", "localhost"): print("  ⚠ 沒有認證:審核者名字是自報的;稽核依據是 signoff.md 的 git 歷史")
    try: srv.serve_forever()
    except KeyboardInterrupt: pass
    finally: srv.server_close()
    return 0
