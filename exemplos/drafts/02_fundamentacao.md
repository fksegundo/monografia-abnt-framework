# 2 FUNDAMENTAÇÃO TEÓRICA

## 2.1 Computação em nuvem

A computação em nuvem permite o acesso on-demand a um conjunto de recursos
computacionais configuráveis, entregues como serviços por meio da internet. O
National Institute of Standards and Technology (NIST) define a computação em
nuvem por meio de cinco características essenciais, três modelos de serviço e
quatro modelos de implantação (MELL; GRANCE, 2011). Entre os modelos de
serviço, destacam-se o Software as a Service (SaaS), a Platform as a Service
(PaaS) e a Infrastructure as a Service (IaaS).

## 2.2 Arquiteturas multi-cloud

Uma arquitetura multi-cloud utiliza serviços de mais de um provedor de nuvem
simultaneamente. Diferentemente de uma nuvem híbrida, que combina nuvem
pública e privada, a estratégia multi-cloud distribui cargas entre provedores
públicos distintos. Essa abordagem reduz o vendor lock-in, aumenta a
resiliência e permite escolher o fornecedor mais adequado para cada carga.

## 2.3 Migração de dados

A migração de dados é o processo de transferência de dados entre sistemas,
formatos ou ambientes. Em ambientes multi-cloud, a migração pode ocorrer
entre contas de um mesmo provedor, entre provedores distintos ou entre
on-premise e a nuvem. Para isso, são utilizadas ferramentas de transporte e
sincronização que operam em modo batch ou streaming.

### 2.3.1 Estratégias de migração

As estratégias clássicas de migração para a nuvem incluem o lift-and-shift, no
qual a aplicação é movida sem alterações significativas, e o re-platform, que
introduz pequenas otimizações. Em cargas de dados, também se aplica a
estratégia data lake, na qual os dados são centralizados em um repositório
único, e a abordagem hot-warm-cold, que organiza os dados conforme a
frequência de acesso (LANEY, 2001).

### 2.3.2 Integridade e consolidação

A garantia de integridade é fator crítico em qualquer migração. Técnicas de
validação, como checksums e comparação de contagens de registros, são utilizadas
para confirmar que os dados foram transferidos sem perdas ou corrupção. Além
disso, as políticas de retenção e os controles de acesso precisam ser
conservados durante a transição.

## 2.4 Quadro-resumo comparativo

| Estratégia | Esforço | Velocidade | Integridade |
|------------|---------|------------|-------------|
| lift-and-shift | Baixo | Alta | Boa |
| re-platform | Médio | Média | Boa |
| data lake | Alto | Média | Boa |

[INSERIR FIGURA 1 AQUI]
