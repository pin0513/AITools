"""e2e:在真的瀏覽器裡執行核對面板的 JavaScript(Python 測試只驗注入的資料,驗不到頁面腳本)。
需要 node + playwright + chromium;環境沒有就 skip。CDN 請求導向 vendor/mermaid.min.js,驗:無 JS 錯誤、每條需求一張卡、每張卡的圖都畫成 SVG、無語法錯誤圖、
主 CDN 失敗會改用備援、兩者都失敗會顯示提示。"""
import json, os, pathlib, shutil, subprocess, tempfile, unittest
from core import config as C

ROOT = C.ROOT; BOARD = ROOT / "examples" / "matrix" / "_board"
SCRIPT = r"""
const { chromium } = require('playwright'); const fs = require('fs');
const [lib, panel, mode, query] = process.argv.slice(2); const LIB = fs.readFileSync(lib, 'utf8');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
  const p = await b.newPage({ viewport: { width: 400, height: 900 } }); const errs = [];
  p.on('pageerror', e => errs.push(String(e)));
  await p.route('**/*', r => { const u = r.request().url();
    if (u.includes('cdn.jsdelivr.net/npm/mermaid')) return mode === 'primary' ? r.fulfill({ body: LIB, contentType: 'application/javascript' }) : r.abort();
    if (u.includes('unpkg.com/mermaid')) return mode === 'fallback' ? r.fulfill({ body: LIB, contentType: 'application/javascript' }) : r.abort();
    return u.startsWith('file:') ? r.continue() : r.abort(); });
  await p.goto('file://' + panel, { waitUntil: 'load' }); await p.waitForTimeout(2500);
  const r = await p.evaluate(() => { const ev = [...document.querySelectorAll('section')].find(s => s.querySelector('h2')?.textContent.includes('E. 證據鏈'));
    return { cards: ev ? ev.querySelectorAll('article.evc').length : 0, dg: ev ? ev.querySelectorAll('.dg').length : 0, svgs: ev ? ev.querySelectorAll('.dg svg').length : 0,
      errSvg: [...document.querySelectorAll('svg')].filter(s => /Syntax error|Parse error/i.test(s.textContent)).length,
      notice: !!document.querySelector('[role=status]'), overflow: document.documentElement.scrollWidth > innerWidth + 1 }; });
  const parseErrors = await p.evaluate(async () => { const out = []; for (const n of document.querySelectorAll('pre.mermaid, pre.pre[data-src]')) {
      const code = n.dataset.src || n.textContent; try { await mermaid.parse(code); } catch (e) { out.push(code.split('\n')[0] + ': ' + String(e.message || e).split('\n')[0]); } } return out; }).catch(() => ['mermaid 未載入']);
  let lookup = null;
  if (query) { await p.fill('#lk', query); await p.waitForTimeout(300);
    lookup = await p.evaluate(() => { const box = document.getElementById('lkout'); return { shown: !box.hidden, rows: box.querySelectorAll('tr').length, assets: box.querySelectorAll('details').length }; }); }
  const card = await p.evaluate(() => { const d = [...document.querySelectorAll('article.evc details')].find(x => x.querySelector('summary')?.textContent.includes('詞彙與已知資產'));
    return d ? d.querySelector('summary').textContent : ''; });
  console.log(JSON.stringify({ ...r, errs, lookup, card, parseErrors })); await b.close(); })();
"""

def _node_ok():
    if not shutil.which("node"): return False
    r = subprocess.run(["node", "-e", "require('playwright')"], capture_output=True, env={**os.environ, "NODE_PATH": _npm_root()})
    return r.returncode == 0 and pathlib.Path("/opt/pw-browsers").exists()

def _npm_root():
    try: return subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    except Exception: return ""

@unittest.skipUnless(_node_ok(), "需要 node + playwright + /opt/pw-browsers")
class PanelBrowserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = pathlib.Path(tempfile.mkdtemp()); cls.js = cls.tmp / "run.js"; cls.js.write_text(SCRIPT, encoding="utf-8")

    @classmethod
    def tearDownClass(cls): shutil.rmtree(cls.tmp)

    def run_panel(self, panel, mode, query=""):
        r = subprocess.run(["node", str(self.js), str(ROOT / "vendor" / "mermaid.min.js"), str(panel), mode] + ([query] if query else []), capture_output=True, text=True,
                           env={**os.environ, "NODE_PATH": _npm_root()}, timeout=120)
        return json.loads(r.stdout.strip().splitlines()[-1])

    def test_every_panel_renders_every_requirement_with_diagrams(self):
        for panel in sorted((BOARD / "tc").glob("*.html")):
            with self.subTest(panel=panel.name):
                exp = json.loads((ROOT / "examples" / "matrix" / panel.stem / "expected.json").read_text(encoding="utf-8"))
                n_req = 4   # 3 REQ + 1 NFR
                r = self.run_panel(panel, "primary")
                self.assertEqual(r["errs"], []); self.assertEqual(r["cards"], n_req)
                self.assertGreaterEqual(r["dg"], n_req); self.assertEqual(r["svgs"], r["dg"], "每張預設顯示的圖都要畫成 SVG")
                self.assertEqual(r["errSvg"], 0); self.assertFalse(r["notice"]); self.assertFalse(r["overflow"], "400px 寬不得水平捲動")
                self.assertEqual(r["parseErrors"], [], "所有圖(含收合的)都要能被 mermaid 解析")

    def test_fallback_cdn_and_failure_notice(self):
        panel = sorted((BOARD / "tc").glob("*.html"))[0]
        r = self.run_panel(panel, "fallback"); self.assertEqual(r["svgs"], r["dg"]); self.assertFalse(r["notice"])
        r = self.run_panel(panel, "none"); self.assertEqual(r["svgs"], 0); self.assertTrue(r["notice"]); self.assertEqual(r["errs"], [])

    def test_lookup_finds_glossary_naming_and_docs_on_testcase1(self):
        panel = ROOT / "examples" / "testcase1-form-system" / "specs" / "rd" / "issue-c" / "spec-review" / "check-panel.html"
        r = self.run_panel(panel, "primary", "FormSubmission")
        self.assertEqual(r["errs"], []); self.assertTrue(r["lookup"]["shown"]); self.assertGreater(r["lookup"]["rows"], 2)
        self.assertIn("詞彙與已知資產", r["card"])
        r = self.run_panel(panel, "primary", "INotifier")
        self.assertGreaterEqual(r["lookup"]["assets"], 1, "docs/guidelines 與 specs/done 都提到 INotifier")

    def test_hand_written_example_diagrams_all_parse(self):
        for panel in (ROOT / "examples" / "testcase1-form-system" / "specs" / "rd" / "issue-c" / "spec-review" / "check-panel.html",
                      ROOT / "examples" / "avatar-upload" / "check-panel.html"):
            with self.subTest(panel=panel.parent.name):
                r = self.run_panel(panel, "primary")
                self.assertEqual(r["errs"], []); self.assertEqual(r["parseErrors"], [])
