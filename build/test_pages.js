const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 1000 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type()==='error') errs.push(m.text()); });
  await p.goto('file:///home/claude/web/index.html');
  await p.waitForTimeout(500);
  const state = () => p.evaluate(() => ({
    parts: [...document.querySelectorAll('section.part')].filter(s => s.offsetParent !== null).map(s => s.id),
    concepts: [...document.querySelectorAll('.concept')].filter(c => c.offsetParent !== null).map(c => c.id),
    h3vis: [...document.querySelectorAll('.prose h3')].filter(h => h.offsetParent !== null).length,
    h2vis: [...document.querySelectorAll('section.part h2')].filter(h => h.offsetParent !== null).length,
    hash: location.hash, title: document.title, y: Math.round(scrollY),
    cur: [...document.querySelectorAll('.sidebar a[aria-current]')].map(a => a.textContent.trim()).join('|'),
    rail: [...document.querySelectorAll('.otp-list')].filter(u => !u.hidden).map(u => u.dataset.sec)
  }));
  console.log('load', JSON.stringify(await state()));
  await p.click('.sidebar .toc a[href="#part-4"]'); await p.waitForTimeout(200);
  console.log('3부 page', JSON.stringify(await state()));
  await p.screenshot({ path: 'pg_part.png' });
  await p.click('section.active .concept-list a[href="#s21"]'); await p.waitForTimeout(200);
  console.log('concept s21', JSON.stringify(await state()));
  await p.screenshot({ path: 'pg_concept.png' });
  await p.click('section.active .concept.active .pager .next'); await p.waitForTimeout(200);
  console.log('next', JSON.stringify(await state()));
  await p.evaluate(() => scrollTo(0, 400));
  await p.click('section.active .concept.active .pager .prev'); await p.waitForTimeout(200);
  console.log('prev', JSON.stringify(await state()));
  await p.click('section.active .concept.active .crumb a'); await p.waitForTimeout(200);
  console.log('crumb', JSON.stringify(await state()));
  // every page reachable, exactly one visible
  const ids = await p.evaluate(() => [...document.querySelectorAll('section.part')].map(s => s.id).concat([...document.querySelectorAll('.concept')].map(c => c.id.slice(2))));
  let ok = 0, bad = [];
  for (const id of ids) {
    await p.evaluate((id) => { location.hash = '#' + id; }, id); await p.waitForTimeout(40);
    const s = await state();
    const isPart = id.startsWith('part-');
    const good = isPart ? (s.parts.length === 1 && s.parts[0] === id && s.concepts.length === 0 && s.h2vis === 1)
                        : (s.parts.length === 1 && s.concepts.length === 1 && s.concepts[0] === 'c-' + id && s.h3vis === 1 && s.h2vis === 0);
    if (good) ok++; else bad.push(id);
  }
  console.log('pages ok', ok, '/', ids.length, 'bad', JSON.stringify(bad));
  // walk the whole book with "next" from the home page
  await p.evaluate(() => { location.hash = '#part-0'; }); await p.waitForTimeout(100);
  let steps = 0;
  while (steps < 400) {
    const n = await p.$('section.part.active .concept.active .pager .next, section.part.active:not(.show-concept) > .part-pager .next');
    if (!n) break;
    await n.click(); await p.waitForTimeout(15); steps++;
  }
  console.log('next-walk steps', steps, JSON.stringify((await state()).hash));
  // xref deep links resolve to a concept page
  const xr = await p.evaluate(() => [...document.querySelectorAll('a.xref')].map(a => a.getAttribute('href')));
  const known = new Set(ids); const missing = xr.filter(h => !known.has(h.slice(1)));
  console.log('xrefs', xr.length, 'missing', JSON.stringify(missing));
  await p.goto('file:///home/claude/web/index.html#s30'); await p.waitForTimeout(300);
  console.log('deep s30', JSON.stringify(await state()));
  await p.click('.brand'); await p.waitForTimeout(200);
  console.log('brand', JSON.stringify(await state()));
  await p.setViewportSize({ width: 390, height: 800 });
  await p.evaluate(() => { location.hash = '#part-4'; }); await p.waitForTimeout(300);
  await p.screenshot({ path: 'pg_mobile.png' });
  console.log('errors', JSON.stringify(errs));
  await b.close();
})();
