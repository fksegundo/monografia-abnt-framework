---
description: Gera/expande o conteúdo de um draft de capítulo seguindo o estilo do projeto.
agent: build
---

Use a skill `gerar-draft` para produzir o conteúdo deste capítulo/draft:
$ARGUMENTS

Siga o fluxo da skill: confira a estrutura e o estilo em `contexto/`, monte o
material de apoio se necessário, e produza/expanda o draft em Markdown seguindo
`contexto/estilo_de_escrita.md`. Salve o resultado em `drafts/` com prefixo
numérico coerente. Ao final, indique ao usuário como gerar o documento com o
`gerar_monografia.py`.
