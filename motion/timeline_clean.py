"""Beat-synced edit for oneflow-clean: the scenes are authored on an internal timeline (0–49.8 s); playback is
time-warped so that every scene change lands on a beat of the 128 BPM track. Shared by build_clean.py (JS warp,
camera hits, beat pulse) and music_clean.py (arrangement + UI sounds placed on the real timeline).
"""
BPM = 128
B = 60 / BPM
# (internal time of a scene change, beat it lands on in the real video)
ANCH = [(0, 0), (1.5, 3), (2.9, 5.5), (4.02, 8), (4.35, 8.5), (5.85, 11), (7.95, 14), (9.22, 16), (10.45, 18), (12.42, 21),
        (13.95, 24), (16.05, 28), (17.32, 30), (18.05, 31.5), (19.95, 35), (21.7, 38), (22.55, 40), (24.15, 44), (28.6, 52),
        (30.0, 55), (31.35, 57), (33.35, 60), (34.6, 62), (40.55, 72), (41.95, 75), (42.85, 77), (44.7, 80), (46.9, 84), (49.8, 90)]
DUR = ANCH[-1][1] * B  # 42.19 s
# camera hits on scene changes: punch = zoom kick, whip = horizontal whip-pan, flash = white flash + zoom
CUTS = [(8, 'flash'), (11, 'punch'), (16, 'whip'), (21, 'flash'), (24, 'whip'), (28, 'punch'), (31.5, 'punch'), (35, 'whip'),
        (44, 'flash'), (52, 'whip'), (57, 'punch'), (60, 'flash'), (72, 'whip'), (77, 'punch'), (84, 'flash')]
# beats where the four-on-the-floor kick plays (half-open ranges)
KICK = [(8, 40), (44, 76)]


def real(ti):
    """Internal (authored) time → real video time."""
    for (a, ba), (b, bb) in zip(ANCH, ANCH[1:]):
        if ti <= b:
            return (ba + (bb - ba) * (ti - a) / (b - a)) * B
    return DUR


def kick_on(beat):
    return any(a <= beat < b for a, b in KICK)
