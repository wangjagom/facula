const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 1100 } });
  const errs=[]; p.on('pageerror', e=>errs.push(e.message));
  await p.goto('file:///home/claude/web/index.html#part-2'); await p.waitForTimeout(500);
  const y = await p.evaluate(() => { const d=document.querySelector('details.more'); return d.getBoundingClientRect().top + scrollY - 160; });
  await p.evaluate(y => scrollTo({top:y, behavior:'instant'}), y); await p.waitForTimeout(300);
  await p.screenshot({ path: 'more_closed.png' });
  await p.click('details.more > summary'); await p.waitForTimeout(300);
  await p.screenshot({ path: 'more_open.png' });
  console.log('open', await p.evaluate(() => document.querySelector('details.more').open), 'errors', JSON.stringify(errs), 'details count', await p.evaluate(()=>document.querySelectorAll('details.more').length));
  await b.close();
})();
