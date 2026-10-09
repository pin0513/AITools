"""e2e:在真的瀏覽器裡執行核對面板的 JavaScript(Python 測試只驗注入的資料,驗不到頁面腳本)。
需要 node + playwright + chromium;環境沒有就 skip。CDN 請求導向 vendor/mermaid.min.js,驗:無 JS 錯誤、分頁、每條需求一張卡、
圖預設不展開(只放晶片)、點晶片開 modal 畫出 SVG、全部圖都畫得出來、主 CDN 失敗會改用備援、兩者都失敗會顯示提示。"""
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
  await p.click('nav.tabs [data-tab=evidence]').catch(() => {}); await p.waitForTimeout(300);
  const r = await p.evaluate(() => { const ev = document.getElementById('tab-evidence');
    return { tabs: document.querySelectorAll('nav.tabs [role=tab]').length, cards: ev ? ev.querySelectorAll('article.evc').length : 0,
      inline: [...document.querySelectorAll('#app .dg')].filter(n => n.offsetParent !== null).length, chips: ev ? ev.querySelectorAll('.chip[data-open^="dg:"]').length : 0,
      notice: !!document.querySelector('[role=status]'), overflow: document.documentElement.scrollWidth > innerWidth + 1 }; });
  let modalSvg = 0;
  if (r.chips) { await p.click('#tab-evidence .chip[data-open^="dg:"]'); await p.waitForTimeout(1200); modalSvg = await p.locator('#mdl .dg svg').count();
    r.errSvg = await p.evaluate(() => [...document.querySelectorAll('#mdl svg')].filter(s => /Syntax error|Parse error/i.test(s.textContent)).length); await p.keyboard.press('Escape'); }
  r.modalSvg = modalSvg;
  const parseErrors = await p.evaluate(async () => { const out = []; let i = 0; for (const [id, code] of Object.entries(window.__DG || {})) {
      try { await mermaid.render('tchk' + (i++), code); } catch (e) { out.push(id + ': ' + String(e.message || e).split('\n')[0]); } } return out; }).catch(() => ['mermaid 未載入']);
  let lookup = null;
  if (query) { await p.click('nav.tabs [data-tab=evidence]'); await p.fill('#lk', query); await p.waitForTimeout(300);
    lookup = await p.evaluate(() => { const box = document.getElementById('lkout'); return { shown: !box.hidden, rows: box.querySelectorAll('tr').length, assets: box.querySelectorAll('details').length }; }); }
  const card = await p.evaluate(() => { const c = document.querySelector('article.evc .chip[data-open^="tb:nm:"]'); return c ? c.parentElement.textContent : ''; });
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
        panels = [p for p in sorted((BOARD / "tc").glob("*.html")) if (ROOT / "examples" / "matrix" / p.stem / "expected.json").exists()]
        self.assertEqual(len(panels), 15)
        for panel in panels:   # 只測矩陣 15 份;testcase1 等其他範例由 test_hand_written_example_diagrams_all_parse 測
            with self.subTest(panel=panel.name):
                n_req = 4   # 3 REQ + 1 NFR
                r = self.run_panel(panel, "primary")
                self.assertEqual(r["errs"], []); self.assertEqual(r["cards"], n_req); self.assertGreaterEqual(r["tabs"], 6)
                self.assertEqual(r["inline"], 0, "圖預設不展開"); self.assertGreaterEqual(r["chips"], n_req, "每條需求至少一張圖的晶片")
                self.assertEqual(r["modalSvg"], 1, "點晶片 → modal 畫出那一張圖"); self.assertEqual(r["errSvg"], 0)
                self.assertFalse(r["notice"]); self.assertFalse(r["overflow"], "400px 寬不得水平捲動")
                self.assertEqual(r["parseErrors"], [], "所有圖都要畫得出來")

    def test_fallback_cdn_and_failure_notice(self):
        panel = sorted((BOARD / "tc").glob("*.html"))[0]
        r = self.run_panel(panel, "fallback"); self.assertEqual(r["modalSvg"], 1); self.assertFalse(r["notice"])
        r = self.run_panel(panel, "none"); self.assertEqual(r["modalSvg"], 0); self.assertTrue(r["notice"]); self.assertEqual(r["errs"], [])

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

AUDIT_SCRIPT = r"""
const { chromium } = require('playwright'); const fs = require('fs');
const [lib, panel] = process.argv.slice(2); const LIB = fs.readFileSync(lib, 'utf8');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
  const p = await b.newPage({ viewport: { width: 1200, height: 900 } }); const errs = [];
  p.on('pageerror', e => errs.push(String(e)));
  await p.route('**/*', r => { const u = r.request().url();
    if (u.includes('mermaid')) return r.fulfill({ body: LIB, contentType: 'application/javascript' });
    return u.startsWith('file:') ? r.continue() : r.abort(); });
  await p.goto('file://' + panel + '#audit', { waitUntil: 'load' }); await p.waitForTimeout(1500);
  const vis = () => p.evaluate(() => [...document.querySelectorAll('#audlist > .aud')].filter(d => !d.hidden).length);
  const out = { todo: await vis() };
  await p.click('.audbar button[data-f="all"]'); out.all = await vis();
  await p.click('.audbar button[data-f="SA"]'); out.sa = await vis();
  await p.click('.audbar button[data-f="table-row"]'); out.rows = await vis();
  await p.click('.audbar button[data-f="all"]');
  await p.fill('#reviewer', 'Paul');
  await p.click('#audlist > .aud[data-id="AUTO-SEQ-REQ-001"]'); await p.waitForTimeout(1000);
  const m = p.locator('#mdl'); out.modalOpen = await m.evaluate(d => d.open); out.hash = await p.evaluate(() => location.hash);
  out.svg = await m.locator('.audg .dg svg').count();
  out.prov = await m.locator('dl.prov dt').allTextContents();
  const duty = m.locator('.duty').first();
  await duty.locator('input[value="approved"]').check(); await p.waitForTimeout(100);
  out.cmdApprove = await p.inputValue('#socmd');
  await duty.locator('input[value="rejected"]').check(); await p.waitForTimeout(100);
  out.statRejectNoNote = await p.textContent('#sostat');
  await duty.locator('input.note').fill('補上 Repository'); await p.waitForTimeout(100);
  out.cmdReject = await p.inputValue('#socmd');
  await p.keyboard.press('Escape');
  await p.click('#somd'); await p.waitForTimeout(100); out.md = await p.inputValue('#socmd');
  await p.goto('file://' + panel + '#tab=audit&open=aud:AUTO-SEQ-REQ-001', { waitUntil: 'load' }); await p.reload({ waitUntil: 'load' }); await p.waitForTimeout(1000);
  out.persisted = await p.evaluate(() => !!document.querySelector('#mdl[open] fieldset.dec input[value="rejected"]:checked'));
  out.errs = errs; console.log(JSON.stringify(out)); await b.close(); })();
"""

@unittest.skipUnless(_node_ok(), "需要 node + playwright + /opt/pw-browsers")
class AuditBoardBrowserTest(unittest.TestCase):
    """F. 圖與表審計:看板上和人一起確認——篩選、展開看圖與來源/過程/目標、做判斷 → 產生 signoff 指令 / md 列,判斷留在瀏覽器。"""
    def test_audit_queue_and_human_decisions_produce_signoff_commands(self):
        panel = ROOT / "examples" / "testcase1-form-system" / "specs" / "rd" / "issue-c" / "spec-review" / "check-panel.html"
        audit = json.loads((panel.parent / "audit" / "audit.json").read_text(encoding="utf-8"))
        tmp = pathlib.Path(tempfile.mkdtemp())
        try:
            js = tmp / "audit.js"; js.write_text(AUDIT_SCRIPT, encoding="utf-8")
            r = subprocess.run(["node", str(js), str(ROOT / "vendor" / "mermaid.min.js"), str(panel)], capture_output=True, text=True,
                               env={**os.environ, "NODE_PATH": _npm_root()}, timeout=120)
            o = json.loads(r.stdout.strip().splitlines()[-1])
        finally: shutil.rmtree(tmp)
        S = audit["summary"]
        self.assertEqual(o["errs"], [])
        self.assertEqual(o["all"], len(audit["items"])); self.assertEqual(o["sa"], S["by_phase"]["SA"] + S["table_rows"])
        self.assertEqual(o["rows"], S["table_rows"]); self.assertGreater(o["todo"], 0)
        self.assertTrue(o["modalOpen"]); self.assertIn("open=aud%3AAUTO-SEQ-REQ-001", o["hash"], "modal 有可分享的連結")
        self.assertEqual(o["svg"], 1, "點開後圖要畫出來")
        for k in ("來源", "過程", "目標", "機器核對", "渲染", "內容 hash"): self.assertIn(k, o["prov"])
        self.assertRegex(o["cmdApprove"], r'^python3 spec-dev\.py signoff \S+ AUTO-SEQ-REQ-001 --duty buildable --hash [0-9a-f]{12} --by "Paul"$')
        self.assertIn("有退回或不需要沒寫理由", o["statRejectNoNote"])
        self.assertIn("--reject", o["cmdReject"]); self.assertIn('--note "補上 Repository"', o["cmdReject"])
        self.assertRegex(o["md"], r"^\| AUTO-SEQ-REQ-001 \| buildable \| .* \| rejected \| Paul \| \d{4}-\d{2}-\d{2} \| 補上 Repository \|$")
        self.assertTrue(o["persisted"], "判斷要留在瀏覽器,用連結重開不丟")
