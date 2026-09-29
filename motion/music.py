"""Original 28-second track for the ONEFLOW motion video — synthesized from scratch (no samples, no licensing).

120 BPM (a beat every 0.5 s), so every scene cut (2, 5, 8, 13, 16, 20, 24 s) lands on a beat. Am–F–C–G, one chord per bar.
Intro swell + logo hit → groove with kick/hats → riser → full drop at 8 s → half-time accent on «−50%» → final hit at 24 s.

python3 music.py  →  music.wav (44.1 kHz, stereo, 16-bit)
"""
import os
import wave

import numpy as np

SR, T, BPM = 44100, 28.0, 120
N = int(SR * T)
BEAT = 60 / BPM
rng = np.random.default_rng(7)
L, R = np.zeros(N), np.zeros(N)
side = np.ones(N)  # sidechain gain driven by the kick


def at(t):
    return int(round(t * SR))


def add(sig, t0, gain=1.0, pan=0.0):
    i = at(t0)
    if i >= N:
        return
    sig = sig[: N - i]
    L[i:i + len(sig)] += sig * gain * (1 - max(0, pan))
    R[i:i + len(sig)] += sig * gain * (1 + min(0, pan))


def lowpass(x, fc):
    """Static low-pass via FFT (smooth roll-off)."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / np.sqrt(1 + (f / fc) ** 4)
    return np.fft.irfft(X, len(x))


def highpass(x, fc):
    return x - lowpass(x, fc)


def sweep_lp(x, f0, f1):
    """One-pole low-pass whose cutoff glides exponentially from f0 to f1 (used for risers/whooshes)."""
    y = np.zeros_like(x)
    fc = f0 * (f1 / f0) ** np.linspace(0, 1, len(x))
    a = 1 - np.exp(-2 * np.pi * fc / SR)
    s = 0.0
    for i in range(len(x)):
        s += a[i] * (x[i] - s)
        y[i] = s
    return y


def env(n, attack, decay):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(attack, 1e-4)) * np.exp(-t / decay)


# ---------------------------------------------------------------- instruments
def kick():
    n = at(.5); t = np.arange(n) / SR
    f = 44 + 120 * np.exp(-t * 34)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6.5)
    click = rng.standard_normal(n) * np.exp(-t * 400) * .35
    return np.tanh((body + click) * 1.6)


def clap():
    n = at(.35); t = np.arange(n) / SR
    nz = highpass(lowpass(rng.standard_normal(n), 3200), 900)
    e = sum(np.exp(-np.maximum(0, t - o) * 90) * (t >= o) for o in (0, .012, .024)) * .6 + np.exp(-t * 16) * .7
    return nz * e


def hat(open_=False):
    n = at(.25 if open_ else .08); t = np.arange(n) / SR
    return highpass(rng.standard_normal(n), 7000) * np.exp(-t * (14 if open_ else 70))


def bass(freq, dur):
    n = at(dur); t = np.arange(n) / SR
    saw = sum(np.sin(2 * np.pi * freq * k * t) / k for k in range(1, 7))
    sub = np.sin(2 * np.pi * freq * t)
    return lowpass(saw * .5 + sub, 420) * env(n, .004, dur * .6)


def pad(freqs, dur):
    n = at(dur); t = np.arange(n) / SR
    l = np.zeros(n); r = np.zeros(n)
    for f in freqs:
        for det, side_ in ((-.11, 'l'), (0, 'c'), (.13, 'r')):
            ff = f * 2 ** (det / 12)
            v = sum(np.sin(2 * np.pi * ff * k * t + rng.uniform(0, 6)) / k for k in range(1, 9))
            if side_ != 'r':
                l += v
            if side_ != 'l':
                r += v
    e = np.minimum(1, t / .25) * np.minimum(1, (dur - t) / .3)
    return lowpass(l, 1900) * e, lowpass(r, 1900) * e


def impact(big=1.0):
    n = at(2.2); t = np.arange(n) / SR
    boom = np.sin(2 * np.pi * (38 + 60 * np.exp(-t * 12)) * t) * np.exp(-t * 2.2)
    air = lowpass(rng.standard_normal(n), 2500) * np.exp(-t * 3.2) * .35
    return np.tanh((boom + air) * 1.3) * big


def riser(dur, f0=300, f1=9000):
    n = at(dur)
    x = sweep_lp(rng.standard_normal(n), f0, f1)
    return x * np.linspace(0, 1, n) ** 2.2


def whoosh(dur=.45):
    n = at(dur)
    x = sweep_lp(rng.standard_normal(n), 400, 6000)
    return highpass(x, 250) * np.sin(np.linspace(0, np.pi, n)) ** 2


# ---------------------------------------------------------------- arrangement
NOTE = lambda m: 440 * 2 ** ((m - 69) / 12)  # noqa: E731  MIDI → Hz
CHORDS = [(57, [57, 60, 64]), (53, [53, 57, 60]), (48, [55, 60, 64]), (55, [55, 59, 62])]  # Am F C G (root, voicing)
beats = lambda a, b, step=BEAT: np.arange(a, b - 1e-9, step)  # noqa: E731

K = kick()
kicks = list(beats(2, 20)) + [20.0, 21.0] + list(beats(22, 24)) + [24.0]
for t in kicks:
    add(K, t, .95)
    i = at(t); n = min(at(.42), N - i)
    side[i:i + n] = np.minimum(side[i:i + n], 1 - .62 * np.exp(-np.arange(n) / SR / .11))

C = clap()
for t in list(beats(5 + BEAT, 20, 2 * BEAT)) + list(beats(22 + BEAT, 24, 2 * BEAT)):
    add(C, t, .42, pan=.08)
for t in beats(2 + BEAT / 2, 20, BEAT):
    add(hat(), t, .2, pan=-.25)
for t in beats(8, 20, BEAT / 2):
    add(hat(), t + BEAT / 4, .08, pan=.3)
for t in list(beats(8 + 1.75, 20, 2)) + [23.75]:
    add(hat(True), t, .14, pan=-.1)

# bass: 8th-note pulse on the chord root from the drop, sustained root in the intro
for bar in range(14):
    t0 = bar * 2.0
    root = NOTE(CHORDS[bar % 4][0] - 24)
    if 2 <= t0 < 8:
        add(bass(root, 1.9), t0, .38)
    elif 8 <= t0 < 20 or 22 <= t0 < 24:
        for k in range(8):
            add(bass(root, .24), t0 + k * BEAT / 2, .42 if k % 2 == 0 else .3)
    elif 20 <= t0 < 22:
        add(bass(root, 1.9), t0, .45)

# pads: whole track, swelling in the intro, sustained final chord
for bar in range(12):
    t0 = bar * 2.0
    l, r = pad([NOTE(m) for m in CHORDS[bar % 4][1]], 2.05)
    g = .05 if t0 < 2 else .075
    add(l, t0, g, pan=.4); add(r, t0, g, pan=-.4)
l, r = pad([NOTE(m) for m in (57, 60, 64, 69)], 4.0)
add(l, 24, .09, pan=.4); add(r, 24, .09, pan=-.4)

# FX: logo hit, whooshes on every cut, risers into the drop and the end card
add(impact(.55), .12)
add(riser(1.6, 200, 5000), .1, .18)
for cut in (2, 5, 8, 13, 16, 20, 24):
    add(whoosh(), cut - .38, .32)
add(riser(2.0), 6.0, .3)
add(riser(1.0), 23.0, .28)
add(impact(1.0), 8.0, .8)
add(impact(.7), 20.0, .7)
add(impact(1.0), 24.0, .85)

# ---------------------------------------------------------------- master
drums_free = np.ones(N)
mix_l, mix_r = L * side, R * side
fade = np.ones(N); fs = at(26.6); fade[fs:] = np.linspace(1, 0, N - fs) ** 1.5
fin = np.ones(N); fin[: at(.05)] = np.linspace(0, 1, at(.05))
mix_l *= fade * fin; mix_r *= fade * fin
peak = max(np.abs(mix_l).max(), np.abs(mix_r).max())
mix_l, mix_r = np.tanh(mix_l / peak * 1.25) / np.tanh(1.25) * .93, np.tanh(mix_r / peak * 1.25) / np.tanh(1.25) * .93
out = (np.stack([mix_l, mix_r], 1) * 32767).astype('<i2')
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'music.wav')
with wave.open(path, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes())
print(path, f'{T:.0f}s')
