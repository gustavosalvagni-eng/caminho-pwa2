# Validação — Caminho 2.0.0

## Resultado executado

**6 grupos Node aprovados**, abrangendo validação de dados, merge do diário antigo, escape HTML, divisão de texto para voz, integridade dos IDs/referências, manifesto, existência de assets e simulação do ciclo do service worker.

**8 grupos de DOM/layout no Chromium aprovados**, abrangendo inicial, imagem carregada, leitor, painel de referência, favoritos, progresso, busca, diário antigo, edição, exportação, importação/mesclagem, rejeição de JSON inválido, escape de HTML, catálogo de música, contador do Terço, larguras de 360/390/430/1280px e preservação de dados corrompidos. Nenhum erro de página JavaScript foi registrado nesses fluxos.

Arquivos de resultado: `RESULTADOS_NODE.txt` e `RESULTADOS_DOM.json`.

## Escopo real e limitações

A navegação de Chromium por HTTP, localhost e file foi bloqueada por política do ambiente. A validação visual foi feita com `page.set_content`, HTML/CSS/JavaScript reais incorporados e imagens inline. O localStorage do harness é um objeto em memória. Isso permite testar o código de interface e de manipulação dos registros, **não comprova persistência real entre reinícios, instalação da PWA, cache de rede do service worker ou funcionamento no Safari**.

O teste de service worker utiliza uma máquina virtual Node com caches e rede simulados. Verifica que o código prepara os arquivos, mantém caches de terceiros e não devolve HTML como JavaScript ausente. A operação real em HTTPS precisa ser verificada após reativar a hospedagem.

Os MP3s foram inspecionados por ferramenta de metadados remotos: tipo áudio, duração, bytes e CORS. Não houve escuta humana nem reprodução audível em iPhone. O botão TTS e a geração de trechos foram verificados; a qualidade e disponibilidade da voz física não foram testadas.

O script `tests/test_mobile.py` é um roteiro de integração real para execução futura em ambiente permitido. Não foi incluído entre testes aprovados. Não se afirma “zero erros em todos os navegadores”.

## Conferência após publicação

1. Abrir a URL no Safari e confirmar o selo 2.0 e as duas imagens.
2. Abrir uma leitura, tocar uma referência e conferir o link externo.
3. Tocar Ouvir texto; testar pausar/parar com uma voz portuguesa instalada.
4. Reproduzir uma música; guardar uma faixa e repetir sem conexão.
5. Criar uma entrada de teste no diário, fechar/reabrir e exportar. Importar o mesmo backup para confirmar ausência de duplicação.
6. Após Ajuda confirmar o preparo offline, fechar, desconectar e reabrir o aplicativo instalado.

Não limpar os dados do Safari antes de exportar o diário. Nenhum teste exigiu dados pessoais reais: entradas do harness são sintéticas.
