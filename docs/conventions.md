# Convenções de evidência e comparação

## Qualidade e proveniência

Qualidade da fonte e comparabilidade são eixos independentes:

| evidence_quality | Significado |
| --- | --- |
| diary_transcription | Transcrição do DOCX fornecido. Um relato no diário continua sendo um relato; não equivale a captura original examinada. |
| project_export | Exportação existente no contexto local, com escopo declarado. |
| user_report | Dados fornecidos diretamente pelo usuário; não implica exame independente de capturas/logs. |
| conversation_recollection | Resumo de assistente no chat anterior, sem verificação das capturas ou registros primários originais. |
| direct_capture | Reservado a capturas/logs originais efetivamente examinados em futuras atualizações. |
| derived | Cálculo reproduzível, com fórmula e fontes; nunca resultado bruto medido. |

Cada JSON deve informar schema_version, record_type, source_id e evidence_quality. Um registro pode preservar números exatos da fonte e ainda ter condições incompletas. Não graduar recordações como medições primárias.

## Campos e datas

- JSON usa números com ponto decimal; porcentagens são pontos percentuais (60.2 significa 60,2%). Duração em segundos; dano, DPS e pontuação são métricas diferentes.
- `null` significa desconhecido/não fornecido. Campo omitido também não implica zero. Zero só é usado quando explicitamente registrado.
- `recorded_date` indica a seção datada; `event_date` fica null quando o dia exato é incerto. O fuso de registros com horário é America/Sao_Paulo, salvo indicação contrária.
- Datas aproximadas ficam em texto ou intervalo com qualificador; não converter “~17 setembro” em um dia exato.
- Dados carregados de datas anteriores precisam de data por campo e marcação de não reconfirmação. Não montar um snapshot de data única a partir do roster misto.
- Talentos em ordem Normal/Skill/Burst. Constelação 0 e refinamento 1 são valores explícitos, não padrões automáticos.
- Snapshots diários desta importação são observações parciais. `observations_verbatim` preserva todo o conteúdo, inclusive artefatos e substats, enquanto `characters` indexa os cabeçalhos de snapshots explícitos; não é uma normalização completa de builds.
- Não transportar metas, personagens Trial ou sandbox para o inventário/roster da conta do diário. Estoque compartilhado não deve ser contado duas vezes.

## Benchmark e comparabilidade

Um teste futuro deve registrar: ID imutável, conta/ambiente, data, membros e builds, ferramenta/versão, alvo/nível/resistências, preset, modificadores, duração/limites da janela, rotação/energia, repetições, resultado exibido e fonte bruta.

`comparison_group` é uma família de condições documentadas, não garantia de controle experimental. Na importação, A e B compartilham o preset conhecido, mas diferem em equipe e execução. Não interpretar a diferença como progresso longitudinal.

- DPS de equipe, dano de Frostflake/Bloom, tempo de clear, score de evento e dano individual em Stygian têm unidades/condições distintas. Nunca uni-los numa única curva de DPS.
- A tentativa A de 9.459 DPS teve setup falho; 10.275 DPS é a tentativa bem-sucedida. A diferença não prova ganho de build.
- Percentuais exibidos são arredondados e podem não somar 100. Não recalcular os resultados exibidos silenciosamente. Pequenas diferenças entre DPS e dano/duração podem refletir precisão da interface; preservar ambos.
- Logs parciais continuam parciais; não inventar eventos entre os trechos.
- A progressão de nível de Ganyu para 82/84 não recebe DPS interpolado.
- A série Team C 1.643 → 3.503 → 4.475 → 4.974 → 5.187 vem de recordação no chat; datas, alvo, duração, builds e escopo da conta não estão disponíveis na leitura recuperada. Comparabilidade não verificada; excluída das comparações padronizadas.
- A Team C Diluc/Amber→Jean do diário não deve ser fundida com a Team C Skirk do chat. Os demais membros do grupo do diário não foram confirmados no registro de clear.

## Team C — série de 20 segundos

- Identificador da série: `team-c-20s-abyss12-maguu-kenki100-res10`. Preservar protocolo e build de cada dataset, incluindo alvo; os testes históricos A/B contra Mitachurl não são o mesmo alvo.
- Comparações exigem ao menos 3 runs com o mesmo build dentro de cada dataset; preferir 5+ para marcos principais. Preservar todos os resultados, duração, dano total, maior hit e contribuições fornecidas.
- Usar a mediana como referência prática central e registrar também média, melhor, pior, amplitude e número de runs. Não usar apenas o melhor resultado para representar a equipe.
- Manter separada da curva histórica Team C de 30s: não fundir ou comparar diretamente. A duração das recordações antigas continua desconhecida onde não foi individualmente documentada; não reclassificar esses registros retroativamente.
- Mudanças entre datasets representam progressão de estado da equipe. Registrar variáveis alteradas e não atribuir o ganho integral a um upgrade quando mais de uma variável mudou.
- Talentos base/investidos e níveis efetivos em equipe são campos distintos. Em 18/10, Skirk tem 1/8/6 base e Havoc: Warp Lv9 efetivo pelo bônus de +1; nunca substituir E8 base por E9.
- Resumos anteriores sem runs brutos permanecem resumos, com data e condições não reconfirmadas explicitamente desconhecidas.

## Ressalvas históricas da importação

- 26–27/09: texto da espada R4/R5 e título Moon fragmentados; a frase “Diluc elevado para Lv26 ... Midsummer” começa na seção de 26/09 e termina após o título de 27/09. A data do evento fica incerta entre essas seções.
- 07/10: Floors 9/10 são um relato retrospectivo, provavelmente do dia anterior. Não datar a execução com certeza.
- 06/10: substituição Amber→Jean foi chamada Team B em um envio, mas Team C no registro do domínio; manter o conflito.
- Varesa: 05/10 deixa obtenção/pity desconhecidos; a correção de 07/10 informa seletor gratuito e nenhum gasto de wishes. Preserve os dois momentos.
- Nomes, versões e declarações do jogo são preservados como constam no diário, sem validação externa ou correções por suposição.
