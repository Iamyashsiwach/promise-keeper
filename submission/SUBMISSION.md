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

**Evidence status:** The actual Discord run used separate requester and approver
accounts. It recorded a failed first export, a corrected passing receipt, refused
requester self-approval, independent approval, a local draft, and a changed request
that cleared approval and caused the sender gate to retract the draft (exit 3). The
new recording is linked below. The CLI trusts Switch-supplied identity/reference on
a shared machine; this is a collaborative workflow demo, not an adversarial security
boundary. The old `evidence/live-run.json` is from an earlier single-human/two-agent
run and is not the evidence for the current workflow.

## Publish-ready links still required

- Repository: [PromiseKeeper](https://github.com/Iamyashsiwach/promise-keeper).
- New live video: [actual Discord workflow (1:36)](promise-keeper-live-demo.mp4); [GIF](media/promise-keeper-live-demo.gif); [transcript](LIVE-DEMO-TRANSCRIPT.md). These assets are pushed on `main`.
- Tutorial: [BLOG-DRAFT.md](BLOG-DRAFT.md) — pending real screenshots and publication; no published article URL yet.
- Wispr: [original usage evidence](WISPR-USAGE.md) and [scorecard](media/wispr-insights.png).
  No claim that all coding or the earlier chat run used dictation. Confirm current
  event side-track requirements before filing.
- #HowISwitch post: pending publication; no public URL yet.

## #HowISwitch draft — publish with the live demo link

I built PromiseKeeper: the sign-off layer for AI agents in team chat.

In one Switch room, three agents create and check a customer export. The requester
can't approve their own request. A separate data owner reviews the file and signs
its receipt. Change the request and the sender's code gate blocks the old draft.

Built with Switch and Python. Synthetic data; local draft, no customer delivery.

Repository: https://github.com/Iamyashsiwach/promise-keeper

Live demo: https://github.com/Iamyashsiwach/promise-keeper/blob/main/submission/promise-keeper-live-demo.mp4

#HowISwitch

## Ordered finish checklist

- [ ] Confirm current event rules/form requirements and participant registration.
- [x] Connect Discord and invite an actual second person as data owner; verify distinct author identities.
- [x] Run the template and full workflow with two human accounts, including refusal, approval and stale-draft retraction.
- [x] Record the live workflow video (1:36) and create a GIF.
- [x] Push the final video, GIF and README links to `main`; verify the remote branch points to commit `0df3a8b`.
- [ ] Publish tutorial and #HowISwitch post; record the working public URLs here.
- [ ] Attach the actual Wispr scorecard and an accurate usage description if entering.
- [ ] Submit by **8 PM IST November 7, 2026** (internal target ahead of the stated deadline).

Check the current [event requirements](https://www.wemakedevs.org/hackathons/switch) and submission form before filing.
