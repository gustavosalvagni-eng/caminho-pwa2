/* Cache isolado por aplicativo. Nunca remove localStorage ou caches de outros sites. */
'use strict';
const ROOT=new URL('./',self.location.href);
const PREFIX='caminho-v2-core-'+ROOT.pathname+'-';
const CACHE=PREFIX+'2.0.0';
const FILES=['./','index.html','styles.css?v=2.0.0','core.js?v=2.0.0','content.js?v=2.0.0','app.js?v=2.0.0','manifest.webmanifest','icon.svg','assets/icon-192.png','assets/icon-512.png','assets/jesus.webp','assets/maria.webp'];
self.addEventListener('install',event=>{event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(FILES.map(p=>new URL(p,ROOT).href))).then(()=>self.skipWaiting()));});
self.addEventListener('activate',event=>{event.waitUntil((async()=>{const keys=await caches.keys();await Promise.all(keys.filter(k=>(k.startsWith(PREFIX)&&k!==CACHE)||k==='caminho-mobile-v1').map(k=>caches.delete(k)));await self.clients.claim();})());});
self.addEventListener('fetch',event=>{const req=event.request,u=new URL(req.url);if(req.method!=='GET'||u.origin!==ROOT.origin||!u.pathname.startsWith(ROOT.pathname)||req.headers.has('range'))return;
 if(req.mode==='navigate'){event.respondWith(fetch(req).then(async r=>{if(r.ok){const c=await caches.open(CACHE);await c.put(new URL('index.html',ROOT).href,r.clone());}return r;}).catch(async()=>{const c=await caches.open(CACHE);return(await c.match(new URL('index.html',ROOT).href))||Response.error();}));return;}
 // Apenas recursos versionados conhecidos. Não devolve HTML no lugar de JavaScript ou imagens ausentes.
 if(FILES.some(p=>new URL(p,ROOT).href===req.url)){event.respondWith(caches.open(CACHE).then(async cache=>(await cache.match(req))||fetch(req).then(r=>{if(r.ok)cache.put(req,r.clone());return r;})));}
});
