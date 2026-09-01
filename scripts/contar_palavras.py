# -*- coding: utf-8 -*-
"""Conta as palavras de todos os drafts .md de uma pasta.

Estima também o número de páginas (considerando ~300 palavras/página).
Uso:
    python -m scripts.contar_palavras [pasta]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass
    parser = argparse.ArgumentParser(description="Conta palavras dos drafts.")
    parser.add_argument("pasta", nargs="?", default="drafts", help="Pasta contendo os drafts .md.")
    args = parser.parse_args()

    pasta = Path(args.pasta)
    if not pasta.is_absolute():
        pasta = Path(__file__).resolve().parents[1] / pasta

    if not pasta.exists():
        print(f"Pasta não encontrada: {pasta}")
        sys.exit(1)

    drafts = sorted(pasta.glob("*.md"))
    if not drafts:
        print(f"Nenhum arquivo .md em {pasta}")
        sys.exit(1)

    total = 0
    for draft in drafts:
        words = len(draft.read_text(encoding="utf-8-sig").split())
        print(f"  {draft.name}: {words} palavras")
        total += words

    print(f"\n  TOTAL: {total} palavras")
    print(f"  Páginas estimadas (~300 palavras/pg): {total / 300:.0f}")


if __name__ == "__main__":
    main()
