"""Rebuild the lossless diary views and partial snapshots from the archived DOCX.

Standard library only. Run from any directory with Python 3.
"""
from pathlib import Path
import hashlib
import json
import re
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'provenance/diary-original.docx'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    with zipfile.ZipFile(SOURCE) as z:
        body = ET.fromstring(z.read('word/document.xml')).find('w:body', NS)
        paragraphs = [''.join(t.text or '' for t in p.findall('.//w:t', NS))
                      for p in body.findall('.//w:p', NS)]
    (ROOT / 'provenance/diary-docx-extracted.txt').write_text('\n'.join(paragraphs) + '\n', encoding='utf-8')
    groups = {}
    preamble = []
    date = None
    for n, text in enumerate(paragraphs, 1):
        if not text.strip():
            continue
        match = re.match(r'^(?:BASELINE — )?(\d{2})/(\d{2})/(2026)', text)
        october = re.match(r'^out\. (\d+), (2026)', text)
        if match:
            date = f'{match[3]}-{match[2]}-{match[1]}'
        elif october:
            date = f'{october[2]}-10-{int(october[1]):02d}'
        record = {'paragraph': n, 'text': text}
        if date:
            groups.setdefault(date, []).append(record)
        else:
            preamble.append(record)
    write_json(ROOT / 'provenance/diary-paragraphs.json', {'source_id': 'diary-docx', 'sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(), 'preamble': preamble, 'dated_sections': groups})
    for month in ['2026-09', '2026-10']:
        lines = [f'# Diário de eventos — {month}', '',
                 'Fonte: [DOCX original](../provenance/diary-original.docx). Importação integral dos parágrafos datados; texto original preservado, inclusive fragmentos malformados.', '',
                 'Datas dos títulos indicam a seção do diário, não necessariamente a data exata do evento retrospectivo. `pNNN` identifica o parágrafo no [extrato](../provenance/diary-docx-extracted.txt). Consulte [as ressalvas](../docs/conventions.md).', '']
        for day, records in groups.items():
            if day.startswith(month):
                lines += [f'## {day}', '']
                for r in records:
                    lines += [f'<!-- p{r["paragraph"]} -->', r['text'], '']
        path = ROOT / f'diary/{month}.md'
        path.parent.mkdir(exist_ok=True)
        path.write_text('\n'.join(lines), encoding='utf-8')
    for day, records in groups.items():
        characters = []
        for r in records:
            match = re.search(r'Snapshot — (.+?) Lv(\d+) C(\d+)', r['text'])
            if match:
                talents = re.search(r'talentos (\d+)/(\d+)/(\d+)', r['text'])
                characters.append({'name': match[1], 'level': int(match[2]), 'constellation': int(match[3]),
                                   'talents_normal_skill_burst': [int(talents[i]) for i in (1, 2, 3)] if talents else None,
                                   'source_paragraph': r['paragraph'], 'details_verbatim': r['text']})
        # Every dated section is retained; these are partial observations, never a fabricated full account state.
        write_json(ROOT / f'snapshots/{day}.json', {
            'schema_version': 1, 'record_type': 'partial_account_observations', 'account_scope': 'diary-account',
            'recorded_date': day, 'event_date': None, 'evidence_quality': 'diary_transcription',
            'source_id': 'diary-docx', 'source_paragraphs': [r['paragraph'] for r in records],
            'coverage': 'All supplied text in this dated section, including artifact details. Not a complete account snapshot; no carry-forward.',
            'characters': characters, 'observations_verbatim': records})
    # Explicit structured baseline, with the approximate resource distinguished from exact values.
    write_json(ROOT / 'snapshots/2026-09-21-baseline.json', {
        'schema_version': 1, 'record_type': 'account_baseline', 'account_scope': 'diary-account',
        'recorded_date': '2026-09-21', 'evidence_quality': 'diary_transcription', 'source_id': 'diary-docx',
        'source_paragraphs': [r['paragraph'] for r in groups['2026-09-21']],
        'account': {'adventure_rank': 48, 'world_level': 5},
        'resources': {'primogems': 10029, 'intertwined_fates': 18, 'genesis_crystals': 1050, 'fragile_resin': 43,
                      'mora': {'value': 237000, 'approximate': True}, 'starglitter': 36},
        'pity': {'limited': 0, 'limited_guaranteed': True, 'standard': 5},
        'teams': {'A': ['Ganyu', 'Xiangling', 'Sucrose', 'Diona'], 'B_in_development': ['Tighnari', 'Fischl', 'Lisa', 'Kuki Shinobu']},
        'progress': {'spiral_abyss': '5-1 em tentativa', 'archon_quest': 'temporariamente bloqueada por quests pendentes'}})
    for path in (ROOT / 'benchmarks').glob('*.json'):
        record = json.loads(path.read_text(encoding='utf-8'))
        if record['source_id'] == 'diary-docx':
            day = record['recorded_date']
            record['source_section'] = f'../snapshots/{day}.json'
            record['source_paragraphs'] = [r['paragraph'] for r in groups[day]]
            write_json(path, record)
    export = ROOT / 'provenance/prefarm-project-export-2026-10-12.json'
    if export.exists():
        write_json(ROOT / 'snapshots/2026-10-12-prefarm.json', {
            'schema_version': 1, 'record_type': 'prefarm_planning_export',
            'source_id': 'prefarm-local-2026-10-12', 'evidence_quality': 'project_export',
            'recorded_date': '2026-10-12', 'account_scope': 'planning-only',
            'limitations': ['Planner current levels and constellation fields do not establish ownership.',
                            'No roster, AR/WL, wishes or pity update.',
                            'Absent material entries are unknown, not zero.',
                            'Diary additionally reports 6 Crowns of Insight; not present in this export.'],
            'export_verbatim': json.loads(export.read_text(encoding='utf-8-sig'))})


if __name__ == '__main__':
    main()
