# Instruções para agentes

Site Mintlify. Páginas são MDX com frontmatter YAML; a navegação vive em `docs.json`.
`mint dev` para preview, `mint validate` antes de abrir PR, `mint broken-links` para links.

## Sobre o projeto

- Documentação pública do HidePages: guia do painel e API. Idioma: **português do Brasil**.
- A referência de endpoints da aba API é **gerada de `api/openapi.json`**. Não escreva páginas
  de endpoint à mão; atualize a especificação a partir do repositório `api` e, se o endpoint
  for novo, adicione-o à lista do grupo certo em `docs.json`.
- As descrições dentro da especificação estão em inglês, porque vêm do código da API. Os guias
  em volta dela são em português.

## Terminologia

- **White Page**, **Black Page**, **Gray Page**: as três superfícies. Sempre com esses nomes.
- **Publicar** uma página, nunca "deployar". **Rascunho**, nunca "draft" fora de código.
- **Campanha** fica **ok** ou **pendente**; não invente outros estados.
- **Workspace**, não "projeto". **Conta** é quem assina; workspace é o conjunto de dados.
- A plataforma é "o HidePages" (masculino).

## Estilo

- Voz ativa, segunda pessoa ("você").
- Uma ideia por frase. Título em sentence case.
- Negrito para elementos da interface: clique em **Settings**.
- Código para arquivos, comandos, caminhos, campos e valores.
- Nenhuma URL de ambiente local, chave real, hostname interno ou nome de provedor de
  infraestrutura. A API tem uma base URL, `https://api.hidepages.com/v1`, e só.

## Limites de conteúdo

- Não documente endpoints reservados à equipe (contas de terceiros, planos, bloqueio por
  cobrança, vínculo direto de membros). Eles não entram em `api/openapi.json`.
- Não descreva a infraestrutura por trás da plataforma. O usuário usa a ferramenta; qual edge
  serve a página dele não é assunto da documentação.
