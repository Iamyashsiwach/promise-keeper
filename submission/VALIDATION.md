# Validation — November 5, 2026

- Clean ZIP extraction: nine tests pass using Python's standard library.
- Corrected exporter: exact two-column projection matches the three synthetic source orders.
- Rehearsal preparation: creates a separate overbroad starting exporter, refuses existing destinations, copies no live ledger or credentials, and leaves the original ledger hash unchanged.
- Room template: exported from the actual Switch room; Switch UI round-trip check reports valid with three parameters. Fresh-server import/run is not yet tested.
- Video: 1920×1080 H.264, AAC audio, approximately 94 seconds, 30 fps, with a local neural preset voice; English subtitle track included. Representative frames inspected. It is a narrated walkthrough of real supplied screenshots and saved evidence, not a new live screen recording.
- Packaging: excludes .local, SQLite files, Python caches, and Git metadata. A scan for common private-key and API-token patterns found no matches; this is not a comprehensive security audit.
- Runtime remains a trusted-workstation prototype; local reviewer labels are not authenticated chat identity.

No public hosting, publication, or hackathon submission has been performed. Participant review and actual Wispr scorecard are still needed.

V2 media checks: full decode completed without errors; representative output frames inspected; AAC narration has measurable signal and no clipping (measured peak -4.4 dBFS). This is a technical check, not a claim of subjective voice approval.
