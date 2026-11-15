const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1200,height:900}});
 await p.goto('file:///home/claude/web/index.html#part-0'); await p.waitForTimeout(400);
 await p.screenshot({path:'/tmp/s7a.png'});
 await p.goto('file:///home/claude/web/index.html#part-17'); await p.waitForTimeout(400);
 const h=await p.$$eval('section.active h3',e=>e.map(x=>x.textContent)); console.log(h);
 await p.evaluate(()=>{[...document.querySelectorAll('section.active h3')].find(x=>x.textContent.includes('약어 풀이')).scrollIntoView()});
 await p.screenshot({path:'/tmp/s7b.png'});
 await b.close();
})();
