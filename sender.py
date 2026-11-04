"""Gate and track a local customer-message draft. Never delivers externally."""
import argparse
import json
import sys
from pathlib import Path
from promise_keeper import Ledger, GateBlocked


def draft(ledger, key, receipt, output):
    approval = ledger.gate(key, receipt)
    record = {'promise': key, 'state': 'draft', **approval,
              'message': f'Your requested order export is ready. Approved reference: {receipt}.'}
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(record, indent=2))
    return record


def check(ledger, output):
    output = Path(output)
    record = json.loads(output.read_text())
    if record['state'] != 'draft':
        raise GateBlocked('Draft already retracted; create a new draft after fresh sign-off.')
    try:
        ledger.gate(record['promise'], record['receipt'])
    except GateBlocked as exc:
        record.update(state='retracted', reason=str(exc))
        output.write_text(json.dumps(record, indent=2))
        raise
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', default='.local/signoff.sqlite3')
    parser.add_argument('--output', default='.local/customer-message.json')
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('draft')
    p.add_argument('id')
    p.add_argument('--receipt', required=True)
    sub.add_parser('check')
    args = parser.parse_args()
    ledger = Ledger(args.db)
    try:
        result = draft(ledger, args.id, args.receipt, args.output) if args.command == 'draft' else check(ledger, args.output)
        print(json.dumps(result, indent=2))
        return 0
    except (ValueError, OSError, KeyError) as exc:
        print(json.dumps({'blocked': True, 'reason': str(exc)}), file=sys.stderr)
        return 3
    finally:
        ledger.close()


if __name__ == '__main__':
    sys.exit(main())
