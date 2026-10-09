// spec-reviewer 渲染驗證:在 Chromium 開核對面板,CDN 導向本機 mermaid。
// 圖預設不在畫面上(點了才開 modal),所以從 window.__DG 取全部圖,逐張 mermaid.render(真的畫,不只 parse);
// 再實際開一次 modal 確認畫得出 SVG;回報 JS 錯誤、需求卡數、分頁數、溢出。
// 用法:node verify.js <mermaid.min.js> <check-panel.html> [width]
const { chromium } = require('playwright'); const fs = require('fs');
const [lib, panel, width] = process.argv.slice(2); const LIB = fs.readFileSync(lib, 'utf8');
(async () => {
  let b; try { b = await chromium.launch({ executablePath: fs.existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined }); }
  catch (e) { b = await chromium.launch(); }
  const p = await b.newPage({ viewport: { width: +(width || 400), height: 900 } }); const errs = [];
  p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.route('**/*', r => { const u = r.request().url();
    if (/mermaid(@|\/)[\d.]+/.test(u)) return r.fulfill({ body: LIB, contentType: 'application/javascript' });
    return u.startsWith('file:') ? r.continue() : r.abort(); });
  await p.goto('file://' + panel, { waitUntil: 'load' }); await p.waitForTimeout(2000);
  const r = await p.evaluate(async () => {
    const parse = {}; const DG = window.__DG || {}; let i = 0;
    for (const [id, code] of Object.entries(DG)) {
      try { await mermaid.render('vchk' + (i++), code); parse[id] = 'ok'; }
      catch (e) { parse[id] = String(e.message || e).split('\n')[0].slice(0, 200); document.querySelectorAll('[id^="dvchk"]').forEach(n => n.remove()); } }
    let modal = 'no-diagram'; const first = Object.keys(DG)[0];
    if (first && window.__open) { window.__open('dg:' + first); await new Promise(res => setTimeout(res, 1200));
      const m = document.getElementById('mdl'); modal = m && m.open && m.querySelector('.dg svg') ? 'ok' : 'modal 沒有畫出圖'; if (m && m.open) m.close(); }
    const visible = n => n.offsetParent !== null;
    return { parse, modal, cards: document.querySelectorAll('article.evc').length, tabs: document.querySelectorAll('nav.tabs [role=tab]').length,
             visible_dg: [...document.querySelectorAll('#app .dg')].filter(visible).length, visible_svgs: [...document.querySelectorAll('#app .dg svg')].filter(visible).length,
             overflow: document.documentElement.scrollWidth > innerWidth + 1, notice: !!document.querySelector('[role=status]') };
  }).catch(e => ({ fatal: String(e) }));
  console.log(JSON.stringify({ ...r, errs })); await b.close(); })();
