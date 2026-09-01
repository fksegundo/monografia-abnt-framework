# -*- coding: utf-8 -*-
"""Aplica formatação de corpo ABNT (Arial 12, justificado, recuo) a um
documento .docx existente, preservando títulos.

Uso:
    python -m scripts.formatador_abnt <arquivo.docx>
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt


def _reconfigurar_stdout() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


def formatar_tcc(filename: str) -> None:
    path = Path(filename)
    if not path.exists():
        raise SystemExit(f"Arquivo não encontrado: {path}")

    doc = Document(str(path))

    for p in doc.paragraphs:
        if not p.text.strip():
            continue
        if p.style.name.startswith("Heading") or (p.text.strip().isupper() and len(p.text.strip()) < 50):
            continue
        for run in p.runs:
            run.font.name = "Arial"
            run.font.size = Pt(12)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.first_line_indent = Cm(1.25)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(6)

    doc.save(str(path))
    print(f"Formatação ABNT aplicada com sucesso em {path}!")


def main() -> None:
    _reconfigurar_stdout()
    parser = argparse.ArgumentParser(description="Aplica formatação ABNT de corpo a um .docx (in-place).")
    parser.add_argument("arquivo", help="Caminho do arquivo .docx.")
    args = parser.parse_args()
    formatar_tcc(args.arquivo)


if __name__ == "__main__":
    main()
