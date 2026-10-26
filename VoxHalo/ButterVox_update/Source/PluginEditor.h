#pragma once
#include <juce_audio_utils/juce_audio_utils.h>
#include "PluginProcessor.h"

// Draws the live parts of the Butter Vox interface on top of the baked artwork:
// melting-butter sliders, butter-dish knobs, brass-free pill buttons and the preset menu.
class ButterLookAndFeel : public juce::LookAndFeel_V4
{
public:
    ButterLookAndFeel();
    void drawLinearSlider (juce::Graphics&, int x, int y, int w, int h, float sliderPos,
                           float minPos, float maxPos, juce::Slider::SliderStyle, juce::Slider&) override;
    void drawRotarySlider (juce::Graphics&, int x, int y, int w, int h, float sliderPos,
                           float startAngle, float endAngle, juce::Slider&) override;
    void drawButtonBackground (juce::Graphics&, juce::Button&, const juce::Colour&, bool, bool) override;
    juce::Font getTextButtonFont (juce::TextButton&, int buttonHeight) override;
    void drawComboBox (juce::Graphics&, int w, int h, bool, int, int, int, int, juce::ComboBox&) override;
    juce::Font getComboBoxFont (juce::ComboBox&) override;
    void positionComboBoxText (juce::ComboBox&, juce::Label&) override;
    int getSliderThumbRadius (juce::Slider&) override { return 14; }
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
    ButterLookAndFeel laf;
    std::unique_ptr<Content> content;
    juce::TooltipWindow tooltip { this, 450 };

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (VoxHaloEditor)
};
