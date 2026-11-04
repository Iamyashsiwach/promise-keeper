# Live demo and build checkpoints

These are prompts for a real Switch room, not a transcript of work already performed.

The first live run is complete and preserved in `evidence/live-run.json`. The root exporter is now corrected. For another live rehearsal, first run `python3 scripts/prepare_rehearsal.py ../promise-keeper-rehearsal` with a new destination, then point separate agents at that copy. Never reset or overwrite the completed live ledger. The included video is a walkthrough of the recorded run, not a new execution.

## First request — dictate using Wispr

“@promise-coordinator I need a CSV export for our customer. Use the three synthetic orders in the project. Include order number and total only. Email addresses and internal notes must never appear. Ask me to confirm the agreement, then work with promise-builder to produce and verify the file.”

Confirm the allowed fields as `order_number` and `total`, and the expected row count as 3. Record the actual Switch message reference.

## Show the failure

The initial exporter deliberately outputs extra private columns. Have the agents actually run it and show the verifier's failure. The builder then changes the exporter, regenerates the CSV, and verifies again. Keep the verifier unchanged.

## Review the passing version

Read the CSV yourself. Run the approve command with the actual latest receipt and your reviewer label, then have the coordinator run status. State in the demo that this is a local reviewer command, not authenticated chat approval.

## Change the agreement

Dictate: “Change the request: include email too. Record this as a new revision, but don't approve or rebuild yet. Show whether my previous approval still applies.”

The coordinator should confirm the changed fields, record a new revision, and show `needs-verification` with no approval. That is the primary versioning demonstration. It does not need to build the second export during the short video.

## Evidence to capture

- Real person/agent conversation and handoff in Mattermost through Switch.
- Failing verification and real exporter diff.
- Passing receipt, human review, and current approved status.
- New agreement revision with the earlier approval invalidated.
- Actual elapsed time and number of human decisions; no invented time-saved or revenue claims.
- Wispr Insights usage scorecard, excluding unrelated personal text.

## Work order, November 5–7, 2026 (IST)

1. Nov 5: finish local Switch setup, create agents/room, and complete the first live run.
2. Nov 6: fix integration issues; repeat from a fresh demo ledger; export the actual room template; capture evidence and draft README/blog.
3. Nov 7: freeze features; verify a fresh checkout; record the short video; inspect the submission form; submit before the official 11:59 PM IST deadline, targeting 8 PM internally.

Use a new `--db` path for a fresh rehearsal so you preserve earlier evidence. Do not present scripted test approvals as real human participation.
