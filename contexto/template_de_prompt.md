# Template de Prompt para Geração de Drafts com IA

Use este template (com outra IA ou com o agente opencode deste framework) para
pedir que uma IA escreva os drafts do seu trabalho. Copie, substitua os campos
entre `<...>` e cole na IA.

---

## Prompt padrão

```
Você é um assistente de redação acadêmica. Preciso que você escreva o draft
de um capítulo do meu trabalho.

## Contexto do trabalho

- Tipo: <monografia | TCC | artigo>
- Tema: <tema principal>
- Objetivo geral: <objetivo>
- Estrutura de capítulos: veja o arquivo `contexto/estrutura_do_trabalho.md`
- Estilo de escrita: siga RIGOROSAMENTE o guia em `contexto/estilo_de_escrita.md`

## Capítulo a redigir

- Número/Nome: <ex.: Capítulo 2 — Fundamentação Teórica>
- Seções necessárias: <2.1, 2.2, ...>
- Resumo do que deve conter: <descrição do conteúdo esperado>

## Material de apoio (opcional)

- <caminho dos arquivos de contexto/citações/base, ex.: contexto/material_apoio/*.md>

## Regras

1. Nunca cite nomes de empresas reais sem autorização.
2. Use a numeração de títulos markdown correta (# , ## , ###).
3. Cada parágrafo deve ser útil, com citação ou análise fundamentada.
4. **Anti-alucinação:** apoie-se no material fornecido e pode complementar com
   **busca em fontes seguras e verificáveis** (artigos, documentação oficial,
   sites confiáveis). **Nunca invente** autores, datas, dados, citações ou URLs.
   Se não houver fonte segura, escreva de forma genérica e didática; onde houver
   dúvida, marque `[VERIFICAR]`.
5. Se houver links no material, **consulte o conteúdo real de cada link** antes
   de citar; não atribua às fontes o que elas não dizem.
6. Ao final, informe a contagem aproximada de palavras.
7. Escreva o resultado como um arquivo de draft .md pronto para ser salvo em
   `drafts/`.
```

---

## Dicas

- Deixe os arquivos de apoio prontos em `contexto/material_apoio/` para a IA
  consultar (referências, levantamentos, anotações).
- **Links do material:** liste as URLs a consultar no
  `contexto/material_apoio/links.md` (um por linha). Rode
  `python -m scripts.material` para baixar o conteúdo delas como texto local
  (menos risco de a IA inventar), ou deixe que a IA/agente siga cada link.
- Gere capítulo por capítulo para a IA não perder o fio e para você revisar
  aos poucos.
- Depois de gerar, guarde o `.md` em `drafts/` com prefixo numérico (ex.:
  `02_fundamentacao.md`) e gere o documento com o `gerar_monografia.py`.
- **Sempre revisar:** confira autores, anos e URLs das citações (você pode usar
  a skill `checar-referencias`) antes de formatar o documento final.
