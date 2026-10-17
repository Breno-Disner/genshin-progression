"""Build a dependency-free, read-only view of canonical records for GitHub Pages."""
from pathlib import Path
import html
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
REPO = 'https://github.com/Breno-Disner/genshin-progression'


def esc(value):
    return html.escape(str(value), quote=True)


def inline(value):
    # Escape source text before adding the small supported Markdown subset.
    value = esc(value)
    def link(match):
        label, url = match.groups()
        if url.startswith(('https://', 'http://')):
            return f'<a href="{url}">{label}</a>'
        if url.startswith(('../', './')):
            return f'<a href="{REPO}/blob/main/{url.removeprefix("../").removeprefix("./")}">{label}</a>'
        return label
    value = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link, value)
    value = re.sub(r'`([^`]+)`', r'<code>\1</code>', value)
    value = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', value)
    return value


def markdown(text):
    blocks, table = [], []
    def flush():
        if table:
            head, *rows = table
            blocks.append('<div class="table-wrap"><table><thead><tr>' + ''.join(f'<th>{inline(x)}</th>' for x in head) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{inline(x)}</td>' for x in row) + '</tr>' for row in rows) + '</tbody></table></div>')
            table.clear()
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith('<!--'):
            continue
        if line.startswith('|'):
            cells = [x.strip() for x in line.strip('|').split('|')]
            if not all(re.fullmatch(r':?-+:?', x) for x in cells):
                table.append(cells)
            continue
        flush()
        if line.startswith('#'):
            blocks.append(f'<h3>{inline(line.lstrip("# "))}</h3>')
        else:
            blocks.append(f'<p>{inline(line.removeprefix("• "))}</p>')
    flush()
    return '\n'.join(blocks)


def structured(value):
    """Expose every field without conflating missing, null, zero or planning data."""
    if value is None:
        return '<span class="unknown">Não informado</span>'
    if isinstance(value, bool):
        return 'Sim' if value else 'Não'
    if isinstance(value, dict):
        return '<dl class="fields">' + ''.join(f'<div><dt>{esc(k.replace("_", " "))}</dt><dd>{structured(v)}</dd></div>' for k, v in value.items()) + '</dl>'
    if isinstance(value, list):
        return '<ol class="values">' + ''.join(f'<li>{structured(x)}</li>' for x in value) + '</ol>' if value else '<span class="unknown">Lista vazia no registro</span>'
    return esc(value)


def records(folder):
    return [(p, json.loads(p.read_text(encoding='utf-8'))) for p in sorted((ROOT / folder).glob('*.json'), reverse=True)]


def record_card(path, record):
    date = record.get('recorded_date') or 'Data não informada'
    title = record.get('id', path.stem)
    return f'''<article class="record searchable" data-date="{esc(date)}"><div class="record-top"><span class="date">{esc(date)}</span><span class="badge">{esc(record.get('evidence_quality', 'Não informada'))}</span></div><h3>{esc(title)}</h3><p class="muted">{esc(record.get('record_type', '').replace('_', ' '))} · {esc(record.get('account_scope', 'Escopo não informado'))}</p><details><summary>Explorar registro completo</summary>{structured(record)}</details><a class="source" href="{REPO}/blob/main/{path.relative_to(ROOT).as_posix()}">Ver fonte ↗</a></article>'''


def build():
    out = ROOT / '_site'
    out.mkdir(exist_ok=True)
    entries = []
    for path in sorted((ROOT / 'diary').glob('*.md')):
        text = path.read_text(encoding='utf-8')
        for match in re.finditer(r'^## (\d{4}-\d{2}-\d{2})\s*\n(.*?)(?=^## \d{4}-\d{2}-\d{2}|\Z)', text, re.M | re.S):
            date, body = match.groups()
            entries.append((date, body, path))
    entries.sort(key=lambda item: item[0], reverse=True)
    assert entries, 'No diary entries found'
    snapshots, benchmarks = records('snapshots'), records('benchmarks')
    latest_date, latest_body, latest_path = entries[0]
    diary = ''.join(f'<article class="record searchable" data-date="{date}" id="day-{date}"><div class="record-top"><h3>{date}</h3><a class="source" href="{REPO}/blob/main/{path.relative_to(ROOT).as_posix()}#{date}">Fonte ↗</a></div>{markdown(body)}</article>' for date, body, path in entries)
    benchmark_cards = []
    for path, item in benchmarks:
        metric = ''
        if item.get('dps') is not None:
            metric = f'<div class="metric">{esc(format(item["dps"], ",").replace(",", "."))}<small>DPS · {esc(item.get("outcome", "resultado registrado"))}</small></div>'
        elif item.get('clear_seconds') is not None:
            metric = f'<div class="metric">{esc(item["clear_seconds"])}<small>segundos de clear · não é DPS</small></div>'
        card = record_card(path, item).replace('<details>', metric + '<details>', 1)
        benchmark_cards.append(card)
    template = (ROOT / 'web/index.html').read_text(encoding='utf-8')
    replacements = {
        'LATEST_DATE': latest_date, 'ENTRY_COUNT': str(len(entries)),
        'SNAPSHOT_COUNT': str(len(snapshots)), 'BENCHMARK_COUNT': str(len(benchmarks)),
        'LATEST_ENTRY': markdown(latest_body), 'DIARY': diary,
        'SNAPSHOTS': ''.join(record_card(p, r) for p, r in snapshots),
        'BENCHMARKS': ''.join(benchmark_cards),
        'CONVENTIONS': markdown((ROOT / 'docs/conventions.md').read_text(encoding='utf-8')),
    }
    for key, value in replacements.items():
        template = template.replace('{{' + key + '}}', value)
    assert not re.search(r'\{\{[A-Z_]+\}\}', template)
    (out / 'index.html').write_text(template, encoding='utf-8')
    for name in ('style.css', 'app.js'):
        shutil.copyfile(ROOT / 'web' / name, out / name)
    (out / '.nojekyll').touch()
    print(f'Built {len(entries)} diary entries, {len(snapshots)} snapshots, {len(benchmarks)} benchmarks in {out}')


if __name__ == '__main__':
    build()
