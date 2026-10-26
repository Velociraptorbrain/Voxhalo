#include "PluginProcessor.h"
#include "PluginEditor.h"

using namespace juce;

VoxHaloProcessor::VoxHaloProcessor()
    : AudioProcessor (BusesProperties()
                          .withInput  ("Input",  AudioChannelSet::stereo(), true)
                          .withOutput ("Output", AudioChannelSet::stereo(), true)),
      apvts (*this, nullptr, "STATE", createLayout())
{
    for (int i = 0; i < vh::kNumFloat; ++i)
        pv[(size_t) i] = apvts.getRawParameterValue (vh::kParams[i].id);
    syncP = apvts.getRawParameterValue ("sync");
    divP  = apvts.getRawParameterValue ("division");
}

AudioProcessorValueTreeState::ParameterLayout VoxHaloProcessor::createLayout()
{
    AudioProcessorValueTreeState::ParameterLayout layout;

    for (int i = 0; i < vh::kNumFloat; ++i)
    {
        const auto& p = vh::kParams[i];
        NormalisableRange<float> range (p.lo, p.hi);
        if (p.centre > 0.f)
            range.setSkewForCentre (p.centre);

        const String unit (p.unit);
        auto attrs = AudioParameterFloatAttributes()
                         .withLabel (unit)
                         .withStringFromValueFunction ([unit] (float v, int) { return vh::formatValue (v, unit); })
                         .withValueFromStringFunction ([unit] (const String& t) { return vh::parseValue (t, unit); });

        layout.add (std::make_unique<AudioParameterFloat> (ParameterID { p.id, 1 }, p.name, range, p.def, attrs));
    }

    layout.add (std::make_unique<AudioParameterBool>   (ParameterID { "sync", 1 },     "Sync", false));
    layout.add (std::make_unique<AudioParameterChoice> (ParameterID { "division", 1 }, "Division", vh::kDivisions, 5));
    return layout;
}

bool VoxHaloProcessor::isBusesLayoutSupported (const BusesLayout& l) const
{
    return l.getMainInputChannelSet() == AudioChannelSet::stereo()
        && l.getMainOutputChannelSet() == AudioChannelSet::stereo();
}

void VoxHaloProcessor::prepareToPlay (double sampleRate, int samplesPerBlock)
{
    sr = sampleRate;
    const int maxBlock = jmax (samplesPerBlock, 1);

    for (int c = 0; c < 2; ++c)
    {
        dl[c].prepare ((int) (sr * 3.0) + 8);
        hp[c].reset(); deEss[c].reset(); air[c].reset(); fbLP[c].reset(); fbHP[c].reset();
        deEss[c].setHighPass (sr, 6500.0);
        glHP[c].reset();
        glHP[c].setHighPass (sr, 1800.0);
        shim[c].prepare ((int) (sr * 0.1) + 16);
    }

    dryBuf.setSize (2, maxBlock);
    verbBuf.setSize (2, maxBlock);
    reverb.setSampleRate (sr);
    reverb.reset();

    auto init = [this] (SmoothedValue<float>& s, float v, double secs)
    {
        s.reset (sr, secs);
        s.setCurrentAndTargetValue (v);
    };
    init (smIn,      Decibels::decibelsToGain (pv[vh::pIn]->load()),  0.05);
    init (smOut,     Decibels::decibelsToGain (pv[vh::pOut]->load()), 0.05);
    init (smMix,     pv[vh::pMix]->load(),      0.05);
    init (smEchoMix, pv[vh::pEchoMix]->load(),  0.05);
    init (smVerbMix, pv[vh::pVerbMix]->load(),  0.05);
    init (smDrive,   pv[vh::pDrive]->load(),    0.05);
    init (smGlitter, pv[vh::pGlitter]->load(),  0.05);
    init (smTime,    pv[vh::pTime]->load(),     0.12);

    grDb = deEnv = lfoPhase = 0.f;
}

void VoxHaloProcessor::processBlock (AudioBuffer<float>& buffer, MidiBuffer&)
{
    ScopedNoDenormals noDenormals;
    const int n = buffer.getNumSamples();
    if (buffer.getNumChannels() < 2 || n == 0)
        return;

    if (dryBuf.getNumSamples() < n)
    {
        dryBuf.setSize (2, n, false, false, true);
        verbBuf.setSize (2, n, false, false, true);
    }

    float* L = buffer.getWritePointer (0);
    float* R = buffer.getWritePointer (1);
    float* dryL = dryBuf.getWritePointer (0);
    float* dryR = dryBuf.getWritePointer (1);

    auto P = [this] (int i) { return pv[(size_t) i]->load(); };

    // ---- block-rate parameters ----
    smIn.setTargetValue      (Decibels::decibelsToGain (P (vh::pIn)));
    smOut.setTargetValue     (Decibels::decibelsToGain (P (vh::pOut)));
    smMix.setTargetValue     (P (vh::pMix));
    smEchoMix.setTargetValue (P (vh::pEchoMix));
    smVerbMix.setTargetValue (P (vh::pVerbMix));
    smDrive.setTargetValue   (P (vh::pDrive));
    smGlitter.setTargetValue (P (vh::pGlitter));

    double bpm = 120.0;
    if (auto* ph = getPlayHead())
        if (auto pos = ph->getPosition())
            if (auto b = pos->getBpm())
                if (*b > 20.0 && *b < 400.0)
                    bpm = *b;

    const bool sync = syncP->load() > 0.5f;
    const int div = jlimit (0, (int) vh::kDivisions.size() - 1, (int) divP->load());
    float timeMs = sync ? (float) (vh::kDivBeats[div] * 60000.0 / bpm) : P (vh::pTime);
    timeMs = jlimit (5.f, 2900.f, timeMs);
    smTime.setTargetValue (timeMs);

    for (int c = 0; c < 2; ++c)
    {
        hp[c].setHighPass (sr, P (vh::pLowCut));
        air[c].setHighShelf (sr, 9000.0, P (vh::pAir));
        fbLP[c].setLowPass (sr, P (vh::pEchoHi));
        fbHP[c].setHighPass (sr, P (vh::pEchoLo));
    }

    // de-esser
    const float deAmt = P (vh::pDeEss);
    const float deThr = 0.04f;
    const float deAtt = 1.f - std::exp (-1.f / (0.0005f * (float) sr));
    const float deRel = 1.f - std::exp (-1.f / (0.03f * (float) sr));

    // compressor (one-knob)
    const float sq = P (vh::pSquash);
    const float thr = -4.f - sq * 30.f;
    const float ratio = 1.5f + sq * 7.5f;
    const float makeup = (-thr) * (1.f - 1.f / ratio) * 0.45f;
    const float cAtt = 1.f - std::exp (-1.f / (jmax (0.1f, P (vh::pAttack)) * 0.001f * (float) sr));
    const float cRel = 1.f - std::exp (-1.f / (jmax (5.f,  P (vh::pRelease)) * 0.001f * (float) sr));

    // delay
    const float fb = P (vh::pFeedback);
    const float spread = P (vh::pSpread);
    const float modDepth = P (vh::pModDepth);
    const float lfoInc = MathConstants<float>::twoPi * P (vh::pModRate) / (float) sr;
    const float modSamples = modDepth * 0.008f * (float) sr;   // up to +/- 8 ms

    for (int i = 0; i < n; ++i)
    {
        const float gIn = smIn.getNextValue();
        float l = L[i] * gIn, r = R[i] * gIn;
        dryL[i] = l; dryR[i] = r;

        // 1. low cut
        l = hp[0].process (l);
        r = hp[1].process (r);

        // 2. de-ess
        {
            const float sl = deEss[0].process (l), sr2 = deEss[1].process (r);
            const float e = jmax (std::abs (sl), std::abs (sr2));
            deEnv += (e > deEnv ? deAtt : deRel) * (e - deEnv);
            float g = 1.f;
            if (deAmt > 0.001f && deEnv > deThr)
                g = std::pow (deThr / deEnv, deAmt * 0.9f);
            l -= sl * (1.f - g);
            r -= sr2 * (1.f - g);
        }

        // 3. squash
        {
            const float lvl = jmax (std::abs (l), std::abs (r));
            const float lvlDb = Decibels::gainToDecibels (lvl, -100.f);
            const float target = lvlDb > thr ? (lvlDb - thr) * (1.f - 1.f / ratio) : 0.f;
            grDb += (target > grDb ? cAtt : cRel) * (target - grDb);
            const float cg = Decibels::decibelsToGain (makeup - grDb);
            l *= cg; r *= cg;
        }

        // 4. glow: saturation then air shelf
        {
            const float dr = smDrive.getNextValue();
            if (dr > 0.001f)
            {
                const float g = 1.f + dr * 5.f;
                const float comp = 1.f / (1.f + dr * 1.5f);
                l = std::tanh (l * g) * comp;
                r = std::tanh (r * g) * comp;
            }
            l = air[0].process (l);
            r = air[1].process (r);
        }

        // 5. echo
        {
            const float tms = smTime.getNextValue();
            const float d = tms * 0.001f * (float) sr;
            const float lfo = std::sin (lfoPhase);
            lfoPhase += lfoInc;
            if (lfoPhase > MathConstants<float>::twoPi) lfoPhase -= MathConstants<float>::twoPi;

            const float dlL = dl[0].read (d + lfo * modSamples);
            const float dlR = dl[1].read (d - lfo * modSamples);

            const float fbL = std::tanh (fbHP[0].process (fbLP[0].process ((1.f - spread) * dlL + spread * dlR)) * fb);
            const float fbR = std::tanh (fbHP[1].process (fbLP[1].process ((1.f - spread) * dlR + spread * dlL)) * fb);

            dl[0].push (l + fbL);
            dl[1].push (r * (1.f - 0.9f * spread) + fbR);

            const float em = smEchoMix.getNextValue();
            l += dlL * em;
            r += dlR * em;
        }

        L[i] = l; R[i] = r;
    }

    // 6. halo reverb, fed by the post-delay signal so the echoes bloom
    verbBuf.copyFrom (0, 0, buffer, 0, 0, n);
    verbBuf.copyFrom (1, 0, buffer, 1, 0, n);
    {
        Reverb::Parameters rp;
        rp.roomSize = P (vh::pSize);
        rp.damping  = P (vh::pDamp);
        rp.wetLevel = 0.33f;
        rp.dryLevel = 0.f;
        rp.width    = 1.f;
        rp.freezeMode = 0.f;
        reverb.setParameters (rp);
        reverb.processStereo (verbBuf.getWritePointer (0), verbBuf.getWritePointer (1), n);
    }

    const float* vL = verbBuf.getReadPointer (0);
    const float* vR = verbBuf.getReadPointer (1);

    // 7. glitter shimmer, melt mix, dry/wet, output
    const float shimWin = 0.045f * (float) sr;
    for (int i = 0; i < n; ++i)
    {
        const float vm = smVerbMix.getNextValue() * 0.9f;
        const float m = smMix.getNextValue();
        const float og = smOut.getNextValue();
        const float gl = smGlitter.getNextValue();
        float rl = vL[i], rr = vR[i];
        const float sl = glHP[0].process (shim[0].process (rl, 2.0f, shimWin));
        const float sr2 = glHP[1].process (shim[1].process (rr, 2.0f, shimWin));
        rl += sl * gl * 1.4f;
        rr += sr2 * gl * 1.4f;
        const float wl = L[i] + rl * vm;
        const float wr = R[i] + rr * vm;
        L[i] = (dryL[i] * (1.f - m) + wl * m) * og;
        R[i] = (dryR[i] * (1.f - m) + wr * m) * og;
    }

    const float pk = jmax (buffer.getMagnitude (0, 0, n), buffer.getMagnitude (1, 0, n));
    if (pk > meterLevel.load())
        meterLevel.store (pk);
}

// ---- presets / state ----
const String VoxHaloProcessor::getProgramName (int index)
{
    return juce::isPositiveAndBelow (index, vh::kNumPresets) ? String (vh::kPresets[index].name) : String();
}

void VoxHaloProcessor::setCurrentProgram (int index)
{
    if (! juce::isPositiveAndBelow (index, vh::kNumPresets))
        return;

    currentProgram = index;
    const auto& pr = vh::kPresets[index];

    for (int i = 0; i < vh::kNumFloat; ++i)
        if (auto* p = apvts.getParameter (vh::kParams[i].id))
            p->setValueNotifyingHost (p->convertTo0to1 (pr.v[i]));

    if (auto* p = apvts.getParameter ("sync"))
        p->setValueNotifyingHost (pr.sync ? 1.f : 0.f);
    if (auto* p = apvts.getParameter ("division"))
        p->setValueNotifyingHost (p->convertTo0to1 ((float) pr.division));
}

void VoxHaloProcessor::getStateInformation (MemoryBlock& destData)
{
    auto state = apvts.copyState();
    state.setProperty ("program", currentProgram, nullptr);
    if (auto xml = state.createXml())
        copyXmlToBinary (*xml, destData);
}

void VoxHaloProcessor::setStateInformation (const void* data, int sizeInBytes)
{
    if (auto xml = getXmlFromBinary (data, sizeInBytes))
        if (xml->hasTagName (apvts.state.getType()))
        {
            auto tree = ValueTree::fromXml (*xml);
            currentProgram = jlimit (0, vh::kNumPresets - 1, (int) tree.getProperty ("program", 0));
            apvts.replaceState (tree);
        }
}

AudioProcessorEditor* VoxHaloProcessor::createEditor() { return new VoxHaloEditor (*this); }

AudioProcessor* JUCE_CALLTYPE createPluginFilter() { return new VoxHaloProcessor(); }
