import tempfile
import unittest
import json
import subprocess
import sys
from pathlib import Path
from promise_keeper import Ledger, GateBlocked


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.ledger = Ledger(self.root / 'ledger.db')
        self.csv = self.root / 'export.csv'
        self.csv.write_text('order_number,total\nDEMO-101,49.00\n')
        self.ledger.agree('demo', ['order_number', 'total'], 1, 'test-room/message-1', 'sam')

    def tearDown(self):
        self.ledger.close()
        self.temp.cleanup()

    def approve_current(self):
        receipt = self.ledger.verify('demo', self.csv)['receipt']
        return self.ledger.approve('demo', receipt, 'priya', 'room/approval-1')

    def test_private_column_blocks_approval(self):
        self.csv.write_text('order_number,total,email\nDEMO-101,49.00,one@example.test\n')
        v = self.ledger.verify('demo', self.csv)
        self.assertFalse(v['passed'])
        with self.assertRaises(ValueError):
            self.ledger.approve('demo', v['receipt'], 'reviewer', 'room/approval-1')

    def test_content_change_between_verification_and_approval_is_rejected(self):
        v = self.ledger.verify('demo', self.csv)
        self.csv.write_text('order_number,total\nDEMO-101,999.00\n')
        with self.assertRaises(ValueError):
            self.ledger.approve('demo', v['receipt'], 'reviewer', 'room/approval-1')

    def test_requirement_revision_invalidates_old_receipt(self):
        old = self.approve_current()
        self.ledger.agree('demo', ['order_number', 'total', 'email'], 1, 'test-room/message-2', 'sam')
        self.assertEqual(self.ledger.status('demo')['status'], 'needs-verification')
        with self.assertRaises(ValueError):
            self.ledger.approve('demo', old['receipt'], 'reviewer', 'room/approval-2')

    def test_reverification_invalidates_prior_approval_and_receipt(self):
        old = self.approve_current()
        self.ledger.verify('demo', self.csv)
        self.assertEqual(self.ledger.status('demo')['status'], 'verified')
        with self.assertRaises(ValueError):
            self.ledger.approve('demo', old['receipt'], 'reviewer', 'room/approval-2')

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

    def test_self_approval_is_case_insensitively_refused(self):
        receipt = self.ledger.verify('demo', self.csv)['receipt']
        with self.assertRaisesRegex(ValueError, 'own requests'):
            self.ledger.approve('demo', receipt, '  SAM  ', 'room/sam-approval')
        self.assertIsNone(self.ledger.status('demo')['approval'])

    def test_independent_reviewer_records_message_reference(self):
        receipt = self.ledger.verify('demo', self.csv)['receipt']
        approval = self.ledger.approve('demo', receipt, 'priya', 'room/priya-message')
        self.assertEqual(approval['approval_ref'], 'room/priya-message')
        self.assertEqual(self.ledger.gate('demo')['approver'], 'priya')

    def test_designated_data_owner_is_enforced(self):
        self.ledger.agree('demo', ['order_number', 'total'], 1, 'room/confirm', 'sam', approver=' Priya ')
        receipt = self.ledger.verify('demo', self.csv)['receipt']
        with self.assertRaisesRegex(ValueError, 'designated data owner'):
            self.ledger.approve('demo', receipt, 'someone-else', 'room/other-message')
        self.ledger.approve('demo', receipt, 'PRIYA', 'room/priya-message')
        self.assertEqual(self.ledger.status('demo')['status'], 'approved')

    def test_pii_in_allowed_column_is_redacted(self):
        private = 'customer.secret@example.test'
        self.csv.write_text(f'order_number,total\nDEMO-101,{private}\n')
        result = self.ledger.verify('demo', self.csv)
        self.assertFalse(result['passed'])
        self.assertIn('row 2, column total', ' '.join(result['errors']))
        self.assertNotIn(private, json.dumps(result))
        self.assertNotIn(private, json.dumps(self.ledger.events('demo')))

    def test_denied_header_is_redacted_even_when_requested(self):
        private = 'customer.secret@example.test'
        self.ledger.agree('demo', [private], 1, 'test/header', 'sam')
        self.csv.write_text(f'{private}\nordinary-value\n')
        result = self.ledger.verify('demo', self.csv)
        self.assertFalse(result['passed'])
        self.assertIn('row 1, column 1', ' '.join(result['errors']))
        self.assertNotIn(private, json.dumps(result))

    def test_pii_in_extra_cell_is_redacted(self):
        private = 'customer.secret@example.test'
        self.csv.write_text(f'order_number,total\nDEMO-101,49.00,{private}\n')
        result = self.ledger.verify('demo', self.csv)
        self.assertFalse(result['passed'])
        self.assertIn('row 2, column <extra cells>', ' '.join(result['errors']))
        self.assertNotIn(private, json.dumps(result))

    def test_custom_pattern_adds_to_email_policy(self):
        self.ledger.agree('demo', ['order_number', 'total'], 1, 'room/confirm', 'sam',
                          deny=[r'(?i)internal-note'])
        self.csv.write_text('order_number,total\nDEMO-101,INTERNAL-NOTE\n')
        result = self.ledger.verify('demo', self.csv)
        self.assertFalse(result['passed'])
        self.assertNotIn('INTERNAL-NOTE', json.dumps(result))
        self.csv.write_text('order_number,total\nDEMO-101,person@example.test\n')
        self.assertFalse(self.ledger.verify('demo', self.csv)['passed'])

    def test_invalid_policy_does_not_replace_agreement(self):
        with self.assertRaisesRegex(ValueError, 'Invalid deny pattern'):
            self.ledger.agree('demo', ['order_number', 'total'], 1, 'room/new', 'sam', deny=['['])
        self.assertEqual(self.ledger.status('demo')['revision'], 1)

    def test_empty_identity_or_approval_reference_is_refused(self):
        with self.assertRaises(ValueError):
            self.ledger.agree('demo', ['total'], 1, 'room/confirm', '   ')
        receipt = self.ledger.verify('demo', self.csv)['receipt']
        with self.assertRaises(ValueError):
            self.ledger.approve('demo', receipt, 'priya', '   ')

    def test_gate_closes_after_agreement_or_artifact_change(self):
        with self.assertRaises(GateBlocked):
            self.ledger.gate('demo')
        approval = self.approve_current()
        self.assertEqual(self.ledger.gate('demo')['receipt'], approval['receipt'])
        self.csv.write_text('order_number,total\nDEMO-101,99.00\n')
        with self.assertRaises(GateBlocked):
            self.ledger.gate('demo')
        self.approve_current()
        self.ledger.agree('demo', ['order_number', 'total', 'email'], 1, 'room/new', 'sam')
        with self.assertRaises(GateBlocked):
            self.ledger.gate('demo')

    def test_gate_refuses_old_draft_after_new_approval(self):
        old = self.approve_current()
        self.approve_current()
        with self.assertRaisesRegex(GateBlocked, 'draft receipt'):
            self.ledger.gate('demo', old['receipt'])

    def test_cli_gate_exit_codes(self):
        script = Path(__file__).with_name('promise_keeper.py')
        command = [sys.executable, str(script), '--db', str(self.root / 'ledger.db'), 'gate', 'demo']
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 3)
        self.approve_current()
        allowed = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(allowed.returncode, 0)
        self.assertEqual(json.loads(allowed.stdout)['approver'], 'priya')
        self.ledger.agree('demo', ['order_number', 'total'], 1, 'room/new', 'sam')
        blocked = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(blocked.returncode, 3)
        self.assertTrue(json.loads(blocked.stderr)['blocked'])

    def test_legacy_approval_is_not_a_new_identity_checked_signoff(self):
        p = self.ledger._get('demo')
        p.pop('requester')
        p['approval'] = {'receipt': '1:1', 'reviewer_label': 'sam', 'sha256': 'old'}
        with self.ledger.db:
            self.ledger._save(p, 'legacy-test-fixture', {})
        with self.assertRaises(GateBlocked):
            self.ledger.gate('demo')


if __name__ == '__main__':
    unittest.main()
