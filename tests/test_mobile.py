import json, os
from pathlib import Path
from playwright.sync_api import sync_playwright
BASE=os.environ.get('TEST_URL','http://127.0.0.1:8765/')
ROOT=Path(__file__).resolve().parents[1]

def run():
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  c=b.new_context(viewport={'width':390,'height':844},device_scale_factor=1,is_mobile=True,has_touch=True)
  page=c.new_page(); errors=[];page.on('pageerror',lambda e: errors.append(str(e)))
  page.goto(BASE);page.wait_for_load_state('networkidle')
  assert page.locator('meta[name="application-version"]').get_attribute('content',timeout=3000)=='2.0.0','Versão 2.0 ausente'
  assert page.locator('h1').is_visible()
  assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), 'Overflow na inicial'
  assert page.evaluate('C.docs.length')>=30, 'Biblioteca insuficiente'
  page.locator('[data-route="jornada"]').first.click()
  page.locator('[data-open]').first.click()
  assert page.locator('#reader').is_visible()
  page.locator('#reader [data-ref]').first.click()
  assert page.locator('#reference-dialog').is_visible()
  assert page.locator('#reference-body a[target="_blank"]').count()>=1
  page.locator('#reference-close').click()
  assert page.locator('#reader [data-speak]').is_visible()
  page.locator('#reader [data-favorite]').click()
  page.locator('#reader [data-complete]').click()
  assert json.loads(page.evaluate("localStorage.getItem('caminho-progress-v2')"))
  page.reload();page.wait_for_load_state('networkidle')
  assert json.loads(page.evaluate("localStorage.getItem('caminho-favorites-v2')"))
  page.evaluate("location.hash='#diario'")
  page.wait_for_selector('#journal-form')
  legacy=[{'date':'11/10/2026, 20:00:00','reading':'Registro anterior','motion':'Gratidão','purpose':'Rezar'}]
  page.evaluate('(x)=>localStorage.setItem("caminho-diary",JSON.stringify(x))',legacy)
  page.reload();page.wait_for_selector('#journal-form')
  assert page.locator('#journal-entries').inner_text().find('Registro anterior')>=0
  page.locator('#journal-reading').fill('<img src=x onerror=alert(1)>')
  page.locator('#journal-motion').fill('Serenidade')
  page.locator('#journal-purpose').fill('Fazer uma visita')
  page.locator('#journal-form button[type=submit]').click()
  assert len(json.loads(page.evaluate("localStorage.getItem('caminho-diary')")))==2
  assert page.locator('#journal-entries img').count()==0,'XSS no diário'
  page.locator('[data-edit]').first.click();page.locator('#journal-purpose').fill('Visitar em família');page.locator('#journal-form button[type=submit]').click()
  assert 'Visitar em família' in page.locator('#journal-entries').inner_text()
  with page.expect_download() as info: page.locator('#export-journal').click()
  saved=ROOT/'tests'/'test-export.json';info.value.save_as(saved)
  assert len(json.loads(saved.read_text())['entries'])==2
  page.evaluate("location.hash='#musica'");page.wait_for_selector('#music-player')
  assert page.locator('[data-track]').count()>=2
  page.evaluate("location.hash='#biblioteca'");page.wait_for_selector('#search')
  page.locator('#search').fill('eucaristia');assert 'Eucaristia' in page.locator('#library-list').inner_text()
  page.evaluate("location.hash='#maria'");page.wait_for_selector('.marian-hero')
  page.evaluate("location.hash='#inicio'");page.wait_for_selector('h1')
  page.screenshot(path='/mnt/data/previews/caminho_v2_mobile.png',full_page=True)
  for width in (360,430,1280):
   page.set_viewport_size({'width':width,'height':900});page.wait_for_timeout(100)
   assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), f'Overflow {width}'
  page.screenshot(path='/mnt/data/previews/caminho_v2_desktop.png',full_page=True)
  page.evaluate('navigator.serviceWorker.ready');page.wait_for_timeout(700)
  c.set_offline(True);page.reload(wait_until='domcontentloaded');page.wait_for_selector('h1')
  page.evaluate("location.hash='#biblioteca'");page.wait_for_selector('#search')
  assert page.locator('[data-open]').count()>=30
  assert not errors,errors
  b.close()
 print('PASS: layout, biblioteca, referências, favoritos, progresso, migração do diário, XSS, edição, exportação, áudio, busca e offline')
if __name__=='__main__': run()
