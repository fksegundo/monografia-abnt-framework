# -*- coding: utf-8 -*-
"""Interface de linha de comando unificada do framework.

Um único comando `monografia` com subcomandos que delegam para os scripts
individuais (ver `[project.scripts]` em `pyproject.toml`). Cada subcomando
repassa os argumentos exatamente como o script original espera, ou seja,
`monografia gerar --drafts drafts` equivale a
`python -m scripts.gerar_monografia --drafts drafts`.

Uso:
    monografia --help
    monografia gerar --drafts drafts --template template/modelo.docx
    monografia formatar output/monografia.docx
    monografia figuras output/monografia.docx --config exemplos/mapeamento_figuras.json
    monografia palavras drafts
    monografia template
    monografia extrair-pdf arquivo.pdf saida.md
    monografia material --lista
"""

from __future__ import annotations

import argparse
import subprocess
import sys


SUBCOMANDOS = {
    "gerar": {
        "modulo": "gerar_monografia",
        "descricao": "Gera o documento .docx final a partir dos drafts em Markdown.",
    },
    "formatar": {
        "modulo": "formata_documento",
        "descricao": "Formata um .docx existente segundo ABNT (e adiciona sumário).",
    },
    "formatar-corpo": {
        "modulo": "formatador_abnt",
        "descricao": "Aplica formatação ABNT de corpo a um .docx (in-place).",
    },
    "figuras": {
        "modulo": "inserir_figuras",
        "descricao": "Insere figuras num .docx substituindo placeholders (via JSON).",
    },
    "topicos": {
        "modulo": "gerenciador_topicos",
        "descricao": "Substitui/insere tópicos num .docx a partir de um arquivo de tópicos.",
    },
    "preencher": {
        "modulo": "preencher_json",
        "descricao": "Preenche um .docx a partir de um JSON de conteúdo.",
    },
    "palavras": {
        "modulo": "contar_palavras",
        "descricao": "Conta palavras dos drafts.",
    },
    "extrair-pdf": {
        "modulo": "extrair_pdf",
        "descricao": "Extrai texto de um PDF para um arquivo Markdown.",
    },
    "template": {
        "modulo": "criar_template",
        "descricao": "Regenera o template .docx ABNT genérico e anônimo.",
    },
    "termos": {
        "modulo": "sincronizar_termos_ingles",
        "descricao": "Sincroniza os termos em inglês (itálico) com config/termos_ingles.txt.",
    },
    "material": {
        "modulo": "material",
        "descricao": "Baixa o conteúdo dos links em contexto/material_apoio/links.md para .md locais.",
    },
}


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="monografia",
        description="Framework de geração de monografias (ABNT) a partir de Markdown.",
    )
    sub = parser.add_subparsers(dest="comando", metavar="comando", required=True)

    for nome, info in SUBCOMANDOS.items():
        sub.add_parser(nome, help=info["descricao"])

    args, rest = parser.parse_known_args()
    modulo = SUBCOMANDOS[args.comando]["modulo"]

    cmd = [sys.executable, "-m", f"scripts.{modulo}", *rest]
    raise SystemExit(subprocess.call(cmd))


if __name__ == "__main__":
    main()
