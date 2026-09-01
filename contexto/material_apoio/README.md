# Material de Apoio (Redação)

Coloque aqui arquivos `.md` que a IA deve consultar ao gerar os drafts:

- anotações e levantamentos
- referências bibliográficas já coletadas
- transcrições de ADRs / decisões técnicas
- tabelas de custos / dados de apoio
- qualquer contexto que o redator deva considerar

## Como o material alimenta a redação

1. **Arquivos `.md` locais** desta pasta são automaticamente incluídos no prompt
   gerado pelo helper:
   ```bash
   python .opencode/skills/gerar-draft/scripts/montar_prompt.py \
       --capitulo "Capítulo 2 — Fundamentação Teórica" \
       --saida output/prompt_capitulo2.md
   ```
2. **Links (URLs) em `links.md`** — liste aqui os links de matérias/artigos que
   o agente deve consultar (um por linha, linhas com `#` são ignoradas). O
   agente pode **seguir cada link** (webfetch) e/ou **baixar o conteúdo real**
   para leitura local, evitando alucinações:
   ```bash
   python -m scripts.material            # baixa o conteúdo dos links p/ baixados/
   python -m scripts.material --lista    # só mostra as URLs, sem baixar
   ```
   Os arquivos baixados ficam em `contexto/material_apoio/baixados/` (com a URL
   de origem no topo) e são incluídos automaticamente no prompt.

## Fluxo recomendado

- Cole as URLs em `links.md` e rode `python -m scripts.material`.
- Se algum link falhar, o agente ainda pode acessá-lo via webfetch durante a
  redação.
- Escreva/anote o restante do contexto como `.md` nesta pasta.

> **Atenção à privacidade:** antes de compartilhar o framework, confirme que
> estes arquivos não contêm dados pessoais/confidenciais (nomes, empresas,
> links corporativos, etc.).
