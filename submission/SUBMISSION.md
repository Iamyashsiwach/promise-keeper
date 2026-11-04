# Submission worksheet — draft, not submitted

## Ready-to-use project description

**Name:** PromiseKeeper

**Track:** Best Business Workflow

**Tagline:** A changed request should never inherit an old approval.

**Short description:** PromiseKeeper brings a human, a coordinator agent, and a builder agent into a Switch room to turn an agreed customer export request into a verified artifact. The coordinator records exact columns and row scope, the builder produces and fixes the export, and deterministic checks reject results that violate the agreement. Human review refers to the latest verified version. Changing the request clears the earlier approval.

**What we demonstrated:** A deliberately overbroad CSV failed verification; agents handed the failure back through Switch and corrected the exporter; the human reviewed a passing receipt; a subsequent requirement revision cleared verification and approval. The synthetic data and ledger evidence are included.

**How Switch is used:** Switch Console connects two Codex-powered agents to a Mattermost-backed room. It carries the human confirmation, agent handoffs, tool activity, and results. Agent and room briefs plus the captured room template are included. Python/SQLite handles local evidence and version checks; this project does not implement a new agent model or claim to add these checks to Switch core.

**Limits:** Local trusted-workstation prototype. Caller-supplied reviewer label, not authenticated chat identity. Runtime verification checks columns, row shape/count and file hash, not source-value accuracy. No continuous monitoring, immutable artifacts, deployment, or automatic customer messaging.

## Links to fill after review

- [ ] Public repository URL
- [ ] Accessible video URL, checked without relying on the submitter's login
- [ ] Published blog URL, if entering Best Blog
- [x] Actual Wispr Insights scorecard saved at `media/wispr-insights.png`; usage scope in `WISPR-USAGE.md`
- [ ] Public #HowISwitch post URL, if entering that activity

## Submission gates

- [ ] Participant registration and eligibility confirmed by the participant
- [ ] Read the actual submission form and current rules; record additional required fields
- [ ] Public repository contents reviewed for secrets, credentials, private data, and stale claims
- [x] Room template exported from the live room; Switch round-trip check reports valid, server-specific inputs documented
- [x] Draft narrated walkthrough created from real screenshots and saved evidence
- [ ] Participant reviews video playback and approves the version to publish
- [ ] Clean extraction validation result reviewed in VALIDATION.md
- [ ] Participant reviews blog and social drafts before publication
- [x] Wispr use documented as project explanation/blog dictation; original scorecard attached, no whole-build voice claim
- [ ] Submit by November 7, 2026, 11:59 PM IST; internal target 8 PM IST

Sources checked November 5, 2026: [event](https://www.wemakedevs.org/hackathons/switch), [schedule](https://www.wemakedevs.org/hackathons/switch/schedule), [rules](https://www.wemakedevs.org/hackathons/switch/rules).

Multiple-track entry is allowed, but do not claim cumulative awards or assume one project can win both main workflow prizes. Track 3 issue #804 remains a separate optional effort; an assignment request alone is not a contribution.

## Social draft — not published

I built PromiseKeeper for the Flip the Switch Hackathon: a person and two AI agents work in a shared Switch room to produce a customer export, catch extra private columns, and verify the fix. Change the request, and the old approval is cleared.

Built with Switch, Codex and Python. Demo uses synthetic data; review currently happens through a local CLI.

#HowISwitch

Add reviewed repo/video links before publishing. Mention Wispr only if the usage claim is accurate.
