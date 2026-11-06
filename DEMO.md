# Run the independent sign-off workflow

Use only the three synthetic fixture orders. Sam and Priya represent two distinct
human responsibilities played by real people: requester and designated data owner.
They must use separate chat accounts. Add other teammates to the room as needed;
only the designated data owner can approve. Default team prefix `promise` gives the
mentions below; replace the prefix everywhere if you chose another one.

## Prepare off camera

- Run tests in the corrected source checkout. Then run `python3 scripts/prepare_rehearsal.py ../promise-rehearsal` with a new directory name. That copy has the intentionally bad exporter and no ledger. Its exporter regression test will fail until the builder fixes it.
- Import/use the template on a fresh Console server with a real connected chat app.
  All agents must point to that SAME rehearsal folder. Use actual account usernames
  for requester/approver. Confirm both people joined and provider/tool access works.
- Kickoff must confirm actual identity/reference context, a shared readable folder,
  `signoff-rule`, and coordinator-owned `promise-decisions`/`export-task` documents.
  If these are missing, fix setup before recording; don't invent a successful run.
- Have Priya send `@promise-coordinator I am here and ready to review.` from her
  own configured account during setup. Match the actual author to the configured
  data-owner account; the sentence itself is not identity proof.
- Have Priya ready to open `.local/export.csv` after the fix. This is local: share
  screen or give her access to that actual synthetic file. The draft is never sent.
- Frame the room so authors, mentions, receipts and changes are legible. Record the
  real workflow; shorten waits with labelled cuts if needed. Do not prefill evidence.

## Exact live messages, in order

**1 — Sam:**

> @promise-coordinator Create a customer CSV from all three sample orders. Include order_number and total only, in that order, with exactly three data rows. Never include email or internal notes. Ask me to confirm before starting. Only the designated data owner may approve it.

Expected: coordinator restates scope, actual requester and actual designated owner,
and asks for confirmation. No work starts before confirmation.

**2 — Sam, after checking that restatement:**

> @promise-coordinator Confirmed: order_number,total only, exactly three rows, no email or internal notes. Record revision 1 and begin.

Expected: actual author/ref stored; coordinator @mentions builder; builder runs
unchanged exporter. Coordinator verifies once: normally `1:1`, exit 2, extra columns
and redacted email row/column errors. Then @mentions builder to fix. Builder changes
only exporter, regenerates, verifies once: normally `1:2`, passing. Coordinator uses
status, not another verify. Shared room documents reflect actual scope and receipt.

**3 — Sam, once the passing receipt is visible:**

> @promise-coordinator approve 1:2

Use the ACTUAL passing receipt if it differs. Expected: code rejects this actual
author as requester; one-line refusal in room; approval remains null.

**4 — Priya inspects the actual CSV**, confirming three rows, exact header
`order_number,total`, and appropriate synthetic values. She uses her own account:

> @promise-coordinator approve 1:2

Expected: approval stores her actual account identity and message ref. Coordinator
checks status then @mentions sender with that receipt. Sender runs gate and
`sender.py draft`, posts DRAFT and cites actual receipt. Show the gate output with
approver, receipt, hash and reference; no invented names or references.

**5 — Sam, after the draft is visible:**

> @promise-coordinator Change my request: add email as the third column after order_number and total. Keep exactly three rows. I confirm this change. Record revision 2, but do not rebuild or approve anything. Show whether the old approval still applies and ask the sender to recheck its draft.

Expected: coordinator records revision 2, verification and approval both null,
status needs-verification. Email deny remains active. It immediately @mentions
sender; sender runs `sender.py check`, gets exit 3, marks the local draft retracted
and posts a new **RETRACTED** notice in the room. Do not delete the earlier draft.
No revision-2 build, verification or approval. Finish on this blocked state.

## If the story doesn't match

Stop and show the real failure. A wrong receipt requires using the displayed receipt,
not editing evidence or resetting counters. Self-approval unexpectedly succeeding,
missing real author/reference mapping, or a sender drafting while blocked means
stop and investigate before recording. An email-column request is not permission
to disable the email deny rule. Do not call a scripted CLI rehearsal a live chat run.
