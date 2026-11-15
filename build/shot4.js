const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 1500 } });
  await p.goto('file:///home/claude/web/index.html#part-2'); await p.waitForTimeout(500);
  const y = await p.evaluate(() => { const h=[...document.querySelectorAll('h3')].find(e=>e.textContent.includes('문자열: 따옴표')); return h.getBoundingClientRect().top + scrollY - 30; });
  await p.evaluate(y => scrollTo({top:y, behavior:'instant'}), y); await p.waitForTimeout(300);
  await p.screenshot({ path: 'str1.png' });
  await p.evaluate(() => scrollBy({top:1400, behavior:'instant'})); await p.waitForTimeout(300);
  await p.screenshot({ path: 'str2.png' });
  await b.close();
})();
