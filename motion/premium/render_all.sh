#!/bin/sh
# Render every premium variant to ../out/premium/video/NN-name.mp4 (1280×720), three at a time.
cd "$(dirname "$0")"
ls p??-*.html | xargs -P 3 -I{} sh -c 'f={}; k=$(echo $f | cut -c2-3); node render.js $f ../out/premium/audio/$k.wav ../out/premium/video/${f%.html}.mp4 1280'
