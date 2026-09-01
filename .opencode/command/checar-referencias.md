---
description: Checa/valida as referências bibliográficas, analisa confiança e sugere substituições por fontes verificáveis.
agent: build
---

Use a skill `checar-referencias` para validar as referências bibliográficas do
trabalho.

Escopo (se informado) — $ARGUMENTS

Siga o fluxo da skill:
1. Gere o relatório objetivo com o helper
   `python .opencode/skills/checar-referencias/scripts/analisar_referencias.py --drafts drafts`.
2. Avalie cada referência (confiança Alta/Média/Baixa), verificando de fato
   autores/anos/URLs com busca na web.
3. Se houver documentos locais ou URLs acessíveis, valide o **conteúdo real**
   das fontes com `markitdown` (Microsoft):
   `python .opencode/skills/checar-referencias/scripts/validar_documento.py <arquivo>`
   e `python .opencode/skills/checar-referencias/scripts/baixar_e_validar.py <url> [--buscar "termo"]`.
4. Para as de confiança Baixa or não confirmadas, proponha substituições
   reais, disponíveis e formatadas em ABNT, seguindo o padrão da seção
   "Substituições sugeridas" da skill (um bloco por referência reprovada).
5. Apresente a tabela de resultado e a seção de "Substituições sugeridas" e, se
   autorizado, aplique as trocas nos drafts e regenere o documento.
