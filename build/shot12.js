const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1200,height:1000}});
 for (const [hash,name] of [['#part-5','p5'],['#part-6','p6'],['#part-7','p7']]) {
  await p.goto('file:///home/claude/web/index.html'+hash); await p.waitForTimeout(500);
  const info=await p.$$eval('section.active details.gate',ds=>ds.map(d=>({open:d.open,t:d.querySelector('summary').textContent})));
  console.log(name,JSON.stringify(info));
 }
 await p.goto('file:///home/claude/web/index.html#part-5'); await p.waitForTimeout(400);
 const d=await p.$$('section.active details.gate');
 await d[1].evaluate(e=>{e.open=true; e.scrollIntoView({behavior:'instant',block:'start'})}); await p.waitForTimeout(700); await p.screenshot({path:'/tmp/s12.png'});
 await b.close();
})();
