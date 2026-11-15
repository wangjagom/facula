const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1200,height:1000}});
 await p.goto('file:///home/claude/web/index.html#part-4'); await p.waitForTimeout(500);
 const d=await p.$$('section.active details.gate'); console.log('gates p4',d.length);
 await d[0].evaluate(e=>e.scrollIntoView({behavior:'instant',block:'center'})); await p.waitForTimeout(700); await p.screenshot({path:'/tmp/s11a.png'});
 await d[0].evaluate(e=>e.open=true); await d[0].evaluate(e=>e.scrollIntoView({behavior:'instant',block:'start'})); await p.waitForTimeout(700); await p.screenshot({path:'/tmp/s11b.png'});
 await b.close();
})();
