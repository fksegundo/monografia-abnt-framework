# -*- coding: utf-8 -*-
"""Monta um prompt pronto para redação de um capítulo, combinando o guia de
estilo, a estrutura do trabalho e o material de apoio disponível.

Uso:
    python .opencode/skills/gerar-draft/scripts/montar_prompt.py \
        --capitulo "Capítulo 2 — Fundamentação Teórica" \
        --saida output/prompt_capitulo2.md

Saída: arquivo .md pronto para ser colado em qualquer IA (ou usado pelo
agente redator), apontando os arquivos de contexto relevantes.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]  # sobe de scripts/ -> gerar-draft -> skills -> .opencode -> raiz

URL_RE = re.compile(r"https?://[^\s<>\"']+", re.IGNORECASE)


def _reconfigurar_stdout() -> None:
    """Força stdout UTF-8 para evitar erros de encodage no console Windows."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


def ler(rel: Path) -> str:
    p = RAIZ / rel
    if p.exists():
        return p.read_text(encoding="utf-8")
    return ""


def main() -> None:
    _reconfigurar_stdout()
    parser = argparse.ArgumentParser(description="Monta prompt de redação de capítulo.")
    parser.add_argument("--capitulo", required=True, help="Nome/descrição do capítulo e seções.")
    parser.add_argument("--saida", default=str(RAIZ / "output" / "prompt.md"), help="Caminho do prompt gerado.")
    args = parser.parse_args()

    estilo = ler(Path("contexto/estilo_de_escrita.md"))
    estrutura = ler(Path("contexto/estrutura_do_trabalho.md"))

    apoio_dir = RAIZ / "contexto" / "material_apoio"

    # 1) Links a consultar (links.md) — o redator deve SEGUIR esses links quando
    #    ainda não houver o conteúdo baixado localmente.
    links_txt = (apoio_dir / "links.md").read_text(encoding="utf-8") if (apoio_dir / "links.md").exists() else ""
    links = sorted(set(URL_RE.findall(links_txt)))
    secao_links = ""
    if links:
        linhas = "\n".join(f"- {u}" for u in links)
        secao_links = (
            "## Links do material a consultar\n"
            "Siga cada link abaixo para obter o conteúdo real (a menos que já exista "
            "uma versão baixada em 'baixados/'). SINTETIZE essas fontes com base no que "
            "elas realmente dizem — nunca invente conteúdo atribuído a elas.\n\n"
            f"{linhas}"
        )

    # 2) Arquivos de apoio locais: todos os .md da raiz + os baixados via scripts.material
    arquivos: list[Path] = []
    if apoio_dir.exists():
        arquivos = [p for p in apoio_dir.glob("*.md") if p.name != "links.md"]
        baixados = apoio_dir / "baixados"
        if baixados.exists():
            arquivos += sorted(baixados.glob("*.md"))
    apoio = ""
    if arquivos:
        partes = [f"## {a.relative_to(RAIZ)}\n\n{a.read_text(encoding='utf-8')}" for a in sorted(set(arquivos))]
        apoio = "\n\n---\n\n".join(partes)

    prompt = f"""# Prompt de Redação — {args.capitulo}

## Estilo de escrita (siga rigorosamente)
{estilo or "(arquivo contexto/estilo_de_escrita.md não encontrado)"}

## Estrutura do trabalho
{estrutura or "(arquivo contexto/estrutura_do_trabalho.md não encontrado)"}

## Capítulo a redigir
{args.capitulo}

## Material de apoio
{apoio or "(nenhum material local em contexto/material_apoio)"}

{secao_links}

## Instruções
1. Escreva o draft do capítulo em Markdown, com títulos níveis corretos
   (# capítulo, ## seção, ### subseção).
2. Cada parágrafo deve trazer valor (informação, citação plausível, análise).
3. Nunca cite empresas/entidades reais sem autorização.
4. **Anti-alucinação:** baseie o conteúdo apenas no que o material de apoio
   (arquivos locais e links acima) realmente contém. Se um conceito não estiver
   coberto, escreva de forma genérica e didática — nunca invente citações,
   autores, dados ou URLs. Marque `[VERIFICAR]` onde houver dúvida.
5. Indique ao final o nome sugerido do arquivo em drafts/.
"""

    saida = Path(args.saida)
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text(prompt, encoding="utf-8")
    print(f"Prompt gerado em: {saida}")


if __name__ == "__main__":
    main()
