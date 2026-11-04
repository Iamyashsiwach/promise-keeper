# Submission worksheet — new workflow not yet submitted

**Project:** PromiseKeeper  
**Target:** Best Business Workflow  
**Tagline:** The sign-off layer for AI agents in team chat.

**Description:** A requester, an independent data owner and three agents collaborate
in a Switch room to create a customer export. The coordinator records confirmed
scope and actual chat references; the builder produces a deliberately flawed export,
then fixes it after a redacted check fails. The requester cannot approve their own
request. The designated data owner reviews the file and signs its current receipt.
The sender's code gate allows a local message draft only against current approval.
A changed requirement revokes approval and triggers a visible draft retraction.

**Switch:** Real room participants/authors, shared instructions and room documents,
agent-to-agent @mentions, and a parameterized three-agent/room/kickoff template.
Python/SQLite supplies deterministic checks and a receipt-bound gate. Records called
rule/decision/task are ordinary room documents. No external customer delivery.

**Evidence status:** Core and sender tests pass; the template has offline Switch
lint/parser validation. A fresh-server import and new two-human live run are still
required. The older movie and `evidence/live-run.json` demonstrate the earlier
single-human/two-agent workflow only. Do not submit them as proof of independent
chat approval or the new sender. CLI trusts supplied identity/ref on a shared machine.

## Publish-ready links still required

- Repository: https://github.com/Iamyashsiwach/promise-keeper — currently older main;
  publish the reviewed `win` changes only when authorized. No push in this task.
- New live video: TODO — record [DEMO.md](../DEMO.md), <=2 minutes, then update README's video/GIF placeholders.
- Tutorial: [BLOG-DRAFT.md](BLOG-DRAFT.md) — add real screenshots and publish; URL TODO.
- Wispr: [original usage evidence](WISPR-USAGE.md) and [scorecard](media/wispr-insights.png).
  No claim that all coding or the earlier chat run used dictation. Confirm current
  event side-track requirements before filing.
- #HowISwitch post URL: TODO.

## #HowISwitch draft — publish after the new live run

I built PromiseKeeper: the sign-off layer for AI agents in team chat.

In one Switch room, three agents create and check a customer export. The requester
can't approve their own request. A separate data owner reviews the file and signs
its receipt. Change the request and the sender's code gate blocks the old draft.

Built with Switch and Python. Synthetic data; local draft, no customer delivery.

[ADD REVIEWED REPO LINK] [ADD NEW LIVE DEMO LINK]

#HowISwitch

## Ordered finish checklist

- [ ] Confirm current event rules/form requirements and participant registration.
- [ ] Connect real Slack/Discord and invite an actual second person as data owner.
- [ ] Import/run the template on a fresh Console server; confirm documents and identities.
- [ ] Rehearse DEMO.md from a new isolated copy; retain actual outcomes.
- [ ] Record the new live video; add real screenshots to tutorial and README GIF.
- [ ] Review changes, publish the new repository version when authorized, verify anonymous access.
- [ ] Publish tutorial and #HowISwitch post; replace every TODO with a working public URL.
- [ ] Attach the actual Wispr scorecard and an accurate usage description if entering.
- [ ] Submit by **8 PM IST November 7, 2026** (internal target ahead of the stated deadline).

The user's four requested criteria guide this review; equal weights and README/video-only
judging are not asserted here as independently verified event rules. See the actual
[event page](https://www.wemakedevs.org/hackathons/switch) before submitting.
