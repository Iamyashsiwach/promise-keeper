# Build a two-person sign-off room for AI agents in Switch

An agent can finish an export and still include the wrong columns. A team also needs
to know who requested the file, who reviewed it, and whether that review still applies.
In this tutorial you will set up PromiseKeeper: two people and three agents in one
Switch room, with a small Python gate for a local customer-message draft.

This is a tutorial draft. The new two-person live run and screenshots still need to
be captured; the included older evidence demonstrates only a single-human workflow.

## 1. Get Console, Python and a teammate ready

Install [Switch Console](https://docs.switchagents.ai/switch-rooms/getting-started/install-switch-console)
and follow the [quickstart](https://docs.switchagents.ai/switch-rooms/getting-started/index)
to add your server and sign in to an installed coding provider. Use Python 3.11+.
PromiseKeeper uses only the Python standard library; do not install extra packages.

Connect your real Slack or Discord workspace using Switch's messaging-app setup.
Invite a real colleague: you play requester Sam; they play data owner Priya. These
are roles, not extra accounts for you to impersonate. Record the actual usernames.

[SCREENSHOT 1: Console's connected messaging app; hide credentials.]

## 2. Prepare the starting project

Use the reviewed `win` checkout until it is published; the current public main is
the older workflow. Once the reviewed version is published, clone that version:

```sh
git clone https://github.com/Iamyashsiwach/promise-keeper.git
cd promise-keeper
python3 -m unittest -v
python3 scripts/prepare_rehearsal.py ../promise-rehearsal
```

The destination must not exist. The source exporter is corrected; the rehearsal copy
intentionally restores extra email and internal-notes columns. This makes the failure
repeatable without touching the historical ledger. Rehearsal starts with no database.
Its exporter regression test should fail until the builder corrects the exporter.

## 3. Import the team template

In Console, select **Templates → Import template**. Paste `switch-room.template.yaml`,
save it privately and select **Use template**. The template follows Switch's documented
[template format](https://docs.switchagents.ai/switch-rooms/administer/room-templates)
and upstream [triage-pair example](https://github.com/sandbox-quantum/switch/blob/main/examples/agent-templates/triage-pair.template.yaml).

Fill in a unique `team` prefix (use `promise` for the messages below), your installed
provider, online machine, connected `bridge`, actual requester username, and distinct
data-owner username. For `directory`, select the absolute `promise-rehearsal` path.
**All three agents must use that same directory**, because they share one ledger.
Enable agent management on the server where required by the template guide. Review
the three agent cards, then select **Create all**. Importing saves a template;
running it creates agents/room and posts the kickoff. If someone wasn't found on the
messaging app, add them and resolve it before continuing.

[SCREENSHOT 2: Template form with three agent cards, bridge and shared directory.]

The agents use `addressing: anyone` to receive instructions from either person and
from one another. Keep the room limited to trusted participants. Don't enable bypass
permissions just to hurry the demo.

## 4. Check the room context

The kickoff asks the coordinator to check actual authors/message references, both
human accounts, all three agents' folder access and the shared rule. It creates
`promise-decisions` and `export-task` using documented room-document tools.
`signoff-rule` is created by the template. These are ordinary documents, not native
Decisions/Tasks/Rules objects. See [shared context](https://docs.switchagents.ai/switch-rooms/using/shared-context)
and the [payments-room guide](https://docs.switchagents.ai/switch-rooms/building/payments-room).

If an agent cannot resolve an actual author or reference, stop and fix that context.
Names typed inside a message do not prove who sent it. A missing tool is not permission
to pretend that a document was written.

[SCREENSHOT 3: Real room participants, kickoff and shared room documents.]

## 5. Ask, confirm and catch the bad export

Follow [DEMO.md](../DEMO.md) for the complete copyable messages. As requester, send:

> @promise-coordinator Create a customer CSV from all three sample orders. Include order_number and total only, in that order, with exactly three data rows. Never include email or internal notes. Ask me to confirm before starting. Only the designated data owner may approve it.

After the restatement, confirm the exact scope. The coordinator records revision 1
with the actual requester/ref and @mentions the builder. The initial export is
intentionally overbroad. The coordinator verifies it before permitting a fix. Errors
identify logical CSV row and column without printing a matched email value.

[SCREENSHOT 4: Actual addressed handoff and redacted failed verification.]

The builder fixes only the exporter, regenerates the file and verifies once. A fresh
run normally produces passing receipt `1:2`; use the actual displayed receipt.
Don't re-verify after sign-off, because every verification invalidates prior approval.

## 6. Try the wrong signer, then the right one

As Sam, send `@promise-coordinator approve 1:2` using the actual receipt. The code
must refuse: the requester cannot approve their own request. Priya then opens the
actual generated CSV, checks it, and sends the same instruction from her own account.
The coordinator records that actual author/ref and checks stored status.

[SCREENSHOT 5: Sam's refusal and Priya's actual account/reference on approval.]

This is a trusted-workstation workflow. The CLI accepts author/ref arguments; it
doesn't independently authenticate chat. Agent instructions require the real Switch
context and cannot prevent a filesystem owner from lying or editing the code.

## 7. Gate a draft, then change the request

The coordinator @mentions the sender with the approved receipt. The sender runs the
code gate and `sender.py draft`; it writes a local message draft, citing the receipt.
No external customer transport is configured. As Sam, now send the final confirmed
change from DEMO.md: add email, keep three rows, record only, don't rebuild or approve.

Recording revision 2 clears both verification and approval. The sender rechecks its
draft, gets exit 3, marks it retracted locally, and posts a visible retraction notice.
The old chat message remains visible. Email detection stays active even if a column
named email is requested; this scope change does not waive the privacy policy.

[SCREENSHOT 6: Revision 2, null approval and actual blocked sender/retraction notice.]

## What you have built

A shared room carries who asked, what was confirmed, who signed and each handoff.
Python checks columns, row shape/count, deny patterns and the current file hash.
Checks do not prove every value correct or catch every type of sensitive data.
Artifact edits are detected when checks run; there is no continuous watcher or
immutable snapshot. The result is a local prototype you can inspect and reproduce.

I used Wispr Flow to dictate explanation prompts and a draft introduction. The
[original scorecard](WISPR-USAGE.md) reports 105 words at capture time; those are
app-wide counters, not proof that the entire implementation was voice-built.
