# Genshin Progression

Registro canônico de progressão da conta documentada no Diário de Eventos. A partir desta importação, mudanças e correções devem ser registradas neste repositório, com Git como trilha de auditoria.

## Navegação

- [Dashboard](https://breno-disner.github.io/genshin-progression/): diário pesquisável, snapshots e benchmarks, atualizado automaticamente a cada push em `main`. Veja [como visualizar e publicar](docs/dashboard.md).
- [Setembro de 2026](diary/2026-09.md) e [outubro de 2026](diary/2026-10.md): entradas datadas integrais.
- [Snapshots](snapshots/README.md): observações estruturadas, baseline e pré-farm.
- [Benchmarks](benchmarks/README.md): resultados das Teams A, B e C, com métricas e escopos separados.
- [Convenções](docs/conventions.md): qualidade da evidência, datas, campos desconhecidos e comparabilidade.
- [Fontes e limitações da importação](provenance/README.md): origem e cobertura.

## Atualizações

1. Adicione uma entrada factual ao mês correspondente, com data, fonte e incertezas.
2. Salve snapshots completos quando fornecidos; não descarte armas, talentos, stats ou substats. Atualizações parciais permanecem parciais.
3. Para cada teste, registre composição/build, alvo, resistências, preset, duração, condições e resultado bruto disponível. Preserve tentativas falhas.
4. Não substitua um valor histórico por um valor atual. Corrija com referência ao registro original e motivo explícito.
5. Faça um commit descritivo por atualização coerente. Não reescreva o histórico para esconder correções.

Valores não informados são desconhecidos, nunca zero. Planos não confirmam posse. A Team C do diário e a série Skirk chamada Team C no chat têm identidades distintas até confirmação.

## Reproduzir a migração

Com Python 3: `python tools/import_diary.py`. O script reconstrói as duas páginas mensais, a transcrição por parágrafo e os snapshots parciais a partir do DOCX arquivado. Ele não altera benchmarks nem fontes. Valide com `python tools/validate.py`.

Não há OCR novo, consulta à conta do jogo ou atualização de estado atual implícita nesta importação. O último dia da importação é 2026-10-12; o diário inclui atualizações posteriores com fonte própria, atualmente até 2026-10-18.
