# -*- coding: utf-8 -*-
"""Baixa o conteúdo dos links do material de apoio para arquivos .md locais.

O agente (opencode) consulta `contexto/material_apoio/` ao redigir. Este
script permite que os links listados em `contexto/material_apoio/links.md`
sejam transformados em texto local consultável e verificável: para cada URL
listada, o conteúdo é baixado e extraído para Markdown via `markitdown`,
ficando disponível para o redator sem depender da rede no momento da redação.

Isso evita alucinações: em vez de a IA "inventar" o que um link diz, o
conteúdo real fica num arquivo `.md` local que ela pode ler e citar.

Uso:
    python -m scripts.material [--links contexto/material_apoio/links.md]
                               [--destino contexto/material_apoio/baixados]
                               [--lista]

`--lista` apenas exibe as URLs encontradas em `links.md`, sem baixar.

Os arquivos baixados são nomeados `NN_slug.md` (NN = nº de ordem) e começam
com um cabeçalho apontando a URL de origem, ex.:

    > Fonte: https://exemplo.com/artigo
    > Baixado por scripts.material
    [conteúdo extraído...]
"""

from __future__ import annotations

import argparse
import io
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
DEFAULT_LINKS = RAIZ / "contexto" / "material_apoio" / "links.md"
DEFAULT_DESTINO = RAIZ / "contexto" / "material_apoio" / "baixados"

URL_RE = re.compile(r"https?://[^\s<>\"']+", re.IGNORECASE)


def _reconfigurar_stdout() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


def extrair_urls(texto: str) -> list[str]:
    """Retorna as URLs (http/https) encontradas num texto, sem duplicatas."""
    vistos: set[str] = set()
    resultado: list[str] = []
    for url in URL_RE.findall(texto):
        url = url.rstrip(".,;:)]}\"'")
        if url not in vistos:
            vistos.add(url)
            resultado.append(url)
    return resultado


def ler_links(arquivo: Path) -> list[str]:
    if not arquivo.exists():
        raise SystemExit(f"Arquivo de links não encontrado: {arquivo}")
    return extrair_urls(arquivo.read_text(encoding="utf-8"))


def slugificar(url: str) -> str:
    """Cria um slug seguro a partir de uma URL."""
    nome = url.rstrip("/").split("/")[-1] or "fonte"
    nome = re.sub(r"\.[a-z0-9]{2,4}$", "", nome, flags=re.IGNORECASE)
    nome = re.sub(r"[^a-z0-9]+", "_", nome.lower()).strip("_")
    return (nome[:60] or "fonte") or "fonte"


def baixar_para_markdown(url: str, destino: Path) -> Path:
    """Baixa uma URL e salva o texto extraído como .md no destino."""
    try:
        from markitdown import MarkItDown
        import requests
    except ImportError:
        raise SystemExit(
            "Instale as dependências: python -m pip install 'markitdown[pdf]' requests"
        )

    print(f"[+] Baixando: {url}")
    headers = {"User-Agent": "Mozilla/5.0 (compatible; monografia-material)"}
    resp = requests.get(url, headers=headers, timeout=60)
    resp.raise_for_status()
    ct = resp.headers.get("Content-Type", "")

    md = MarkItDown()
    if "pdf" in ct.lower() or url.lower().endswith(".pdf"):
        stream = io.BytesIO(resp.content)
        stream.name = "material.pdf"
        result = md.convert(stream)
    else:
        result = md.convert(url)

    header = (
        f"> Fonte: {url}\n"
        f"> Baixado por `scripts.material` — texto extraído automaticamente.\n"
        f"> Confirme por que a fonte é relevante antes de citar.\n\n"
    )
    texto = header + (result.text_content or "")
    if len(texto.strip()) <= len(header):
        raise RuntimeError(f"Conteúdo vazio/extraído sem texto para: {url}")

    destino.mkdir(parents=True, exist_ok=True)
    nome = f"{slugificar(url)}.md"
    # evita sobrescrever: se já existe, anexa um sufixo numérico
    caminho = destino / nome
    i = 1
    while caminho.exists():
        caminho = destino / f"{slugificar(url)}_{i}.md"
        i += 1
    caminho.write_text(texto, encoding="utf-8")
    return caminho


def main() -> None:
    _reconfigurar_stdout()
    parser = argparse.ArgumentParser(description="Baixa os links do material de apoio.")
    parser.add_argument("--links", default=str(DEFAULT_LINKS), help="Arquivo de links (padrão: contexto/material_apoio/links.md).")
    parser.add_argument("--destino", default=str(DEFAULT_DESTINO), help="Pasta onde salvar os .md baixados.")
    parser.add_argument("--lista", action="store_true", help="Apenas lista as URLs, sem baixar.")
    args = parser.parse_args()

    links = ler_links(Path(args.links))

    if not links:
        print(f"Nenhuma URL encontrada em {args.links}")
        return

    if args.lista:
        print("URLs encontradas em %s (%d):" % (args.links, len(links)))
        for u in links:
            print("  -", u)
        return

    destino = Path(args.destino)
    ok, falhas = 0, []
    for url in links:
        try:
            caminho = baixar_para_markdown(url, destino)
            print(f"    Salvo em: {caminho}")
            ok += 1
        except Exception as exc:  # noqa: BLE001
            print(f"    [x] Falhou: {exc}")
            falhas.append(url)

    print(f"\nResumo: {ok} baixado(s), {len(falhas)} falha(s).")
    if falhas:
        print("Falhas:")
        for u in falhas:
            print("  -", u)
        print("\nUse 'monografia material --lista' para conferir as URLs.")


if __name__ == "__main__":
    main()
