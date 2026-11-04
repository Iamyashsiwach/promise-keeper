"""Create an isolated seeded demo; never reset the completed live run."""
import argparse
from pathlib import Path
import shutil


CORRECT = "fields = ['order_number', 'total']"
SEEDED = "fields = ['order_number', 'total', 'email', 'internal_notes']"
FILES = ['promise_keeper.py', 'sender.py', 'export_orders.py', 'test_ledger.py',
         'test_export.py', 'test_sender.py', 'test_rehearsal.py', 'README.md',
         'DEMO.md', 'switch-room.template.yaml']
DIRECTORIES = ['agents', 'fixtures', 'evidence', 'scripts', 'submission']


def prepare(destination):
    source = Path(__file__).resolve().parents[1]
    destination = Path(destination).expanduser().resolve()
    if destination == source or destination.is_relative_to(source):
        raise ValueError('Choose a new directory outside this project.')
    if destination.exists():
        raise ValueError('Destination already exists; choose a new directory.')
    for name in FILES + DIRECTORIES:
        if not (source / name).exists():
            raise ValueError(f'Missing rehearsal source: {name}')
    exporter_text = (source / 'export_orders.py').read_text()
    if exporter_text.count(CORRECT) == 1:
        exporter_text = exporter_text.replace(CORRECT, SEEDED)
    elif exporter_text.count(SEEDED) != 1:
        raise ValueError('Exporter changed; inspect source before preparing a rehearsal.')
    # An allowlist excludes live ledgers, credentials, caches and .git entirely.
    destination.mkdir(parents=True, exist_ok=False)
    for name in FILES:
        shutil.copy2(source / name, destination / name)
    for name in DIRECTORIES:
        shutil.copytree(source / name, destination / name,
                        ignore=shutil.ignore_patterns('__pycache__', '.DS_Store', '.env', '.env.*', '.local', '*.sqlite3*'))
    (destination / 'export_orders.py').write_text(exporter_text)
    (destination / 'REHEARSAL.txt').write_text(
        'Isolated starting state: exporter intentionally includes email and internal_notes.\n'
        'All three agents must point to THIS same directory. Use DEMO.md.\n'
        'Two actual human accounts are required; do not impersonate the data owner.\n'
        'No live ledger, credentials or Git history were copied.\n'
        'Use .local/signoff.sqlite3 and customer-export for the new run.\n'
        'Evidence/videos are historical, not a new live run.\n'
        'test_export must fail until the builder fixes the exporter; other tests should pass.\n')
    return destination


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', help='New directory outside this project')
    args = parser.parse_args()
    try:
        print(prepare(args.destination))
    except (OSError, ValueError) as exc:
        parser.exit(2, f'{exc}\n')
