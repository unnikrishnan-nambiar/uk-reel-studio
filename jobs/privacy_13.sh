#!/bin/bash
for n in 1 3; do echo "=== V$n"; bash /home/claude/uk-reel-studio/jobs/privacy_v$n/render.sh || echo "FAIL V$n"; done
echo ALLDONE
