"""Local evidence ledger for the PromiseKeeper Switch workflow. Python 3.11+."""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import sqlite3
import sys
from datetime import datetime, timezone


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inspect_csv(path, fields, expected_rows):
    """Check bytes once, then use those same bytes for hashing and parsing."""
    data = Path(path).read_bytes()
    errors = []
    rows = []
    try:
        reader = csv.DictReader(io.StringIO(data.decode('utf-8-sig'), newline=''))
        if reader.fieldnames != fields:
            errors.append(f'Expected columns {fields}; found {reader.fieldnames}.')
        rows = list(reader)
        if any(None in row or any(v is None for v in row.values()) for row in rows):
            errors.append('CSV contains malformed rows.')
        if len(rows) != expected_rows:
            errors.append(f'Expected {expected_rows} rows; found {len(rows)}.')
    except (UnicodeError, csv.Error) as exc:
        errors.append(f'Cannot parse CSV: {exc}')
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

    def agree(self, key, fields, rows, request_ref):
        self._validate(fields, rows)
        with self.db:
            self.db.execute('BEGIN IMMEDIATE')
            try:
                old = self._get(key)
            except ValueError:
                old = None
            p = {'id': key, 'revision': old['revision'] + 1 if old else 1,
                 'fields': fields, 'expected_rows': rows, 'request_ref': request_ref,
                 'generation': old['generation'] if old else 0,
                 'verification': None, 'approval': None}
            self._save(p, 'agreement-recorded', {'revision': p['revision'], 'request_ref': request_ref})
        return p

    def verify(self, key, path):
        with self.db:
            self.db.execute('BEGIN IMMEDIATE')
            p = self._get(key)
            p['generation'] += 1
            p['approval'] = None
            # An unreadable replacement must invalidate earlier approval too.
            try:
                result = inspect_csv(path, p['fields'], p['expected_rows'])
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
            now = inspect_csv(v['artifact'], p['fields'], p['expected_rows'])
        except OSError:
            return False
        return now['passed'] and now['sha256'] == v['sha256']

    def approve(self, key, receipt, actor):
        if not actor.strip():
            raise ValueError('Reviewer label must be nonempty.')
        with self.db:
            self.db.execute('BEGIN IMMEDIATE')
            p = self._get(key)
            v = p['verification']
            if not v or receipt != v['receipt'] or not self._current(p):
                raise ValueError('Approval refused: receipt is stale, verification failed, or artifact changed. Verify again.')
            p['approval'] = {'receipt': receipt, 'reviewer_label': actor, 'sha256': v['sha256']}
            self._save(p, 'approval-recorded', p['approval'])
        return p['approval']

    def status(self, key):
        with self.db:
            self.db.execute('BEGIN IMMEDIATE')
            p = self._get(key)
            current = self._current(p)
            if p['approval'] and not current:
                p['approval'] = None
                self._save(p, 'approval-invalidated', {'reason': 'Artifact missing, changed, or no longer valid.'})
            p['status'] = 'approved' if p['approval'] and current else 'verified' if current else 'needs-verification'
        return p

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
    p = sub.add_parser('verify')
    p.add_argument('id')
    p.add_argument('artifact')
    p = sub.add_parser('approve', help='Local reviewer action; not an authenticated chat approval')
    p.add_argument('id')
    p.add_argument('--receipt', required=True)
    p.add_argument('--reviewer', required=True)
    for command in ['status', 'events']:
        sub.add_parser(command).add_argument('id')
    args = parser.parse_args()
    ledger = Ledger(args.db)
    try:
        if args.command == 'agree':
            result = ledger.agree(args.id, args.fields, args.rows, args.request_ref)
        elif args.command == 'verify':
            result = ledger.verify(args.id, args.artifact)
        elif args.command == 'approve':
            result = ledger.approve(args.id, args.receipt, args.reviewer)
        else:
            result = getattr(ledger, args.command)(args.id)
        print(json.dumps(result, indent=2))
        return 2 if args.command == 'verify' and not result['passed'] else 0
    except (ValueError, OSError) as exc:
        print(json.dumps({'error': str(exc)}), file=sys.stderr)
        return 2
    finally:
        ledger.close()


if __name__ == '__main__':
    sys.exit(main())
