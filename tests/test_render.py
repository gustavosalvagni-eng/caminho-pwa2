"""Offline DOM/visual harness. Network navigation is prohibited by the environment.
Uses real Chromium layout/DOM, in-memory Storage fixture; not a real PWA install test.
"""
import base64,json,re
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=Path('/mnt/data/previews');OUT.mkdir(exist_ok=True)

def build_html(store=None,route='inicio'):
 html=(ROOT/'index.html').read_text()
 html=html.replace('<head>','<head><base href="https://caminho.test/caminho-pwa2/">')
 html=re.sub(r'<link[^>]*>', '', html)
 html=html.replace('</head>','<style>'+(ROOT/'styles.css').read_text()+'</style></head>')
 html=re.sub(r'<script[^>]*src=[^>]*></script>', '', html)
 fixture="window._store="+json.dumps(store or {})+"; Object.defineProperty(window,'localStorage',{value:{getItem:k=>Object.hasOwn(_store,k)?_store[k]:null,setItem:(k,v)=>_store[k]=String(v),removeItem:k=>delete _store[k],clear:()=>{window._store={}}},configurable:true});"
 html=html.replace('</body>', '<script>'+fixture+'</script>'+''.join('<script>'+ (ROOT/f).read_text().replace('</script','<\\/script')+'</script>' for f in ['core.js','content.js','app.js'])+'</body>')
 for name in ['jesus','maria']:
  img='data:image/webp;base64,'+base64.b64encode((ROOT/'assets'/f'{name}.webp').read_bytes()).decode()
  html=html.replace('src="assets/'+name+'.webp"','src="'+img+'"')
 return html

def run():
 results=[]
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  c=b.new_context(viewport={'width':390,'height':844},device_scale_factor=1,is_mobile=True,has_touch=True,accept_downloads=True)
  page=c.new_page();page.set_default_timeout(6000);errs=[];page.on('pageerror',lambda err:errs.append(str(err)))
  page.set_content(build_html(),wait_until='load');page.wait_for_selector('h1');page.wait_for_timeout(500)
  assert page.evaluate('C.docs.length')==37
  assert page.locator('meta[name="application-version"]').get_attribute('content')=='2.0.0'
  assert page.locator('.hero-image').evaluate('el=>el.naturalWidth')>0
  page.screenshot(path=str(OUT/'Caminho_V2_Inicio_Celular.png'),full_page=True)
  assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
  results.append('Inicial 390px, imagem carregada, versão e 37 conteúdos')
  page.locator('.bottom-nav [data-route="jornada"]').click();page.locator('[data-open]').first.click();page.wait_for_selector('#reader')
  assert page.locator('#reader [data-speak]').count()==1
  page.locator('#reader [data-ref]').first.click();page.wait_for_selector('dialog[open]')
  assert 'não transcrição' in page.locator('#reference-body').inner_text()
  assert page.locator('#reference-body a').get_attribute('href').startswith('https://www.bibliacatolica.com.br/')
  page.screenshot(path=str(OUT/'Caminho_V2_Referencia.png'),full_page=False)
  page.locator('#reference-close').click();assert not page.locator('dialog').is_visible()
  page.locator('[data-favorite]').click();page.locator('[data-complete]').click()
  assert json.loads(page.evaluate("localStorage.getItem('caminho-favorites-v2')"))==['passo-oracao']
  assert json.loads(page.evaluate("localStorage.getItem('caminho-progress-v2')"))==['passo-oracao']
  page.screenshot(path=str(OUT/'Caminho_V2_Leitura.png'),full_page=True)
  results.append('Referências, fonte externa, favoritos, progresso e controles TTS')
  page.locator('.bottom-nav [data-route="biblioteca"]').click();page.wait_for_selector('#search')
  page.locator('#search').fill('eucaristia');assert page.locator('#library-list [data-open]').count()>0
  page.locator('#search').fill('nada_que_exista');assert page.locator('.empty').is_visible()
  page.locator('#search').fill('');assert page.locator('#library-list [data-open]').count()==37
  results.append('Busca com acentos e estado vazio')
  page.locator('.bottom-nav [data-route="mais"]').click();page.locator('[data-route="diario"]').click();page.wait_for_selector('#journal-form')
  legacy=[{'date':'11/10/2026','reading':'Leitura anterior','motion':'Paz','purpose':'Rezar'}]
  page.evaluate('(v)=>localStorage.setItem("caminho-diary",JSON.stringify(v))',legacy)
  page.locator('.bottom-nav [data-route="mais"]').click();page.locator('[data-route="diario"]').click()
  assert 'Leitura anterior' in page.locator('#journal-entries').inner_text()
  page.locator('#journal-reading').fill('<img src=x onerror=alert(1)>');page.locator('#journal-motion').fill('Gratidão');page.locator('#journal-purpose').fill('Visitar em família');page.locator('#journal-form button[type=submit]').click()
  assert len(json.loads(page.evaluate("localStorage.getItem('caminho-diary')")))==2
  assert page.locator('#journal-entries img').count()==0
  page.locator('[data-edit]').first.click();page.locator('#journal-purpose').fill('Rezar em família');page.locator('#journal-form button[type=submit]').click()
  assert 'Rezar em família' in page.locator('#journal-entries').inner_text()
  with page.expect_download() as dl:page.locator('#export-journal').click()
  dest=OUT/'synthetic_test_export.json';dl.value.save_as(dest);assert len(json.loads(dest.read_text())['entries'])==2;dest.unlink()
  page.on('dialog',lambda dialog:dialog.accept())
  page.locator('#import-journal').set_input_files({'name':'bad.json','mimeType':'application/json','buffer':b'{oops'})
  page.wait_for_timeout(100);assert len(json.loads(page.evaluate("localStorage.getItem('caminho-diary')")))==2
  backup={'schema':'caminho.diary','version':2,'entries':legacy+[{'date':'12/10/2026','reading':'Jo 6','motion':'Confiança','purpose':'Participar da Missa'}]}
  page.locator('#import-journal').set_input_files({'name':'backup.json','mimeType':'application/json','buffer':json.dumps(backup).encode()})
  page.wait_for_timeout(100);assert len(json.loads(page.evaluate("localStorage.getItem('caminho-diary')")))==3
  results.append('Diário v1, criação, edição, exportação, rejeição de JSON inválido, merge e proteção XSS')
  page.locator('.bottom-nav [data-route="mais"]').click();page.locator('[data-route="musica"]').click();page.wait_for_selector('#music-player');assert page.locator('#music-player').is_visible();assert page.locator('[data-track]').count()==2
  page.screenshot(path=str(OUT/'Caminho_V2_Musica.png'),full_page=True)
  results.append('Player MP3, catálogo de duas faixas e créditos')
  page.locator('.bottom-nav [data-route="oracoes"]').click();page.wait_for_selector('.rosary-banner');page.locator('[data-route="rosario"]').first.click()
  page.wait_for_selector('.mystery-card')
  assert page.locator('.mystery-card').count()==5
  for i in range(10):
   page.locator('#count-bead').click()
   page.wait_for_timeout(30)
  assert page.locator('.count-number').inner_text()=='10/10'
  page.locator('#next-decade').click();assert page.locator('.count-number').inner_text()=='0/10'
  assert 'Dezena 2' in page.locator('.rosary-count').inner_text()
  results.append('Rosário: grupos, contagem manual, conclusão e avanço de dezena')
  page.locator('.bottom-nav [data-route="mais"]').click();page.locator('[data-route="maria"]').click();page.wait_for_selector('.marian-hero')
  page.screenshot(path=str(OUT/'Caminho_V2_Maria.png'),full_page=True,timeout=6000)
  page.locator('.bottom-nav [data-route="inicio"]').click();page.wait_for_selector('.hero-image')
  for width in [360,430,1280]:
   page.set_viewport_size({'width':width,'height':900});page.wait_for_timeout(100)
   assert page.evaluate('document.documentElement.scrollWidth<=window.innerWidth'),width
  # Desktop screenshot is generated in a separate browser context.
  results.append('Sem overflow horizontal: 360, 390, 430 e 1280px')
  page2=c.new_page()
  page2.set_default_timeout(4000)
  page2.on('pageerror',lambda err:errs.append(str(err)))
  page2.set_content(build_html({'caminho-diary':'invalid-existing-content'}),wait_until='domcontentloaded')
  page2.locator('.bottom-nav [data-route="mais"]').click()
  page2.wait_for_selector('[data-route="diario"]')
  page2.locator('[data-route="diario"]').click()
  page2.wait_for_selector('#journal-reading')
  assert page2.locator('#journal-reading').is_disabled()
  assert page2.evaluate("localStorage.getItem('caminho-diary')")=='invalid-existing-content'
  results.append('Dados anteriores corrompidos são preservados e bloqueiam escrita')
  assert not errs,errs
  b.close()
 print(json.dumps({'status':'PASS','groups':results,'page_errors':errs,'scope':'Chromium DOM + layout. Storage em fixture; não é instalação PWA/Safari real.'},ensure_ascii=False,indent=2))
 (ROOT/'docs'/'RESULTADOS_DOM.json').write_text(json.dumps({'status':'PASS','groups':results,'errors':errs,'scope':'Chromium DOM/layout; armazenamento simulado. Não equivale a teste real no Safari ou instalação PWA.'},ensure_ascii=False,indent=2))
if __name__=='__main__':run()
