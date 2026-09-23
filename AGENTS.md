# Instruções para agentes

Site Mintlify. Páginas são MDX com frontmatter YAML; a navegação vive em `docs.json`.
`mint dev` para preview, `mint validate` antes de abrir PR, `mint broken-links` para links.

## Sobre o projeto

- Documentação pública do HidePages: guia do painel e API. Idioma: **português do Brasil**.
- A referência de endpoints da aba API é **gerada** por `scripts/gen-referencia.py` a partir da
  especificação bruta da API. Não escreva páginas de endpoint à mão nem edite `api/openapi.json`;
  rode o script (README explica) e ele refaz spec, páginas e grupos em `docs.json`.
- As descrições dentro da especificação estão em inglês, porque vêm do código da API. Os guias
  em volta dela são em português.

## Terminologia

- **White Page**, **Black Page**, **Gray Page**: as três superfícies. Sempre com esses nomes.
- **Publicar** uma página, nunca "deployar". **Rascunho**, nunca "draft" fora de código.
- **Campanha** fica **Ativa** ou **Pendente**; os outros status (Assinatura Bloqueada, Cota
  Excedida, Pagamento Pendente) são de cobrança. Não invente outros.
- **Builder** é o editor de páginas. Não existe "Builder V1/V2" na doc; a pasta `builder-v2/`
  mantém o nome só para não quebrar links. As abas do inspetor são **Estilo** e **Ajustes**.
- Modos de entrega de cada superfície: **Nativo**, **Mirror**, **Redirect**.
- **Workspace**, não "projeto". **Conta** é quem assina; workspace é o conjunto de dados.
- A plataforma é "o HidePages" (masculino).

## Estilo

- Voz ativa, segunda pessoa ("você").
- Uma ideia por frase. Título em sentence case.
- Negrito para elementos da interface: clique em **Settings**.
- Código para arquivos, comandos, caminhos, campos e valores.
- Nenhuma URL de ambiente local, chave real, hostname interno ou nome de provedor de
  infraestrutura. A API tem uma base URL, `https://api.hidepages.com/v1`, e só.

## Imagens

- Todo print existe em duas versões, `images/<seção>/<nome>-light.webp` e `-dark.webp`, e entra
  na página pelo snippet:

  ```mdx
  import { Print } from '/snippets/print.mdx';

  <Print src="dominios/dns-dialog" alt="O que o print mostra" />
  ```
- Capture do app em produção com uma conta de teste, nunca de ambiente local: a URL, o domínio e
  os dados precisam parecer os de um cliente. Viewport 1440x900, escala 2, `pt-BR`, e troque o
  tema pela classe `dark`/`light` no `<html>` para gerar as duas versões.
- Borre IP, e-mail de cliente e qualquer dado real antes de capturar. Nada de chave de API,
  token ou preço de plano que não seja público.
- `cwebp -q 82` para converter. Recorte no elemento; a barra lateral só entra quando o contexto
  da navegação importa.

## Limites de conteúdo

- Só entra na doc o que uma chave de **cliente** consegue chamar. Operação que exige
  ADMIN/SUPPORT, campo aceito só de staff, ou ação que deixa a conta em estado que só a equipe
  conserta (apagar o único workspace) ficam em `EXCLUIR`/`CAMPOS_STAFF` no script.
- Não descreva a infraestrutura por trás da plataforma. O usuário usa a ferramenta; qual edge
  serve a página dele não é assunto da documentação.
