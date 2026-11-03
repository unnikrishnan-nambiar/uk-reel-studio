# uk-reel-studio

Your reel editor as a Claude Code project. Drop a raw phone video in, tell Claude "edit the new video", and it cuts, translates, animates and renders the reel in your approved panel template (white, or dark on request), with a static outlined hook you pick from scored options.

## One-time setup (Intel Mac)
1. Install Claude Code: https://docs.claude.com/en/docs/claude-code (needs a Claude Pro or Max plan).
2. Open **Terminal** and run:
   ```bash
   git clone https://github.com/unnikrishnan-nambiar/uk-reel-studio.git ~/uk-reel-studio
   cd ~/uk-reel-studio
   ./setup.sh
   ```
   It installs ffmpeg, Python 3.11, Chromium for rendering, the speech model (~1 GB, handles Malayalam + English) and the hair-cutout model. Takes 10–20 minutes the first time.

## Every reel
1. **Get the video onto the Mac** — any of:
   - AirDrop it, then move it into `~/uk-reel-studio/input/`
   - iPhone Files app → save to **iCloud Drive › Reel Inbox** (created by setup)
2. In Terminal:
   ```bash
   cd ~/uk-reel-studio
   claude
   ```
   and say: **"edit the new video"**.
3. Claude reads the transcript, plans the layouts, shows you 4–6 hooks **with scores** and asks you to pick, shows a preview sheet, then renders.
4. Finished files: `output/<name>.mp4` (master, 1080×1920, 60 fps) and `output/<name>-share.mp4` (smaller, for AirDrop to the phone).

Rendering a 40-second reel takes roughly 30–60 minutes on an Intel Mac (hair cut-outs and 60 fps frames are the slow part). Keep the laptop plugged in and awake.

## What's inside
| Path | What |
|---|---|
| `CLAUDE.md` | House rules Claude follows (fonts, hook style, no branding, etc.) |
| `.claude/skills/` | edit-reel workflow, panel template look, hook writer, content ideas, guide pages |
| `engine/reel.py` | The pipeline (`./reel prep / cut / masks / overlay / preview / comp / hook / join / all / score`) |
| `templates/hook.html` | Static 3-line outlined hook (small / BIG RED / small) |
| `templates/scenes/scenes.html` | Full-screen animation cards: template websites, download, upload to Claude, chat flow, before/after |
| `jobs/ppt-example/` | The PPT reel as a worked example (job.json + overlay.html) |
| `ideas/` | Outliers, 7-day Hype Test plan, scripts and hooks |

## Recording tips
- Sit a little further from the phone with space above your head: the head-over-panel effect needs headroom.
- Say the hook sentence first, clearly; pause a beat between steps (cuts are made at pauses).
- Keep the phone vertical (9:16).
