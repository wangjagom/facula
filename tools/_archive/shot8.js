const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1200,height:1000}});
 await p.goto('file:///home/claude/web/index.html#part-3'); await p.waitForTimeout(500);
 const els=await p.$$('section.active figure.syntax');
 console.log(els.length);
 await els[0].scrollIntoViewIfNeeded(); await p.screenshot({path:'/tmp/s8a.png'});
 await els[2].scrollIntoViewIfNeeded(); await p.screenshot({path:'/tmp/s8b.png'});
 await p.goto('file:///home/claude/web/index.html#part-4'); await p.waitForTimeout(500);
 const e4=await p.$$('section.active figure.syntax'); await e4[0].scrollIntoViewIfNeeded(); await p.screenshot({path:'/tmp/s8c.png'});
 await b.close();
})();
