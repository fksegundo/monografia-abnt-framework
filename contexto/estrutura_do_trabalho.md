# Estrutura do Trabalho (modelo de capítulos)

Documento-modelo de como organizar os drafts de um trabalho acadêmico com este
framework. Adapte os capítulos ao seu trabalho.

## Pré-textuais

| Draft | Conteúdo |
|-------|----------|
| `00_pre_textual.md` | RESUMO, ABSTRACT (Keywords/Palavras-chave), Lista de Abreviaturas e Siglas, Lista de Figuras, Lista de Quadros, Lista de Tabelas |

> O primeiro draft (em ordem alfabética numérica) é tratado como pré-textual
> pelo `gerar_monografia.py` (resumo, abstract, siglas e listas).

## Capítulos típicos

| Draft | Conteúdo sugerido |
|-------|-------------------|
| `01_introducao.md` | **1 INTRODUÇÃO** — contexto, problema, objetivos (geral e específicos), justificativa, organização do trabalho |
| `02_fundamentacao.md` | **2 FUNDAMENTAÇÃO TEÓRICA** — conceitos, revisão de literatura, quadros comparativos |
| `03_metodologia.md` | **3 METODOLOGIA** — caracterização da pesquisa, métodos, instrumentos de coleta, tratamento dos dados |
| `04_analise.md` | **4 ANÁLISE / RESULTADOS E DISCUSSÃO** — apresentação e discussão dos resultados |
| `05_implementacao.md` | **5 IMPLEMENTAÇÃO / ESTUDO DE CASO** — detalhamento da solução aplicada (se houver) |
| `06_consideracoes.md` | **6 CONSIDERAÇÕES FINAIS** — síntese, limitações, trabalhos futuros |
| `07_referencias.md` | **REFERÊNCIAS** — lista bibliográfica em ABNT |

## Níveis de título markdown → Heading ABNT

| Markdown | Nível |
|----------|-------|
| `# 1 INTRODUÇÃO` | Capítulo (Heading 1) |
| `## 1.1 Objetivos` | Seção (Heading 2) |
| `### 1.1.1 Objetivo geral` | Subseção (Heading 3) |
| `#### ...` | Sub-subseção (Heading 4+) |

## Formatação inline suportada nos drafts

- `**negrito**`, `*itálico*`, `` `código` ``
- Tabelas markdown (linhas com `|`)
- Blocos de código entre ` ``` `
- `[INSERIR FIGURA N AQUI]` como marcador de imagem (substituído depois pelo
  `inserir_figuras.py`)
