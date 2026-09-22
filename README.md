# Documentação do HidePages

Site de documentação do HidePages, publicado em [docs.hidepages.com](https://docs.hidepages.com)
com [Mintlify](https://mintlify.com). Duas abas:

- **Guia**, em português, para quem usa o painel: páginas, domínios, campanhas, conversões,
  testes A/B e os conceitos por trás do cloaking.
- **API**, para quem integra: guias em português e a referência de endpoints, gerada da
  especificação OpenAPI da própria API (`api/openapi.json`).

## Estrutura

```
docs.json          navegação, tema, links
index.mdx          página inicial
primeiros-passos.mdx
builder-v2/ paginas/ dominios/ campanhas/ conversoes/ conceitos/ testes-ab/   guia
api/               aba de API: introdução, autenticação, erros, paginação, guias/
api/openapi.json   a especificação; a referência é gerada dela
images/ logo/      assets
```

## Rodar localmente

```bash
npm i -g mint
mint dev            # preview em http://localhost:3000
mint validate       # build estrito: falha em aviso
mint broken-links   # links quebrados
```

## Atualizar a referência da API

A referência não é escrita à mão. Quando a API muda, gere a especificação nova no repositório
`api` (o roteiro está em `docs/AGENTS.md` lá) e substitua `api/openapi.json` aqui. O
`docs.json` lista os endpoints por grupo; um endpoint novo precisa ser adicionado à lista
para aparecer na navegação.

Endpoints reservados à equipe (contas, planos, bloqueio por cobrança) ficam fora da
especificação publicada.

## Publicação

Cada merge em `main` publica automaticamente pela integração do Mintlify com o GitHub.
