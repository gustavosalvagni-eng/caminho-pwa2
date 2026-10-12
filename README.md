# Caminho 2.0 — PWA para celular

Oração, discernimento e formação católica. Versão estática independente do projeto Django, pensada primeiro para celular. Não exige Node.js, Python, servidor próprio ou API paga para usar o site publicado.

## O que está incluído

- Novo visual com duas imagens originais geradas por IA: Jesus ensinando e Nossa Senhora em contemplação.
- Biblioteca pesquisável de **37 conteúdos**: 10 passos de discernimento, 8 temas, 8 orações, 4 meditações marianas, 4 santos e 3 práticas de vida interior.
- Linha do tempo com 15 acontecimentos e Terço com 20 mistérios, meditações autorais e contador manual de dezenas.
- Referências clicáveis: painel explicativo e botão para abrir o texto completo na Bíblia Ave-Maria ou na fonte eclesial. As passagens integrais não estão transcritas no pacote nem disponíveis offline.
- Favoritos, progresso de leitura, ajuste de tamanho do texto e efeitos reduzidos.
- Leitura em voz alta com Web Speech API: iniciar, pausar, continuar e parar; vozes disponíveis no aparelho, com preferência por português local. A disponibilidade e qualidade dependem do navegador e das vozes instaladas.
- Duas gravações clássicas com intérprete, fonte e licença identificados. Reprodução online e cache opcional por faixa. Nenhum áudio começa automaticamente.
- Diário local com criação, edição, exclusão, exportação JSON e importação com mesclagem. Dados antigos no formato da primeira versão são aceitos.

## Publicar / reativar no GitHub Pages

Repositório: https://github.com/gustavosalvagni-eng/caminho-pwa2

Depois de os arquivos desta versão estarem na branch `main`, acesse **Settings → Pages → Deploy from a branch → main → /(root) → Save**. A habilitação do Pages depende das permissões administrativas da conta; enviar arquivos ao repositório não habilita automaticamente a hospedagem.

Endereço previsto, após a publicação terminar:
https://gustavosalvagni-eng.github.io/caminho-pwa2/

O serviço deve abrir o título Caminho e o selo **2.0**. Se ainda aparecer a versão inicial, feche as abas antigas e reabra o endereço com conexão. **Não limpe os dados do site nem apague o armazenamento antes de exportar seu diário.**

## Instalar no iPhone

Abra o site publicado no Safari → Compartilhar → Adicionar à Tela de Início. A instalação usa o mesmo site em HTTPS. No Android, use o menu de instalação do navegador.

## Offline, fontes e áudio

O service worker guarda interface, imagens e reflexões após uma primeira carga completa. As fontes externas exigem internet. Em **Mais → Música**, toque em **Guardar offline** para baixar uma faixa voluntariamente. O navegador pode remover caches por falta de espaço. O texto narrado pode exigir uma voz previamente instalada; o aplicativo não promete narração offline em todos os aparelhos.

As músicas são carregadas de URLs públicas do Wikimedia; os arquivos MP3 não são embutidos neste ZIP. As fontes podem ficar indisponíveis. Cada faixa também tem link de origem. Detalhes em `docs/FONTES_E_LICENCAS.md`.

## Privacidade e preservação do diário

A chave de armazenamento permanece **`caminho-diary`**. A versão nova não a exclui e não exige migração destrutiva. Os campos originais `date`, `reading`, `motion` e `purpose` continuam reconhecidos. A importação valida os registros antes de mesclar; arquivos inválidos não substituem os dados existentes.

Não há login, banco remoto, analytics nem sincronização. **Local não significa criptografado:** quem tem acesso ao navegador pode ler os registros, assim como outros scripts hospedados na mesma origem `gustavosalvagni-eng.github.io`. Não use o diário para informações cujo sigilo dependa de autenticação forte. Nenhum registro pessoal é enviado ao repositório.

Para backup: Mais → Diário → Exportar. Guarde o JSON fora do navegador. Ao trocar de aparelho, utilize Importar. A importação de um backup idêntico não duplica entradas iguais. Caso os dados anteriores estejam corrompidos, o app bloqueia alterações e oferece exportação do conteúdo bruto, sem apagá-lo.

Não remova todos os dados do Safari como procedimento de atualização.

## Desenvolvimento e testes

Código de produção: HTML, CSS e JavaScript, sem frameworks e sem dependências externas obrigatórias de execução. O conteúdo público está em `content.js`.

Testes determinísticos (requer Node.js 22+ somente para desenvolvimento):
```sh
node --test tests/*.test.cjs
```

Testes de DOM/layout (requer Python, Playwright e Chromium):
```sh
python tests/test_render.py
```

O segundo comando usa HTML inline e armazenamento simulado, pois a navegação normal do browser estava bloqueada no ambiente de validação. Não equivale a instalação em iPhone, teste de voz audível ou operação real de service worker. Veja `docs/VALIDACAO.md`. O script `tests/test_mobile.py` permanece como roteiro adicional para um ambiente com servidor HTTP autorizado; não foi aprovado nem executado integralmente nesta entrega.

Para desenvolvimento local, em um ambiente que permita:
```sh
python -m http.server 8000
```
Abra `http://localhost:8000/`. A PWA precisa de HTTPS em produção; localhost é só para desenvolvimento. Abrir o HTML por `file://` não é uma instalação PWA.

## Estrutura

`index.html` estrutura; `styles.css` visual; `core.js` validação e funções puras; `content.js` biblioteca; `app.js` navegação, diário, voz e música; `sw.js` cache; `manifest.webmanifest` instalação; `assets/` imagens e ícones; `tests/` verificação; `docs/` fontes e evidências.

## Limites editoriais

Reflexões, práticas e contextos são autorais, não citações de santos. As orações tradicionais são identificadas. As imagens são representações devocionais, não fotografias ou reconstituições históricas. O aplicativo não possui aprovação eclesiástica formal e não substitui direção espiritual ou acompanhamento pastoral. O convite da página inicial não é apresentado como liturgia diária.
