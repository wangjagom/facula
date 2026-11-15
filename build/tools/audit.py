import sys,json
from playwright.sync_api import sync_playwright
url=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=1)
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url); pg.wait_for_timeout(1200)
    ids=pg.evaluate("()=>[...document.querySelectorAll('h3[id]')].map(h=>h.id)")
    res=[]
    for i in ids:
        pg.evaluate(f"()=>{{location.hash='#{i}'}}"); pg.wait_for_timeout(250)
        r=pg.evaluate("""(id)=>{const sec=document.getElementById(id).closest('section,article,.concept')||document.body;const out=[];
         const vw=document.documentElement.clientWidth;
         if(document.documentElement.scrollWidth>vw+1) out.push('PAGE-OVERFLOW '+document.documentElement.scrollWidth);
         sec.querySelectorAll('*').forEach(e=>{const r=e.getBoundingClientRect();if(r.width>0&&r.right>vw+2){let s=e.parentElement,sc=false;while(s){const o=getComputedStyle(s).overflowX;if(o==='auto'||o==='scroll'){sc=true;break}s=s.parentElement}if(!sc)out.push('WIDE '+e.tagName+'.'+e.className+' '+Math.round(r.right))}});
         sec.querySelectorAll('table[data-cols]').forEach(t=>{const hs=[...t.querySelectorAll('th')].map(h=>h.textContent.trim());if(hs.some(h=>!h))out.push('CARD-EMPTYHEAD '+hs.join('|'));
           const first=[...t.querySelectorAll('tbody tr')].map(r=>r.children[0]&&r.children[0].textContent.trim());if(first.some(f=>!f))out.push('CARD-EMPTYFIRST '+hs.join('|'));});
         return out.slice(0,8)}""",i)
        if r: res.append((i,pg.evaluate(f"()=>document.getElementById('{i}').textContent.trim().slice(0,30)"),r))
    for x in res: print(x)
    print('errs',errs, len(ids))
    b.close()
