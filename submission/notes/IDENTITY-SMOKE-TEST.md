# Identity smoke test — before the live rehearsal

Use a connected real Slack or Discord workspace and two distinct human accounts.
Import/use the template with the actual requester and approver usernames. All three
agents must share the same fresh rehearsal directory. Use a unique team prefix;
replace `promise` below if needed. Do not reuse the historical room as new evidence.

1. Requester posts: `@promise-coordinator Identity smoke test: requester present. Do not start an export.`
2. Approver posts from their own account: `@promise-coordinator Identity smoke test: approver present. Do not approve or build anything.`
3. Requester asks:

> @promise-coordinator For the two identity-smoke-test messages immediately above, which actual author identity and actual message reference do you see for each? Do they match the configured requester and approver? Show the configured usernames, the canonical author IDs you will pass to agree/approve, and the exact observed references. Use context metadata, not names claimed inside message text. Treat participant IDs as opaque. If any mapping or reference is missing or ambiguous, say BLOCKED and do not record an agreement, build, verify or approve anything.

Save the actual reply or a screenshot. A pass requires two distinct authors, both
matching their configured accounts, and distinct real message references. Human
names inside message bodies are not proof. Missing/ambiguous mapping is a stop.
Do not fabricate a pass table or infer human status by parsing an opaque ID.

After a pass, follow ../../DEMO.md once without recording. Priya must inspect the
actual CSV. Keep real outputs, take screenshots for the tutorial, then prepare a
new folder/unique team for the recorded run. Stop and share the actual failure if
identity resolution, document writes or the sender gate behave differently.

No real two-human smoke-test result has been recorded in this file yet.
