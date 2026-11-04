# I built a Switch workflow where a changed request cancels an old approval

An AI agent can finish a task and still produce the wrong result. PromiseKeeper brings people and agents together to check that the work matches the agreed requirements.

In my demo, a builder agent creates a customer spreadsheet, and a coordinator verifies its columns and row count. A person reviews the verified file. If the requirements change, the old approval is cleared, and the updated request needs fresh verification and review.

I wanted to connect three things that are easy to separate during a task: what a person requested, what an agent produced, and which exact result the person reviewed.

The demonstration uses three synthetic orders. I requested a customer CSV with two columns, `order_number` and `total`, excluding email addresses and internal notes. The initial exporter deliberately included all four fields. That planted mistake made the check visible and repeatable; it was not a real customer data incident.

## The team in the room

I used Switch Console with a local Switch server, bundled Mattermost, and two agents powered by my existing Codex provider.

- `promise-coordinator` clarifies the request, records the agreed columns and row count, and checks the evidence.
- `promise-builder` runs and fixes the exporter.
- I confirm the requirement and review the passing artifact.

Both agents work from the project folder. Their agent briefs and room instructions are included in the repository. Switch carries the actual requests and agent handoffs in a shared conversation; the agents invoke a small Python CLI for the evidence checks. It is not a custom Switch protocol implementation or a standalone chatbot masquerading as a room integration.

## The first live run

The coordinator asked me to confirm the exact column order and three-row scope before recording revision 1. It then addressed the builder through Switch. The builder ran the original exporter and left the result untouched for the first check.

The exporter exited successfully. Verification did not:

```text
Expected columns ['order_number', 'total'];
found ['order_number', 'total', 'email', 'internal_notes'].
```

That failed check received receipt `1:1`. The coordinator sent the failure back to the builder, which changed the exporter to use only the two approved columns and regenerated the CSV. Builder verification passed as `1:2`; the coordinator's verification produced the latest receipt, `1:3`.

The resulting file was small enough to inspect directly:

```csv
order_number,total
DEMO-101,49.00
DEMO-102,75.50
DEMO-103,12.00
```

I recorded my local review against receipt `1:3`. Then I changed the requirement: include email as the third column, keeping three rows. I explicitly asked the agent not to rebuild or approve anything yet.

The coordinator recorded revision 2. Verification and approval became `null`, and the status became `needs-verification`. The older two-column CSV was left alone. Approving the earlier result did not approve the new request.

The repository includes the six recorded ledger events, with timestamps in IST and local artifact paths made relative. They document the run but are not an independent identity or security audit.

## What the Python component does

The CLI stores agreement revisions, verification receipts, and review records in SQLite. Verification reads the CSV bytes once, checks ordered column names, row structure and count, and hashes those same bytes. Approval requires the latest passing receipt and checks that the artifact still matches it.

A new agreement clears verification and approval. Every new verification creates a new receipt and clears prior approval. Checking status also detects whether the verified file is missing or changed.

There are nine automated checks: eight ledger regression tests and one test of the corrected exporter against the synthetic source values. The runtime verifier itself does not compare cell values with source orders; that distinction matters.

## Reproducing the setup

Start with the [Switch installation guide](https://docs.switchagents.ai/switch-rooms/getting-started/install-switch-console) and [quickstart](https://docs.switchagents.ai/switch-rooms/getting-started/index). For this setup, Docker runs bundled Mattermost. Register the two agents, select the project folder as their working directory, and apply the included role and room instructions.

The room template in the project was captured from the actual working room. It names existing agents; it does not install them. Review the bridge, participant names, and parameters before importing on a different server.

Run `python3 -m unittest -v` to check the corrected project. To rehearse the initial failure, use `scripts/prepare_rehearsal.py` to create a new copy with the deliberately overbroad exporter. It does not copy or erase the completed live ledger.

## Where I used Wispr Flow

I used Wispr Flow to dictate a request for a simpler project explanation and a draft of this introduction, then refined the wording with my coding assistant. The supplied Insights scorecard shows 105 total dictated words and two AI prompts at capture time. Those are application-wide counters, not a claim that the entire build was done by voice. I also used typed and pasted commands. The demo video's neural narration was generated separately and is not Wispr evidence.

## What remains limited

This is a trusted-workstation prototype. The reviewer label is caller-supplied, and review currently happens through a local CLI, not authenticated chat approval. Agents' instructions are working conventions rather than filesystem security boundaries. The database is not tamper-resistant against someone who can edit it.

There is no continuous file watcher or immutable artifact store. Changes are detected when the relevant CLI command runs. The demo creates a local file; it does not deliver a file to a customer or deploy an application.

For a production version, I would add authenticated review events, immutable artifact storage, and verification of the actual data values before expanding to more workflows.

The useful result of this build is concrete: the room records the request, the agents do and check the work, and a later request cannot silently inherit an earlier approval.

---

Editorial checklist before publication: add the reviewed public repository URL, embed actual room screenshots or the recorded walkthrough, and review the usage description against the original Insights screenshot. This draft has not been published.
