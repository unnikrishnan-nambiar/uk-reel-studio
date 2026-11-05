---
name: panel-template
description: The approved uk_speaks.ai panel reel look (white default, dark Night Studio on request): static outlined hook, panel sliding over a rounded video card, full-screen animation cards, Inter captions.
---

# Panel reel template (approved on the Excel and PPT reels, Oct–Nov 2026)

## Hook (first ~4–5 s) — static, full face
- Only him, full screen, gentle 4 % push-in. Nothing animates.
- `templates/hook.html`: line 1 small white (76px), line 2 BIG RED `#ff2d2d` (140px, 18px stroke; lower `red_size` for long lines), line 3 small white. All white fill with thick black outline (`-webkit-text-stroke:14px #000; paint-order:stroke fill`).
- Spoken subtitles on the chest (y≈1420), 2 words at a time, white with black stroke.
- Examples he approved: "Still sending the / BORING EXCEL / to clients?" · "Stop making the / SAME AI SLIDES / Fix it free in 3 steps".

## Body — three layouts
1. **Full face**: grade 0.3, captions on the chest, BLACK text with a white outline (never gold/yellow), key word big with the small word above.
2. **Half panel**: panel slides DOWN from the top to y=1000 in 0.45 s (ease-in-out) while the video zooms out to 0.72 into a centred rounded card (R=44), bottom 36 px above the frame. Sides = panel colour (never blur). His head overlaps the panel edge by up to 110 px using ISNet person masks (fine hair, edge decontamination above the line). Captions black on the paper just above his head.
3. **Full-screen card**: opaque. White grid cards (scenes.html: links, download, upload, flow, before/after) with black captions at the bottom; dark `#0d0e11` "THE RESULT" card with no captions.

## White (default)
- Panel paper: `radial-gradient(90% 70% at 50% 40%,#fbfbfa,#f1f1ee 70%,#e9e9e5)` + faint blurred leaf shadow + 7 % noise.
- Mock-ups: clean light windows/cards, soft shadows `0 34px 70px rgba(0,0,0,.2)`, black pills with white text, yellow `#FFD43B` highlight chips.

## Dark (Night Studio) — `"theme": "dark"` in job.json
- Panel `radial-gradient(90% 70% at 50% 40%,#1b1f29,#12141a 65%,#0b0c10)`, no leaf shadow, 5 % screen noise.
- Panel captions white with lime `#C6FF3D` key words; pills lime with ink `#0E0F13` text; surfaces `#161A22`, lines `#2A2F3A`, ivory text `#F4F1EA`.
- Both overlay.html and scenes.html switch with `?theme=dark` (CSS under `html.dark`). Check hair at full resolution for halos on dark.

## Words on boxes (Nov 2026)
- Hook: ONE box (never stacked), whole hook on ~2 lines, 72px: yellow text on black (default) or black on yellow (`"box_color": "yellow"`). Set `"style": "box"` and `"box_text"` in job.json hook.
- Captions: one box per chunk, never stacked/side by side. Chunk with a `{KEY}` word → one yellow box `#FFD84D`, black text; plain chunk → one black box `#0d0d0d`, yellow text `#FFF06A`. Copy the CSS from `jobs/gemini-example/overlay.html`.
- Screen recordings he sends: full screen, 1.06→1.0 zoom-in, 0.15 s fades (`jobs/gemini-example/mk_broll_full.py`).

## Look rules
- Inter only. No italics. No branding. No emoji/stickers/bounce. English text only.
- Every visual is an animation (fade + 30–40 px rise + small blur clearing, 0.4–0.5 s; slides/cards scale in with a light overshoot). No raw screen recordings.
- Change layout every 3–7 s; hard switches happen under opaque cards.

## Checks before delivering
Contact sheet across the reel: hook clear of the eyes, captions never on hair/face, rounded corners visible, no black gaps during slides, panel content not clipped, hair overlap clean at full res. 1080×1920, 60 fps, −14 LUFS.
