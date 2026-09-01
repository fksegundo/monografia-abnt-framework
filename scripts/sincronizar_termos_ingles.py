# -*- coding: utf-8 -*-
"""Sincroniza os termos em inglês/estrangeirismos com o arquivo de configuração.

O framework aplica itálico a termos estrangeiros no corpo do texto (ver
`scripts/formatacao/abnt.py`). A lista oficial é a soma de uma base genérica
com o conteúdo de `config/termos_ingles.txt`. Este helper permite:

- Ver quais termos estrangeiros os drafts já marcam em itálico (`*...*`) e que
  ainda não estão na lista;
- Adicionar termos manualmente;
- Sincronizar automaticamente os termos em itálico dos drafts para o arquivo.

Uso:
    python -m scripts.sincronizar_termos_ingles --drafts drafts
    python -m scripts.sincronizar_termos_ingles --sincronizar-drafts drafts
    python -m scripts.sincronizar_termos_ingles --adicionar "multi-cloud" "data lake"
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import scripts.formatacao.abnt as abnt

RAIZ = Path(__file__).resolve().parents[1]
DEFAULT_TERMOS_PATH = RAIZ / "config" / "termos_ingles.txt"

# Itálico simples do Markdown (exclui **negrito**). Opcionalmente captura _..._.
ITALICO_RE = re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)")


def _reconfigurar_stdout() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


def ler_config(arquivo: Path = DEFAULT_TERMOS_PATH) -> list[str]:
    return abnt.ler_termos_ingles(arquivo)


def termos_em_italico(drafts: Path) -> set[str]:
    """Coleta as strings marcadas em itálico (`*...*`) nos drafts Markdown."""
    achados: set[str] = set()
    if not drafts.is_dir():
        return achados
    for md in sorted(drafts.glob("*.md")):
        for linha in md.read_text(encoding="utf-8-sig").splitlines():
            for m in ITALICO_RE.finditer(linha):
                termo = m.group(1).strip()
                if termo and not termo.startswith("INSERIR"):
                    achados.add(termo)
    return achados


def adicionar_termos(novos: list[str], arquivo: Path = DEFAULT_TERMOS_PATH) -> int:
    """Adiciona termos ao arquivo de configuração, sem duplicar. Retorna quantos foram adicionados."""
    atuais = ler_config(arquivo)
    atuais_lower = {t.strip().lower() for t in atuais}

    adicionados = 0
    linhas = []
    if arquivo.exists():
        linhas = arquivo.read_text(encoding="utf-8-sig").splitlines()

    for termo in novos:
        t = termo.strip()
        if not t:
            continue
        if t.lower() in atuais_lower:
            continue
        linhas.append(t)
        atuais_lower.add(t.lower())
        adicionados += 1

    if adicionados:
        # Garante uma linha em branco de separação antes dos termos adicionados,
        # se o arquivo terminar sem quebra suficiente.
        texto = "\n".join(linhas).rstrip() + "\n"
        arquivo.parent.mkdir(parents=True, exist_ok=True)
        arquivo.write_text(texto, encoding="utf-8")

    return adicionados


def main() -> None:
    _reconfigurar_stdout()
    parser = argparse.ArgumentParser(
        description="Sincroniza termos em inglês com config/termos_ingles.txt."
    )
    parser.add_argument("--adicionar", nargs="+", default=[], help="Termos a adicionar manualmente.")
    parser.add_argument("--drafts", help="Pasta de drafts .md para listar termos em itálico não cadastrados.")
    parser.add_argument("--sincronizar-drafts", dest="sincronizar", help="Pasta de drafts cujos termos em itálico serão adicionados automaticamente.")
    args = parser.parse_args()

    adicionados = adicionar_termos(args.adicionar)

    if adicionados:
        print(f"Termos adicionados ao config: {adicionados}")

    if args.sincronizar:
        candidatos = termos_em_italico(Path(args.sincronizar))
        n = adicionar_termos(sorted(candidatos))
        print(f"Sincronizados {n} termos em itálico dos drafts para o config.")
        adicionados += n

    os_termos = set(ler_config())
    print(f"\nTotal de termos cadastrados (base + config): {len(set(abnt.TERMOS_INGLES_BASE) | os_termos)}")

    if args.drafts:
        candidatos = termos_em_italico(Path(args.drafts))
        cadastrados = set(t.lower() for t in os_termos)
        pendentes = sorted(t for t in candidatos if t.lower() not in cadastrados)
        if pendentes:
            print("\nTermos em itálico nos drafts AINDA NÃO cadastrados no config:")
            for t in pendentes:
                print(f"  - {t}")
        else:
            print("\nTodos os termos em itálico dos drafts já estão cadastrados.")


if __name__ == "__main__":
    main()
