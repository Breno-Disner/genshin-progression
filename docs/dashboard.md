# Dashboard de progressão

Interface de leitura gerada diretamente de `diary/`, `snapshots/`, `benchmarks/` e das convenções. Nenhum registro da conta é editado pelo site. Entradas futuras aparecem após reconstruir o dashboard; não é necessário manter cópias manuais dos números na interface.

## Visualização local

1. Execute `python tools/validate.py`.
2. Execute `python tools/build_site.py`.
3. Execute `python -m http.server 8766 --bind 127.0.0.1 --directory _site`.
4. Abra `http://127.0.0.1:8766` no navegador.

O build usa apenas a biblioteca padrão do Python. A interface usa HTML, CSS e JavaScript, sem instalação de pacotes. Fontes do Google são opcionais; fontes locais de fallback permanecem disponíveis. A pasta gerada `_site/` é ignorada pelo Git.

## Conteúdo

- Visão geral: gráfico de progressão DPS, última entrada do diário e quantidades derivadas dos registros disponíveis.
- Diário: texto integral das entradas datadas, busca sem distinção de acentos, filtro por data e links para a fonte.
- Snapshots: cada arquivo histórico separadamente, com todos os campos acessíveis em um painel expansível.
- Benchmarks: cada resultado separado, incluindo falhas, recordações e clears que não são DPS. Condições e limitações permanecem no registro completo.
- Fontes e critérios: convenções de evidência e comparação do repositório.

`null` é exibido como não informado; zero permanece zero. Metas e dados históricos não são apresentados como posse ou estado atual confirmado. A interface não reúne protocolos incompatíveis em um gráfico de evolução.

## Gráfico de progressão

O gráfico da página inicial é derivado dos JSONs de benchmarks. Cada equipe tem uma cor; linhas só conectam marcos da mesma equipe e protocolo. Maguu Kenki (Team C) e Mitachurl (Teams A/B) ficam em painéis separados. A/B possuem inicialmente um ponto cada; o site não inventa histórico nem estende esses pontos como linhas constantes.

Datas vêm de `event_date`, nunca da data em que um resumo retrospectivo foi registrado. A ordem do baseline sem data da Team C vem dos vínculos `previous_dataset`. O eixo horizontal mostra marcos, não intervalos de tempo; as conexões não interpolam medições.

Datasets com múltiplos runs usam mediana, e os resultados A/B de run único são identificados. A tabela expansível preserva o tamanho da amostra, a ressalva do resumo antigo sem runs e o link de cada fonte. Plans, clears, tentativas de setup falho e recordações antigas/30s não entram na curva. Mudanças de estado da equipe não são isolamentos causais de um upgrade.

Verifique a seleção e ordenação com `python tools/test_progression.py`; verifique o JavaScript com `node --check web/app.js`.

## GitHub Pages

O workflow `.github/workflows/pages.yml` valida os registros, constrói somente a interface em `_site/` e publica esse artefato pelo GitHub Pages. Após a ativação do Pages com origem GitHub Actions, pushes em `main` atualizam o site automaticamente; também há acionamento manual.

Em 17/10/2026, a primeira tentativa de ativação foi recusada pelo GitHub porque o plano não suportava Pages no repositório privado. Em seguida, o usuário autorizou explicitamente tornar público o repositório canônico inteiro, incluindo documentos de origem e histórico Git. A visibilidade foi alterada para pública e GitHub Pages foi ativado com origem GitHub Actions.

O endereço configurado do dashboard é [Genshin Progression](https://breno-disner.github.io/genshin-progression/). Pushes em `main` validam, constroem e publicam automaticamente; não é necessária credencial entre repositórios nem variável de ativação.

O site público expõe o texto do diário e todos os campos dos snapshots e benchmarks exibidos. O workflow não inclui o DOCX ou o diretório de proveniência no artefato do site; esses arquivos e o histórico Git estão acessíveis diretamente no repositório público.

Documentação oficial: [workflows personalizados do GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).
