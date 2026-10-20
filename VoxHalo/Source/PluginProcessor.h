#pragma once
#include <juce_audio_processors/juce_audio_processors.h>
#include <array>
#include "Params.h"
#include "Presets.h"
#include "Dsp.h"

class VoxHaloProcessor : public juce::AudioProcessor
{
public:
    VoxHaloProcessor();
    ~VoxHaloProcessor() override = default;

    void prepareToPlay (double sampleRate, int samplesPerBlock) override;
    void releaseResources() override {}
    bool isBusesLayoutSupported (const BusesLayout& layouts) const override;
    void processBlock (juce::AudioBuffer<float>&, juce::MidiBuffer&) override;

    juce::AudioProcessorEditor* createEditor() override;
    bool hasEditor() const override { return true; }

    const juce::String getName() const override { return "VoxHalo"; }
    bool acceptsMidi() const override { return false; }
    bool producesMidi() const override { return false; }
    bool isMidiEffect() const override { return false; }
    double getTailLengthSeconds() const override { return 6.0; }

    int getNumPrograms() override { return vh::kNumPresets; }
    int getCurrentProgram() override { return currentProgram; }
    void setCurrentProgram (int index) override;
    const juce::String getProgramName (int index) override;
    void changeProgramName (int, const juce::String&) override {}

    void getStateInformation (juce::MemoryBlock& destData) override;
    void setStateInformation (const void* data, int sizeInBytes) override;

    juce::AudioProcessorValueTreeState apvts;

private:
    static juce::AudioProcessorValueTreeState::ParameterLayout createLayout();

    std::array<std::atomic<float>*, vh::kNumFloat> pv {};
    std::atomic<float>* syncP = nullptr;
    std::atomic<float>* divP = nullptr;
    int currentProgram = 0;

    double sr = 44100.0;
    vh::Biquad hp[2], deEss[2], air[2], fbLP[2], fbHP[2];
    vh::DelayLine dl[2];
    juce::SmoothedValue<float> smIn, smOut, smMix, smEchoMix, smVerbMix, smDrive, smTime;
    float grDb = 0.f, deEnv = 0.f, lfoPhase = 0.f;
    juce::Reverb reverb;
    juce::AudioBuffer<float> dryBuf, verbBuf;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (VoxHaloProcessor)
};
