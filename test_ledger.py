import tempfile
import unittest
from pathlib import Path
from promise_keeper import Ledger


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.ledger = Ledger(self.root / 'ledger.db')
        self.csv = self.root / 'export.csv'
        self.csv.write_text('order_number,total\nDEMO-101,49.00\n')
        self.ledger.agree('demo', ['order_number', 'total'], 1, 'test-room/message-1')

    def tearDown(self):
        self.ledger.close()
        self.temp.cleanup()

    def approve_current(self):
        receipt = self.ledger.verify('demo', self.csv)['receipt']
        return self.ledger.approve('demo', receipt, 'local-test-reviewer')

    def test_private_column_blocks_approval(self):
        self.csv.write_text('order_number,total,email\nDEMO-101,49.00,one@example.test\n')
        v = self.ledger.verify('demo', self.csv)
        self.assertFalse(v['passed'])
        with self.assertRaises(ValueError):
            self.ledger.approve('demo', v['receipt'], 'reviewer')

    def test_content_change_between_verification_and_approval_is_rejected(self):
        v = self.ledger.verify('demo', self.csv)
        self.csv.write_text('order_number,total\nDEMO-101,999.00\n')
        with self.assertRaises(ValueError):
            self.ledger.approve('demo', v['receipt'], 'reviewer')

    def test_requirement_revision_invalidates_old_receipt(self):
        old = self.approve_current()
        self.ledger.agree('demo', ['order_number', 'total', 'email'], 1, 'test-room/message-2')
        self.assertEqual(self.ledger.status('demo')['status'], 'needs-verification')
        with self.assertRaises(ValueError):
            self.ledger.approve('demo', old['receipt'], 'reviewer')

    def test_reverification_invalidates_prior_approval_and_receipt(self):
        old = self.approve_current()
        self.ledger.verify('demo', self.csv)
        self.assertEqual(self.ledger.status('demo')['status'], 'verified')
        with self.assertRaises(ValueError):
            self.ledger.approve('demo', old['receipt'], 'reviewer')

    def test_artifact_change_invalidates_approval_when_checked(self):
        self.approve_current()
        self.csv.write_text('order_number,total\nDEMO-101,999.00\n')
        self.assertIsNone(self.ledger.status('demo')['approval'])
        self.assertEqual(self.ledger.events('demo')[-1]['kind'], 'approval-invalidated')

    def test_missing_artifact_revokes_approval(self):
        self.approve_current()
        self.csv.unlink()
        self.assertEqual(self.ledger.status('demo')['status'], 'needs-verification')

    def test_malformed_or_incomplete_export_fails(self):
        for content in ['order_number,total\n', 'order_number,total\nDEMO-101\n', 'order_number,total\nDEMO-101,1,extra\n']:
            with self.subTest(content=content):
                self.csv.write_text(content)
                self.assertFalse(self.ledger.verify('demo', self.csv)['passed'])

    def test_approval_and_events_survive_restart(self):
        self.approve_current()
        self.ledger.close()
        self.ledger = Ledger(self.root / 'ledger.db')
        self.assertEqual(self.ledger.status('demo')['status'], 'approved')
        self.assertEqual([e['kind'] for e in self.ledger.events('demo')],
                         ['agreement-recorded', 'verification-passed', 'approval-recorded'])


if __name__ == '__main__':
    unittest.main()
