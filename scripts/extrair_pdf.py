# -*- coding: utf-8 -*-
"""Extrai o texto de um PDF para um arquivo Markdown.

Uso:
    python -m scripts.extrair_pdf <entrada.pdf> <saida.md>
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _reconfigurar_stdout() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


def extract(pdf_path: str, md_path: str) -> None:
    try:
        from pypdf import PdfReader
    except ImportError:
        print("A biblioteca 'pypdf' não está instalada. Execute: pip install pypdf")
        sys.exit(1)

    reader = PdfReader(pdf_path)
    out = Path(md_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(str(out), "w", encoding="utf-8") as f:
        for i, page in enumerate(reader.pages):
            f.write(f"\n## Pagina {i + 1}\n\n")
            text = page.extract_text()
            if text:
                f.write(text)
    print(f"Sucesso: extração de {pdf_path} via pypdf.")


def main() -> None:
    _reconfigurar_stdout()
    parser = argparse.ArgumentParser(description="Extrai texto de um PDF para Markdown.")
    parser.add_argument("pdf", help="Caminho do PDF de entrada.")
    parser.add_argument("saida", help="Caminho do .md de saída.")
    args = parser.parse_args()
    extract(args.pdf, args.saida)


if __name__ == "__main__":
    main()
