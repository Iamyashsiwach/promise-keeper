"""Create a new isolated starting state; never reset the completed live run."""
import argparse
from pathlib import Path
import shutil


def prepare(destination):
    source = Path(__file__).resolve().parents[1]
    destination = Path(destination).expanduser().resolve()
    if destination == source or destination.is_relative_to(source):
        raise ValueError('Choose a new directory outside this project.')
    destination.mkdir(parents=True, exist_ok=False)
    for name in ['promise_keeper.py', 'export_orders.py', 'test_ledger.py',
                 'test_export.py', 'README.md', 'DEMO.md', 'switch-room.template.yaml']:
        path = source / name
        if path.exists():
            shutil.copy2(path, destination / name)
    for name in ['agents', 'fixtures', 'evidence']:
        shutil.copytree(source / name, destination / name)
    exporter = destination / 'export_orders.py'
    text = exporter.read_text()
    old = "fields = ['order_number', 'total']"
    if text.count(old) != 1:
        raise ValueError('Exporter changed; inspect this new copy before rehearsing.')
    exporter.write_text(text.replace(old, "fields = ['order_number', 'total', 'email', 'internal_notes']"))
    (destination / 'REHEARSAL.txt').write_text(
        'Isolated rehearsal starting state. The exporter deliberately includes extra columns.\n'
        'No live ledger or credentials were copied. Evidence is historical, not a new run.\n'
        'Register separate agents pointing here, or change managed-agent directories explicitly.\n'
        'The test_export regression test should fail until the builder fixes this exporter.\n')
    return destination


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', help='New directory; existing directories are refused')
    args = parser.parse_args()
    try:
        print(prepare(args.destination))
    except (OSError, ValueError) as exc:
        parser.exit(2, f'{exc}\n')
