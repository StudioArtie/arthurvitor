# Site artie. studio criativo

## O que tem aqui
- `index.html`: o site inteiro (textos, estrutura, cores e animações)
- `img/`: fotos, logotipo, raposa e ícones
- `fonts/`: Winco e Helvetica Neue

## Como ver
Dê dois cliques em `index.html`. Depois de editar, salve e aperte F5 no navegador.

## Como editar
Abra `index.html` no VS Code (gratuito: https://code.visualstudio.com) e use Ctrl+F (no Mac, Cmd+F) para achar os trechos.

- **Textos:** troque só o texto entre as tags, sem apagar os `<` `>`.
- **Cores:** no bloco `:root` com `--wine`, `--flame`, `--black`, `--frame` (a moldura preta) e `--white`.
- **Velocidade do carrossel:** procure `const SPEED = 26` (pixels por segundo). Número maior passa mais rápido.
- **Projetos do Behance:** perto do fim do arquivo, em `PROJETOS DO BEHANCE`, adicione `{ nome: '...', tipo: '...', capa: 'img/....jpg', link: 'https://www.behance.net/gallery/...' }`. O card abre direto o projeto no Behance.
- **Projetos:** procure `PROJETOS:` perto do fim do arquivo. Cada projeto é um bloco `{ ... }` com nome, tipo, capa, texto e galeria. Para adicionar um, copie o bloco do artie, cole no lugar de um `{ emBreve: true, ... }` e troque os dados. Coloque as imagens na pasta `img/`.
- **Trajetória:** procure `LINHA DO TEMPO`. Cada marco é um `<li class="stop">`. Coloque `trab` na classe para marcos de trabalho (bolinha preenchida).
- **Contatos:** procure `CONTATOS:`.
- **Fotos:** `img/hero-camiseta.jpg` (abertura) e `img/arthur-retrato.jpg` (foto na trajetória). Para trocar, salve a foto nova com o mesmo nome.

## Como colocar no ar
Arraste a pasta inteira em https://app.netlify.com/drop.

## Atenção
- A licença da Winco que veio no arquivo é "Demo for Personal Use". Para um site comercial, compre a licença comercial.
- As animações usam a GSAP, carregada da internet. Sem conexão, o site funciona, mas sem animações.

## Projetos do Behance (automático)
Todo dia, a rotina `.github/workflows/behance.yml` lê os projetos do seu Behance (ArtieStudio), baixa as capas para `img/behance/` e atualiza o `behance.json`. O carrossel mostra esses projetos depois dos que estão escritos no `index.html`, sem repetir.

- **Rodar na hora:** no GitHub, aba **Actions → Atualizar projetos do Behance → Run workflow**.
- **Trocar a capa de um projeto automático:** adicione o projeto na lista `PROJETOS` do `index.html`, com a capa que quiser. O automático deixa de aparecer, porque o site não repete o mesmo projeto.
