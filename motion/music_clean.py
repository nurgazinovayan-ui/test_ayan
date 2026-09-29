"""Light, bright track + UI sound design for oneflow-clean.html (49.8 s). Synthesized from scratch — no samples, no licensing.

120 BPM, Fmaj7 – Am7 – Dm7 – C. Soft pluck arpeggios and pads from the start, beat comes in with the 3D corridor (6 s),
drops out for the brand mark (24 s), final chord under the logo. Ticks on words, clicks on cursor clicks, whooshes on
camera moves, a rising tone under the progress bar, a chime + sparkle on «Готово», a soft hit on the logo.

python3 music_clean.py  →  music-clean.wav
"""
import math
import os
import wave

import numpy as np

SR, T, BPM = 44100, 49.8, 120
A = 11.3  # the AI-assistant scene plays A seconds later (longer trends scene, «Тексты» and Creative Predictor come first)
S = 18.7  # launch / brand / logo scenes play S seconds later
N = int(SR * T)
BEAT = 60 / BPM
rng = np.random.default_rng(21)
L, R = np.zeros(N), np.zeros(N)
side = np.ones(N)
at = lambda t: int(round(t * SR))  # noqa: E731
NOTE = lambda m: 440 * 2 ** ((m - 69) / 12)  # noqa: E731


def add(sig, t0, gain=1.0, pan=0.0):
    i = at(t0)
    if i >= N:
        return
    sig = sig[: N - i]
    L[i:i + len(sig)] += sig * gain * (1 - max(0, pan))
    R[i:i + len(sig)] += sig * gain * (1 + min(0, pan))


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


# ---------------------------------------------------------------- voices
def pluck(f, dur=.5):
    t = tt(dur)
    v = np.sin(2 * np.pi * f * t) + .35 * np.sin(2 * np.pi * 2 * f * t) + .12 * np.sin(2 * np.pi * 3 * f * t)
    return v * np.exp(-t * 7) * np.minimum(1, t / .003)


def bell(f, dur=1.4):
    t = tt(dur)
    v = np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * 2.76 * f * t) * np.exp(-t * 4) + .25 * np.sin(2 * np.pi * 5.4 * f * t) * np.exp(-t * 7)
    return v * np.exp(-t * 2.4) * np.minimum(1, t / .002)


def pad(freqs, dur):
    t = tt(dur); l = np.zeros(len(t)); r = np.zeros(len(t))
    for f in freqs:
        for det, sd in ((-.08, 'l'), (0, 'c'), (.09, 'r')):
            ff = f * 2 ** (det / 12)
            v = sum(np.sin(2 * np.pi * ff * k * t + rng.uniform(0, 6)) / (k * k) for k in range(1, 6))
            if sd != 'r':
                l += v
            if sd != 'l':
                r += v
    e = np.minimum(1, t / .5) * np.minimum(1, (dur - t) / .5)
    return lowpass(l, 2400) * e, lowpass(r, 2400) * e


def kick():
    t = tt(.4); f = 48 + 90 * np.exp(-t * 30)
    return np.tanh(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 8) * 1.3)


def clap():
    t = tt(.3); nz = highpass(lowpass(rng.standard_normal(len(t)), 4000), 1000)
    return nz * (sum(np.exp(-np.maximum(0, t - o) * 110) * (t >= o) for o in (0, .01, .02)) * .5 + np.exp(-t * 18) * .6)


def shaker():
    t = tt(.07)
    return highpass(rng.standard_normal(len(t)), 6500) * np.exp(-t * 60) * np.minimum(1, t / .01)


def bass(f, dur):
    t = tt(dur)
    return lowpass(np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * 2 * f * t), 500) * np.exp(-t * 2.2) * np.minimum(1, t / .006)


def tick(f=2400):
    t = tt(.05)
    return np.sin(2 * np.pi * f * t) * np.exp(-t * 90)


def click():
    t = tt(.06)
    return (highpass(rng.standard_normal(len(t)), 2500) * .6 + np.sin(2 * np.pi * 1800 * t)) * np.exp(-t * 120)


def whoosh(dur=.55, up=True):
    x = sweep_lp(rng.standard_normal(at(dur)), 300 if up else 5000, 5000 if up else 300)
    return highpass(x, 200) * np.sin(np.linspace(0, np.pi, len(x))) ** 2


def pop():
    t = tt(.18); f = 300 + 700 * np.exp(-t * 25)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 16)


def riser(dur):
    t = tt(dur); f = 220 * 2 ** (t / dur * 2)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * (t / dur) ** 1.5 * .5 + sweep_lp(rng.standard_normal(len(t)), 400, 7000) * (t / dur) ** 2 * .5


def sparkle(dur=1.2):
    t = tt(dur); x = highpass(rng.standard_normal(len(t)), 7000)
    return x * (rng.random(len(t)) < .02) * np.exp(-t * 2.5) * 3


def soft_hit():
    t = tt(2.4)
    return np.tanh((np.sin(2 * np.pi * (46 + 40 * np.exp(-t * 10)) * t) * np.exp(-t * 2.4) + lowpass(rng.standard_normal(len(t)), 1800) * np.exp(-t * 4) * .25) * 1.1)


# ---------------------------------------------------------------- arrangement
CH = [(41, [53, 57, 60, 64]), (45, [57, 60, 64, 67]), (38, [50, 53, 57, 60]), (48, [48, 52, 55, 59])]  # Fmaj7 Am7 Dm7 Cmaj7
for bar in range(25):
    t0 = bar * 2.0
    if t0 >= T:
        break
    root, notes = CH[bar % 4]
    if t0 < 28 + S:
        l, r = pad([NOTE(m) for m in notes], 2.1)
        g = .05 if t0 < 6 else .045
        add(l, t0, g, .4); add(r, t0, g, -.4)
        arp = [notes[i % 4] + 12 * (i // 4 % 2) for i in (0, 1, 2, 3, 4, 3, 2, 1)]
        for k, m in enumerate(arp):
            add(pluck(NOTE(m + 12)), t0 + k * BEAT / 2, .13 if t0 < 6 else .09 if t0 < 24 + S else .07, pan=.3 if k % 2 else -.3)
    if 6 <= t0 < 24 + S:
        for k in range(8):
            add(bass(NOTE(root - 12), .24), t0 + k * BEAT / 2, .32 if k % 2 == 0 else .22)
l, r = pad([NOTE(m) for m in (53, 57, 60, 64, 69)], 3.0)
add(l, 28 + S, .06, .4); add(r, 28 + S, .06, -.4)

K = kick()
for t in np.arange(6.0, 24.0 + S - 1e-9, BEAT):
    add(K, t, .7)
    i = at(t); n = min(at(.35), N - i); side[i:i + n] = np.minimum(side[i:i + n], 1 - .45 * np.exp(-np.arange(n) / SR / .1))
for t in np.arange(6.0 + BEAT, 24.0 + S - 1e-9, 2 * BEAT):
    add(clap(), t, .28, .1)
for t in np.arange(4.0, 24.0 + S - 1e-9, BEAT / 4):
    add(shaker(), t, .05 if (t * 4) % 2 else .08, -.3)

# UI sound design
for t in (.15, .42, 1.5, 1.66, 1.88, 2.9, 3.42, 6.25, 6.5, 6.75, 7.0, 7.95, 8.1, 8.25, 18.2, 18.42, 26.0 + S, 26.5 + S, 27.0 + S, 22.05 + A, 22.3 + A, 22.5 + A, 22.7 + A,
          19.95, 20.1, 20.25, 22.55, 22.7, 22.85, 24.15, 24.3, 24.45, 28.75, 28.9):
    add(tick(2600), t, .1, pan=.15)
add(pop(), 3.12, .3)
for t in (4.02, 17.2, 21.7, 30.0, 23.25 + S):
    add(click(), t, .35)
for t, g in ((4.22, .35), (5.62, .25), (5.85, .3), (9.22, .4), (13.95, .3), (16.05, .3), (17.32, .22), (20.2, .3), (23.9, .25), (24.35, .3), (28.4, .25), (33.05, .25), (22.55 + S, .25), (25.3 + S, .4), (23.25 + A, .3), (28.9 + A, .25)):
    add(whoosh(), t - .1, g)
add(riser(1.75), 10.45, .12)
for k, m in enumerate((72, 76, 79, 84)):
    add(bell(NOTE(m)), 12.45 + k * .07, .16, pan=(k - 1.5) * .2)
add(sparkle(), 12.55, .5)
add(bell(NOTE(84), 1.0), 23.3 + S, .12)
add(pop(), 24.15 + S, .3)
add(soft_hit(), 28.2 + S, .55)
add(sparkle(1.8), 28.3 + S, .35)
for k, m in enumerate((65, 69, 72, 77)):
    add(bell(NOTE(m), 2.0), 28.2 + S + k * .05, .07)

# AI assistant scene: typing, reply, nodes popping onto the canvas, checks, «собрано ассистентом»
ty = np.random.default_rng(5)


def typing(t0, t1, cps, g=.05):
    for k in range(int((t1 - t0) * cps / 2)):
        add(tick(ty.uniform(1500, 2100)), t0 + k * 2 / cps + ty.uniform(0, .015), g, pan=ty.uniform(-.2, .2))


typing(23.8 + A, 25.2 + A, 34)
add(pop(), 25.0 + A, .22)
for t in (25.3, 25.9, 26.5, 27.1):
    add(pop(), t + A, .25)
for t, m in ((25.6, 84), (26.2, 88), (26.8, 91)):
    add(bell(NOTE(m), .9), t + A, .1)
add(sparkle(.9), 27.25 + A, .3)

# trends: «Адаптировать» click → adapted scenario card, its three lines
add(pop(), 21.9, .28)
for t, m in ((22.1, 79), (22.3, 84), (22.5, 88)):
    add(bell(NOTE(m), .7), t, .07)
# texts: typed request, streamed answer, file chip
typing(24.9, 25.95, 34)
typing(26.05, 27.55, 90, .025)
add(pop(), 27.65, .25); add(bell(NOTE(91), .9), 27.7, .08)
# Creative Predictor: cards pop in, «Оценить» click, scores rise, winner chime
for t in (29.1, 29.2, 29.3):
    add(pop(), t, .2)
add(riser(1.0), 30.2, .1)
for k, m in enumerate((76, 79, 84)):
    add(bell(NOTE(m)), 31.35 + k * .07, .13, pan=(k - 1) * .2)
add(sparkle(), 31.4, .4)

# master
mix_l, mix_r = L * side, R * side
fade = np.ones(N); fs = at(29.8 + S); fade[fs:] = np.linspace(1, 0, N - fs) ** 1.4
fin = np.ones(N); fin[: at(.03)] = np.linspace(0, 1, at(.03))
mix_l *= fade * fin; mix_r *= fade * fin
peak = max(np.abs(mix_l).max(), np.abs(mix_r).max())
DRIVE = 2.4  # soft-clip compression: brings the body up without letting clicks/hits peak out
mix_l = np.tanh(mix_l / peak * DRIVE) / math.tanh(DRIVE) * .92; mix_r = np.tanh(mix_r / peak * DRIVE) / math.tanh(DRIVE) * .92
out = (np.stack([mix_l, mix_r], 1) * 32767).astype('<i2')
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'music-clean.wav')
with wave.open(path, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes())
print(path)
