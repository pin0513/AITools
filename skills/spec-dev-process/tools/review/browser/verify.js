// spec-reviewer 渲染驗證:在 Chromium 開核對面板,CDN 導向本機 mermaid,逐張圖 mermaid.parse(含收合的),回報 JS 錯誤、卡片數、溢出。
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
  await p.goto('file://' + panel, { waitUntil: 'load' }); await p.waitForTimeout(2500);
  const r = await p.evaluate(async () => {
    const parse = {}; for (const n of document.querySelectorAll('[data-did]')) { const id = n.dataset.did; if (id in parse) continue;
      const code = n.dataset.src || n.textContent; try { await mermaid.parse(code); parse[id] = 'ok'; } catch (e) { parse[id] = String(e.message || e).split('\n')[0].slice(0, 200); } }
    const ev = [...document.querySelectorAll('section')].find(s => s.querySelector('h2')?.textContent.includes('E. 證據鏈'));
    return { parse, cards: ev ? ev.querySelectorAll('article.evc').length : 0, visible_svgs: ev ? ev.querySelectorAll('.dg svg').length : 0, visible_dg: ev ? ev.querySelectorAll('.dg').length : 0,
             overflow: document.documentElement.scrollWidth > innerWidth + 1, notice: !!document.querySelector('[role=status]') };
  }).catch(e => ({ fatal: String(e) }));
  console.log(JSON.stringify({ ...r, errs })); await b.close(); })();
