#!/bin/bash
set -e
for n in 1 2 3; do echo "=== V$n"; bash /home/claude/uk-reel-studio/jobs/privacy_v$n/render.sh; done
echo ALLDONE
