"""e2e:一站式審查站台(spec-dev.py serve)。在 testcase1 的複本上起站台:
API —— 讀檔不逃出根目錄、確認事項的 hash 防護 / 退回與不需要要理由 / 同一人一次做多項、提問與回答寫回 threads.md;
瀏覽器 —— 填名字 → 全部通過 → 送出 → signoff.md 更新、看板重新整理後仍開在那張圖;提問 → 未結提問;點 檔:行 → 原文抽屜標出那一行。"""
import json, os, pathlib, shutil, subprocess, tempfile, threading, unittest, urllib.request
from core import config as C
from tools.review import serve_v1 as SV
from tests.e2e.test_panel_browser import _node_ok, _npm_root

ROOT = C.ROOT; TC1 = ROOT / "examples" / "testcase1-form-system"

def http(base, path, body=None):
    req = urllib.request.Request(base + path, data=None if body is None else json.dumps(body).encode(), headers={"Content-Type": "application/json"},
                                 method="GET" if body is None else "POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r: return r.status, (json.loads(r.read()) if "json" in r.headers.get("Content-Type", "") else r.read().decode())
    except urllib.error.HTTPError as e: return e.code, json.loads(e.read() or b"{}")

class ServeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = pathlib.Path(tempfile.mkdtemp()); cls.proj = cls.tmp / "tc1"
        shutil.copytree(TC1, cls.proj, ignore=shutil.ignore_patterns("audit"))
        spec = cls.proj / "specs" / "rd" / "issue-c" / "spec"
        cls.srv, cls.site = SV.start(spec, C.load_config(spec, None), False, "127.0.0.1", 0)
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()
        cls.base = f"http://127.0.0.1:{cls.srv.server_address[1]}"
        cls.audit = cls.site.audit_dir

    @classmethod
    def tearDownClass(cls): cls.srv.shutdown(); cls.srv.server_close(); shutil.rmtree(cls.tmp)

    def items(self): return {i["id"]: i for i in json.loads((self.audit / "audit.json").read_text(encoding="utf-8"))["items"]}

    def test_1_page_and_read_stay_inside_root(self):
        st, html = http(self.base, "/"); self.assertEqual(st, 200); self.assertIn("window.__SERVE__", html); self.assertIn("/vendor/mermaid.min.js", html)
        st, r = http(self.base, "/api/read?p=specs/rd/issue-c/spec/10-requirements.md"); self.assertIn("REQ-001", r["text"])
        self.assertIn("REQ-001", http(self.base, "/api/read?p=10-requirements.md")[1]["text"], "spec 目錄相對路徑")
        self.assertIn("CMP-001", http(self.base, "/api/read?p=30")[1]["text"], "2 位數簡寫")
        for bad in ("../../../../etc/passwd", "/etc/passwd", "specs/../../../x", "nope.md", "passwd", "../../../../../../../../etc/hosts"):
            self.assertEqual(http(self.base, "/api/read?p=" + bad)[1], {"error": "檔案不存在"}, bad)
        self.assertEqual(http(self.base, "/api/nope")[0], 404); self.assertEqual(http(self.base, "/api/delete", {})[0], 404)
        req = urllib.request.Request(self.base + "/api/signoff", data=b"[1]", method="POST")
        with self.assertRaises(urllib.error.HTTPError) as e: urllib.request.urlopen(req)
        self.assertEqual(e.exception.code, 400)

    def test_2_duties_by_thing_not_person(self):
        it = self.items()["AUTO-TRACE-REQ-001"]; self.assertEqual(it["duties"], ["intent", "testable"])
        r = http(self.base, "/api/signoff", {"id": it["id"], "duties": ["intent", "testable"], "decision": "approved", "hash": "000000000000", "by": "Paul"})[1]
        self.assertIn("拒絕核准", r["error"])
        self.assertIn("沒有「buildable」", http(self.base, "/api/signoff", {"id": it["id"], "duties": ["buildable"], "decision": "approved", "hash": it["hash"], "by": "Paul"})[1]["error"])
        self.assertIn("理由", http(self.base, "/api/signoff", {"id": it["id"], "duties": ["testable"], "decision": "n/a", "hash": it["hash"], "by": "Paul"})[1]["error"])
        r = http(self.base, "/api/signoff", {"id": it["id"], "duties": ["intent", "testable"], "decision": "approved", "hash": it["hash"], "by": "Paul"})[1]
        self.assertTrue(r.get("ok"), r)   # 同一個人一次做完兩項(跨職能)
        it2 = self.items()["AUTO-TRACE-REQ-001"]; self.assertEqual(it2["signoff"], "approved")
        self.assertEqual({k: v["by"] for k, v in it2["signoffs"].items()}, {"intent": "Paul", "testable": "Paul"})
        seq = self.items()["AUTO-SEQ-REQ-001"]
        r = http(self.base, "/api/signoff", {"id": seq["id"], "duties": ["buildable"], "decision": "n/a", "note": "沿用既有流程,無新元件", "hash": seq["hash"], "by": "Amy"})[1]
        self.assertTrue(r.get("ok"), r); self.assertEqual(self.items()["AUTO-SEQ-REQ-001"]["signoff"], "approved", "不需要(附理由)也算做完")

    def test_3_threads(self):
        r = http(self.base, "/api/ask", {"item": "SEQ-001", "to": "PM", "by": "Amy", "text": "審核者指派是誰決定?"})[1]; self.assertTrue(r.get("ok"), r)
        th = json.loads((self.audit / "audit.json").read_text(encoding="utf-8"))["threads"]; q = th[-1]
        self.assertEqual((q["item"], q["to"], q["status"]), ("SEQ-001", "PM", "open"))
        self.assertEqual(r["rules"].get("G-RV-threads"), 1, "未結提問要進 Gate(WARN)")
        r = http(self.base, "/api/answer", {"n": q["n"], "by": "Paul", "text": "由表單擁有者設定"})[1]; self.assertTrue(r.get("ok"), r)
        q2 = [x for x in json.loads((self.audit / "audit.json").read_text(encoding="utf-8"))["threads"] if x["n"] == q["n"]][0]
        self.assertEqual(q2["status"], "closed"); self.assertIn("Paul:由表單擁有者設定", q2["answer"])
        self.assertIn("審核者指派是誰決定?", (self.audit / "threads.md").read_text(encoding="utf-8"))

    @unittest.skipUnless(_node_ok(), "需要 node + playwright")
    def test_4_browser_flow(self):
        js = self.tmp / "flow.js"
        js.write_text(r"""
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
  const p = await b.newPage({ viewport: { width: 1200, height: 900 } }); const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto(process.argv[2]); await p.waitForTimeout(1500); const out = {};
  out.serveTitle = await p.textContent('#audit h2');
  await p.fill('#reviewer', 'Paul');
  const it = p.locator('#aud-STM-DOM-001'); await p.click('.audbar button[data-f="all"]'); await it.locator(':scope > summary').click(); await p.waitForTimeout(500);
  out.duties = await it.locator('.duty').count();
  await it.locator('button.allok').click(); await it.locator('button.send').click(); await p.waitForTimeout(2500);
  const it2 = p.locator('#aud-STM-DOM-001'); out.reopened = await it2.evaluate(d => d.open);
  out.chips = await it2.locator(':scope > summary').textContent();
  await it2.locator('.qtext').fill('Rejected 之後能再送嗎?'); await it2.locator('.qto').selectOption('PM'); await it2.locator('button.qbtn').click(); await p.waitForTimeout(2500);
  out.inbox = await p.locator('.qinbox').textContent().catch(() => '');
  await p.locator('#aud-STM-DOM-001 dl.prov .loc.link').first().click(); await p.waitForTimeout(800);
  out.viewer = { shown: await p.locator('#srcv').isVisible(), path: await p.textContent('#srcv .p'), hit: await p.locator('#srcv .ln.hit').count() };
  out.errs = errs; console.log(JSON.stringify(out)); await b.close(); })();
""", encoding="utf-8")
        r = subprocess.run(["node", str(js), self.base + "/"], capture_output=True, text=True, env={**os.environ, "NODE_PATH": _npm_root()}, timeout=120)
        o = json.loads(r.stdout.strip().splitlines()[-1]) if r.stdout.strip() else self.fail(r.stderr[-800:])
        self.assertEqual(o["errs"], []); self.assertIn("站台模式", o["serveTitle"])
        self.assertEqual(o["duties"], 2); self.assertTrue(o["reopened"], "送出後重新整理,仍開在那張圖")
        self.assertIn("全部做完", o["chips"])
        sm = (self.audit / "signoff.md").read_text(encoding="utf-8")
        self.assertRegex(sm, r"\| STM-DOM-001 \| buildable \| .* \| approved \| Paul \|"); self.assertRegex(sm, r"\| STM-DOM-001 \| testable \| .* \| approved \| Paul \|")
        self.assertIn("Rejected 之後能再送嗎?", o["inbox"])
        self.assertTrue(o["viewer"]["shown"]); self.assertIn("20-domain-model.md", o["viewer"]["path"]); self.assertEqual(o["viewer"]["hit"], 1)
