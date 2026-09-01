# Exemplos

Esta pasta contém exemplos prontos para testar o framework de ponta a ponta,
sem precisar escrever conteúdo próprio.

## `drafts/` — drafts de demonstração

Um trabalho completo em Markdown (tema neutro: migração de dados para
ambientes multi-cloud), organizado com prefixos numéricos:

```
drafts/
├── 00_pre_textual.md      # RESUMO, ABSTRACT, lista de siglas
├── 01_introducao.md       # 1 INTRODUÇÃO
├── 02_fundamentacao.md    # 2 FUNDAMENTAÇÃO TEÓRICA
├── 03_metodologia.md      # 3 METODOLOGIA
├── 04_consideracoes.md    # 4 CONSIDERAÇÕES FINAIS
└── 05_referencias.md      # REFERÊNCIAS
```

Para gerar o documento de exemplo:

```bash
python -m scripts.gerar_monografia \
    --template template/modelo.docx \
    --drafts exemplos/drafts \
    --saida output/monografia_exemplo.docx \
    --md-saida output/monografia_exemplo.md
```

## `mapeamento_figuras.json`

Exemplo de configuração para o `inserir_figuras.py` (mapeia o placeholder
`[INSERIR FIGURA N AQUI]` para a imagem, legenda e fonte correspondentes).
