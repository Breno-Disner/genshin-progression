"""Check import coverage, provenance and benchmark consistency. Standard library only."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def main():
    index = json.loads((ROOT / 'provenance/diary-paragraphs.json').read_text(encoding='utf-8'))
    assert index['sha256'] == hashlib.sha256((ROOT / 'provenance/diary-original.docx').read_bytes()).hexdigest()
    lines = (ROOT / 'provenance/diary-docx-extracted.txt').read_text(encoding='utf-8').splitlines()
    paragraphs = index['preamble'] + [p for section in index['dated_sections'].values() for p in section]
    assert {p['paragraph'] for p in paragraphs} == {n for n, text in enumerate(lines, 1) if text.strip()}
    for p in paragraphs:
        assert lines[p['paragraph'] - 1] == p['text']
    for day, records in index['dated_sections'].items():
        monthly = (ROOT / f'diary/{day[:7]}.md').read_text(encoding='utf-8')
        snapshot = json.loads((ROOT / f'snapshots/{day}.json').read_text(encoding='utf-8'))
        assert snapshot['observations_verbatim'] == records
        for p in records:
            assert f'<!-- p{p["paragraph"]} -->\n{p["text"]}' in monthly
    count = 0
    for directory in ('snapshots', 'benchmarks'):
        for path in (ROOT / directory).glob('*.json'):
            r = json.loads(path.read_text(encoding='utf-8'))
            assert r['schema_version'] == 1 and r['source_id'] and r['record_type'] and r['evidence_quality'], path
            count += 1
            for p in r.get('source_paragraphs', []):
                assert 1 <= p <= len(lines), (path, p)
            if r.get('source_section'):
                assert (path.parent / r['source_section']).exists()
            contributions = r.get('damage_by_character', {})
            if len(contributions) == 4:
                assert sum(contributions.values()) == r['total_damage'], path
            if r.get('duration_seconds') and r.get('dps'):
                # Display precision need not reproduce DPS to the final integer.
                assert abs(r['total_damage'] / r['duration_seconds'] - r['dps']) / r['dps'] < 0.002, path
    for path in ROOT.rglob('*.md'):
        for link in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            if not re.match(r'\w+://', link) and not link.startswith('#'):
                assert (path.parent / link.split('#')[0]).exists(), (path, link)
    print(f'OK: {count} structured records; {len(index["dated_sections"])} dated sections; '
          f'{len(paragraphs)} nonempty source paragraphs preserved; hash, links and benchmark totals valid.')


if __name__ == '__main__':
    main()
