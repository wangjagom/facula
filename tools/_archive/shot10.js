const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1200,height:1000}});
 await p.goto('file:///home/claude/web/index.html#part-2'); await p.waitForTimeout(500);
 await p.evaluate(()=>{const h=[...document.querySelectorAll('section.active h3')].find(x=>x.textContent.includes('객체: 이름표')); h.scrollIntoView({behavior:'instant'})});
 await p.waitForTimeout(900); await p.screenshot({path:'/tmp/s10a.png'});
 await p.goto('file:///home/claude/web/index.html#part-3'); await p.waitForTimeout(500);
 await p.evaluate(()=>{const h=[...document.querySelectorAll('section.active h3')].find(x=>x.textContent.includes('if:')); h.scrollIntoView({behavior:'instant'})});
 await p.waitForTimeout(900); await p.screenshot({path:'/tmp/s10b.png'});
 await b.close();
})();
