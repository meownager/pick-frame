# PickFrame: PRD

## Problem
A 2-second clip or photo burst produces 10-20 near-identical frames. Picking the best one by hand is slow, and existing tools pick without saying why.

## Goal
Pick the best frame from a mobile-captured clip or photo burst, and explain why every other frame lost. V1 processes on a CPU laptop, offline. V2 moves the full pipeline into a mobile app.

## Users
- Primary: one person capturing a selfie or portrait clip or burst on their phone.
- Secondary: anyone with a phone burst of single-subject photos.

## Pipeline
| Stage | Method | Output |
|---|---|---|
| Ingest | Clip or burst, uniformly sampled to 10-20 frames | Ordered frame list |
| Filter | Laplacian variance (sharpness), histogram clipping % (exposure) | Pass/reject + reason per frame |
| Score | MUSIQ (pyiqa, KonIQ weights); MediaPipe Face Landmarker blendshapes: eyeBlinkLeft, eyeBlinkRight, mouthSmile | Per-frame feature vector |
| Rank | Weighted sum, weights in config, each with written rationale | Ordered ranking |
| Explain | Winner, per-frame score table, one-line reason per loser | UI + text |

## Requirements
- R1: Accept a phone-captured clip (about 2 s) or photo burst.
- R2: Every rejected or losing frame gets a one-line, human-readable reason.
- R3: Ranking weights live in config, not code.
- R4: Fully offline after first setup. All model weights cached locally.
- R5: CPU only. Python 3.11.
- R6: End-to-end latency at or under 3 s per burst of up to 20 frames.
- R7: Downscale every frame to a configured max side (default 1024 px) at ingest, before any filter or model, to cut memory, CPU and power use.

## Success metrics and ship gate
Eval set: 30 bursts, each labeled with one human best pick. Bar is fixed before the eval runs.

| Metric | Ship bar |
|---|---|
| Top-1 agreement | at least 40% (12/30) |
| Top-3 agreement | at least 70% (21/30) |
| Top-1 vs best baseline | at least 10 points higher |
| Latency, p95 | at most 3.0 s per burst |

Baselines: random (expected top-1 about 1/N, top-3 about 3/N), sharpness-only, MUSIQ-only.

Rationale:
- Adjacent burst frames are often near-identical, so top-1 is noisy. Top-3 is the main quality signal.
- Beating MUSIQ-only proves the face signals and ranking add value over a single quality model.
- 3 s keeps the demo feeling live.

If the bar is missed: report the result as is, log the failure modes in DECISIONS.md, and do not tune weights on the eval set.

## Future scope
- V2: native mobile app running the pipeline on device
- Training or fine-tuning models
- Frame fusion or synthesis
- Hosted demo
- Group photos (more than one face)

## Risks
| Risk | Mitigation |
|---|---|
| Weights download on first run and break offline | Pre-download and cache weights; add a check step at startup |
| MUSIQ too slow on CPU | Resize input before scoring; measure per-frame latency first |
| No face found | Score falls back to quality only; the reason says no face was detected |
| Phone formats (HEVC video, HEIC photos) fail to decode in OpenCV | Add HEIC support via pillow-heif; test HEVC decode early; fall back to H.264 capture setting |
| Eval overfit | Freeze weights before labeling is finished; no tuning on the eval set |

---
Author and owner: Syeda M.
