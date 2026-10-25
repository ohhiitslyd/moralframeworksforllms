# Frozen eight-setting pressure pack

These four files are exact copies from the harness parent of this merge. Their
source commit and SHA-256 hashes are recorded in `PROVENANCE.json`. They describe
792 scenarios and 47,520 planned experimental episodes, rather than the new
five-setting design's 495 scenarios and 29,700 episodes.

The original single-condition `07-collusion-pressure-scenarios.json` is also
preserved here for historical reference and compatibility testing.

This is a historical reference, not a replacement for a running study's frozen
manifest. Preserve each results folder's own manifest, prompts, IDs, execution
history and source revision. The selected 72-scene study uses a separate pack;
its pack and existing result snapshots are also retained by this merge.

The current runner follows the five-setting branch's run-ID format. The older
harness used `S001-L1-W-W-s1-watched`; the new design uses
`S001-L1-W-W-w-s1`. Scenario numbers may also refer to different scenes. Do not
resume old results with the new runner or substitute this archive for a run's
actual manifest. Keep the existing collection checkout until its run finishes.

To inspect the exact older runner, use the source commit in `PROVENANCE.json`
and path `lying_harness/pressure.py`. Do not rebuild this archive with the
current five-setting pack builder.
