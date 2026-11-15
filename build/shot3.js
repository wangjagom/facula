const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1, reducedMotion: 'reduce' });
  await p.goto('file:///home/claude/web/index.html');
  await p.waitForTimeout(600);
  const targets = [['반복문: 같은 일을 여러 번','loop'],['컨트롤러 파일 읽기','ctrl'],['바인딩 경로는 자바스크립트 경로와 같아요','path8'],['this: "나 자신"','this']];
  for (const [t, name] of targets) {
    const y = await p.evaluate((t) => { document.documentElement.style.scrollBehavior='auto'; const h=[...document.querySelectorAll('h3')].find(e=>e.textContent.includes(t)); if(!h) return -1; return h.getBoundingClientRect().top + window.scrollY - 40; }, t);
    if (y < 0) { console.log('not found', t); continue; }
    await p.evaluate((y) => window.scrollTo(0, y), y);
    await p.waitForTimeout(400);
    await p.screenshot({ path: `/home/claude/build/s_${name}.png` });
  }
  await b.close();
})();
