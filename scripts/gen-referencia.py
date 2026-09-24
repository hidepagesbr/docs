#!/usr/bin/env python3
"""Gera a referência da aba API a partir do OpenAPI bruto da API.

Uso: python3 scripts/gen-referencia.py <openapi-bruto.json>

O que faz:
  1. Filtra o spec: remove operações reservadas à equipe (lista EXCLUIR), campos que só
     staff pode enviar (CAMPOS_STAFF), o esquema de segurança BearerJWT e schemas que
     sobram sem referência. Fixa servers/título. Escreve api/openapi.json.
  2. Reescreve api/referencia/<tag-slug>/<kebab(operationId)>.mdx para cada operação.
  3. Reescreve os grupos de referência da aba API em docs.json (grupos GRUPOS, na ordem),
     preservando os grupos que não são de referência ("Comece por aqui", "Guias").
"""
import json, os, re, shutil, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC_SAIDA = os.path.join(RAIZ, "api", "openapi.json")
DIR_REF = os.path.join(RAIZ, "api", "referencia")
DOCS_JSON = os.path.join(RAIZ, "docs.json")

# Operações fora da doc pública: exigem chave ADMIN/SUPPORT ou deixam a conta em estado
# que só a equipe conserta. Formato "METHOD /path".
EXCLUIR = {
    "GET /health",
    "GET /v1/users", "POST /v1/users", "PATCH /v1/users/{id}", "DELETE /v1/users/{id}",
    "POST /v1/plans", "PATCH /v1/plans/{id}", "DELETE /v1/plans/{id}",
    "PATCH /v1/subscriptions/{id}",
    "POST /v1/campaigns/{id}/block",
    "POST /v1/templates", "PATCH /v1/templates/{id}", "DELETE /v1/templates/{id}",
    "POST /v1/workspaces", "POST /v1/workspaces/{id}/members",
    "PATCH /v1/api-keys/{id}",      # hasRole('ADMIN'); cliente revoga a chave apagando
    "DELETE /v1/workspaces/{id}",   # apaga o único workspace da conta; só staff recria
}
# Campos aceitos só de staff (ignorados para cliente): não aparecem na doc.
CAMPOS_STAFF = {("CreateApiKeyRequest", "role"), ("UpdateDomainRequest", "status")}
# Parágrafos de descrição que só fazem sentido com esses campos.
PARAGRAFOS_STAFF = [re.compile(r"\n*`status` is accepted from \*\*staff only\*\*.*?(?=\n\n|\Z)", re.S)]
# Frases das descrições que falam do que uma chave de staff faz. A API continua tendo os
# papéis; a doc pública não fala deles. Texto exato do spec -> substituto (vazio = apagar).
FRASES_STAFF = [
    (" A staff key sees every workspace on\nthe deployment.", ""),
    (" Staff see every account's pages.", ""),
    ("So staff backing up a customer's page get it in their own\npages and the customer's is untouched — nothing here writes to the source.",
     "So a member backing up a shared page gets it in their own\npages and the source is untouched — nothing here writes to it."),
    (" `role` is clamped to `CLIENT`\nunless the caller is `ADMIN`, so a client cannot escalate by asking for one.", ""),
    ("**An account may hold three `CLIENT` keys.**", "**An account may hold three keys.**"),
    (" `ADMIN` and `SUPPORT` keys are not counted and\nnot limited.", ""),
    ("Readable by its owner, by any member of it, and by staff.", "Readable by its owner and by any member of it."),
    ("Owner or staff.", "The owner, or an admin member."),
    ("An account may read itself; staff may read any.", "An account may read itself."),
    ("whether a `CLIENT` key authenticates", "whether a key authenticates"),
    ("\n\nThis is the one resource a `SUPPORT` key may write, because repairing a customer's page is\nwhat support is for.", ""),
    (" Without `campaignId` an endpoint reports on the owner of the caller's active\nworkspace, which for a staff key is the staff account itself — pass `campaignId` to read a\ncustomer's numbers.",
     " Without `campaignId` an endpoint reports on the owner of the caller's active\nworkspace."),
    ("Platform accounts. Mostly staff-only.", "The caller's own account."),
    (" Null for a staff key listing a workspace it does not belong to.", ""),
    (" `ADMIN` may still write.", ""),
]
# Nada disso pode sobrar na doc publicada; se a API ganhar uma frase nova, o script para aqui.
PROIBIDO = re.compile(r"\b(staff|Staff|SUPPORT|ADMIN)\b")
# Host de ambiente local ou de teste: o spec vem de uma instância rodando, e o que ela põe em
# `info.contact` e nos exemplos é a configuração dela, não a de produção.
HOST_LOCAL = re.compile(r"localhost|127\.0\.0\.1|\.test\b|\.local\b|\.internal\b")


def limpar_texto(texto):
    if not isinstance(texto, str):
        return texto
    for antigo, novo in FRASES_STAFF:
        texto = texto.replace(antigo, novo)
    return texto


def limpar_descricoes(obj):
    """Aplica FRASES_STAFF a todo `description`/`summary` do spec, em qualquer profundidade."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("description", "summary"):
                obj[k] = limpar_texto(v)
            else:
                limpar_descricoes(v)
    elif isinstance(obj, list):
        for v in obj:
            limpar_descricoes(v)

# Tag do spec -> (grupo em PT-BR, ordem). A pasta é o slug da tag.
GRUPOS = [
    ("Pages", "Páginas"), ("Domains", "Domínios"), ("Campaigns", "Campanhas"),
    ("Funnel steps", "Etapas de funil"), ("A/B tests", "Testes A/B"),
    ("Conversion integrations", "Integrações de conversão"), ("Analytics", "Analytics"),
    ("Folders", "Pastas"), ("Tags", "Tags"), ("Templates", "Templates"), ("Elements", "Elementos"),
    ("Workspaces", "Workspaces e membros"), ("API keys", "Chaves de API"),
    ("Subscriptions", "Assinatura"), ("Plans", "Planos"), ("Users", "Conta"),
]
ORDEM_METODO = ["get", "post", "patch", "put", "delete"]


def slug(s):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")


def kebab(s):
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "-", s).lower()


def filtrar(spec):
    spec["info"]["title"] = "HidePages API"
    spec["servers"] = [{"url": "https://api.hidepages.com"}]
    spec["info"]["contact"] = {"name": "HidePages", "url": "https://app.hidepages.com"}
    for p in list(spec["paths"]):
        for m in list(spec["paths"][p]):
            if f"{m.upper()} {p}" in EXCLUIR:
                del spec["paths"][p][m]
        if not spec["paths"][p]:
            del spec["paths"][p]
    for p, ops in spec["paths"].items():
        for op in ops.values():
            if "description" in op:
                for rx in PARAGRAFOS_STAFF:
                    op["description"] = rx.sub("", op["description"]).strip() + "\n"
    schemas = spec["components"]["schemas"]
    for nome, campo in CAMPOS_STAFF:
        schemas.get(nome, {}).get("properties", {}).pop(campo, None)
    spec["components"].get("securitySchemes", {}).pop("BearerJWT", None)
    spec["security"] = [{"ApiKey": []}]
    # poda schemas sem referência (iterativo, porque schema referencia schema)
    while True:
        texto = json.dumps(spec["paths"]) + json.dumps(schemas)
        soltos = [n for n in schemas if f'#/components/schemas/{n}"' not in texto]
        if not soltos:
            break
        for n in soltos:
            del schemas[n]
    tags_usadas = {op["tags"][0] for ops in spec["paths"].values() for op in ops.values()}
    spec["tags"] = [t for t in spec.get("tags", []) if t["name"] in tags_usadas]
    limpar_descricoes(spec)
    sobras = sorted({m.group(0) for m in PROIBIDO.finditer(json.dumps(spec, ensure_ascii=False))})
    if sobras:
        sys.exit(f"menção a papel de equipe sobrou na doc pública ({', '.join(sobras)}); "
                 "acrescente a frase a FRASES_STAFF ou a operação a EXCLUIR")
    locais = sorted({m.group(0) for m in HOST_LOCAL.finditer(json.dumps(spec, ensure_ascii=False))})
    if locais:
        sys.exit(f"host local ou de teste sobrou na doc pública ({', '.join(locais)})")
    return spec


def operacoes(spec):
    for p in sorted(spec["paths"]):
        for m in sorted(spec["paths"][p], key=ORDEM_METODO.index):
            yield m, p, spec["paths"][p][m]


def escrever_paginas(spec):
    shutil.rmtree(DIR_REF, ignore_errors=True)
    grupos = {tag: [] for tag, _ in GRUPOS}
    for m, p, op in operacoes(spec):
        tag = op["tags"][0]
        if tag not in grupos:
            sys.exit(f"tag sem grupo em GRUPOS: {tag!r} ({m.upper()} {p})")
        caminho = f"api/referencia/{slug(tag)}/{kebab(op['operationId'])}"
        arq = os.path.join(RAIZ, caminho + ".mdx")
        os.makedirs(os.path.dirname(arq), exist_ok=True)
        titulo = op.get("summary", op["operationId"]).replace('"', '\\"')
        with open(arq, "w") as f:
            f.write(f'---\ntitle: "{titulo}"\nopenapi: "/api/openapi.json {m.upper()} {p}"\n---\n')
        grupos[tag].append(caminho)
    return grupos


def escrever_docs_json(grupos):
    dj = json.load(open(DOCS_JSON))
    aba = next(t for t in dj["navigation"]["tabs"] if t["tab"] == "API")
    fixos = [g for g in aba["groups"] if not any(p.startswith("api/referencia/") for p in g["pages"])]
    aba["groups"] = fixos + [{"group": nome, "pages": grupos[tag]} for tag, nome in GRUPOS if grupos[tag]]
    with open(DOCS_JSON, "w") as f:
        json.dump(dj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    spec = filtrar(json.load(open(sys.argv[1])))
    with open(SPEC_SAIDA, "w") as f:
        json.dump(spec, f, ensure_ascii=False, indent=2)
        f.write("\n")
    grupos = escrever_paginas(spec)
    escrever_docs_json(grupos)
    total = sum(len(v) for v in grupos.values())
    print(f"endpoints publicados: {total}; schemas: {len(spec['components']['schemas'])}")


if __name__ == "__main__":
    main()
