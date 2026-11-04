"""Check the actual sample exporter against the original customer agreement."""
import csv
import json
from pathlib import Path
import tempfile
import unittest
from export_orders import export_orders


class ExportTests(unittest.TestCase):
    def test_exact_customer_projection_preserves_source_values(self):
        source = Path(__file__).parent / 'fixtures/orders.json'
        orders = json.loads(source.read_text())
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'export.csv'
            export_orders(source, target)
            with target.open(newline='') as file:
                reader = csv.DictReader(file)
                self.assertEqual(reader.fieldnames, ['order_number', 'total'])
                self.assertEqual(list(reader), [
                    {'order_number': order['order_number'], 'total': order['total']}
                    for order in orders
                ])


if __name__ == '__main__':
    unittest.main()
