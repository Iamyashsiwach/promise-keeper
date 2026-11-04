"""Export sample orders using the human-confirmed customer columns."""
import argparse
import csv
import json
from pathlib import Path


def export_orders(source, target):
    orders = json.loads(Path(source).read_text())
    fields = ['order_number', 'total']
    Path(target).parent.mkdir(parents=True, exist_ok=True)
    with Path(target).open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(orders)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', default='fixtures/orders.json')
    parser.add_argument('--output', default='.local/export.csv')
    args = parser.parse_args()
    export_orders(args.source, args.output)
