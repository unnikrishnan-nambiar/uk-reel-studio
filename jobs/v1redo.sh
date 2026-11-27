#!/bin/bash
while pgrep -f "privacy_13.sh" >/dev/null; do sleep 15; done
cd /home/claude/uk-reel-studio/jobs/privacy_v1
rm -rf ovT cut60.mp4 cut60.mov edit.json body.mp4 body.wav body_v.mp4 body_a.wav p*.mov
bash render.sh && echo V1DONE
