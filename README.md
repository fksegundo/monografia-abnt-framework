# Framework de Monografias (ABNT)

Conjunto de ferramentas em Python para **apoiar a escrita** de trabalhos
acadêmicos (monografias, TCCs, artigos) com auxílio de IA, seguindo as normas
ABNT, a partir de rascunhos escritos em Markdown.

O fluxo básico é: você (e a IA) escrevem o conteúdo em arquivos `.md` (chamados
*drafts*) e o framework injeta esse conteúdo num [template `.docx`](#template)
preparado, aplicando a formatação ABNT (fontes, recuos, espaçamento, títulos,
sumário automático) e gerando o documento final.

[![Licença MIT](https://img.shields.io/badge/Licen%C3%A7a-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
[![opencode](https://img.shields.io/badge/opencode-pronto-blueviolet)](https://opencode.ai)

---

## Por que usar

| Etapa | Do que o framework cuida |
|---|---|
| **Apoio à escrita** | Agente `redator` + skill `gerar-draft`: escreve cada capítulo segundo o seu estilo, usando o material de apoio. |
| **Anti-alucinação** | A IA se baseia no material fornecido e pode buscar fontes seguras e verificáveis para complementar; nunca inventa citações. Marca `[VERIFICAR]` onde houver dúvida. |
| **Checagem de referências** | Skill `checar-referencias`: valida autores/anos/URLs na web, mede a confiança de cada referência e sugere **substituições por fontes reais**. |
| **Revisão** | Fluxo capítulo a capítulo, `contar_palavras`, trechos verificáveis. |
| **Formatação ABNT** | Um comando injeta os drafts num template e aplica ABNT (fontes, recuo, espaçamento, títulos, sumário, itálico de termos em inglês, figuras). |

---

## Início rápido (Quickstart)

O repositório já vem com **drafts de exemplo** em `exemplos/drafts/` e um
**template ABNT genérico** em `template/modelo.docx`. Para ver tudo funcionando:

```bash
# 1. Instale as dependências
python -m pip install -r requirements.txt

# 2. Gere o documento de exemplo (5 capítulos + referências)
python -m scripts.gerar_monografia \
    --template template/modelo.docx \
    --drafts exemplos/drafts \
    --saida output/monografia_exemplo.docx \
    --md-saida output/monografia_exemplo.md
```

Abra `output/monografia_exemplo.docx` no Word (atualize o sumário com botão
direito → *Atualizar campo*).

> Para usar o comando unificado (`monografia gerar ...`), instale o pacote:
> `python -m pip install -e .` (consulte [Instalação](#instalação)).

---

## Estrutura do projeto

```
framework_monografia/
├── README.md
├── requirements.txt
├── AGENTS.md                 # Instruções para agentes de IA (opencode)
├── opencode.json             # Configuração do opencode (agentes/skills)
├── .opencode/                # Agente redator + skills (gerar-draft, checar-referencias)
├── config/
│   └── termos_ingles.txt     # Termos estrangeiros que ficam em itálico (customizáveis)
├── template/                 # Template .docx de origem (capa, folha, sumário, placeholders)
├── drafts/                   # Seus rascunhos em Markdown (ordene com prefixos numéricos)
├── assets/                   # Figuras, imagens, gráficos
├── output/                   # Documentos e prompts gerados (.docx, .md)
├── contexto/                 # Guias para redação assistida por IA
│   ├── estilo_de_escrita.md      # Diretrizes de estilo (tom, citações, anonimato)
│   ├── estrutura_do_trabalho.md  # Modelo de capítulos e títulos
│   ├── template_de_prompt.md     # Prompt pronto para criar drafts com IA
│   └── material_apoio/           # Fontes que a IA consulta (locals + links.md + baixados/)
├── exemplos/                 # Exemplos de config/mapeamento e drafts prontos
└── scripts/                  # Automação
    ├── gerar_monografia.py     # Gera o documento final a partir dos drafts (principal)
    ├── material.py             # Baixa o conteúdo dos links do material (links.md → .md locais)
    ├── formata_documento.py    # Formata um .docx existente (ABNT + sumário)
    ├── gerenciador_topicos.py  # Substitui/insere tópicos pelo sumário
    ├── inserir_figuras.py      # Insere figuras por placeholder
    ├── preencher_json.py       # Preenche um docx a partir de JSON
    ├── formatador_abnt.py      # Formata só o corpo (in-place)
    ├── extrair_pdf.py          # Extrai texto de PDF para Markdown
    ├── contar_palavras.py      # Conta palavras dos drafts
    ├── criar_template.py       # Regenera o template ABNT genérico/anônimo
    ├── sincronizar_termos_ingles.py  # Sincroniza termos estrangeiros com config/
    └── formatacao/
        └── abnt.py             # Utilitários de formatação compartilhados
```

---

## Instalação

Requer Python 3.9+.

**Opção A — só dependências (basta script):**

```bash
python -m pip install -r requirements.txt
```

**Opção B — instalar o pacote (habilita o comando `monografia`):**

```bash
python -m pip install -e .
```

Depois de instalar o pacote, os mesmos fluxos ficam disponíveis via um único
comando, ex.:

```bash
monografia gerar --template template/modelo.docx --drafts exemplos/drafts \
  --saida output/monografia.docx --md-saida output/monografia.md
monografia material        # baixa os links do material de apoio
monografia termos          # sincroniza termos em inglês (itálico)
monografia template        # regenera o template ABNT genérico/anônimo
monografia --help          # lista todos os subcomandos
```

Quando o pacote não está instalado, use o equivalente `python -m scripts.<modulo>`
(por exemplo, `python -m scripts.gerar_monografia`).

---

## Apoio à escrita (redação assistida por IA)

Além da formatação, o framework ajuda a **escrever os capítulos** (os drafts)
com IA, mantendo um "contexto" de estilo e material de apoio em `contexto/`.

O fluxo recomendado é um ciclo:

```
 1. PREPARAR o contexto          4. REVISAR o capítulo
 2. MONTAR o material de apoio   5. CHECAR referências (anti-alucinação)
 3. ESCREVER o draft com IA      6. FORMATAR o documento
        ^                                     |
        +-------------------------------------+
```

### 1. Preparar o contexto do seu trabalho

Edite `contexto/`:

- `contexto/estilo_de_escrita.md` — tom, analogias, regras de citação e
  anonimato (não citar empresas reais sem autorização).
- `contexto/estrutura_do_trabalho.md` — quais são os capítulos e seus títulos.

### 2. Montar o material de apoio (fontes de verdade)

Coloque **o que a IA vai consultar** em `contexto/material_apoio/`:

- **Arquivos `.md`** com anotações, levantamentos, transcrições, tabelas.
- **Links (URLs)** de matérias, artigos, documentação e PDFs em
  `contexto/material_apoio/links.md` (um por linha). O agente consegue **seguir
  cada link** e/ou **baixar o conteúdo real** para leitura local:

  ```bash
  # baixa o conteúdo de cada link de links.md para .md locais (via markitdown)
  python -m scripts.material
  python -m scripts.material --lista   # só mostra as URLs, sem baixar
  ```

  Assim, se você fornecer apenas o link de uma matéria, o agente busca e analisa
  o material completo — em vez de "inventar" o que ele diz. Os arquivos baixados
  ficam em `contexto/material_apoio/baixados/` e entram automaticamente no prompt.

### 3. Escrever o draft com IA

Duas formas:

- **Com o opencode (recomendado):** o projeto vem com o agente `redator` e a
  skill `gerar-draft`. Basta pedir, por exemplo:

  > "escreve o draft do capítulo 2 — fundamentação teórica"

  O assistente lê o contexto, monta/baixa o material de apoio, segue os links
  que faltarem e escreve o capítulo em `drafts/`.

- **Com outra IA (ChatGPT, Claude, etc.):** copie o prompt pronto de
  `contexto/template_de_prompt.md`, preencha os campos e cole na IA. Ou monte o
  prompt automaticamente:
  ```bash
  python .opencode/skills/gerar-draft/scripts/montar_prompt.py \
      --capitulo "Capítulo 2 — Fundamentação Teórica" \
      --saida output/prompt_capitulo2.md
  ```

A skill escreve capítulo por capítulo, **marca termos estrangeiros em itálico**
(`*...*`) e os registra automaticamente em `config/termos_ingles.txt`.

### 4. Revisar

Escreva e revise **capítulo por capítulo** em `drafts/` (prefixos numéricos):
`00_pre_textual.md`, `01_introducao.md`, `02_fundamentacao.md`, ...

```bash
python -m scripts.contar_palavras drafts      # acompanhe o tamanho
```

> **Anti-alucinação:** o texto deve se apoiar no material de apoio e pode
> complementar com busca em fontes seguras e verificáveis (artigos, docs
> oficiais, sites confiáveis). Nunca atribuir às fontes conteúdo que elas não
> contêm, nem inventar autores, dados ou URLs. Se faltar fonte segura, o texto
> fica genérico e marcado como `[VERIFICAR]`.

### 5. Checar referências (evitar alucinação)

A IA pode alucinar referências. Antes de formatar, rode a skill de checagem:

> "checa as referências do trabalho"

Ela valida autores/anos/URLs na web, classifica cada referência em
**Alta / Média / Baixa** confiança e, para as de **Baixa** (suspeitas de
alucinação), pesquisa uma **fonte real** e sugere a substituição em ABNT.
Também **valida o conteúdo real** das fontes (locais ou URLs) via `markitdown`
para confirmar se a citação procede.

```bash
# relatório objetivo (refs não citadas, sem URL/DOI, citações inline)
python .opencode/skills/checar-referencias/scripts/analisar_referencias.py --drafts drafts
```

> Dependência opcional para a validação de conteúdo:
> `python -m pip install "markitdown[pdf] requests"` (ver `requirements.txt`).

### 6. Formatar o documento

```bash
python -m scripts.gerar_monografia \
    --template template/modelo.docx \
    --drafts drafts \
    --saida output/monografia.docx \
    --md-saida output/monografia.md
```

> **Privacidade:** antes de compartilhar o framework, confira que
> `contexto/material_apoio/` e demais arquivos não contêm dados pessoais ou de
> empresas reais.

---

## Checagem de referências

IA pode alucinar referências. O framework inclui uma skill de checagem que
valida as referências, mede o nível de confiança de cada uma e sugere
substituições por fontes reais e verificáveis.

No opencode, peça, ex.:

> "checa as referências do trabalho"

A skill:
1. Gera um relatório objetivo com o helper
   `python .opencode/skills/checar-referencias/scripts/analisar_referencias.py --drafts drafts`
   (que aponta refs não citadas no corpo, refs sem URL/DOI e as citações inline).
2. Verifica autores/anos/URLs na web e classifica cada referência em
   **Alta / Média / Baixa** confiança.
3. **Valida o conteúdo real das fontes** quando há documentos locais ou URLs
   acessíveis, usando `markitdown` (Microsoft) para extrair o texto do
   PDF/DOCX/página e conferir se o material existe e contém o que a citação
   afirma. Helpers:
   `validar_documento.py <arquivo>` e `baixar_e_validar.py <url> [--buscar "termo"]`.
4. Para as de **confiança Baixa** (suspeitas de alucinação), pesquisa uma
   fonte real e disponível que sustente o mesmo conceito e apresenta a
   substituição em ABNT, no seguinte formato (um bloco por referência):
   ```text
   Ref. original: <autor, ano>
   Confiança: Baixa (não encontrada)
   Substituição sugerida (ABNT):
   <referência ABNT da fonte real>
   Fonte: <URL/DOI>
   ```
5. Se você autorizar, aplica as trocas nos drafts e regenere o documento.

> Dependência opcional para a validação de conteúdo:
> `python -m pip install "markitdown[pdf] requests"` (ver `requirements.txt`).

---

## Configuração de uso com o opencode

Este projeto foi criado para trabalhar junto com o
[opencode](https://opencode.ai), um assistente de IA para terminal. O repositório
já vem configurado com **agentes, skills e comandos** em `opencode.json` e
`.opencode/`, então você pode escrever e checar o trabalho por instrução.

### O que já vem pronto

- **Agente `redator`** — escreve os drafts dos capítulos seguindo o contexto em
  `contexto/` (estilo, estrutura, anonimato).
- **Skill `gerar-draft`** — gera um capítulo Markdown preparado para o framework,
  monta/baixa o material de apoio (incluindo os links de `links.md`) e segue os
  links que faltarem.
- **Skill `checar-referencias`** — valida referências, mede confiança e sugere
  substituições por fontes reais.
- **Comandos customizados** (`.opencode/command/`) — atalhos como
  `checar-referencias`.

### Exemplos de uso

```text
/redator: escreve o draft do capítulo 2 — fundamentação teórica
/checar-referencias: checa as referências do trabalho
"atualiza o resumo no draft pré-textual"
```

### Como adaptar

- **Ajustar o estilo:** edite `contexto/estilo_de_escrita.md`.
- **Definir os capítulos:** edite `contexto/estrutura_do_trabalho.md`.
- **Orientar a redação:** adicione material de apoio em `contexto/material_apoio/`
  e liste as URLs em `contexto/material_apoio/links.md` (o opencode o consulta na
  hora de escrever).

> Saiba mais sobre como configurar agentes, skills e comandos na documentação do
> opencode: https://opencode.ai/docs.

---

## Termos em inglês (itálico)

A ABNT exige que palavras estrangeiras apareçam em **itálico**. O framework
aplica isso automaticamente para uma lista de termos que é a soma de duas partes:

- **base genérica** (`scripts/formatacao/abnt.py`, `TERMOS_INGLES_BASE`) — termos
  comuns válidos para qualquer trabalho;
- **termos do seu tema** em `config/termos_ingles.txt` — um por linha, linhas
  com `#` são ignoradas. Esse arquivo é customizável e já vem com os termos usados
  no exemplo de dados como demonstração.

```text
# config/termos_ingles.txt
multi-cloud
data lake
vendor lock-in
```

Adicione ou remova termos livremente; a comparação é case-insensitive e termos
compostos (com espaços/hífens) funcionam.

### Sincronizar automaticamente

Se os seus drafts marcam termos estrangeiros em itálico (`*termo*`), você pode
registrá-los de uma vez no `config/termos_ingles.txt`:

```bash
# lista os termos em itálico dos drafts que ainda não estão no config
python -m scripts.sincronizar_termos_ingles --drafts drafts

# adiciona ao config todos os termos em itálico encontrados nos drafts
python -m scripts.sincronizar_termos_ingles --sincronizar-drafts drafts

# adiciona termos manualmente
python -m scripts.sincronizar_termos_ingles --adicionar "multi-cloud" "data lake"
```

> A skill `gerar-draft` do opencode já faz isso automaticamente: ela marca termos
> estrangeiros com `*...*` e roda a sincronização após escrever cada capítulo.

---

## Como usar

### 1. Prepare um template `.docx`

O script principal (`gerar_monografia.py`) injeta os drafts num template que
serve de base para a capa, folha de rosto, sumário e os placeholders dos
textos. coloque esse template em `template/modelo.docx`.

O template deve conter os placeholders que o script reconhece:

| Placeholder no template | Substituído por |
|---|---|
| `Espaço do resumo.` | O conteúdo do RESUMO do draft pré-textual |
| `Versão traduzida do resumo,` | O conteúdo do ABSTRACT |
| `1 INTRODUÇÃO` / `2 DESENVOLVIMENTO` | Marcos entre os quais o conteúdo é injetado |

> Dica: um novo coordenador/instituição costuma fornecer o próprio template
> Word. Basta substituir o arquivo `template/modelo.docx`.

### 2. Escreva seus drafts em Markdown

Coloque os arquivos `.md` em `drafts/`, com prefixos numéricos para garantir
a ordem de inserção:

```
drafts/
├── 00_pre_textual.md      # RESUMO, ABSTRACT, siglas, listas
├── 01_introducao.md       # Capítulo 1
├── 02_fundamentacao.md     # Capítulo 2
├── 03_metodologia.md       # Capítulo 3
└── ...                     # Demais capítulos até Referências
```

O primeiro draft (ordenado) é tratado como pré-textual. Nele, use títulos
`# ` para `RESUMO`, `ABSTRACT`, `LISTA DE ...` e coloque os textos abaixo.

Nos drafts de corpo, use os níveis de título markdown:

- `# 1 INTRODUÇÃO` → capítulo (Heading 1)
- `## 1.1 Objetivos` → seção (Heading 2)
- `### 1.1.1 ...` → subseção (Heading 3)

Formatação inline suportada: `**negrito**`, `*itálico*`, `` `código` ``.
Tabelas markdown e blocos de código (```) também são convertidos.

Coloque `[INSERIR FIGURA 1 AQUI]` (ou similar) no local onde uma imagem deve
entrar; depois use `inserir_figuras.py` para substituí-lo.

### 3. Gere o documento

```bash
python -m scripts.gerar_monografia \
    --template template/modelo.docx \
    --drafts drafts \
    --saida output/monografia.docx \
    --md-saida output/monografia.md
```

O documento `.docx` gerado terá o conteúdo formatado em ABNT, com títulos
capturados para o sumário. No Word, atualize o campo do sumário
(botão direito → *Atualizar campo*).

---

## Ferramentas auxiliares

### Formatar um `.docx` já existente

```bash
python -m scripts.formata_documento saida.docx --saida output/formatado.docx
```

Aplica ABNT (Arial 12, justificado, recuo), classifica títulos em
Heading 1–5 e adiciona sumário automático.

### Inserir figuras por placeholder

Crie um JSON com o mapeamento (veja `exemplos/mapeamento_figuras.json`) e rode:

```bash
python -m scripts.inserir_figuras output/monografia.docx \
    --config exemplos/mapeamento_figuras.json
```

### Contar palavras dos drafts

```bash
python -m scripts.contar_palavras drafts
```

### Extrair texto de um PDF

```bash
python -m scripts.extrair_pdf material.pdf material.md
```

---

## Observações

- Sempre faça um backup do original antes de rodar scripts que modificam
  arquivos in-place (`formatador_abnt.py` salva sobre o original;
  `formata_documento.py` cria um `.backup` automaticamente quando in-place).
- O `.venv` e as dependências ficam fora do controle de versão.
