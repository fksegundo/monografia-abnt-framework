# -*- coding: utf-8 -*-
"""Extrai o conteúdo textual de um documento (PDF, DOCX, DOC, PPTX, HTML, etc.)
para Markdown, usando a biblioteca markitdown (Microsoft).

Serve para validar o conteúdo real de uma fonte citada no trabalho: em vez de
confiar apenas no metadado (autor/ano/título), extrai-se o texto e confere-se
se o documento realmente existe e se contém o trecho/conceito citado.

Uso:
    python .opencode/skills/checar-referencias/scripts/validar_documento.py \
        <arquivo> [--saida output/documento.md]

Exemplos:
    python .../validar_documento.py docs/fonte.pdf
    python .../validar_documento.py fonte.docx --saida output/fonte_extraido.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]


def _reconfigurar_stdout() -> None:
    """Força stdout UTF-8 para evitar erros de encodage no console Windows."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


def validar(caminho: str, saida: str | None = None) -> str:
    try:
        from markitdown import MarkItDown
    except ImportError:
        raise SystemExit(
            "markitdown não instalado. Execute: python -m pip install 'markitdown[pdf]'"
        )

    arquivo = Path(caminho)
    if not arquivo.exists():
        raise SystemExit(f"Arquivo não encontrado: {arquivo}")

    md = MarkItDown()
    result = md.convert(str(arquivo))
    conteudo = result.text_content

    if not saida:
        saida = f"output/{arquivo.stem}_extraido.md"
    out = Path(saida)
    if not out.is_absolute():
        out = RAIZ / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(conteudo, encoding="utf-8")

    print(f"Fonte: {arquivo.name}")
    print(f"Tamanho do texto extraído: {len(conteudo)} caracteres")
    print(f"Extração salva em: {out}")
    return conteudo


if __name__ == "__main__":
    _reconfigurar_stdout()
    parser = argparse.ArgumentParser(description="Extrai texto de documento via markitdown.")
    parser.add_argument("arquivo", help="Caminho do documento (pdf, docx, pptx, html, etc.).")
    parser.add_argument("--saida", help="Caminho do markdown extraído (opcional).")
    args = parser.parse_args()
    validar(args.arquivo, args.saida)
