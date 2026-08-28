# Demo production sources

The public demo is available at https://youtu.be/hyHVu464XAM.

This folder keeps the reviewed 1920×1080 browser captures, narration text,
architecture frame, edit plan, and deterministic FFmpeg build script. Generated
voice, ASR timing, caption images, intermediate clips, and final video files live
under the ignored `output/` directory.

The published build was verified as:

- 2:17 total duration, below the competition's 3-minute limit;
- 1920×1080 H.264 at 30 fps and `yuv420p`;
- mono AAC narration at 24 kHz;
- approximately -16 LUFS integrated loudness;
- burned-in English captions generated from a post-synthesis ASR pass.

`build_video.py` expects `output/narration.wav` and
`output/narration_asr.json`. It is production tooling for this submission, not a
runtime dependency of ScriptProof.
