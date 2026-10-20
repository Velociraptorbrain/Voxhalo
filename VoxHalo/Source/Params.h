#pragma once
#include <juce_audio_processors/juce_audio_processors.h>

// Single source of truth for every parameter. The processor, the editor,
// the presets and the tooltips all read from this table.
namespace vh
{
struct ParamInfo
{
    const char* id;
    const char* name;
    const char* unit;   // "%", "dB", "Hz", "hz" (two decimals), "ms", ""
    float lo, hi, def, centre;   // centre > 0 adds a skew so the middle of the slider sits at "centre"
    const char* tip;
};

enum ParamIndex
{
    pIn, pLowCut, pDeEss, pSquash, pAttack, pRelease, pDrive, pAir,
    pTime, pFeedback, pEchoHi, pEchoLo, pModRate, pModDepth, pSpread, pEchoMix,
    pSize, pDamp, pVerbMix, pMix, pOut,
    kNumFloat
};

inline const ParamInfo kParams[kNumFloat] =
{
    { "in",       "Input",     "dB", -24.f, 12.f,   0.f,    0.f,   "Input level into the chain. Lower it if your vocal is hot, raise it for quiet takes." },
    { "lowcut",   "Low Cut",   "Hz",  20.f, 400.f,  80.f,  100.f,  "High-pass filter. Removes rumble, plosives and proximity boom before anything else." },
    { "deess",    "De-Ess",    "%",    0.f, 1.f,    0.3f,   0.f,   "Tames harsh S and T sounds. Raise it until sibilance sounds smooth." },
    { "squash",   "Squash",    "%",    0.f, 1.f,    0.4f,   0.f,   "One-knob compressor. Sets threshold and ratio together for an even, upfront vocal." },
    { "attack",   "Attack",    "ms",   0.1f, 80.f,  8.f,    10.f,  "How fast the compressor reacts. Slower keeps punch, faster smooths peaks." },
    { "release",  "Release",   "ms",  20.f, 800.f, 160.f,  150.f,  "How fast the compressor lets go. Short is lively, long is smooth." },
    { "drive",    "Drive",     "%",    0.f, 1.f,    0.15f,  0.f,   "Warm tube-style saturation. Adds harmonics and presence." },
    { "air",      "Air",       "dB",  -6.f, 9.f,    2.f,    0.f,   "High-shelf boost or cut at 9 kHz. Adds sparkle or softens a bright vocal." },
    { "time",     "Time",      "ms",  20.f, 1500.f, 320.f, 300.f,  "Delay time in milliseconds. Greyed out while Sync is on." },
    { "feedback", "Feedback",  "%",    0.f, 0.95f,  0.35f,  0.f,   "How many repeats the delay makes. Higher values give longer echo trails." },
    { "echohi",   "Hi Cut",    "Hz", 1000.f, 20000.f, 6000.f, 5000.f, "Low-pass filter inside the feedback loop. Each repeat gets darker as it fades." },
    { "echolo",   "Lo Cut",    "Hz",  20.f, 1000.f, 150.f, 200.f,  "High-pass filter inside the feedback loop. Keeps repeats thin and out of the way of the vocal." },
    { "modrate",  "Mod Rate",  "hz",  0.05f, 8.f,   0.6f,   1.f,   "Speed of the delay-time wobble. Slow gives gentle chorus, fast gives warble." },
    { "moddepth", "Mod Depth", "%",    0.f, 1.f,    0.15f,  0.f,   "Amount of delay-time wobble. Adds tape-style movement and width." },
    { "spread",   "Spread",    "%",    0.f, 1.f,    0.5f,   0.f,   "Stereo ping-pong amount. 0% is centered, 100% bounces left and right." },
    { "echomix",  "Echo Mix",  "%",    0.f, 1.f,    0.25f,  0.f,   "Level of the delay added to your vocal." },
    { "size",     "Size",      "%",    0.f, 1.f,    0.4f,   0.f,   "Room size of the halo reverb, from a small booth to a cathedral." },
    { "damp",     "Damp",      "%",    0.f, 1.f,    0.5f,   0.f,   "High-frequency damping of the reverb. Higher is darker and softer." },
    { "verbmix",  "Halo Mix",  "%",    0.f, 1.f,    0.15f,  0.f,   "Level of the reverb added after the delay, so echoes bloom into the space." },
    { "mix",      "Mix",       "%",    0.f, 1.f,    1.f,    0.f,   "Blend between your dry input (0%) and the full chain (100%)." },
    { "out",      "Output",    "dB", -24.f, 12.f,   0.f,    0.f,   "Final output level." },
};

inline const juce::StringArray kDivisions { "1/16", "1/8T", "1/8", "1/8D", "1/4T", "1/4", "1/4D", "1/2", "1/1" };
inline const float kDivBeats[] = { 0.25f, 1.f / 3.f, 0.5f, 0.75f, 2.f / 3.f, 1.f, 1.5f, 2.f, 4.f };
inline const char* kSyncTip = "Locks the delay to your DAW tempo. When on, the Division menu sets the note length.";
inline const char* kDivTip  = "Note length used when Sync is on. T = triplet, D = dotted.";

inline juce::String formatValue (float v, const juce::String& unit)
{
    if (unit == "%")  return juce::String (juce::roundToInt (v * 100.f)) + "%";
    if (unit == "dB") return juce::String (v, 1) + " dB";
    if (unit == "Hz") return v >= 1000.f ? juce::String (v / 1000.f, 1) + " kHz" : juce::String (juce::roundToInt (v)) + " Hz";
    if (unit == "hz") return juce::String (v, 2) + " Hz";
    if (unit == "ms") return (v < 100.f ? juce::String (v, 1) : juce::String (juce::roundToInt (v))) + " ms";
    return juce::String (v, 2);
}

inline float parseValue (const juce::String& t, const juce::String& unit)
{
    float v = t.retainCharacters ("0123456789.-").getFloatValue();
    if (t.containsIgnoreCase ("k")) v *= 1000.f;
    if (unit == "%") v *= 0.01f;
    return v;
}
} // namespace vh
