# Snapshots

- `YYYY-MM-DD.json`: observações parciais integrais da seção datada do DOCX, com parágrafos de origem. Incluem todos os dados fornecidos em texto; não completam campos ausentes com dados posteriores.
- [Baseline estruturado 21/09](2026-09-21-baseline.json): conta, recursos, pity e equipes explicitamente registrados.
- [Pré-farm 12/10](2026-10-12-prefarm.json): wrapper da exportação local, com escopo de planejamento. Níveis “current” do planejador não provam posse.
- O roster sem data única está em [proveniência](../provenance/diary-paragraphs.json), com as datas por campo preservadas.

Os detalhes de arma, stats e artefatos permanecem nos campos verbatim. Não interpretar a lista `characters` como roster completo: ela apenas indexa cabeçalhos “Snapshot — ...” do documento. Dados não informados são desconhecidos.
