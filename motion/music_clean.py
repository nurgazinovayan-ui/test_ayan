"""Driving 128 BPM track + UI sound design for oneflow-clean.html. Synthesized from scratch — no samples, no licensing.

F – C – Dm – Bb (I–V–vi–IV), one chord per bar. Intro build under the offer → drop on the click into the app (beat 8):
four-on-the-floor kick with sidechain pumping, rolling 16th bass, claps, 16th hats, open hats, supersaw chords, pluck arp.
Short breakdown + snare roll under «Адаптируйте их под себя автоматически» → second drop on «Тексты» (beat 44), lead arp
from the assistant scene (beat 60), breakdown under the brand mark, final impact on the logo (beat 84).
Every scene change gets an impact; UI sounds (ticks, clicks, typing, pops, chimes) sit on the time-warped cut.

python3 music_clean.py  →  music-clean.wav
"""
import math
import os
import wave

import numpy as np

import timeline_clean as tl

SR, BPM, B = 44100, tl.BPM, tl.B
T = tl.DUR
N = int(SR * T) + 1
rng = np.random.default_rng(21)
at = lambda t: int(round(t * SR))  # noqa: E731
NOTE = lambda m: 440 * 2 ** ((m - 69) / 12)  # noqa: E731
bt = lambda b: b * B  # noqa: E731  beat → seconds
R = tl.real  # authored scene time → real time
A, S = 11.3, 18.7  # authored offsets of the assistant scene and of the launch / brand / logo scenes

MUS = [np.zeros(N), np.zeros(N)]   # sidechained music bus
DRM = [np.zeros(N), np.zeros(N)]   # drums
FX = [np.zeros(N), np.zeros(N)]    # impacts, risers, UI sounds


def add(bus, sig, t0, gain=1.0, pan=0.0):
    i = at(t0)
    if i >= N or i + len(sig) <= 0:
        return
    if i < 0:
        sig, i = sig[-i:], 0
    sig = sig[: N - i]
    bus[0][i:i + len(sig)] += sig * gain * (1 - max(0, pan))
    bus[1][i:i + len(sig)] += sig * gain * (1 + min(0, pan))


def add2(bus, lr, t0, gain=1.0):
    i = at(t0)
    if i >= N:
        return
    n = min(len(lr[0]), N - i)
    bus[0][i:i + n] += lr[0][:n] * gain
    bus[1][i:i + n] += lr[1][:n] * gain


def lowpass(x, fc):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X / np.sqrt(1 + (f / fc) ** 4), len(x))


def highpass(x, fc):
    return x - lowpass(x, fc)


def sweep_lp(x, f0, f1):
    y = np.zeros_like(x); fc = f0 * (f1 / f0) ** np.linspace(0, 1, len(x)); a = 1 - np.exp(-2 * np.pi * fc / SR); s = 0.0
    for i in range(len(x)):
        s += a[i] * (x[i] - s); y[i] = s
    return y


def tt(dur):
    return np.arange(at(dur)) / SR


def saw(f, t, ph=0.0, top=9000):
    n = int(max(1, min(48, top // f)))
    return sum(np.sin(2 * np.pi * f * k * t + ph * k) / k for k in range(1, n + 1)) * .6


# ---------------------------------------------------------------- voices
def kick():
    t = tt(.42); f = 44 + 150 * np.exp(-t * 38)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7.5)
    click = highpass(rng.standard_normal(len(t)), 3000) * np.exp(-t * 300) * .5
    return np.tanh((body + click) * 1.6)


def clap():
    t = tt(.35); nz = highpass(lowpass(rng.standard_normal(len(t)), 5000), 900)
    env = sum(np.exp(-np.maximum(0, t - o) * 120) * (t >= o) for o in (0, .009, .018)) * .45 + np.exp(-t * 14) * .7
    snare = np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30) * .5
    return nz * env + snare


def snare_hit():
    t = tt(.18)
    return highpass(rng.standard_normal(len(t)), 1200) * np.exp(-t * 26) * .8 + np.sin(2 * np.pi * 210 * t) * np.exp(-t * 35) * .5


def hat(open_=False):
    t = tt(.28 if open_ else .05)
    return highpass(rng.standard_normal(len(t)), 8000) * np.exp(-t * (11 if open_ else 80)) * np.minimum(1, t / .002)


def pluck(f, dur=.32):
    t = tt(dur)
    return lowpass(saw(f, t), 5200) * np.exp(-t * 12) * np.minimum(1, t / .002)


def bass(f, dur=B / 4 * .92):
    t = tt(dur); v = saw(f, t, top=1600) + np.sin(2 * np.pi * f / 2 * t) * .9
    return lowpass(v, 900) * np.minimum(1, t / .004) * np.minimum(1, (dur - t) / .01)


def supersaw(freqs, dur, fc=4200):
    t = tt(dur); l = np.zeros(len(t)); r = np.zeros(len(t))
    for f in freqs:
        for k, det in enumerate((-.14, -.07, 0, .07, .14)):
            v = saw(f * 2 ** (det / 12), t, ph=rng.uniform(0, 6), top=6000)
            if k <= 2:
                l += v
            if k >= 2:
                r += v
    e = np.minimum(1, t / .02) * np.minimum(1, (dur - t) / .08)
    return lowpass(l, fc) * e, lowpass(r, fc) * e


def bell(f, dur=1.2):
    t = tt(dur)
    v = np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * 2.76 * f * t) * np.exp(-t * 4) + .25 * np.sin(2 * np.pi * 5.4 * f * t) * np.exp(-t * 7)
    return v * np.exp(-t * 2.6) * np.minimum(1, t / .002)


def tick(f=2400):
    t = tt(.05)
    return np.sin(2 * np.pi * f * t) * np.exp(-t * 90)


def click():
    t = tt(.06)
    return (highpass(rng.standard_normal(len(t)), 2500) * .6 + np.sin(2 * np.pi * 1800 * t)) * np.exp(-t * 120)


def pop():
    t = tt(.18); f = 300 + 700 * np.exp(-t * 25)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 16)


def whoosh(dur=.45, up=True):
    x = sweep_lp(rng.standard_normal(at(dur)), 400 if up else 6000, 6000 if up else 400)
    return highpass(x, 250) * np.sin(np.linspace(0, np.pi, len(x))) ** 2


def riser(dur):
    t = tt(dur); f = 180 * 2 ** (t / dur * 3)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * (t / dur) ** 2 * .35 + sweep_lp(rng.standard_normal(len(t)), 300, 9000) * (t / dur) ** 2.2 * .6


def impact():
    t = tt(1.6)
    sub = np.sin(2 * np.pi * np.cumsum(38 + 70 * np.exp(-t * 9)) / SR) * np.exp(-t * 3.2)
    crash = highpass(rng.standard_normal(len(t)), 3500) * np.exp(-t * 3.5) * .35
    return np.tanh((sub + crash) * 1.4)


def sparkle(dur=1.0):
    t = tt(dur); x = highpass(rng.standard_normal(len(t)), 7000)
    return x * (rng.random(len(t)) < .02) * np.exp(-t * 2.8) * 3


def snare_roll(b0, b1, g=.22):
    """Accelerating snare roll from beat b0 to b1 (8ths → 16ths → 32nds), rising in level."""
    b = b0
    while b < b1 - 1e-9:
        p = (b - b0) / (b1 - b0)
        add(DRM, snare_hit(), bt(b), g * (.35 + .65 * p), pan=.1)
        b += .5 if p < .5 else .25 if p < .8 else .125


# ---------------------------------------------------------------- arrangement
CH = [(41, [53, 57, 60, 65]), (36, [52, 55, 60, 64]), (38, [50, 53, 57, 62]), (34, [50, 53, 58, 62])]  # F  C  Dm  Bb
BARS = int(math.ceil(90 / 4))
pads = {i: supersaw([NOTE(m) for m in CH[i][1]], 4 * B + .05) for i in range(4)}
stabs = {i: supersaw([NOTE(m + 12) for m in CH[i][1]], B * .42, 6500) for i in range(4)}
bassn = {i: bass(NOTE(CH[i][0])) for i in range(4)}
plk = {}

full = lambda b: tl.kick_on(b)  # noqa: E731
for bar in range(BARS):
    b0 = bar * 4; ci = bar % 4; root, notes = CH[ci]
    if b0 >= 90:
        break
    intro, brk1, brk2 = b0 < 8, 40 <= b0 < 44, 76 <= b0 < 84
    if b0 < 84:
        l, r = pads[ci]
        if intro:  # filtered pad opening up into the drop
            l = sweep_lp(l, 500 + b0 * 250, 900 + b0 * 500); r = sweep_lp(r, 500 + b0 * 250, 900 + b0 * 500)
        add2(MUS, (l, r), bt(b0), .05 if intro or brk1 or brk2 else .04)
    if full(b0):
        for k in range(16):  # rolling bass: every 16th except on the kick
            if k % 4:
                add(MUS, bassn[ci], bt(b0 + k / 4), .3 if k % 4 == 2 else .2)
        if b0 >= 44:  # offbeat supersaw stabs in the second half
            for k in range(4):
                add2(MUS, stabs[ci], bt(b0 + k + .5), .05)
    if b0 >= 8 and not brk2:  # pluck arp, 16ths; lead register from the assistant scene
        up = 24 if b0 >= 60 else 12
        seq = [notes[i % 4] + 12 * (i // 4 % 2) for i in (0, 1, 2, 3, 4, 3, 2, 1, 0, 2, 1, 3, 4, 2, 3, 1)]
        for k, m in enumerate(seq):
            key = m + up
            if key not in plk:
                plk[key] = pluck(NOTE(key))
            add(MUS, plk[key], bt(b0 + k / 4), (.05 if brk1 else .085) * (1.15 if k % 4 == 0 else 1), pan=.35 if k % 2 else -.35)
# final chord on the logo
l, r = supersaw([NOTE(m) for m in (53, 57, 60, 65, 69)], 5.0, 3000)
env = np.exp(-tt(5.0) * .7)
add2(MUS, (l * env, r * env), bt(84), .07)

# drums
side = np.ones(N)
K = kick()
for b in np.arange(0, 90, 1.0):
    if full(b):
        add(DRM, K, bt(b), .75)
        i = at(bt(b)); n = min(at(.4), N - i); side[i:i + n] = np.minimum(side[i:i + n], 1 - .6 * np.exp(-np.arange(n) / SR / .09))
        if b % 4 in (1, 3):
            add(DRM, clap(), bt(b), .3, .08)
        add(DRM, hat(True), bt(b + .5), .09, .25)
    if b >= 4 and b < 84:
        for k in range(4):
            add(DRM, hat(), bt(b + k / 4), (.07 if k == 2 else .045) * (.6 if not full(b) else 1), -.3)
for b in (0, 3, 5.5):  # intro hits under the offer words
    add(DRM, K, bt(b), .55)
snare_roll(4, 8); snare_roll(42, 44); snare_roll(80, 84, .26); snare_roll(68, 72, .18)
add(FX, riser(bt(4)), 0, .16); add(FX, riser(bt(4)), bt(40), .16); add(FX, riser(bt(7)), bt(77), .18)

# impacts on every cut
for b, kind in tl.CUTS:
    add(FX, impact(), bt(b), .42 if kind == 'flash' else .3)
    add(FX, whoosh(.35), bt(b) - .32, .22 if kind == 'whip' else .12)

# ---------------------------------------------------------------- UI sound design (authored times → real)
for t in (.15, .42, 1.5, 1.66, 1.88, 2.9, 3.42, 6.25, 6.5, 6.75, 7.0, 7.95, 8.1, 8.25, 18.2, 18.42, 19.95, 20.1, 20.25, 22.55, 22.7, 22.85,
          24.15, 24.3, 24.45, 28.75, 28.9, 22.05 + A, 22.3 + A, 22.5 + A, 22.7 + A, 26.0 + S, 26.5 + S, 27.0 + S):
    add(FX, tick(2600), R(t), .09, pan=.15)
add(FX, pop(), R(3.12), .3)
for t in (4.02, 17.2, 21.7, 30.0, 23.25 + S):
    add(FX, click(), R(t), .35)
for k, m in enumerate((72, 76, 79, 84)):  # «Готово»
    add(FX, bell(NOTE(m)), R(12.45) + k * .06, .14, pan=(k - 1.5) * .2)
add(FX, sparkle(), R(12.55), .5)
add(FX, pop(), R(21.9), .28)  # adapted trend card
for t, m in ((22.1, 79), (22.3, 84), (22.5, 88)):
    add(FX, bell(NOTE(m), .7), R(t), .06)
ty = np.random.default_rng(5)


def typing(t0, t1, cps, g=.05):
    for k in range(int((t1 - t0) * cps / 2)):
        add(FX, tick(ty.uniform(1500, 2100)), R(t0 + k * 2 / cps + ty.uniform(0, .015)), g, pan=ty.uniform(-.2, .2))


typing(24.9, 25.95, 34); typing(26.05, 27.55, 90, .022)
add(FX, pop(), R(27.65), .25)
for t in (29.1, 29.2, 29.3):
    add(FX, pop(), R(t), .2)
for k, m in enumerate((76, 79, 84)):  # predictor winner
    add(FX, bell(NOTE(m)), R(31.35) + k * .06, .12, pan=(k - 1) * .2)
add(FX, sparkle(), R(31.4), .4)
typing(23.8 + A, 25.2 + A, 34)
add(FX, pop(), R(25.0 + A), .22)
for t in (25.3, 25.9, 26.5, 27.1):
    add(FX, pop(), R(t + A), .25)
for t, m in ((25.6, 84), (26.2, 88), (26.8, 91)):
    add(FX, bell(NOTE(m), .9), R(t + A), .09)
add(FX, sparkle(.9), R(27.25 + A), .3)
add(FX, bell(NOTE(84), 1.0), R(23.3 + S), .12)  # launch button turns blue
add(FX, sparkle(1.8), bt(84) + .1, .35)

# ---------------------------------------------------------------- master
mix = []
for ch in range(2):
    m = MUS[ch] * side + DRM[ch] + FX[ch]
    mix.append(m)
mix_l, mix_r = mix
fade = np.ones(N); fs = at(T - 1.6); fade[fs:] = np.linspace(1, 0, N - fs) ** 1.3
fin = np.ones(N); fin[: at(.02)] = np.linspace(0, 1, at(.02))
mix_l *= fade * fin; mix_r *= fade * fin
peak = max(np.abs(mix_l).max(), np.abs(mix_r).max())
DRIVE = 2.8  # soft-clip compression: loud, dense body without letting impacts peak out
mix_l = np.tanh(mix_l / peak * DRIVE) / math.tanh(DRIVE) * .93; mix_r = np.tanh(mix_r / peak * DRIVE) / math.tanh(DRIVE) * .93
out = (np.stack([mix_l, mix_r], 1) * 32767).astype('<i2')
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'music-clean.wav')
with wave.open(path, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes())
print(path, f'{T:.2f} s')
