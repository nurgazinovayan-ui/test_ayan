"""Synthesized soundtracks for the premium promos (no samples, no licensing): one parametric arrangement, ten flavours.

Intro under the offer (pads + plucks), the groove drops on the first bar after ~5.5 s, a riser before the logo, an impact
and a final chord on the logo, fade to the end. python3 music.py [nn …] → ../out/premium/audio/NN.wav
"""
import math
import os
import sys
import wave

import numpy as np

import build

SR = 44100
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'out', 'premium', 'audio')
NOTE = lambda m: 440 * 2 ** ((m - 69) / 12)  # noqa: E731
PROG = {'bright': [(41, [53, 57, 60, 65]), (36, [52, 55, 60, 64]), (38, [50, 53, 57, 62]), (34, [50, 53, 58, 62])],   # F C Dm Bb
        'dark': [(38, [50, 53, 57, 62]), (34, [50, 53, 58, 62]), (41, [53, 57, 60, 65]), (36, [52, 55, 60, 64])],     # Dm Bb F C
        'minor': [(45, [57, 60, 64, 69]), (41, [53, 57, 60, 65]), (36, [52, 55, 60, 64]), (43, [55, 59, 62, 67])],    # Am F C G
        'dreamy': [(36, [52, 55, 59, 64]), (45, [55, 60, 64, 67]), (41, [53, 57, 60, 64]), (43, [55, 59, 62, 65])]}   # Cmaj7 Am7 Fmaj7 G7
# bpm, progression, drums ('half' | 'four'), energy 0..1, lowpass of the music bus, logo time
P = {1: (96, 'dark', 'half', .55, 3200, 39.1), 2: (112, 'bright', 'four', .5, 5200, 40.3), 3: (120, 'dark', 'four', .75, 3800, 39.2),
     4: (124, 'dark', 'four', .85, 3400, 35.2), 5: (116, 'bright', 'four', .55, 6000, 36.5), 6: (128, 'minor', 'four', .9, 6500, 36.9),
     7: (122, 'dreamy', 'four', .7, 4200, 36.1), 8: (110, 'bright', 'four', .45, 5200, 35.8), 9: (118, 'dreamy', 'four', .6, 5600, 35.8),
     10: (126, 'dark', 'four', .8, 4400, 38.5)}


def lowpass(x, fc):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X / np.sqrt(1 + (f / fc) ** 4), len(x))


def highpass(x, fc):
    return x - lowpass(x, fc)


def tt(d):
    return np.arange(int(d * SR)) / SR


def saw(f, t, ph=0.0, top=8000):
    return sum(np.sin(2 * np.pi * f * k * t + ph * k) / k for k in range(1, int(max(1, min(40, top // f))) + 1)) * .6


def make(k):
    bpm, prog, drums, en, lp, logo_t = P[k]
    T = build.load(k).T
    B = 60 / bpm; N = int(SR * T) + 1; rng = np.random.default_rng(k)
    D, F = [np.zeros(N), np.zeros(N)], [np.zeros(N), np.zeros(N)]
    M = [np.zeros(N), np.zeros(N)]

    def add(bus, sig, t0, g=1.0, pan=0.0):
        i = int(round(t0 * SR))
        if i >= N or i < 0:
            return
        n = min(len(sig), N - i)
        bus[0][i:i + n] += sig[:n] * g * (1 - max(0, pan)); bus[1][i:i + n] += sig[:n] * g * (1 + min(0, pan))

    def add2(bus, lr, t0, g=1.0):
        i = int(round(t0 * SR)); n = min(len(lr[0]), N - i)
        if n > 0:
            bus[0][i:i + n] += lr[0][:n] * g; bus[1][i:i + n] += lr[1][:n] * g

    def pad(freqs, dur):
        t = tt(dur); l = np.zeros(len(t)); r = np.zeros(len(t))
        for f in freqs:
            for j, det in enumerate((-.1, 0, .1)):
                v = saw(f * 2 ** (det / 12), t, rng.uniform(0, 6), 4000)
                if j < 2:
                    l += v
                if j > 0:
                    r += v
        e = np.minimum(1, t / .4) * np.minimum(1, (dur - t) / .3)
        return lowpass(l, lp * .6) * e, lowpass(r, lp * .6) * e

    def pluck(f, dur=.4):
        t = tt(dur)
        return lowpass(saw(f, t, 0, 6000), lp) * np.exp(-t * 9) * np.minimum(1, t / .002)

    def kick():
        t = tt(.42)
        return np.tanh(np.sin(2 * np.pi * np.cumsum(44 + 140 * np.exp(-t * 36)) / SR) * np.exp(-t * 7) * 1.6 + highpass(rng.standard_normal(len(t)), 3000) * np.exp(-t * 300) * .4)

    def clap():
        t = tt(.3); nz = highpass(lowpass(rng.standard_normal(len(t)), 5000), 900)
        return nz * (sum(np.exp(-np.maximum(0, t - o) * 120) * (t >= o) for o in (0, .01, .02)) * .45 + np.exp(-t * 15) * .6)

    def hat(op=False):
        t = tt(.26 if op else .05)
        return highpass(rng.standard_normal(len(t)), 8000) * np.exp(-t * (11 if op else 80))

    def bass(f, dur):
        t = tt(dur)
        return lowpass(saw(f, t, 0, 1500) + np.sin(np.pi * f * t) * .9, 800) * np.minimum(1, t / .004) * np.minimum(1, (dur - t) / .01)

    def riser(dur):
        t = tt(dur); x = highpass(rng.standard_normal(len(t)), 400)
        return (np.sin(2 * np.pi * np.cumsum(200 * 2 ** (t / dur * 3)) / SR) * .3 + lowpass(x, 6000) * .5) * (t / dur) ** 2

    def impact():
        t = tt(2.2)
        return np.tanh((np.sin(2 * np.pi * np.cumsum(36 + 70 * np.exp(-t * 9)) / SR) * np.exp(-t * 2.6) + highpass(rng.standard_normal(len(t)), 3000) * np.exp(-t * 3) * .3) * 1.3)

    def bell(f, dur=1.6):
        t = tt(dur)
        return (np.sin(2 * np.pi * f * t) + .45 * np.sin(2 * np.pi * 2.76 * f * t) * np.exp(-t * 4)) * np.exp(-t * 2.4) * np.minimum(1, t / .002)

    drop = math.ceil(5.5 / (4 * B)) * 4 * B          # first bar line after the offer
    brk = logo_t - 4 * B                              # one bar of riser before the logo
    pads = {i: pad([NOTE(m) for m in PROG[prog][i][1]], 4 * B + .3) for i in range(4)}
    bars = int(T / (4 * B)) + 1
    for bar in range(bars):
        t0 = bar * 4 * B
        if t0 >= logo_t:
            break
        root, notes = PROG[prog][bar % 4]
        add2(M, pads[bar % 4], t0, .045 if t0 < drop else .022)
        step = B / 2 if (t0 < drop or drums == 'half') else B / 4
        seq = [notes[i % 4] + 12 * (i // 4 % 2) for i in (0, 1, 2, 3, 4, 3, 2, 1, 0, 2, 1, 3, 4, 2, 3, 1)]
        for j in range(int(4 * B / step)):
            m = seq[j % 16] + 12
            add(M, pluck(NOTE(m)), t0 + j * step, (.07 if t0 < drop else .06) * (1.2 if j % 4 == 0 else 1), .3 if j % 2 else -.3)
        if drop <= t0 < brk:
            for j in range(16 if drums == 'four' else 8):
                if drums == 'four' and j % 4 == 0:
                    continue
                d = B / 4 if drums == 'four' else B / 2
                add(M, bass(NOTE(root - 12), d * .9), t0 + j * d, .13 + .08 * en)
    # final chord on the logo
    root, notes = PROG[prog][0]
    l, r = pad([NOTE(m) for m in notes + [notes[0] + 12]], T - logo_t + .2)
    env = np.exp(-tt(T - logo_t + .2) * .5)
    add2(M, (l * env, r * env), logo_t, .035)
    for j, m in enumerate(notes):
        add(F, bell(NOTE(m + 24)), logo_t + j * .06, .07, (j - 1.5) * .2)
    # drums
    side = np.ones(N); K = kick()
    b = drop
    while b < brk - 1e-6:
        beat = round((b - drop) / B)
        if drums == 'four' or beat % 2 == 0:
            add(D, K, b, .55 + .25 * en)
            i = int(b * SR); n = min(int(.4 * SR), N - i); side[i:i + n] = np.minimum(side[i:i + n], 1 - (.35 + .3 * en) * np.exp(-np.arange(n) / SR / .1))
        if beat % 2 == 1 and en > .5:
            add(D, clap(), b, .18 + .12 * en, .08)
        if drums == 'four':
            add(D, hat(True), b + B / 2, .05 + .05 * en, .25)
            for q in range(4):
                add(D, hat(), b + q * B / 4, (.03 + .03 * en) * (1.4 if q == 2 else 1), -.3)
        else:
            add(D, hat(), b + B / 2, .05, -.3)
        b += B
    add(F, riser(4 * B), brk, .1 + .08 * en)
    add(F, impact(), logo_t, .45)
    add(F, riser(drop - .2), .2, .06)
    add(F, impact(), drop, .28)
    mix = [M[c] * side + D[c] + F[c] for c in range(2)]
    fade = np.ones(N); fs = int((T - 1.6) * SR); fade[fs:] = np.linspace(1, 0, N - fs) ** 1.3
    fin = np.ones(N); fin[:int(.02 * SR)] = np.linspace(0, 1, int(.02 * SR))
    mix = [m * fade * fin for m in mix]
    pk = max(np.abs(m).max() for m in mix); drv = 1.7
    mix = [np.tanh(m / pk * drv) / math.tanh(drv) * .8 for m in mix]
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f'{k:02d}.wav')
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.stack(mix, 1) * 32767).astype('<i2').tobytes())
    return path


if __name__ == '__main__':
    for k in [int(a) for a in sys.argv[1:]] or range(1, 11):
        print(make(k))
