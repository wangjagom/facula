const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1200,height:1000}});
 await p.goto('file:///home/claude/web/index.html#part-4'); await p.waitForTimeout(500);
 await p.evaluate(()=>{const h=[...document.querySelectorAll('section.active h3')].find(x=>x.textContent.includes('함수 기본')); window.scrollTo(0,h.getBoundingClientRect().top+scrollY-20)});
 await p.waitForTimeout(300); await p.screenshot({path:'/tmp/s9a.png'});
 await p.evaluate(()=>window.scrollBy(0,950)); await p.screenshot({path:'/tmp/s9b.png'});
 await b.close();
})();
