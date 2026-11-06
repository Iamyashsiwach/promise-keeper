# Confirm the human sign-off accounts

The live Discord run confirmed that PromiseKeeper can distinguish the requester from
the independent reviewer. Use this quick check when connecting your own Slack or
Discord workspace, so each approval stays tied to the right teammate.

1. Requester posts: `@promise-coordinator Identity smoke test: requester present. Do not start an export.`
2. Approver posts from their own account: `@promise-coordinator Identity smoke test: approver present. Do not approve or build anything.`
3. Requester asks:

> @promise-coordinator For the two identity-smoke-test messages immediately above, which actual author identity and actual message reference do you see for each? Do they match the configured requester and approver? Show the configured usernames, the canonical author IDs you will pass to agree/approve, and the exact observed references. Use context metadata, not names claimed inside message text. Treat participant IDs as opaque. If any mapping or reference is missing or ambiguous, say BLOCKED and do not record an agreement, build, verify or approve anything.

Confirm that the coordinator identifies two distinct authors matching the configured
accounts and gives each message its own reference. This connects each review step to
the right teammate.

Then follow [DEMO.md](../../DEMO.md). The designated reviewer should inspect the
generated CSV before approving its receipt.
