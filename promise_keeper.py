"""Local evidence ledger for the PromiseKeeper Switch workflow. Python 3.11+."""
import argparse
import csv
import hashlib
import io
import json
import re
from pathlib import Path
import sqlite3
import sys
from datetime import datetime, timezone


def digest(data):
    return hashlib.sha256(data).hexdigest()


EMAIL_DENY = r'(?i)[a-z0-9.!#$%&\x27*+/=?^_`{|}~-]+@[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)+'


class GateBlocked(ValueError):
    """The current evidence does not authorize a customer-message draft."""


def compile_patterns(patterns):
    compiled = []
    for index, pattern in enumerate(patterns, 1):
        try:
            compiled.append(re.compile(pattern))
        except (re.error, TypeError):
            raise ValueError(f'Invalid deny pattern {index}.') from None
    return compiled


def identity(value):
    return value.strip().casefold()


def inspect_csv(path, fields, expected_rows, deny_patterns=None):
    """Check bytes once, then use those same bytes for hashing and parsing."""
    data = Path(path).read_bytes()
    errors = []
    rows = []
    patterns = compile_patterns(deny_patterns if deny_patterns is not None else [EMAIL_DENY])
    try:
        reader = csv.DictReader(io.StringIO(data.decode('utf-8-sig'), newline=''))
        if reader.fieldnames != fields:
            errors.append('CSV columns do not match the agreed names and order.')
        rows = list(reader)
        if any(None in row or any(v is None for v in row.values()) for row in rows):
            errors.append('CSV contains malformed rows.')
        if len(rows) != expected_rows:
            errors.append(f'Expected {expected_rows} rows; found {len(rows)}.')
        # Inspect every data cell, including unexpected columns and surplus cells.
        # Row numbers are logical CSV records: header=1, first data record=2.
        for row_number, row in enumerate(rows, 2):
            for column, values in row.items():
                cells = values if isinstance(values, list) else [values]
                if any(pattern.search(value) for value in cells if value is not None for pattern in patterns):
                    label = column if column is not None else '<extra cells>'
                    if any(pattern.search(label) for pattern in patterns):
                        label = '<redacted header>'
                    errors.append(f'Denied content at row {row_number}, column {label}.')
    except (UnicodeError, csv.Error):
        errors.append('Cannot parse CSV as UTF-8 CSV.')
    return {'sha256': digest(data), 'rows': len(rows), 'passed': not errors,
            'errors': errors}


class Ledger:
    def __init__(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path)
        self.db.execute('CREATE TABLE IF NOT EXISTS promises (id TEXT PRIMARY KEY, body TEXT NOT NULL)')
        self.db.execute('CREATE TABLE IF NOT EXISTS events (seq INTEGER PRIMARY KEY, at TEXT, promise_id TEXT, kind TEXT, detail TEXT)')
        self.db.commit()

    def close(self):
        self.db.close()

    def _get(self, key):
        row = self.db.execute('SELECT body FROM promises WHERE id = ?', (key,)).fetchone()
        if not row:
            raise ValueError(f'Unknown promise: {key}')
        return json.loads(row[0])

    def _save(self, p, kind, detail):
        self.db.execute('INSERT INTO promises VALUES (?, ?) ON CONFLICT(id) DO UPDATE SET body=excluded.body',
                        (p['id'], json.dumps(p)))
        self.db.execute('INSERT INTO events(at,promise_id,kind,detail) VALUES (?,?,?,?)',
                        (datetime.now(timezone.utc).isoformat(), p['id'], kind, json.dumps(detail)))

    @staticmethod
    def _validate(fields, rows):
        if not fields or len(set(fields)) != len(fields) or any(not x.strip() for x in fields):
            raise ValueError('Provide unique, nonempty column names.')
        if rows < 0:
            raise ValueError('Expected row count cannot be negative.')

    def agree(self, key, fields, rows, request_ref, requester, deny=None, approver=None):
        self._validate(fields, rows)
        if not requester.strip() or not request_ref.strip():
            raise ValueError('Requester and request reference must be nonempty.')
        if approver is not None and (not approver.strip() or identity(approver) == identity(requester)):
            raise ValueError('Designated approver must differ from requester.')
        patterns = list(dict.fromkeys([EMAIL_DENY, *(deny or [])]))
        compile_patterns(patterns)
        with self.db:
            self.db.execute('BEGIN IMMEDIATE')
            try:
                old = self._get(key)
            except ValueError:
                old = None
            p = {'id': key, 'revision': old['revision'] + 1 if old else 1,
                 'fields': fields, 'expected_rows': rows, 'request_ref': request_ref,
                 'requester': requester.strip(), 'approver': approver.strip() if approver else None,
                 'deny_patterns': patterns,
                 'generation': old['generation'] if old else 0,
                 'verification': None, 'approval': None}
            self._save(p, 'agreement-recorded', {'revision': p['revision'], 'request_ref': request_ref,
                                               'requester': p['requester'], 'approver': p['approver']})
        return p

    def verify(self, key, path):
        with self.db:
            self.db.execute('BEGIN IMMEDIATE')
            p = self._get(key)
            p['generation'] += 1
            p['approval'] = None
            # An unreadable replacement must invalidate earlier approval too.
            try:
                result = inspect_csv(path, p['fields'], p['expected_rows'], p.get('deny_patterns'))
            except OSError as exc:
                result = {'sha256': None, 'rows': 0, 'passed': False, 'errors': [str(exc)]}
            result.update({'artifact': str(Path(path).resolve()), 'revision': p['revision'],
                           'receipt': f"{p['revision']}:{p['generation']}"})
            p['verification'] = result
            self._save(p, 'verification-passed' if result['passed'] else 'verification-failed', result)
        return result

    @staticmethod
    def _current(p):
        v = p['verification']
        if not v or not v['passed'] or v['revision'] != p['revision']:
            return False
        try:
            now = inspect_csv(v['artifact'], p['fields'], p['expected_rows'], p.get('deny_patterns'))
        except OSError:
            return False
        return now['passed'] and now['sha256'] == v['sha256']

    def approve(self, key, receipt, actor, approval_ref):
        if not actor.strip() or not approval_ref.strip():
            raise ValueError('Reviewer and approval reference must be nonempty.')
        with self.db:
            self.db.execute('BEGIN IMMEDIATE')
            p = self._get(key)
            if not p.get('requester'):
                raise ValueError('Legacy agreement has no requester; record a new agreement first.')
            if identity(actor) == identity(p['requester']):
                raise ValueError('Approval refused: requesters cannot approve their own requests.')
            if p.get('approver') and identity(actor) != identity(p['approver']):
                raise ValueError('Approval refused: reviewer is not the designated data owner.')
            v = p['verification']
            if not v or receipt != v['receipt'] or not self._current(p):
                raise ValueError('Approval refused: receipt is stale, verification failed, or artifact changed. Verify again.')
            p['approval'] = {'receipt': receipt, 'reviewer_label': actor.strip(),
                             'approval_ref': approval_ref.strip(), 'revision': p['revision'],
                             'sha256': v['sha256']}
            self._save(p, 'approval-recorded', p['approval'])
        return p['approval']

    def status(self, key):
        with self.db:
            self.db.execute('BEGIN IMMEDIATE')
            p = self._get(key)
            current = self._current(p)
            a = p['approval']
            valid_approval = bool(a and current and p.get('requester') and a.get('approval_ref')
                                  and a.get('revision') == p['revision']
                                  and a.get('receipt') == p['verification']['receipt']
                                  and a.get('sha256') == p['verification']['sha256']
                                  and identity(a['reviewer_label']) != identity(p['requester'])
                                  and (not p.get('approver') or identity(a['reviewer_label']) == identity(p['approver'])))
            if a and not valid_approval:
                p['approval'] = None
                self._save(p, 'approval-invalidated', {'reason': 'Artifact or sign-off is missing, changed, or no longer valid.'})
            p['status'] = 'approved' if p['approval'] and current else 'verified' if current else 'needs-verification'
        return p

    def gate(self, key, receipt=None):
        try:
            p = self.status(key)
        except ValueError as exc:
            raise GateBlocked(str(exc)) from None
        if p['status'] != 'approved':
            raise GateBlocked(f"Release blocked: revision {p['revision']} needs verification and independent approval.")
        a = p['approval']
        if receipt is not None and receipt != a['receipt']:
            raise GateBlocked('Release blocked: the draft receipt is not the currently approved receipt.')
        return {'revision': p['revision'], 'receipt': a['receipt'], 'sha256': a['sha256'],
                'approver': a['reviewer_label'], 'approval_ref': a['approval_ref']}

    def events(self, key):
        return [{'seq': r[0], 'at': r[1], 'kind': r[2], 'detail': json.loads(r[3])}
                for r in self.db.execute('SELECT seq,at,kind,detail FROM events WHERE promise_id=? ORDER BY seq', (key,))]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', default='.local/ledger.sqlite3')
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('agree', help='Record or revise a human-confirmed agreement')
    p.add_argument('id')
    p.add_argument('--fields', nargs='+', required=True)
    p.add_argument('--rows', type=int, required=True)
    p.add_argument('--request-ref', required=True, help='Switch conversation/message reference')
    p.add_argument('--requester', required=True, help='Actual human author identity from Switch')
    p.add_argument('--approver', help='Designated data owner identity; always set in the room workflow')
    p.add_argument('--deny', action='append', default=[], help='Additional deny regex; email detection is always enabled')
    p = sub.add_parser('verify')
    p.add_argument('id')
    p.add_argument('artifact')
    p = sub.add_parser('approve', help='Record sign-off using the actual human author and message reference')
    p.add_argument('id')
    p.add_argument('--receipt', required=True)
    p.add_argument('--reviewer', required=True)
    p.add_argument('--approval-ref', required=True)
    p = sub.add_parser('gate', help='Exit 3 unless the current revision and file have independent sign-off')
    p.add_argument('id')
    p.add_argument('--receipt', help='Also require this draft receipt to still be current')
    for command in ['status', 'events']:
        sub.add_parser(command).add_argument('id')
    args = parser.parse_args()
    ledger = Ledger(args.db)
    try:
        if args.command == 'agree':
            result = ledger.agree(args.id, args.fields, args.rows, args.request_ref,
                                  args.requester, args.deny, args.approver)
        elif args.command == 'verify':
            result = ledger.verify(args.id, args.artifact)
        elif args.command == 'approve':
            result = ledger.approve(args.id, args.receipt, args.reviewer, args.approval_ref)
        elif args.command == 'gate':
            result = ledger.gate(args.id, args.receipt)
        else:
            result = getattr(ledger, args.command)(args.id)
        print(json.dumps(result, indent=2))
        return 2 if args.command == 'verify' and not result['passed'] else 0
    except GateBlocked as exc:
        print(json.dumps({'blocked': True, 'reason': str(exc)}), file=sys.stderr)
        return 3
    except (ValueError, OSError) as exc:
        print(json.dumps({'error': str(exc)}), file=sys.stderr)
        return 2
    finally:
        ledger.close()


if __name__ == '__main__':
    sys.exit(main())
