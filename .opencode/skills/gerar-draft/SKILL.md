---
name: gerar-draft
description: Gera ou expande um draft de capítulo acadêmico em Markdown usando IA, seguindo o guia de estilo do projeto. Use quando o usuário pedir para gerar, escrever, expandir ou redigir conteúdo de um trabalho/monografia/TCC/capítulo/draft, ou preparar material/contexto para redação assistida.
---

# Gerar Draft de Conteúdo Acadêmico

Esta skill orquestra a **geração de conteúdo** dos drafts (não a formatação —
isso é feito pelo `gerar_monografia.py`). Ela monta o contexto a partir dos
guias em `contexto/` e aciona o agente redator para escrever o capítulo.

## Quando usar

- O usuário quer escrever, expandir ou revisar o conteúdo de um capítulo/draft.
- O usuário quer montar o "contexto" (material de apoio) para redação.
- O usuário pergunta "como gero os drafts" ou "como gero o conteúdo".

## Passos

1. **Conferir a estrutura** — leia `contexto/estrutura_do_trabalho.md` para
   saber qual draft/prefixo corresponde ao capítulo pedido.
2. **Conferir o estilo** — leia `contexto/estilo_de_escrita.md`.
3. **Baixar o material dos links (se houver)** — se existir
   `contexto/material_apoio/links.md`, rode o helper para baixar o conteúdo
   real de cada URL para arquivos `.md` locais em
   `contexto/material_apoio/baixados/` (evita alucinação — a IA lê a fonte de
   verdade, não inventa):
   ```bash
   python -m scripts.material
   ```
   Se faltarem dependências (`markitdown`/`requests`), avise ou use `webfetch`
   para consultar cada link diretamente durante a redação.
4. **Montar o material de apoio (se houver)** — se existir material em
   `contexto/material_apoio/`, use o helper para combinar num prompt:
   ```bash
   python .opencode/skills/gerar-draft/scripts/montar_prompt.py \
       --capitulo "<nome do capítulo>" \
       --saida output/prompt_<capitulo>.md
   ```
   Isso gera um `output/prompt_*.md` pronto para ser colado na IA, já listando
   os `links.md` a consultar e os arquivos baixados.
5. **Seguir os links não baixados** — ao redigir, se algum link do material
   ainda não tiver versão local, use `webfetch`/`websearch` para ler o conteúdo
   real da fonte antes de citá-la. Sintetize o que a fonte realmente diz; nunca
   atribua a ela conteúdo inventado.
6. **Acionar o redator** — delegue ao agente `redator` (ou escreva você mesmo
   seguindo o estilo) o conteúdo do capítulo pedido. Forneça: tema, objetivo,
   capítulo, seções, e indique o caminho do material de apoio gerado.
7. **Salvar o draft** — grave o resultado em `drafts/` com prefixo numérico
   coerente (ex.: `drafts/02_fundamentacao.md`).
8. **Sincronizar os termos em inglês** (recomendado) — depois de salvar, rode o
   helper para adicionar automaticamente ao `config/termos_ingles.txt` os termos
   estrangeiros que o draft marcou em itálico (`*...*`) e que ainda não estavam
   cadastrados:
   ```bash
   python -m scripts.sincronizar_termos_ingles --sincronizar-drafts drafts
   ```
   Peça confirmação do usuário antes de alterar o arquivo, se preferir. Este
   passo mantém a lista de termos atualizada com o tema em questão.
9. **(Recomendado)** Ao terminar todos os capítulos, avise o usuário para gerar
   o documento:
   ```bash
   python -m scripts.gerar_monografia --drafts drafts \
       --template template/modelo.docx \
       --saida output/monografia.docx
   ```

## Convenções

- Seguir `contexto/estilo_de_escrita.md` (tom, analogias, citações, anonimato).
- Nunca citar empresas reais sem autorização.
- Cada parágrafo com valor; nada de "encher linguiça".
- Saída em Markdown com níveis de heading corretos.
- **Marcar termos estrangeiros com itálico** (`*termo*`) no Markdown. Isso
  garante que eles sejam destacados e registrados automaticamente no
  `config/termos_ingles.txt` (passo 6). Ex.: `arquitetura *multi-cloud*`.
- **Nunca alucinar:** apoie-se no material de apoio (local ou links seguidos) e
  complemente apenas com **busca em fontes seguras e verificáveis**. Jamais
  invente autores, dados, datas ou URLs; se não houver fonte segura, escreva de
  forma genérica/didática e marque `[VERIFICAR]`.
