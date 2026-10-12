# Fontes, arte e condições de uso

## Conteúdo editorial

As reflexões, práticas e sinopses foram redigidas para o Caminho. As passagens bíblicas integrais da edição Ave-Maria não foram copiadas para o app: cada referência abre um contexto autoral e link à fonte. Não se afirma que esta edição moderna está em domínio público.

- Bíblia Católica, edição Ave-Maria: https://www.bibliacatolica.com.br/biblia-ave-maria/sao-mateus/6/
- Catecismo, índice oficial em português: https://www.vatican.va/archive/cathechism_po/index_new/indice_po.html
- Catecismo, tradição da oração, §§2650–2696: https://www.vatican.va/archive/cathechism_po/index_new/p4s1cap2_2650-2696_po.html
- Mistérios do Rosário, Vaticano: https://www.vatican.va/special/rosary/documents/misteri_po.html
- João Paulo II, Rosarium Virginis Mariae, especialmente n.38 sobre distribuição semanal: https://www.vatican.va/content/john-paul-ii/pt/apost_letters/2002/documents/hf_jp-ii_apl_20021016_rosarium-virginis-mariae.html
- Catequese sobre Inácio e discernimento, Francisco, 7/9/2022: https://www.vatican.va/content/francesco/pt/audiences/2022/documents/20220907-udienza-generale.html
- Catequese sobre Agostinho, Bento XVI, 9/1/2008: https://www.vatican.va/content/benedict-xvi/pt/audiences/2008/documents/hf_ben-xvi_aud_20080109.html
- Teresinha, Divini amoris scientia: https://www.vatican.va/content/john-paul-ii/pt/apost_letters/1997/documents/hf_jp-ii_apl_19101997_divini-amoris.html
- Opus Dei, santificação do trabalho: https://opusdei.org/pt-br/article/santificacao-do-trabalho/

As referências completas e links por assunto estão no objeto `C.refs` em `content.js`. Números de Catecismo citados no corpo são localizadores; não implicam que o parágrafo integral seja exibido offline. As sínteses não têm aprovação eclesiástica formal.

## Gravações

### Bach — Aria das Variações Goldberg

Intérprete: **Kimiko Ishizaka, piano**, projeto Open Goldberg Variations. A gravação foi disponibilizada sob **CC0 1.0**. A composição de Bach e os direitos da gravação são questões separadas; a escolha desta gravação se fundamenta na declaração específica de CC0.

- Projeto: https://opengoldbergvariations.org/
- Fonte do arquivo: https://commons.wikimedia.org/wiki/File:Kimiko_Ishizaka_-_01_-_Aria.ogg
- CC0: https://creativecommons.org/publicdomain/zero/1.0/
- MP3 do transcode público: https://upload.wikimedia.org/wikipedia/commons/transcoded/e/e6/Kimiko_Ishizaka_-_01_-_Aria.ogg/Kimiko_Ishizaka_-_01_-_Aria.ogg.mp3
- Probe nesta entrega: áudio MPEG, 7.021.056 bytes, duração informada 299,572 segundos, requisições entre origens permitidas.

### Bruckner — Ave Maria

Intérprete: **U.S. Navy Band, Sea Chanters**. A página do arquivo identifica a gravação como obra do governo federal norte-americano e **domínio público nos Estados Unidos**. Essa designação jurisdicional não foi substituída por uma licença CC0 nem generalizada como garantia jurídica mundial.

- Fonte e declaração de direitos: https://commons.wikimedia.org/wiki/File:Ave_Maria_(USNB).ogg
- MP3 do transcode público: https://upload.wikimedia.org/wikipedia/commons/transcoded/a/a3/Ave_Maria_%28USNB%29.ogg/Ave_Maria_%28USNB%29.ogg.mp3
- Probe nesta entrega: áudio MPEG, 3.970.337 bytes, duração informada 193,75 segundos, requisições entre origens permitidas.

O app não atribui estas faixas aos monges de Solesmes nem a Schubert. Áudio clássico não significa necessariamente canto gregoriano. As durações visíveis são arredondadas. Links de mídia podem mudar; há link para a fonte de cada gravação. O pacote não contém MP3s: carrega online ou guarda por ação do usuário.

## Arte

`assets/jesus.webp` e `assets/maria.webp` derivam das imagens geradas por IA nesta conversa a pedido do usuário. São representações devocionais, sem alegação de autenticidade histórica ou de aparição. Os ícones de interface são SVGs do próprio projeto. Nenhuma fonte tipográfica é distribuída; são usadas fontes do sistema.

## Tecnologia

- Web Speech API, propriedades da voz e serviço local: https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisVoice/localService
- Service workers: https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers
- Configuração de publicação do Pages: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

A aplicação não inclui chave de API, conta paga para narração ou autenticação simulada. A eventual requisição ao provedor de voz do sistema depende da voz escolhida e do navegador.
