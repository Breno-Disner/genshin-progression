# Correção de 22/10 — cálice Cryo e causalidade do benchmark Team C

Fonte: adendo explícito do usuário neste chat, após os seis resultados de 22/10. source_id: `user-correction-2026-10-22-cryo-goblet`. Dados transcritos do relato, sem inspeção independente de capturas.

## Cálice atual e histórico

Lavawalker's Epiphany — 5★ +20. Principal Cryo DMG Bonus 46,6%. Substats: DEF 19,7%; DEF +23; CR 6,6%; ER 10,4%.

O mesmo cálice estava em +8 com principal Cryo 22,8%. Aprimoramento +8→+20 adicionou 23,8 pontos percentuais. Com Finale 2pc (+15 pontos), Cryo total atual = 46,6 + 15,0 = 61,6%, exibido arredondado como 62% no Dummy++. A diferença exata total é 61,6 − 22,8 = 38,8 pontos.

A hipótese anterior de ~24 pontos de bônus Cryo sem fonte está resolvida e retirada da interpretação atual. Nenhum buff de combate desconhecido ou mudança de preset é necessário para explicar esse bônus.

## Transição corrigida

1. Nova tiara Finale CD +20.
2. Nova pluma Finale +20.
3. Cálice Cryo existente aprimorado de +8 para +20.
4. Ativação de Finale 2pc (+15% Cryo DMG).

Ficha pós-transição: ATQ 1.894; CR 92,1%; CD 162,0%; ER 131,1%; Cryo 61,6% (62% arredondado). Ficha histórica aproximada: ATQ 1.475; CR 74,2%; CD 125,1%; ER 127,2%; Cryo 22,8%.

## Resultados preservados

Os seis runs não mudam: mediana 25.169,5 DPS; média 25.332,2; melhor 26.280; pior 24.588. Mediana anterior 13.669,5, ganho +84,13%. Mediana pessoal Skirk 220.814,5 → 453.124,5 (+105,21%); maior hit 18.482 → 34.468 (+86,49%).

Conclusão fornecida: aumento plenamente consistente com a transição observada de três artefatos mais bônus de conjunto, sem necessidade de bônus desconhecido ou preset alterado. Isso não separa experimentalmente a contribuição de cada upgrade e não reconfirma uso/ausência de N5D.

Correção aplicada aos snapshots, análise causal, índices e diário; evidência inicial preservada no histórico Git. [Dataset corrigido](../benchmarks/team-c-2026-10-22-20s.json) · [Artefatos corrigidos](../snapshots/2026-10-22-skirk-finale.json) · [Estado do benchmark](../snapshots/2026-10-22-team-c-benchmark-state.json).
