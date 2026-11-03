---
name: edit-reel
description: Turn a raw phone video in input/ into a finished uk_speaks.ai reel in the approved panel template. Use when he says edit the video, make the reel, new video uploaded.
---

# Edit a reel from a phone video

Read `CLAUDE.md` (house rules) and `.claude/skills/panel-template/SKILL.md` (the look) first. The worked example is `jobs/ppt-example/` — copy its structure.

## 1. Prep
```bash
./reel prep input/<video>.mp4 jobs/<slug>
```
Gives `jobs/<slug>/src60.mp4` (1080×1920, 60 fps), `words.json` (word times; the ASR writes Malayalam/Devanagari script for Manglish, so read it phonetically), `silences.json`, suggested speech segments and `sheet.jpg`. Open `sheet.jpg` to see framing (where the head top is).

Write down the story in English, sentence by sentence, with source times. If a phrase is unclear, ask him rather than guessing.

## 2. Plan the edit (job.json)
- **hook**: first sentence (a, b in source seconds). It's a separate static full-face clip.
- **body_segs**: the rest, split at silences, dead air > 0.3 s removed, ~0.06 s padding. Drop false starts and repeats.
- **Layout timeline (body time)** — mix all three:
  - full face: first ~1 s of the body, the "try this"/step moments, the CTA and the end;
  - half panel (z=1): explanations with a visual (before/after, lists of links, flows);
  - full-screen cards: the main demo moments (opaque, they cover everything; z underneath can switch instantly).
- **tr**: `[t0, t1, from, to]` — panel down `[t, t+0.45, 0, 1]`, back to face `[t, t+0.45, 1, 0]`; under a full card use an instant switch `[t, t+0.01, …]`.
- **yo**: vertical offset of the zoomed video so his head top sits ~70–90 px ABOVE the panel edge (y=1000): `yo ≈ 920 − head_top_px × 0.72`. Too small cuts the hair flat; too big leaves no overlap.
- **panel_ranges**: body times where z>0 (+0.1 s margin) — masks are made only there.
- **cards**: full-screen scenes from `templates/scenes/scenes.html` (`links`, `download`, `upload`, `flow`, `ba`) with `s0` (scene start time), `speed` and `scale` (0.85 leaves room for captions at the bottom). New scene types go into scenes.html with the same `frame(t)` pattern.
- **caps**: `[source_time, "text {KEY}"]`, 1–2 words, faithful translation.

## 3. Write overlay.html
Copy `jobs/ppt-example/overlay.html` and change the content. It has two passes:
- `pass=P` — the panel (1080×1000 paper). Content lives in y 190–740; captions on the panel sit just above his head (≤ 870).
- `pass=T` — full-screen cards made in HTML (e.g. a `.md` file typing, a dark "THE RESULT" card) + captions.
Keep `LAY` (layout per body time) in sync with `tr` and `cards` so captions get the right style/position: `f` face (white, yellow key word on the chest), `l` panel (black above head), `w` white card (black at the bottom), `d` dark card (no captions).
Slides/images go in `templates/scenes/img/`.

## 4. Hook — he must confirm
Write 4–6 options in the 3-line format (small / BIG RED / small) that match his first sentence. Score each: `./reel score "Stop making the SAME AI SLIDES Fix it free in 3 steps"`. Aim ≥ 90 ("Stop" + a concrete payoff, number, "free/only" tension). Ask him with AskUserQuestion, recommended first, scores in the labels. Use his exact pick. `red_size` 140 by default; lower (≈118) when the red line is longer than ~12 characters. Check: `./reel hookpreview jobs/<slug>` → `hook_preview.jpg`.

## 5. Preview, then render
```bash
./reel cut jobs/<slug>
./reel masks jobs/<slug>            # slow: ~1.5 s per frame per worker
./reel preview jobs/<slug> 0.5,2,5,9,13,18,24,30   # renders just those frames → jobs/<slug>/test.jpg
```
Look at test.jpg: hair over the panel edge (no flat cut, no halo), captions never on hair/face/eyes, panel content not clipped, cards readable. Fix and re-preview. Then:
```bash
nohup ./reel all jobs/<slug> > jobs/<slug>/all.log 2>&1 &
```
(`all` skips overlay frames that already exist — delete `ovP/ovT/ovC` after changing overlay.html.) Poll the log.

## 6. Deliver
Check `output/<name>-sheet.jpg`. Tell him: master `output/<name>.mp4`, phone copy `output/<name>-share.mp4`, which visuals are illustrative, and anything you guessed in the translation.
