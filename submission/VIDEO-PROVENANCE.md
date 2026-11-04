# Revised video provenance

Current files: `promise-keeper-v2.mp4` and `promise-keeper-walkthrough.mp4` contain the same revised 1:34 cut.

- This is an edited walkthrough of a completed run, not a new live screen recording.
- The request/confirmation and builder-handoff excerpts are cropped from the participant's supplied actual room screenshots in `media/`. Crops remove unrelated setup prose; message content has not been rewritten.
- Other panels are editorial illustrations of the workflow and saved ledger events in `../evidence/live-run.json`. They are not screenshots of a product dashboard or new software features.
- Narration uses the open-source Kokoro neural text-to-speech model with the `am_michael` preset, generated locally. It does not use a cloned participant voice or prove Wispr usage.
- [Voice runtime and model download source](https://github.com/thewh1teagle/kokoro-onnx). The runtime is MIT licensed; its README identifies model weights as Apache 2.0. Model weights and voice files are not included in this package.
- Output: 1920×1080, 30 fps, H.264/AAC, English subtitle track. `NARRATION-V2.md` contains the revised spoken script; `video-v2-timeline.json` has exact scene timings.
- The earlier Mac-system-voice cut was preserved outside the submission package as an intermediate version.
- Wispr Insights evidence is now saved separately in media/wispr-insights.png. Participant review, hosting, and submission remain outstanding.
