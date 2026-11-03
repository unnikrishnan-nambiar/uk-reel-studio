# uk-reel-studio — reel editor for @uk_speaks.ai

This project turns a raw talking-head video from Unnikrishnan's phone into a finished Instagram reel in his approved panel template. It runs on his Intel Mac. He talks Manglish (Malayalam + English); every on-screen word is short, clean English.

## When he says "edit the new video" (or drops a video and says anything like it)
Follow `.claude/skills/edit-reel/SKILL.md` step by step. Short version:
1. Find the newest video in `input/` (also check the iCloud folder `~/Library/Mobile Documents/com~apple~CloudDocs/Reel Inbox/` if it exists). Copy it into `input/` if it came from iCloud.
2. `./reel prep input/<video> jobs/<slug>` → transcript, silences, contact sheet. Read the transcript and `sheet.jpg`, understand the story.
3. Write `jobs/<slug>/job.json` and `jobs/<slug>/overlay.html` (start from `jobs/ppt-example/`).
4. Write hook options, score them with `./reel score "<hook>"`, and ASK HIM to pick (template + score in the question). Never render the final hook without his pick.
5. `./reel preview jobs/<slug> t1,t2,...` and look at `test.jpg` before the full render.
6. `./reel all jobs/<slug>` (long: run in the background with `nohup … &` and poll), then check `output/<slug>-sheet.jpg`.
7. Tell him where the files are: `output/<name>.mp4` (master) and `output/<name>-share.mp4`.

## House rules (all approved by him — never break them)
- **Template:** white panel template by default (`theme: "white"`); dark Night Studio version only when he asks (`theme: "dark"`). See `.claude/skills/panel-template/SKILL.md`.
- **One font: Inter** (800 for titles, 600/700 small). No italics, no serif, no other fonts.
- **Hook:** static, full face, at the top from frame 0. 3 lines with thick black outline: small white line / BIG RED key words / small white line. Hook text matches what he says in the first sentence. Score ≥ 90 with `./reel score`, he confirms in chat.
- **Animations, never raw screen recordings** in the reel. Mock-ups are clean HTML (windows, chats, slides, diagrams).
- Mix three layouts: full face ↔ half panel (panel slides down, video zooms out into a rounded card, his hair overlaps the panel) ↔ full-screen animation cards. Change layout every 3–7 s.
- Sides around the video card use the panel colour (never blur). Rounded corners (R=44).
- English captions, 1–2 words per chunk, key word in `{BRACES}`. Translate his Manglish faithfully. **Never invent claims, numbers or results.** Illustrative mock-ups (sample decks, sample chats) are fine but tell him in the final message.
- No branding (no handle, logo, watermark, end card). No emoji, stickers or bouncy ad effects.
- Output 1080×1920, 60 fps, −14 LUFS. No covers unless he asks.
- Recording tip to give him when framing is tight: sit a little further back with space above the head.

## Content and ideas
- `ideas/` has his outlier research, 7-day "Hype Test" plan, reel scripts and hooks. Use them when he asks what to post next or to script a reel (skill `content-ideas`).
- Every reel ends with a comment-keyword CTA ("Comment PPT"). The matching free guide lives on his website repo `unnikrishnan-nambiar/uk_speaks.ai` under `g/<keyword>/` (skill `guide-page`).

## Commands
`./reel prep|cut|masks|overlay|preview|test|comp|hookpreview|hook|join|all|score` — see `engine/reel.py` header. Set `REEL_WORKERS=3` on a laptop with 6+ cores.
