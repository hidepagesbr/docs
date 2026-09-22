# Contribuir com a documentação

## Editar

1. Abra a página no GitHub e clique no lápis, ou clone o repositório e edite localmente.
2. Rode `mint dev` para ver o resultado e `mint validate` antes de abrir o PR.
3. Abra o pull request contra `main`. O merge publica.

## Escrever

- Fale com quem lê: "você", voz ativa, uma ideia por frase.
- Comece pelo objetivo. "Para verificar o domínio, chame `verify`", não "O endpoint `verify`
  pode ser chamado para verificar".
- Um termo por conceito. Veja a terminologia em `AGENTS.md`.
- Mostre um exemplo real, curto e completo.
- Nada de URL local, chave de exemplo com cara de chave real, hostname interno ou nome de
  fornecedor de infraestrutura.

## A referência da API

É gerada de `api/openapi.json`. Para mudar a descrição de um endpoint, mude no código da API
(as anotações OpenAPI) e regenere a especificação; não edite o JSON à mão.
