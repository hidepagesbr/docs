# Documentação do HidePages

Site de documentação do HidePages, publicado em [docs.hidepages.com](https://docs.hidepages.com)
com [Mintlify](https://mintlify.com). Duas abas:

- **Guia**, em português e com prints do painel, para quem usa o HidePages: como iniciar,
  domínios, Builder, campanhas, testes A/B, conversões, painel e conta.
- **API**, para quem integra: guias em português e a referência de endpoints, gerada da
  especificação OpenAPI da própria API (`api/openapi.json`).

## Estrutura

```
docs.json          navegação, tema, links
index.mdx          página inicial
primeiros-passos.mdx
conceitos/ dominios/ builder-v2/ campanhas/ testes-ab/ conversoes/ painel/ conta/   guia
snippets/print.mdx componente de print claro/escuro
api/               aba de API: introdução, autenticação, erros, paginação, guias/
api/openapi.json   a especificação; a referência é gerada dela
images/<seção>/    prints (-light.webp e -dark.webp)
logo/              assets
```

## Rodar localmente

```bash
npm i -g mint
mint dev            # preview em http://localhost:3000
mint validate       # build estrito: falha em aviso
mint broken-links   # links quebrados
```

## Atualizar a referência da API

A referência não é escrita à mão. Quando a API muda, gere a especificação bruta no
repositório `api` (o roteiro está em `docs/AGENTS.md` lá) e rode o gerador aqui:

```bash
python3 scripts/gen-referencia.py /caminho/openapi-bruto.json
mint validate && mint broken-links
```

O script filtra a especificação (remove o que só a equipe pode chamar, campos aceitos só de
staff e schemas órfãos), escreve `api/openapi.json`, recria `api/referencia/**` e refaz os
grupos de referência da aba API em `docs.json`. Endpoint novo com tag nova exige uma entrada
em `GRUPOS` no script; operação nova reservada à equipe exige uma entrada em `EXCLUIR`.

## Publicação

Cada merge em `main` publica automaticamente pela integração do Mintlify com o GitHub.
