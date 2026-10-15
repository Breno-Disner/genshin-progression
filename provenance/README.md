# Fontes e cobertura

Importação realizada em 2026-10-15, preservando o histórico inicial do repositório.

| source_id | Fonte | Cobertura e limite |
| --- | --- | --- |
| diary-docx | [DOCX original](diary-original.docx) — “Genshin Progression — Diário de Eventos.docx”, anexo recuperado de GenLab 2 | Fonte principal. Entradas 21/09–12/10/2026 e roster sem data única. |
| genlab2-retrieved | [Trechos do chat](genlab2-excerpts.md), conversa 6ac65d1e-e84c-83e9-9288-5b3c9303d2e5 | Resumos de assistente recuperados; não são capturas nem acesso completo a todos os testes antigos. |
| prefarm-local-2026-10-12 | [Exportação local preservada](prefarm-project-export-2026-10-12.json) | Escopo exclusivo de pré-farm; metas não indicam posse. |

SHA-256 do DOCX original: `ed45fdbef4831ea379cb1193d1a7569b7c8913535c312d059c321ba728997b79`.

[Extrato textual](diary-docx-extracted.txt): uma linha por parágrafo OOXML, inclusive linhas vazias. [Índice JSON](diary-paragraphs.json) preserva números de parágrafo, texto, preâmbulo e seções datadas. Identificadores pNNN nos meses apontam para essas linhas. O DOCX é a fonte de autoridade para layout; a extração textual não preserva estilos.

O roster de referência tem datas por campo e não constitui um snapshot completo de uma data específica. Ele permanece integralmente no preâmbulo do índice; não foi retroativamente aplicado ao baseline de setembro.

A importação mensal mantém até os fragmentos malformados do documento, com ressalvas nas convenções. Não há perda intencional de detalhes de snapshots. Benchmarks JSON são transcrições estruturadas dos resultados disponíveis, não exports originais da ferramenta. Logs completos e capturas originais não foram recuperados.

O Google Doc homônimo foi localizado durante a busca, mas esta migração foi feita diretamente do anexo DOCX recuperado. O original foi copiado sem modificações. Nenhum arquivo sincronizado do projeto foi editado.
