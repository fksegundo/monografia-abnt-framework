---
name: checar-referencias
description: Valida as referências bibliográficas de um trabalho acadêmico, analisa o nível de confiança de cada uma e sugere substituições por referências disponíveis e verificáveis. Use quando o usuário pedir para checar, validar, revisar ou corrigir referências, citações, bibliografia, "referências alucinadas" ou links de fontes.
---

# Checagem de Referências

Esta skill avalia as referências bibliográficas dos drafts/acadêmicos, separa
as que são **confiáveis e verificáveis** das que são **duvidosas ou
inventadas**, e — quando necessário — **sugere substituições** por referências
reais cujo material está acessível e pode ser conferido.

Ela complementa o `estilo_de_escrita.md` (seção "Citações Oficiais") e o
processo de geração de drafts: uma IA pode alucinar referências; esta skill
existe para pegá-las.

## Quando usar

- O usuário pede para validar/checar/revisar referências ou bibliografia.
- Suspeita de "referências alucinadas" (citações inventadas pela IA).
- Antes de entregar ou defender o trabalho, para garantir que toda fonte é real.

## Passos

### 1. Extrair as referências e citações

1. Gere um relatório objetivo da estrutura do material:
   ```bash
   python .opencode/skills/checar-referencias/scripts/analisar_referencias.py \
       --drafts drafts --saida output/relatorio_referencias.md
   ```
   (ou use `--arquivo caminho.md` para um único arquivo.)
   O relatório lista, para cada referência, se ela é citada no corpo, se tem
   URL/DOI, e a amostra de citações inline.

2. Abra os arquivos `drafts/` (ou o `.md`) e leia a lista completa de
   REFERÊNCIAS e as citações inline no texto.

### 2. Avaliar cada referência — nível de confiança

Para cada item, atribua um nível de confiança **Alta | Média | Baixa**:

| Nível | Critério |
|-------|----------|
| **Alta** | Fonte é verificável: tem DOI/URL válida, autor real, editora/veículo real, e você (ou o usuário) consegue acessar o material. Documentação oficial de tecnologia (AWS, Google, Apache, Databricks) costuma cair aqui se o link existir. |
| **Média** | Fonte plausível e real, mas difícil de verificar remotamente: sem URL/DOI, livro impresso sem link, ou link sem acesso direto. Vale confirmar com o usuário. |
| **Baixa** | Suspeita de alucinação: autor/ano/veículo provavelmente inventados, título irreconhecível, URL morta/inexistente, ou combinação improvável. **É aqui que entra a substituição.** |

**Verifique ativamente**, não confie no palpite:
- Use busca na web (`websearch`) para confirmar se o artigo/livro/documento
  realmente existe, com autor, ano e fonte corretos.
- Teste os URLs (se houver `webfetch` disponível) ou, na dúvida, marque como
  "não confirmado".
- **Se houver documentos locais** (PDF/DOCX anexados pelo usuário na pasta de
  material de apoio), extraia o conteúdo real com `markitdown` e confira se ele
  contém o que a citação afirma:
  ```bash
  python .opencode/skills/checar-referencias/scripts/validar_documento.py <arquivo> [--saida output/extraido.md]
  ```
- **Para fontes com URL**, quando a página/documento estiver acessível, baixe e
  valide o conteúdo (confirma existência, autor e trechos):
  ```bash
  python .opencode/skills/checar-referencias/scripts/baixar_e_validar.py <url> [--buscar "termo"]
  ```
  O script salva o texto extraído e (com `--buscar`) mostra se o termo/frase
  realmente aparece no material. Use a saída para classificar a confiança e
  embasar substituições.
- **Requisito de dependência:** para usar os helpers acima, instale
  `python -m pip install "markitdown[pdf] requests"` (ver `requirements.txt`).
- Confira formatação ABNT (vide seção 4).

### 3. Sugerir substituição (para confiança Baixa / não confirmada)

Para cada referência reprovada:

1. **Identifique o conceito** que a citação pretendia sustentar no texto
   (olhe a frase onde ela aparece).
2. **Busque uma referência real e disponível** cobrindo o mesmo conceito:
   - Documentação oficial dos provedores/tecnologias (AWS, Google, Apache,
     Databricks, Oracle, etc.).
   - Artigos acadêmicos com DOI e acesso livre (ou pelo menos DOI válido).
   - Book/genérico bem estabelecidos e verificáveis.
3. **Garanta que o material é acessível** (link válido ou DOI resolúvel) para
   o item ter confiança Alta.
4. **Formate a substituição em ABNT** e indique o que trocar.

### 4. Padrão ABNT

Uso o formato que o projeto já adota, ex.:

```
AUTOR, Nome. **Título**: subtítulo. Cidade: Editora, ano. Disponível em: <url>. Acesso em: dd mmm. aaaa.
```

- Entidades que assinam (ex.: AMAZON WEB SERVICES, GOOGLE CLOUD, APACHE
  SOFTWARE FOUNDATION) vêm como autor institucional.
- Referências de URL devem ter `Disponível em:` e `Acesso em:`.

## Saída esperada

Produza um relatório em dois blocos: (1) uma **avaliação de confiança** e
(2) uma seção **"Substituições sugeridas"**, um bloco por referência
reprovada, contendo a referência original, um resumo da verificação por item e
as fontes de substituição verificadas em ABNT.

### Bloco 1 — Avaliação de confiança (tabela)

| Referência atual | Confiança | Problema | Substituição sugerida (ABNT) | Disponível? |
|---|---|---|---|---|
| (citando o item) | Alta/Média/Baixa | descrição | nova referência completa | Sim, <url/doi> |

### Bloco 2 — Substituições sugeridas (padrão do modelo)

Para cada referência reprovada, um item com:
- **Referência original** (ABNT) e onde ela é citada.
- **Resumo da verificação** — por que ela falhou (URL morta, autor/veículo
  inventado, título não confirmado, conteúdo ausente do material extraído por
  `markitdown`, etc.).
- **Fonte(s) de substituição verificada(s)** — uma ou mais referências reais,
  formatadas em ABNT, com `Disponível em:`/`Acesso em:` quando aplicável, e
  a confirmação de que o material foi acessado/validado.

E, ao final:

- **Ação para o usuário:** confirmar as de confiança Média; trocar as de
  confiança Baixa pelas sugeridas.
- Se o usuário autorizar, **aplique as substituições** nos drafts (editando o
  arquivo `.md`) e regenere o documento.

## Convenções

- **Nunca** "corrigir" uma referência mantendo dados que você não confirmou.
- Priorize fontes oficiais e verificáveis sobre suposições.
- Não invente URLs. Se não achar uma fonte confiável, diga que a substituição
  não foi encontrada e sugira remover a citação ou reformular a frase.
- Respeite o anonimato de empresa/entidades (ver `estilo_de_escrita.md`).
