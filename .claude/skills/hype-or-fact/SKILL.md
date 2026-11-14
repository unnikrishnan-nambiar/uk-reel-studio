---
name: hype-or-fact
description: The "HYPE or FACT?" reel template - he tests another creator's AI claim on camera with a screen recording. Use when he says hype test, hype or fact, hypebust, or sends a reference reel plus his test footage.
---
# HYPE or FACT? template

Job folder to copy: `jobs/hof/` (first episode: "Claude deleted me from the internet", Nov 2026).

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
