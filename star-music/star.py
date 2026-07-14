from wave import open
from struct import Struct
from math import floor

frame_rate = 11025


def encode(x):
    i = int(16384 * x)
    return Struct("h").pack(i)


def play(sampler, name="star.wav", seconds=25):
    out = open(name, "wb")
    out.setnchannels(1)
    out.setsampwidth(2)
    out.setframerate(frame_rate)
    t = 0
    while t < seconds * frame_rate:
        sample = sampler(t)
        out.writeframes(encode(sample))
        t = t + 1
    out.close()


def tri(frequency, amplititude=0.3):
    period = frame_rate // frequency

    def sampler(t):
        saw_wave = t / period - floor(t / period + 0.5)
        tri_wave = 2 * abs(2 * saw_wave) - 1
        return amplititude * tri_wave

    return sampler


c_freq, d_freq, e_freq, f_freq, g_freq, a_freq, b_freq = (
    261.63,
    293.66,
    329.63,
    349.23,
    392.00,
    440.00,
    493.88,
)


def both(f, g):
    return lambda t: f(t) + g(t)


def note(f, start, end, fade=0.01):
    def sampler(t):
        seconds = t / frame_rate
        if seconds < start:
            return 0
        elif seconds > end:
            return 0
        elif seconds < start + fade:
            return (seconds - start) / fade * f(t)
        elif seconds > end - fade:
            return (end - seconds) / fade * f(t)
        else:
            return f(t)

    return sampler


def tune_at(octave):
    c, e = tri(octave * c_freq), tri(octave * e_freq)
    g, low_g = tri(octave * g_freq), tri(octave * g_freq / 2)
    d, f = tri(octave * d_freq), tri(octave * f_freq)
    a, b = tri(octave * a_freq), tri(octave * b_freq)
    return tune(a, b, c, d, e, f, g, low_g)


def tune(a, b, c, d, e, f, g, low_g):
    """
    z = 0
    song = note(e, z, z + 1 / 8)
    z += 1 / 8
    song = both(song, note(e, z, z + 1 / 8))
    z += 1 / 4
    song = both(song, note(e, z, z + 1 / 8))
    z += 1 / 4
    song = both(song, note(c, z, z + 1 / 8))
    z += 1 / 8
    song = both(song, note(e, z, z + 1 / 8))
    z += 1 / 4
    song = both(song, note(g, z, z + 1 / 4))
    z += 1 / 2
    song = both(song, note(low_g, z, z + 1 / 4))
    z += 1 / 2
    """
    z = 0
    song = note(c, z, z + 1)
    z += 1 / 2
    song = both(song, note(c, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(g, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(g, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(a, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(a, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(g, z, z + 1))
    # pause
    z += 1
    song = both(song, note(f, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(f, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(e, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(e, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(d, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(d, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(c, z, z + 1))
    # pause
    z += 1
    song = both(song, note(g, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(g, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(f, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(f, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(e, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(e, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(d, z, z + 1))
    # pause
    z += 1
    song = both(song, note(g, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(g, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(f, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(f, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(e, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(e, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(d, z, z + 1))
    # pause
    z += 1
    song = both(song, note(c, z, z + 1))
    z += 1 / 2
    song = both(song, note(c, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(g, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(g, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(a, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(a, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(g, z, z + 1))
    # pause
    z += 1
    song = both(song, note(f, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(f, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(e, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(e, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(d, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(d, z, z + 1 / 2))
    z += 1 / 2
    song = both(song, note(c, z, z + 1))
    z += 1

    return song


play(tune_at(1))
