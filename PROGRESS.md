# Build status — November 5, 2026

## Completed

- Installed official Switch Console 0.40.1 on this Apple silicon Mac.
- Started Docker Desktop and verified server version 29.8.2.
- Started a local Switch server; UI reports version 0.31.0 and Running.
- Connected bundled Mattermost; created the `promise-keeper` channel with `promise-coordinator` and `promise-builder`.
- Registered both agents with Codex (reported Ready by Switch), project working directory, role instructions, default owner/owner-agent addressing, and permission bypass left off.
- Implemented local ledger, verifier, sample exporter, agent briefs, and demo instructions.
- Eight ledger regression tests pass. CLI smoke check rejects the deliberately flawed export and refuses approval of its failing receipt.
- Sent a setup-only readiness check through the actual Mattermost room. The coordinator completed a real 24-second session with six tool calls, read the project files, and replied with the actual CLI syntax and limitations. No agreement, export, approval, or code edit was requested in that check.
- Completed the first customer workflow: human-confirmed revision 1, coordinator-to-builder handoff, actual overbroad export, failed receipt `1:1`, exporter correction, successful receipts `1:2` and `1:3`, and local reviewer approval of receipt `1:3`.
- Confirmed the next requirement in Switch: revision 2 adds email. The ledger cleared verification and approval; the exporter and artifact still have two columns. Verified this directly in SQLite and checked that all eight tests still pass.
- Saved the six ledger events, with IST timestamps and local artifact paths made relative, in `evidence/live-run.json`.

## Next

1. Participant reviews the prepared 1:34 walkthrough, blog, submission description, and source package.
2. Wispr Insights scorecard supplied and saved; project explanation/blog dictation scope documented in submission/WISPR-USAGE.md.
3. Confirm registration and inspect the actual authenticated submission form for additional fields.
4. Obtain publication authorization, then create the public repository, host the video, and publish the reviewed blog/social material.
5. Complete the submission before the deadline. No external publication or submission has occurred yet.

## Not complete

The first live workflow demonstration is complete. The actual room template has been exported and its Switch round-trip check reports valid. A 1:34 narrated walkthrough with English subtitles, blog draft, video script, submission description, social draft, isolated rehearsal script, and ninth test for the actual exporter have been prepared. The rehearsal script refuses existing destinations and preserves the live ledger. All nine tests pass from a clean ZIP extraction. A review ZIP excludes local databases and caches; see submission/VALIDATION.md.

Still incomplete: participant review, authenticated chat approvals, public repository and video hosting, blog/social publication, and hackathon submission. The video uses real supplied chat screenshots and saved ledger evidence with machine narration; it is not a new live recording or proof of Wispr usage. No reward is guaranteed.

Wispr update: participant supplied an original Insights scorecard showing 105 total words and two AI prompts. Saved unedited with a limited usage statement; no claim that the whole build was dictated.
