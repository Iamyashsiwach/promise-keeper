# Validation of the win branch

## Completed checks

- Python standard library only. No new packages installed.
- A fresh temp source copy was assembled from Git-tracked and new nonignored files,
  without .git or runtime data. `python3 -m unittest -v` passed **25 tests** there.
  [Full captured output](TEST-OUTPUT.txt) is unedited output of that clean-copy run.
- A separate rehearsal was prepared from that copy. The seeded exporter deliberately
  failed its projection regression. After copying the corrected exporter, its entire
  25-test suite passed. This verifies both the intended failure and the repair path.
- Local-only integration exercise used explicitly fictional `sam-test`/`priya-test`
  identities and `local-rehearsal/...` references: failed `1:1`, passed `1:2`, rejected
  self-approval, independent approval, gate/draft, revision 2, blocked/retracted draft.
  This was executed against temporary files; it is not a fabricated live chat run.
- Rehearsal isolation tests verify new sender/brief/helper files are included,
  historical evidence matches, no ledger/credentials/Git history is copied, and an
  existing destination is refused without resetting its marker file.
- Final privacy review also covered denied content in a header, even if that header
  was requested. The error identifies header row/column without echoing the value.
- [Switch template validation](SWITCH-VALIDATION.md): no lint errors/warnings, three
  agent slots, room schema and interpolated kickoff parsed by installed Switch runtime.
- Local Markdown targets resolve. Git diff whitespace check passes.

Historical `evidence/live-run.json` SHA256 before and after:
`8794b60dd59e07c422d4e92492360d61cfde46d6f6ed561f0dd4f175ff08118e`.
It is unchanged from the pre-work commit. The local live ledger was not reset.

## Remaining integration checks

Fresh-server provisioning, real Slack/Discord account mapping, coordinator-owned
room-document writes, the genuine two-human/three-agent live run, and a new live
recording are NOT established by these tests. Follow [DEMO.md](../../DEMO.md) and
[the import checklist](SWITCH-VALIDATION.md). The old video is historical only.
