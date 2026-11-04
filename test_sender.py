import tempfile
import unittest
from pathlib import Path
from promise_keeper import Ledger, GateBlocked
from sender import draft, check


class SenderTests(unittest.TestCase):
    def test_draft_requires_approval_and_retracts_on_revision(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ledger = Ledger(root / 'db')
            self.addCleanup(ledger.close)
            csv = root / 'export.csv'
            csv.write_text('order_number,total\nA,1\n')
            output = root / 'message.json'
            ledger.agree('demo', ['order_number', 'total'], 1, 'test/confirm', 'sam', approver='priya')
            with self.assertRaises(GateBlocked):
                draft(ledger, 'demo', '1:1', output)
            self.assertFalse(output.exists())
            receipt = ledger.verify('demo', csv)['receipt']
            ledger.approve('demo', receipt, 'priya', 'test/approval')
            self.assertEqual(draft(ledger, 'demo', receipt, output)['receipt'], receipt)
            self.assertEqual(check(ledger, output)['state'], 'draft')
            ledger.agree('demo', ['order_number', 'total', 'email'], 1, 'test/change', 'sam', approver='priya')
            with self.assertRaises(GateBlocked):
                check(ledger, output)
            self.assertIn('"state": "retracted"', output.read_text())
            with self.assertRaises(GateBlocked):
                check(ledger, output)
