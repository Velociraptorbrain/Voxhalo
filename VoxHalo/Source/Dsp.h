#pragma once
#include <cmath>
#include <vector>
#include <algorithm>

namespace vh
{
// RBJ biquad, transposed direct form II. No allocation, safe for the audio thread.
struct Biquad
{
    float b0 = 1.f, b1 = 0.f, b2 = 0.f, a1 = 0.f, a2 = 0.f, z1 = 0.f, z2 = 0.f;

    void reset() { z1 = z2 = 0.f; }

    float process (float x)
    {
        const float y = b0 * x + z1;
        z1 = b1 * x - a1 * y + z2;
        z2 = b2 * x - a2 * y;
        return y;
    }

    void set (double a0, double nb0, double nb1, double nb2, double na1, double na2)
    {
        b0 = (float) (nb0 / a0); b1 = (float) (nb1 / a0); b2 = (float) (nb2 / a0);
        a1 = (float) (na1 / a0); a2 = (float) (na2 / a0);
    }

    static double clampFreq (double sr, double f) { return std::min (std::max (f, 10.0), sr * 0.45); }

    void setHighPass (double sr, double f, double q = 0.7071)
    {
        const double w = 6.283185307179586 * clampFreq (sr, f) / sr, c = std::cos (w), al = std::sin (w) / (2.0 * q);
        set (1.0 + al, (1.0 + c) * 0.5, -(1.0 + c), (1.0 + c) * 0.5, -2.0 * c, 1.0 - al);
    }

    void setLowPass (double sr, double f, double q = 0.7071)
    {
        const double w = 6.283185307179586 * clampFreq (sr, f) / sr, c = std::cos (w), al = std::sin (w) / (2.0 * q);
        set (1.0 + al, (1.0 - c) * 0.5, 1.0 - c, (1.0 - c) * 0.5, -2.0 * c, 1.0 - al);
    }

    void setHighShelf (double sr, double f, double gainDb)
    {
        const double A = std::pow (10.0, gainDb / 40.0);
        const double w = 6.283185307179586 * clampFreq (sr, f) / sr, c = std::cos (w), s = std::sin (w);
        const double al = s * 0.5 * 1.41421356237;   // shelf slope S = 1
        const double sq = 2.0 * std::sqrt (A) * al;
        set ((A + 1) - (A - 1) * c + sq,
             A * ((A + 1) + (A - 1) * c + sq),
             -2.0 * A * ((A - 1) + (A + 1) * c),
             A * ((A + 1) + (A - 1) * c - sq),
             2.0 * ((A - 1) - (A + 1) * c),
             (A + 1) - (A - 1) * c - sq);
    }
};

// Circular delay line with linear interpolation.
struct DelayLine
{
    std::vector<float> buf;
    int size = 0, w = 0;

    void prepare (int n) { size = std::max (n, 8); buf.assign ((size_t) size, 0.f); w = 0; }

    // Read BEFORE pushing the current sample: d samples of delay.
    float read (float d) const
    {
        d = std::min (std::max (d, 1.f), (float) (size - 3));
        float rp = (float) w - d;
        while (rp < 0.f) rp += (float) size;
        const int i0 = (int) rp;
        const float fr = rp - (float) i0;
        const int i1 = (i0 + 1 >= size) ? 0 : i0 + 1;
        return buf[(size_t) i0] + (buf[(size_t) i1] - buf[(size_t) i0]) * fr;
    }

    void push (float x) { buf[(size_t) w] = x; if (++w >= size) w = 0; }
};
} // namespace vh
