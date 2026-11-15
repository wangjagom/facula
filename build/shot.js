const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1, reducedMotion: 'reduce' });
  await p.goto('file:///home/claude/web/index.html');
  await p.waitForTimeout(600);
  await p.evaluate(() => { document.documentElement.style.scrollBehavior='auto'; window.scrollTo(0, document.querySelector('#part-9').offsetTop + 300); });
  await p.waitForTimeout(500);
  await p.screenshot({ path: 'mid2.png' });
  await b.close();
})();
