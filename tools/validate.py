"""Check import coverage, provenance and benchmark consistency. Standard library only."""
from pathlib import Path
import hashlib
import json
import re
import statistics

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
            for field in ('source_document', 'build_snapshot', 'previous_dataset'):
                if r.get(field):
                    assert (path.parent / r[field]).exists(), (path, field)
            for correction in r.get('corrections', []):
                assert (path.parent / correction['source_document']).exists()
            accounting = r.get('cryo_bonus_accounting') or r.get('causal_analysis', {}).get('cryo_bonus_accounting')
            if accounting:
                assert abs(accounting['current_goblet_bonus_pct'] - accounting['historical_goblet_bonus_pct'] - accounting['goblet_enhancement_increase_pp']) < 1e-9
                assert abs(accounting['current_goblet_bonus_pct'] + accounting['finale_2pc_bonus_pct'] - accounting['current_cryo_damage_bonus_pct']) < 1e-9
                assert round(accounting['current_cryo_damage_bonus_pct']) == accounting['dummy_display_rounded_pct']
            if r.get('record_type') == 'benchmark_dataset':
                runs = r['runs']
                assert len(runs) >= 3 and r['unchanged_build_within_dataset'], path
                for run in runs:
                    if run.get('damage_by_character') is not None:
                        assert sum(run['damage_by_character'].values()) == run['total_damage'], (path, run['run'])
                    assert abs(run['total_damage'] / run['duration_seconds'] - run['dps']) / run['dps'] < 0.002
                values = [run['dps'] for run in runs]
                aggregate = r['aggregate']
                assert aggregate['run_count'] == len(values)
                assert aggregate['median_dps'] == statistics.median(values)
                assert abs(aggregate['mean_dps'] - statistics.mean(values)) < 1e-9
                assert aggregate['mean_dps_rounded_1dp'] == round(statistics.mean(values), 1)
                assert aggregate['best_dps'] == max(values) and aggregate['worst_dps'] == min(values)
                assert aggregate['range_dps'] == max(values) - min(values)
                previous = json.loads((path.parent / r['previous_dataset']).read_text(encoding='utf-8'))
                previous_stats = previous.get('aggregate', previous.get('summary'))
                increase = (statistics.median(values) / previous_stats['median_dps'] - 1) * 100
                assert r['progression']['median_increase_pct_rounded_1dp'] == round(increase, 1)
                assert r['series_window_seconds'] == previous['series_window_seconds'] == 20
                build = json.loads((path.parent / r['build_snapshot']).read_text(encoding='utf-8'))
                for character in build.get('characters', []):
                    skill = character.get('team_effective_talent_levels', {}).get('skill')
                    if skill:
                        assert character['talents_normal_skill_burst'][1] == skill['base']
                        assert skill['base'] + skill['team_bonus'] == skill['effective']
                progression = r['progression']
                if 'mean_increase_pct_rounded_2dp' in progression:
                    assert round((statistics.mean(values) / previous_stats['mean_dps'] - 1) * 100, 2) == progression['mean_increase_pct_rounded_2dp']
                    assert round(increase, 2) == progression['median_increase_pct_rounded_2dp']
                if 'analysis' in r:
                    analysis = r['analysis']
                    assert analysis['baseline_cryo_res_pct'] - analysis['reported_shred_pct'] == analysis['resulting_cryo_res_pct']
                    assert abs((analysis['res_multiplier_after'] / analysis['res_multiplier_before'] - 1) * 100 - analysis['predicted_increase_pct']) < 1e-9
                if 'cluster' in aggregate:
                    cluster = aggregate['cluster']
                    assert sum(cluster['min_dps'] <= value <= cluster['max_dps'] for value in values) == cluster['run_count']
                if 'median_total_damage' in aggregate:
                    assert aggregate['median_total_damage'] == statistics.median(run['total_damage'] for run in runs)
                for name, comparison in progression.get('character_median_damage', {}).items():
                    current = statistics.median(run['damage_by_character'][name] for run in runs)
                    prior = statistics.median(run['damage_by_character'][name] for run in previous['runs'])
                    assert current == comparison['current'] and prior == comparison['previous']
                    assert round((current / prior - 1) * 100, 2) == comparison['increase_pct_rounded_2dp']
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
