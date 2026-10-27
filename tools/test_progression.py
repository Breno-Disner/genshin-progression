"""Check chart inclusion, protocol isolation, order and accessible source output."""
import json
from pathlib import Path
import unittest
from progression import series, render

ROOT = Path(__file__).resolve().parents[1]


class ProgressionTests(unittest.TestCase):
    def setUp(self):
        self.records = [(p, json.loads(p.read_text(encoding='utf-8')))
                        for p in (ROOT / 'benchmarks').glob('*.json')]

    def test_only_actual_dps_observations(self):
        groups = series(self.records)
        points = [p for teams in groups.values() for values in teams.values() for p in values]
        self.assertTrue(points)
        for p in points:
            self.assertNotEqual(p['record'].get('outcome'), 'failed_setup')
            self.assertNotIn(p['record']['record_type'], ('benchmark_plan', 'content_clear', 'benchmark_recollection_series'))

    def test_protocols_and_team_identities_stay_separate(self):
        groups = series(self.records)
        for teams in groups.values():
            targets = {p['record'].get('protocol', {}).get('enemy')
                       for points in teams.values() for p in points if p['record'].get('protocol')}
            self.assertLessEqual(len(targets), 1)
        self.assertEqual(set(groups['dummy-abyss12-mitachurl100-res10']), {'A', 'B'})

    def test_undated_baseline_uses_predecessor_order(self):
        points = series(self.records)['team-c-20s-abyss12-maguu-kenki100-res10']['C']
        self.assertIsNone(points[0]['date'])
        self.assertTrue(points[0]['summary_only'])
        for earlier, later in zip(points, points[1:]):
            self.assertEqual(later['record']['previous_dataset'], earlier['path'].name)

    def test_source_table_and_single_point_teams(self):
        output = render(self.records, ROOT, 'https://example.com/repo')
        self.assertIn('Valores, evidência e fontes', output)
        self.assertIn('sem escala temporal', output)
        self.assertIn('Anterior · sem data', output)
        for _, record in self.records:
            if record.get('record_type') == 'benchmark_dataset' and record.get('event_date_label'):
                self.assertIn(record['event_date_label'], output)
        self.assertIn('Team A · 1 marco(s)', output)
        self.assertIn('Team B · 1 marco(s)', output)
        # Only C has sufficient observations for a connecting line.
        self.assertEqual(output.count('<polyline '), 1)
        self.assertIn('aria-label="Team C', output)


if __name__ == '__main__':
    unittest.main()
