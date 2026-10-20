#pragma once
#include <juce_audio_utils/juce_audio_utils.h>
#include "PluginProcessor.h"

// Draws the vertical sliders: glowing groove, colour fill, glassy thumb.
class VoxLookAndFeel : public juce::LookAndFeel_V4
{
public:
    VoxLookAndFeel();
    void drawLinearSlider (juce::Graphics&, int x, int y, int w, int h, float sliderPos,
                           float minPos, float maxPos, juce::Slider::SliderStyle, juce::Slider&) override;
    void drawButtonBackground (juce::Graphics&, juce::Button&, const juce::Colour&, bool, bool) override;
    int getSliderThumbRadius (juce::Slider&) override { return 8; }
};

// All widgets live in a fixed-size "content" component that is scaled to the window,
// so the whole UI resizes smoothly with the corner handle.
class VoxHaloEditor : public juce::AudioProcessorEditor
{
public:
    explicit VoxHaloEditor (VoxHaloProcessor&);
    ~VoxHaloEditor() override;
    void resized() override;

    static constexpr int kW = 1200, kH = 480;

private:
    class Content;
    VoxLookAndFeel laf;
    std::unique_ptr<Content> content;
    juce::TooltipWindow tooltip { this, 450 };

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (VoxHaloEditor)
};
