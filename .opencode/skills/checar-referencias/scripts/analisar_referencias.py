# -*- coding: utf-8 -*-
"""Analisa referências num trabalho Markdown (drafts/ ou um .md único).

Extrai a lista da seção REFERÊNCIAS e as citações inline (padrão
"(AUTOR, ANO)"), gerando um relatório que aponta:

- Referências da lista que NÃO são citadas no corpo (suspeitas de sobrar/sobra);
- Citações inline que NÃO têm correspondência na lista de referências
  (possível referência faltando);
- Referências sem URL/DOI (difíceis de verificar remotamente).

O objetivo é fornecer dados objetivos para a skill de checagem avaliar o
nível de confiança e sugerir substituições.

Uso:
    python .opencode/skills/checar-referencias/scripts/analisar_referencias.py \
        [--drafts drafts] [--saida output/relatorio_referencias.md]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]  # scripts -> checar-refs -> skills -> .opencode -> raiz


def _reconfigurar_stdout() -> None:
    """Força stdout UTF-8 para evitar erros de encodage no console Windows."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


def extrair_referencias(texto: str) -> list[dict]:
    """Extrai itens da seção REFERÊNCIAS (cada bloco separado por linha vazia)."""
    refs = []
    in_refs = False
    buff = []
    for linha in texto.splitlines():
        # Aceita "REFERÊNCIAS" ou "# REFERÊNCIAS" ou "## REFERÊNCIAS"
        limpa = linha.strip().lstrip("#").strip().upper()
        if limpa == "REFERÊNCIAS":
            in_refs = True
            continue
        if in_refs:
            if not linha.strip():
                if buff:
                    refs.append("\n".join(buff).strip())
                    buff = []
                continue
            buff.append(linha.strip())
    if buff:
        refs.append("\n".join(buff).strip())
    return refs


def extrair_citacoes(texto: str) -> list[str]:
    """Extrai citações inline no formato (AUTOR, ANO) ou (AUTOR et al., ANO)."""
    pat = re.compile(r"\(([^()]{2,80}?\d{4}[a-z]?)\)")
    return [m.group(1) for m in pat.finditer(texto)]


def citacao_chave(cit: str) -> str:
    """Normaliza uma citação para um sobrenome aproximado (1º termo antes de vírgula, em maiúscula)."""
    primeira = cit.split(",")[0].strip().upper()
    # remove 'et al' e 'e' caso apareçam isolados no início
    primeira = primeira.replace("ET AL", "").replace(" E ", " ").strip()
    return primeira


def referencias_usadas_no_corpo(texto: str) -> set[str]:
    # tudo ANTES da seção REFERÊNCIAS
    corpo = texto.split("REFERÊNCIAS")[0]
    cits = extrair_citacoes(corpo)
    return {citacao_chave(c) for c in cits}


def relatorio(texto: str, arquivo_origem: str) -> str:
    refs = extrair_referencias(texto)
    corpo_refs = referencias_usadas_no_corpo(texto)

    # para cada ref, pegar o sobrenome (antes da primeira vírgula)
    ref_sobre = []
    for r in refs:
        # ABNT: SOBRENOME, Nome. Assume 1º bloco antes de vírgula é sobrenome
        sobrenome = r.split(",")[0].strip().upper()
        # ignora iniciais tipo 'AMAZON WEB SERVICES (AWS)'
        sobrenome = re.sub(r"\(.*?\)", "", sobrenome).strip()
        ref_sobre.append((sobrenome, r))

    # citações inline não cobertas
    cits = extrair_citacoes(texto.split("REFERÊNCIAS")[0])
    nomes_refs = {s for s, _ in ref_sobre if s}
    nao_citadas_corpo = []

    # refs que não aparecem como sobrenome no corpo: compara substring de citação
    for sobrenome, r in ref_sobre:
        if not sobrenome:
            continue
        if not any(sobrenome in c.upper() for c in cits):
            nao_citadas_corpo.append((sobrenome, r))

    refs_sem_link = [(sobrenome, r) for sobrenome, r in ref_sobre
                     if not re.search(r"https?://|doi\.org|Disponível em", r, re.I)]

    linhas = [
        f"# Relatório de Análise de Referências",
        f"",
        f"Fonte: `{arquivo_origem}`",
        f"",
        f"- **Total de referências na lista (REFERÊNCIAS):** {len(refs)}",
        f"- **Total de citações inline no corpo:** {len(cits)}",
        f"",
        f"## A. Referências da lista possivelmente NÃO citadas no corpo",
    ]
    if nao_citadas_corpo:
        for sobrenome, r in nao_citadas_corpo:
            linhas.append(f"- **{sobrenome}** — {r}")
    else:
        linhas.append("- Nenhuma (todas as referências parecem citadas).")

    linhas += [
        "",
        "## B. Referências sem link/DOI (difíceis de verificar)",
    ]
    if refs_sem_link:
        for sobrenome, r in refs_sem_link:
            linhas.append(f"- **{sobrenome}** — {r}")
    else:
        linhas.append("- Todas possuem URL/DOI.")

    linhas += [
        "",
        "## C. Citações inline (amostra para checagem de confiança)",
    ]
    unicas = sorted(set(cits))
    for c in unicas:
        linhas.append(f"- ({c})")
    linhas.append("")
    linhas.append("> Este relatório apenas organiza os dados. A avaliação de confiança")
    linhas.append("> e a sugestão de substituição devem ser feitas pela skill `checar-referencias`.")
    return "\n".join(linhas)


def main() -> None:
    _reconfigurar_stdout()
    parser = argparse.ArgumentParser(description="Analisa referências de um trabalho Markdown.")
    parser.add_argument("--drafts", default=str(RAIZ / "drafts"), help="Pasta dos drafts .md.")
    parser.add_argument("--arquivo", help="Um único arquivo .md a analisar (prioridade sobre --drafts).")
    parser.add_argument("--saida", default=str(RAIZ / "output" / "relatorio_referencias.md"), help="Arquivo de saída.")
    args = parser.parse_args()

    if args.arquivo:
        caminho = Path(args.arquivo)
        if not caminho.is_absolute():
            caminho = RAIZ / caminho
        if not caminho.exists():
            raise SystemExit(f"Arquivo não encontrado: {caminho}")
        texto = caminho.read_text(encoding="utf-8")
        origem = caminho.name
    else:
        pasta = Path(args.drafts)
        if not pasta.is_absolute():
            pasta = RAIZ / pasta
        arquivos = sorted(pasta.glob("*.md"))
        if not arquivos:
            raise SystemExit(f"Nenhum draft em {pasta}")
        partes = []
        for a in arquivos:
            partes.append(a.read_text(encoding="utf-8"))
        texto = "\n\n".join(partes)
        origem = str(pasta)

    saida = Path(args.saida)
    if not saida.is_absolute():
        saida = RAIZ / saida
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text(relatorio(texto, origem), encoding="utf-8")
    print(f"Relatório gerado em: {saida}")


if __name__ == "__main__":
    main()
