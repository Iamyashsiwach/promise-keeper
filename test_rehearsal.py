import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from scripts.prepare_rehearsal import prepare


class RehearsalTests(unittest.TestCase):
    def test_isolated_seeded_copy_and_existing_destination_refusal(self):
        source = Path(__file__).resolve().parent
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'rehearsal'
            prepare(target)
            self.assertFalse((target / '.local').exists())
            self.assertFalse((target / '.git').exists())
            self.assertFalse((target / '.env').exists())
            for name in ['sender.py', 'test_sender.py', 'agents/sender.md', 'scripts/prepare_rehearsal.py']:
                self.assertTrue((target / name).exists())
            self.assertEqual((target / 'evidence/live-run.json').read_bytes(),
                             (source / 'evidence/live-run.json').read_bytes())
            result = subprocess.run([sys.executable, 'export_orders.py'], cwd=target, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            with (target / '.local/export.csv').open() as f:
                rows = list(csv.reader(f))
            self.assertEqual(rows[0], ['order_number', 'total', 'email', 'internal_notes'])
            self.assertEqual(len(rows), 4)
            marker = target / 'do-not-reset.txt'
            marker.write_text('preserve')
            with self.assertRaisesRegex(ValueError, 'already exists'):
                prepare(target)
            self.assertEqual(marker.read_text(), 'preserve')

    def test_source_directory_is_refused(self):
        with self.assertRaisesRegex(ValueError, 'outside'):
            prepare(Path(__file__).resolve().parent)
