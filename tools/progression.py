"""Build source-linked DPS series without merging protocols or inventing dates."""
import html

COLORS = {'A': '#e8c17a', 'B': '#c4a5ef', 'C': '#89d9cd'}


def series(records):
    groups = {}
    for path, record in records:
        group = record.get('comparison_group')
        team = record.get('team')
        kind = record.get('record_type')
        if not group or team not in COLORS or kind not in (
                'benchmark_dataset', 'benchmark_dataset_summary', 'benchmark_transcription'):
            continue
        if record.get('outcome') == 'failed_setup':
            continue
        stats = record.get('aggregate') or record.get('summary') or {}
        value = stats.get('median_dps', record.get('dps'))
        if value is None:
            continue
        point = {'id': record['id'], 'team': team, 'date': record.get('event_date'),
                 'value': value, 'count': stats.get('run_count', 1),
                 'metric': 'Mediana' if 'median_dps' in stats else 'Run único',
                 'summary_only': kind == 'benchmark_dataset_summary',
                 'path': path, 'record': record}
        groups.setdefault(group, {}).setdefault(team, []).append(point)
    for teams in groups.values():
        for points in teams.values():
            # Explicit predecessor links establish order even for an undated baseline.
            by_file = {point['path'].name: point for point in points}
            def depth(point, seen=None):
                seen = (seen or set()) | {point['id']}
                prior = by_file.get(point['record'].get('previous_dataset'))
                return 1 + depth(prior, seen) if prior and prior['id'] not in seen else 0
            points.sort(key=lambda point: (depth(point), point['date'] or '', point['id']))
    return groups


def render(records, root, repo):
    groups = series(records)
    # Prefer the actively tracked multi-run series; all remaining protocols get their own panel.
    ordered = sorted(groups, key=lambda key: ('maguu' not in key, key))
    esc = lambda value: html.escape(str(value), quote=True)
    number = lambda value: f'{value:,.1f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    tabs, panels = [], []
    for index, key in enumerate(ordered):
        teams = groups[key]
        sample = next(iter(teams.values()))[-1]['record']
        protocol = sample.get('protocol') or {}
        label = protocol.get('enemy', key)
        title = f'{label} · Lv{protocol.get("enemy_level", "?")}'
        tabs.append(f'<button type="button" data-chart-tab="{index}" aria-pressed="{str(index == 0).lower()}" aria-controls="progression-panel-{index}">{esc(title)}</button>')
        max_points = max(len(points) for points in teams.values())
        top = max(point['value'] for points in teams.values() for point in points)
        ceiling = max(5000, ((int(top) // 5000) + 1) * 5000)
        x = lambda i, length: 110 + i * 570 / (length - 1) if length > 1 else 395
        y = lambda value: 265 - value / ceiling * 210
        svg = [f'<svg viewBox="0 0 790 335" role="img" aria-labelledby="chart-title-{index} chart-desc-{index}"><title id="chart-title-{index}">Progressão de DPS — {esc(title)}</title><desc id="chart-desc-{index}">Equipes separadas por cor. Eixo horizontal: marcos em ordem registrada, sem escala temporal. Pontos e fontes também disponíveis na tabela.</desc>']
        for tick in range(5):
            value = ceiling * tick / 4
            pos = y(value)
            svg.append(f'<line class="chart-grid" x1="75" x2="730" y1="{pos}" y2="{pos}"/><text class="chart-axis" x="63" y="{pos + 5}" text-anchor="end">{value/1000:g}k</text>')
        svg.append('<text class="chart-axis" x="75" y="25">DPS registrado</text>')
        rows, legends = [], []
        for team, points in sorted(teams.items()):
            color = COLORS[team]
            legends.append(f'<span><i style="background:{color}"></i>Team {team} · {len(points)} marco(s)</span>')
            if len(points) > 1:
                coordinates = ' '.join(f'{x(i, len(points))},{y(point["value"])}' for i, point in enumerate(points))
                svg.append(f'<polyline fill="none" stroke="{color}" stroke-width="3" points="{coordinates}"/>')
            for i, point in enumerate(points):
                date = point['date'] or 'Anterior · sem data'
                url = f'{repo}/blob/main/{point["path"].relative_to(root).as_posix()}'
                caption = f'Team {team} · {date} · {point["metric"]} {number(point["value"])} DPS · {point["count"]} run(s)'
                px, py = x(i, len(points)), y(point['value'])
                svg.append(f'<a href="{esc(url)}" aria-label="{esc(caption)}" tabindex="0"><title>{esc(caption)}</title><circle cx="{px}" cy="{py}" r="6" fill="{color}" stroke="#101817" stroke-width="2"/></a>')
                svg.append(f'<text x="{px}" y="{py - 14}" text-anchor="middle" fill="{color}" class="chart-value">{number(point["value"])}</text>')
                if max_points > 1 or team == sorted(teams)[0]:
                    svg.append(f'<text x="{px}" y="295" text-anchor="middle" class="chart-axis">{esc(date)}</text>')
                evidence = 'Resumo; runs originais ausentes' if point['summary_only'] else f'{point["count"]} run(s)'
                rows.append(f'<tr><td>Team {team}</td><td>{esc(date)}</td><td>{number(point["value"])}</td><td>{point["metric"]} · {evidence}</td><td><a class="source" href="{esc(url)}">Registro ↗</a></td></tr>')
        svg.append('</svg>')
        note = 'A linha conecta marcos, sem interpolar DPS entre eles. O primeiro resumo não tem data de teste; sua ordem vem do vínculo ao dataset seguinte.' if max_points > 1 else 'A e B têm apenas um resultado bem-sucedido cada. Linhas aparecerão quando houver novos marcos no mesmo protocolo; não extrapolamos uma evolução.'
        panels.append(f'<div id="progression-panel-{index}" data-chart-panel="{index}"'+(' hidden' if index else '')+f'><div class="chart-legend">{"".join(legends)}</div><p class="muted">{esc(title)} · Abyss 12 · RES base 10% · janela de ~20s. Medianas quando há múltiplos runs; A/B são runs únicos.</p><div class="chart-scroll">{"".join(svg)}</div><p class="chart-caption">Marcos em ordem registrada · sem escala temporal</p><p class="muted">{esc(note)}</p><details><summary>Valores, evidência e fontes</summary><div class="table-wrap"><table><thead><tr><th>Equipe</th><th>Marco</th><th>DPS</th><th>Amostra</th><th>Fonte</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div></details></div>')
    return '<div class="record progression"><div class="chart-tabs" aria-label="Protocolo do gráfico">'+''.join(tabs)+'</div>'+''.join(panels)+'<p class="muted">Protocolos separados. Excluídos: tentativa A com setup falho, planos, clears de domínio, hits individuais e recordações antigas/30s. Ganhos refletem o estado completo da equipe; não isolam um único upgrade.</p></div>'
