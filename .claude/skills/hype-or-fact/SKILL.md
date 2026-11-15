---
name: hype-or-fact
description: The "HYPE or FACT?" reel template - he tests another creator's AI claim on camera with a screen recording. Use when he says hype test, hype or fact, hypebust, or sends a reference reel plus his test footage.
---
# HYPE or FACT? template

Job folder to copy: **`jobs/hof3/`** (current approved layout, Nov 2026). `jobs/hof/` is the older busy version, `jobs/hof2/` the first minimal one.

## Current approved layout (hof3)
- Hook: 0.3 s of him, then one black/yellow hook box at the top (3 lines). The subject reel plays as a big yellow-framed card on the left (560x996) for ~6 s with its audio while he listens; label under it: `Credits: @handle` (never "viral video"). Then his line.
- Test: big `☐ HYPE OR ☐ FACT` row above his head (top 380, 78 px text, 76 px boxes) - he asked for it bigger, keep it at least this size. Yellow-framed screen card (1032 wide) at the bottom.
- Malayalam subtitles (Noto Sans Malayalam + Inter for English), one box per chunk, words rise in one by one, slow. Above his head during the test, low during the hook.
- End: HYPE ticked, FACT struck, `For India: HYPE`, then `Comment KEYWORD for the guide`.
- Screen material: blurred clips via `jobs/hof/mk_clips.py` (OCR blur every frame, 3+ digit numbers, crop the usage bar), then an OCR scan of the output before sending.

## Layout (fixed, reuse as is)
- **Heading, always on:** `HYPE or FACT?` pill at the top (yellow HYPE box, white FACT box). At the verdict, the winner gets a green tick and the loser is struck through.
- **Claim:** 2-3 s of the reference reel full screen, `Reel: @handle` chip, "THE CLAIM" card with their exact line. Keep their clip short.
- **Ask / go:** his reaction clip with "Does this really work?", then "LET'S TEST IT" stamp on the keyboard pull.
- **Test steps (split):** top 900 px dark panel = screen card (blurred still, slow pan, yellow highlight sweep) + `STEP n` chip + yellow quote card with the exact line Claude or the guide said; bottom 1020 px = his camera (crop y 450-1470 of a 1080x1920 clip).
- **Fix cards (full):** one big white card at a time with a yellow number tile, progress dots.
- **Verdict:** `MY VERDICT` chip + huge HYPE (or FACT) stamp + small qualifier ("for India"). Hold to the end.
- Captions: one box per chunk, never stacked. Chunk with a key word = black on yellow; plain = yellow on black. Inter only.

## Files
- `build_body.py` - SEGS list: [source, in, out, full|split, scene, captions(src_t, text)]. Cuts body.mov + timeline.json.
- `mk_stills.py` - screen stills: crop, OCR blur (phone, email, friend names, cities, RYX), highlight boxes. Always check `stills/check.jpg`.
- `overlay.html` - the template. Per-episode text lives in `QT` (quotes), `LBL` (step chips), `IND` (fix cards), the claim line, verdict word.
- `mk_sfx.py`, `render.py test t1,t2` (check sheet), `render.py full` (overlay + sfx + loudnorm -14 -> hof.mp4).

## Rules
- Verdict is about the claim, never the person. Never call another creator fake.
- Blur every personal detail except his own name. Crop Claude's sidebar (chat titles) and usage bars out.
- Quotes on cards must be exact text from the screen. No invented results.
- Output 1080x1920, 60 fps, -14 LUFS.
