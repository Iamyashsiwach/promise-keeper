# Local-only CLI example

These test identities and references are explicitly NOT real Switch messages.
Use a separate database/artifact; they are not live evidence. In the room the
coordinator must obtain the actual author/ref from Switch context.

```sh
python3 promise_keeper.py --db .local/example.sqlite3 agree example --fields order_number total --rows 3 --requester sam-test --approver priya-test --request-ref local-test-confirmation
python3 export_orders.py --output .local/example.csv
python3 promise_keeper.py --db .local/example.sqlite3 verify example .local/example.csv
```

Inspect the actual file. On a new database the receipt is `1:1`. Use the actual
returned receipt if you reuse the database. Self-approval exits 2:

```sh
python3 promise_keeper.py --db .local/example.sqlite3 approve example --receipt 1:1 --reviewer sam-test --approval-ref local-test-self-attempt
python3 promise_keeper.py --db .local/example.sqlite3 approve example --receipt 1:1 --reviewer priya-test --approval-ref local-test-independent-review
python3 promise_keeper.py --db .local/example.sqlite3 gate example --receipt 1:1
python3 sender.py --db .local/example.sqlite3 --output .local/example-message.json draft example --receipt 1:1
python3 promise_keeper.py --db .local/example.sqlite3 agree example --fields order_number total email --rows 3 --requester sam-test --approver priya-test --request-ref local-test-revision
python3 sender.py --db .local/example.sqlite3 --output .local/example-message.json check
```

Last command exits 3 and marks the local draft retracted. Every new agreement
clears verification/approval. Email deny is retained; repeatable `--deny REGEX`
adds patterns to that default. There is no automatic external send.
