# -*- coding: utf-8 -*-
"""Baixa (quando possível) e valida o conteúdo de uma fonte de referência.

Duas funções:
1. `baixar_e_extrair(url, saida)` — baixa o conteúdo de uma URL (PDF, página
   web, etc.) e extrai o texto para Markdown via markitdown. Útil para
   confirmar que uma referência realmente existe e acessar seu conteúdo.
2. `buscar(markdown, termo)` — procura um termo/frase num markdown extraído,
   para comparar se o material contém a ideia que a citação sustenta.

Uso:
    python .opencode/skills/checar-referencias/scripts/baixar_e_validar.py \
        <url> [--saida output/material.md] [--buscar "termo a procurar"]
"""

from __future__ import annotations

import argparse
import io
import re
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


def baixar_e_extrair(url: str, saida: str | None = None) -> str:
    try:
        from markitdown import MarkItDown
        import requests
    except ImportError:
        raise SystemExit("Instale as dependências: python -m pip install 'markitdown[pdf]' requests")

    if not url.startswith(("http://", "https://")):
        raise SystemExit(f"URL inválida: {url}")

    print(f"Baixando: {url}")
    headers = {"User-Agent": "Mozilla/5.0 (compatible; referencia-check)"}
    resp = requests.get(url, headers=headers, timeout=60)
    resp.raise_for_status()
    ct = resp.headers.get("Content-Type", "")

    md = MarkItDown()
    # Se for PDF ou conteúdo binário, usa markitdown direto sobre o stream
    if "pdf" in ct.lower() or url.lower().endswith(".pdf"):
        stream = io.BytesIO(resp.content)
        stream.name = "material.pdf"
        result = md.convert(stream)
    else:
        result = md.convert(url)

    conteudo = result.text_content

    if not saida:
        nome = url.rstrip("/").split("/")[-1] or "material"
        saida = f"output/{nome}_extraido.md"
    out = Path(saida)
    if not out.is_absolute():
        out = RAIZ / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(conteudo, encoding="utf-8")

    print(f"Tamanho do texto extraído: {len(conteudo)} caracteres")
    print(f"Extração salva em: {out}")
    return conteudo


def buscar(markdown: str, termo: str) -> None:
    """Busca um termo num texto e mostra trechos ao redor."""
    termo_n = re.sub(r"\s+", " ", termo).strip().lower()
    texto_n = re.sub(r"\s+", " ", markdown).lower()
    idx = texto_n.find(termo_n)
    if idx == -1:
        print(f"Termo não encontrado: '{termo}'")
        return
    ini = max(0, idx - 200)
    fim = min(len(markdown), idx + len(termo) + 200)
    print(f"Termo encontrado! Trecho (len {len(termo)} char no índ. {idx}):")
    print("---")
    print(markdown[ini:fim])
    print("---")


def main() -> None:
    _reconfigurar_stdout()
    parser = argparse.ArgumentParser(description="Baixa e valida conteúdo de uma URL de referência.")
    parser.add_argument("url", help="URL da fonte (PDF ou página).")
    parser.add_argument("--saida", help="Caminho do markdown extraído (opcional).")
    parser.add_argument("--buscar", help="Termo/frase a procurar no conteúdo (ex.: nome dos autores).")
    args = parser.parse_args()

    conteudo = baixar_e_extrair(args.url, args.saida)
    if args.buscar:
        buscar(conteudo, args.buscar)


if __name__ == "__main__":
    main()
