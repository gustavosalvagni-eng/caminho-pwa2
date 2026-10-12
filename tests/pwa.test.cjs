const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.join(__dirname,'..');
function worker(){
 const handlers={},removed=[],precache=[],items=new Map();let claimed=false,skipped=false;
 const cache={addAll:async urls=>precache.push(...urls),put:async(k,v)=>items.set(typeof k==='string'?k:k.url,v),match:async k=>items.get(typeof k==='string'?k:k.url)};
 const context={URL,Response,console,self:{location:{href:'https://sample.github.io/caminho-pwa2/sw.js'},addEventListener:(k,v)=>handlers[k]=v,skipWaiting:async()=>{skipped=true},clients:{claim:async()=>{claimed=true}}},caches:{open:async()=>cache,keys:async()=>['unrelated-app','caminho-v2-audio-/caminho-pwa2/','caminho-mobile-v1','caminho-v2-core-/caminho-pwa2/-1.9.0','caminho-v2-core-/caminho-pwa2/-2.0.0'],delete:async k=>{removed.push(k);return true}},fetch:async()=>{throw new Error('Offline fixture')}};
 vm.runInNewContext(fs.readFileSync(path.join(root,'sw.js'),'utf8'),context);
 return{handlers,removed,precache,items,flags:()=>({claimed,skipped})};
}
test('Manifest, assets, scripts e referências do pacote estão completos',()=>{
 const manifest=JSON.parse(fs.readFileSync(path.join(root,'manifest.webmanifest')));assert.equal(manifest.display,'standalone');assert.equal(new URL(manifest.start_url,'https://example.org/caminho-pwa2/').pathname,'/caminho-pwa2/');assert.equal(manifest.scope,'./');
 for(const icon of manifest.icons)assert.ok(fs.existsSync(path.join(root,icon.src)),icon.src);
 for(const file of ['assets/jesus.webp','assets/maria.webp','core.js','content.js','app.js','styles.css'])assert.ok(fs.statSync(path.join(root,file)).size>100,file);
 for(const file of ['core.js','content.js','app.js','sw.js'])assert.doesNotThrow(()=>new vm.Script(fs.readFileSync(path.join(root,file),'utf8')));
 const C=require('../content.js');assert.equal(C.docs.length,37);assert.equal(C.tracks.length,2);for(const track of C.tracks){assert.ok(track.url.startsWith('https://upload.wikimedia.org/'));assert.ok(track.url.endsWith('.mp3'));assert.ok(track.license&&track.artist)}
 assert.equal(Object.values(C.mysteries).flat().length,20);
});
test('Instalação do SW precacheia apenas arquivos existentes no subdiretório',async()=>{
 const w=worker();let job;w.handlers.install({waitUntil:p=>job=p});await job;assert.equal(w.precache.length,12);
 for(const url of w.precache){const u=new URL(url);assert.ok(u.pathname.startsWith('/caminho-pwa2/'));const local=u.pathname.replace('/caminho-pwa2/','')||'index.html';assert.ok(fs.existsSync(path.join(root,local)),local)}assert.ok(w.flags().skipped);
});
test('Ativação preserva cache de áudio e caches de outros aplicativos',async()=>{
 const w=worker();let job;w.handlers.activate({waitUntil:p=>job=p});await job;assert.deepEqual(w.removed,['caminho-mobile-v1','caminho-v2-core-/caminho-pwa2/-1.9.0']);assert.ok(w.flags().claimed);
});
test('Navegação offline retorna o shell; recursos desconhecidos não recebem HTML',async()=>{
 const w=worker();w.items.set('https://sample.github.io/caminho-pwa2/index.html',new Response('<main>Caminho</main>',{headers:{'content-type':'text/html'}}));let response;
 w.handlers.fetch({request:{url:'https://sample.github.io/caminho-pwa2/',method:'GET',mode:'navigate',headers:new Headers()},respondWith:p=>response=p});assert.match(await(await response).text(),/Caminho/);
 for(const [url,headers]of [['https://another.example/file',new Headers()],['https://sample.github.io/other/index.html',new Headers()],['https://sample.github.io/caminho-pwa2/missing.js',new Headers()],['https://sample.github.io/caminho-pwa2/app.js?v=2.0.0',new Headers({range:'bytes=0-100'})]]){let intercepted=false;w.handlers.fetch({request:{url,method:'GET',mode:'cors',headers},respondWith:()=>intercepted=true});assert.equal(intercepted,false,url)}
});
