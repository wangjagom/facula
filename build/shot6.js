const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1200,height:900}});
 await p.goto('file:///home/claude/web/index.html#part-2'); await p.waitForTimeout(500);
 const info=await p.evaluate(()=>[...document.querySelectorAll('section.active details.more')].map(d=>({open:d.open,t:d.querySelector('summary').textContent})));
 console.log(JSON.stringify(info));
 const d=await p.$('section.active details.more'); await d.scrollIntoViewIfNeeded(); await p.screenshot({path:'/tmp/s6a.png'});
 await d.evaluate(e=>e.open=true); await p.screenshot({path:'/tmp/s6b.png'});
 await b.close();
})();
