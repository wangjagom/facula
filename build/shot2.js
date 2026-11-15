const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1, reducedMotion: 'reduce' });
  await p.goto('file:///home/claude/web/index.html');
  await p.waitForTimeout(600);
  const y = await p.evaluate(() => { document.documentElement.style.scrollBehavior='auto'; const h=[...document.querySelectorAll('h3')].find(e=>e.textContent.includes('화살표 함수')); return h.getBoundingClientRect().top + window.scrollY - 40; });
  await p.evaluate((y) => window.scrollTo(0, y), y);
  await p.waitForTimeout(500);
  await p.screenshot({ path: 'arrow.png' });
  const y2 = await p.evaluate(() => { const h=[...document.querySelectorAll('strong')].find(e=>e.textContent.startsWith('find')); return h.getBoundingClientRect().top + window.scrollY - 60; });
  await p.evaluate((y) => window.scrollTo(0, y), y2);
  await p.waitForTimeout(400);
  await p.screenshot({ path: 'find.png' });
  await b.close();
})();
