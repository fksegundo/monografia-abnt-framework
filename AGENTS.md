# AGENTS.md

Instruções para agentes de IA que trabalham neste projeto.

## O que é este projeto

Framework em Python para gerar trabalhos acadêmicos (monografias, TCCs,
artigos) formatados em ABNT a partir de rascunhos escritos em Markdown
(`drafts/`), usando um template `.docx` e scripts em `scripts/`.

## Estrutura

- `template/modelo.docx` — template ABNT de origem (capa, folha, sumário).
- `drafts/*.md` — conteúdo do trabalho em Markdown (prefixos numéricos
  definem a ordem; o primeiro é o pré-textual).
- `contexto/` — guias para redação assistida por IA (estilo, prompts, estrutura).
- `scripts/` — automação de geração e formatação (ver `README.md`).
- `output/` — documentos gerados.
- `assets/` — figuras e imagens.

## Fluxo de trabalho

1. **Gerar conteúdo (opcional)** — usar a skill `gerar-draft` ou ler
   `contexto/` para redigir os drafts com IA.
2. **Checar referências (recomendado)** — usar a skill `checar-referencias`
   para validar a bibliografia, medir confiança e corrigir "referências
   alucinadas" (ver `.opencode/skills/checar-referencias/SKILL.md`).
3. **Gerar documento** — `python -m scripts.gerar_monografia`.
4. **Inserir figuras** — `python -m scripts.inserir_figuras`.

## Convenções

- Respeitar o guia de estilo em `contexto/estilo_de_escrita.md`.
- Nunca citar nomes de empresas/entidades reais sem autorização.
- Mantenha os scripts independentes do conteúdo específico (parametrizados por
  CLI); não embutir conteúdo do trabalho dentro de `scripts/`.

## Ambiente

- Dependências: `pip install -r requirements.txt`.
- Python 3.9+.
