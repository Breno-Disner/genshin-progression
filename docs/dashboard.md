# Dashboard de progressão

Interface de leitura gerada diretamente de `diary/`, `snapshots/`, `benchmarks/` e das convenções. Nenhum registro da conta é editado pelo site. Entradas futuras aparecem após reconstruir o dashboard; não é necessário manter cópias manuais dos números na interface.

## Visualização local

1. Execute `python tools/validate.py`.
2. Execute `python tools/build_site.py`.
3. Execute `python -m http.server 8766 --bind 127.0.0.1 --directory _site`.
4. Abra `http://127.0.0.1:8766` no navegador.

O build usa apenas a biblioteca padrão do Python. A interface usa HTML, CSS e JavaScript, sem instalação de pacotes. Fontes do Google são opcionais; fontes locais de fallback permanecem disponíveis. A pasta gerada `_site/` é ignorada pelo Git.

## Conteúdo

- Visão geral: última entrada do diário e quantidades derivadas dos registros disponíveis.
- Diário: texto integral das entradas datadas, busca sem distinção de acentos, filtro por data e links para a fonte.
- Snapshots: cada arquivo histórico separadamente, com todos os campos acessíveis em um painel expansível.
- Benchmarks: cada resultado separado, incluindo falhas, recordações e clears que não são DPS. Condições e limitações permanecem no registro completo.
- Fontes e critérios: convenções de evidência e comparação do repositório.

`null` é exibido como não informado; zero permanece zero. Metas e dados históricos não são apresentados como posse ou estado atual confirmado. A interface não reúne protocolos incompatíveis em um gráfico de evolução.

## GitHub Pages

O workflow `.github/workflows/pages.yml` valida os registros, constrói somente a interface em `_site/` e publica esse artefato pelo GitHub Pages. Após a ativação do Pages com origem GitHub Actions, pushes em `main` atualizam o site automaticamente; também há acionamento manual.

O repositório está privado na verificação de 17/10/2026. O usuário aprovou explicitamente a publicação pública do dashboard, mantendo o repositório privado. A tentativa de ativação foi recusada pelo GitHub com HTTP 422: “Your current plan does not support GitHub Pages for this repository.” O site ainda não está publicado; o plano atual bloqueia Pages neste repositório privado. Alternativas: plano com suporte a Pages em repositórios privados ou um repositório público separado contendo somente o site gerado.

Publicar um site público expõe o texto do diário e todos os campos dos snapshots e benchmarks exibidos. O workflow não muda a visibilidade do repositório e não inclui o DOCX ou o diretório de proveniência no artefato publicado. Para evitar falhas de deploy enquanto o bloqueio do plano persiste, a publicação automática depende da variável de repositório `PAGES_ENABLED` com valor `true`; ativá-la após configurar Pages.

Documentação oficial: [workflows personalizados do GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).
