# PromiseKeeper — hackathon submission details

**Project:** PromiseKeeper  
**Tracks:** Best Business Workflow; Best Core Contribution (PR #1519)
**Tagline:** Catch risky AI work before it reaches a customer.

**Description:** PromiseKeeper helps teams release AI-generated work with confidence.
In a shared Switch room, a requester sets the scope, three specialist agents create
and check a customer export, and an independent data owner reviews the corrected
file. A release gate ties the local message draft to the current verified receipt.
When the request changes, the old approval clears and the sender retracts its stale
draft. The workflow is configurable for Slack or Discord; the recorded run is in
Discord and uses synthetic data.

**Switch:** Switch connects the real requester and reviewer with three role-specific
agents in one room. Shared instructions, room documents and @mentions carry scope,
handoffs and review. A parameterized template sets up the room and team. Python/SQLite
adds deterministic checks and a receipt-bound release gate.

**Evidence status:** The live Discord run shows separate requester and approver
accounts, a failed first check, a corrected passing receipt, refusal of requester
self-approval, independent approval, and automatic blocking/retraction after the
request changes. The concise video and transcript are linked below. The local gate is
designed for a trusted team workflow; higher-assurance deployments can add
authenticated identity and delivery integrations.

## Publish-ready links still required

- Repository: [PromiseKeeper](https://github.com/Iamyashsiwach/promise-keeper).
- Track 3 contribution: [Switch PR #1519](https://github.com/sandbox-quantum/switch/pull/1519).
- Demo: [actual Discord workflow (1:36)](promise-keeper-live-demo.mp4); [GIF](media/promise-keeper-live-demo.gif); [transcript](LIVE-DEMO-TRANSCRIPT.md). Upload the MP4 to YouTube or Loom and use its public/unlisted watch link in the form.
- Best Blog: [tutorial draft](BLOG-DRAFT.md). Publish it and paste its public link to enter the blog prize.
- Code with Wispr: [usage details](WISPR-USAGE.md); upload [the Insights scorecard](media/wispr-insights.png) in Track Details.
- #HowISwitch: add the public social post link to the form when posted.

## #HowISwitch draft — publish with the live demo link

I built PromiseKeeper: the sign-off layer for AI agents in team chat.

In one Switch room, three agents create and check a customer export. The requester
can't approve their own request. A separate data owner reviews the file and signs
its receipt. Change the request and the sender's code gate blocks the old draft.

Built with Switch and Python. Synthetic data; local draft, no customer delivery.

Repository: https://github.com/Iamyashsiwach/promise-keeper

Live demo: https://github.com/Iamyashsiwach/promise-keeper/blob/main/submission/promise-keeper-live-demo.mp4

#HowISwitch

## Finish checklist

- [ ] Complete the event form with project and contributor details.
- [x] Connect Discord and invite an actual second person as data owner; verify distinct author identities.
- [x] Run the template and full workflow with two human accounts, including refusal, approval and stale-draft retraction.
- [x] Record the live workflow video (1:36) and create a GIF.
- [x] Push the final video, GIF and README links to `main`; verify the remote `main` branch contains them.
- [ ] Publish the tutorial and #HowISwitch post; add their public links.
- [ ] Upload the Wispr scorecard so the submission is considered for Code with Wispr.
- [ ] Submit by **8 PM IST November 7, 2026** (internal target ahead of the stated deadline).

Check the current [event requirements](https://www.wemakedevs.org/hackathons/switch) and submission form before filing.
