#include "PluginEditor.h"

using namespace juce;

namespace
{
const Colour kCyan   { 0xff22d3ee };
const Colour kPink   { 0xfff472b6 };
const Colour kAmber  { 0xfffbbf24 };
const Colour kViolet { 0xff8b6cff };
const Colour kMint   { 0xff34f5c5 };
const Colour kCoral  { 0xffff6b4a };

struct Group { const char* title; std::vector<int> ids; Colour colour; };

const std::vector<Group>& groups()
{
    static const std::vector<Group> g
    {
        { "INPUT + CLEAN", { vh::pIn, vh::pLowCut, vh::pDeEss },                                                   kCyan },
        { "SQUASH",        { vh::pSquash, vh::pAttack, vh::pRelease },                                             kPink },
        { "GLOW",          { vh::pDrive, vh::pAir },                                                               kAmber },
        { "ECHO",          { vh::pTime, vh::pFeedback, vh::pEchoHi, vh::pEchoLo, vh::pModRate, vh::pModDepth,
                             vh::pSpread, vh::pEchoMix },                                                          kViolet },
        { "HALO",          { vh::pSize, vh::pDamp, vh::pVerbMix },                                                 kMint },
        { "OUTPUT",        { vh::pMix, vh::pOut },                                                                 kCoral },
    };
    return g;
}

constexpr int kColW = 48, kPad = 10, kGap = 8, kMargin = 12, kPanelY = 78, kPanelH = 350;
}

//==============================================================================
VoxLookAndFeel::VoxLookAndFeel()
{
    setColour (ResizableWindow::backgroundColourId, Colour (0xff0b0f24));
    setColour (Label::textColourId, Colours::white);
    setColour (Slider::textBoxTextColourId, Colours::white.withAlpha (0.92f));
    setColour (Slider::textBoxBackgroundColourId, Colours::transparentBlack);
    setColour (Slider::textBoxOutlineColourId, Colours::transparentBlack);
    setColour (TextButton::buttonColourId, Colour (0xff222850));
    setColour (TextButton::buttonOnColourId, kViolet);
    setColour (TextButton::textColourOffId, Colours::white);
    setColour (TextButton::textColourOnId, Colours::white);
    setColour (ComboBox::backgroundColourId, Colour (0xff1a2046));
    setColour (ComboBox::textColourId, Colours::white);
    setColour (ComboBox::outlineColourId, Colour (0xff3a4280));
    setColour (ComboBox::arrowColourId, kCyan);
    setColour (PopupMenu::backgroundColourId, Colour (0xff151a3a));
    setColour (PopupMenu::textColourId, Colours::white);
    setColour (PopupMenu::highlightedBackgroundColourId, kViolet);
    setColour (PopupMenu::highlightedTextColourId, Colours::white);
    setColour (TooltipWindow::backgroundColourId, Colour (0xff12183a));
    setColour (TooltipWindow::textColourId, Colours::white);
    setColour (TooltipWindow::outlineColourId, kCyan);
}

void VoxLookAndFeel::drawLinearSlider (Graphics& g, int x, int y, int w, int h, float sliderPos,
                                       float, float, Slider::SliderStyle style, Slider& s)
{
    if (style != Slider::LinearVertical)
    {
        LookAndFeel_V4::drawLinearSlider (g, x, y, w, h, sliderPos, 0.f, 0.f, style, s);
        return;
    }

    const auto accent = s.findColour (Slider::trackColourId);
    const float alpha = s.isEnabled() ? 1.f : 0.3f;
    const float cx = (float) x + (float) w * 0.5f;
    const float trackW = 6.f;
    const Rectangle<float> groove (cx - trackW * 0.5f, (float) y + 8.f, trackW, (float) h - 16.f);
    const float pos = jlimit (groove.getY(), groove.getBottom(), sliderPos);

    // tick marks
    g.setColour (Colours::white.withAlpha (0.12f * alpha));
    for (int i = 0; i <= 10; ++i)
    {
        const float ty = groove.getBottom() - groove.getHeight() * (float) i / 10.f;
        const float len = (i % 5 == 0) ? 9.f : 5.f;
        g.drawLine (cx - trackW * 0.5f - 3.f - len, ty, cx - trackW * 0.5f - 3.f, ty, 1.f);
        g.drawLine (cx + trackW * 0.5f + 3.f, ty, cx + trackW * 0.5f + 3.f + len, ty, 1.f);
    }

    // groove
    g.setColour (Colour (0xff060914).withAlpha (alpha));
    g.fillRoundedRectangle (groove, trackW * 0.5f);
    g.setColour (Colours::white.withAlpha (0.1f * alpha));
    g.drawRoundedRectangle (groove, trackW * 0.5f, 1.f);

    // fill from the bottom to the thumb
    const Rectangle<float> fill (groove.getX(), pos, groove.getWidth(), groove.getBottom() - pos);
    g.setGradientFill (ColourGradient (accent.brighter (0.5f).withAlpha (alpha), cx, pos,
                                       accent.darker (0.7f).withAlpha (alpha), cx, groove.getBottom(), false));
    g.fillRoundedRectangle (fill, trackW * 0.5f);

    // thumb with glow
    const float tw = (float) w * 0.8f, th = 16.f;
    const Rectangle<float> thumb (cx - tw * 0.5f, pos - th * 0.5f, tw, th);
    g.setColour (accent.withAlpha ((s.isMouseOverOrDragging() ? 0.55f : 0.28f) * alpha));
    g.fillRoundedRectangle (thumb.expanded (3.f), th * 0.5f + 3.f);
    g.setGradientFill (ColourGradient (Colour (0xfff7f9ff).withAlpha (alpha), thumb.getX(), thumb.getY(),
                                       Colour (0xff9aa5cf).withAlpha (alpha), thumb.getX(), thumb.getBottom(), false));
    g.fillRoundedRectangle (thumb, 5.f);
    g.setColour (accent.withAlpha (alpha));
    g.fillRoundedRectangle (thumb.getCentreX() - tw * 0.3f, thumb.getCentreY() - 1.f, tw * 0.6f, 2.f, 1.f);
}

void VoxLookAndFeel::drawButtonBackground (Graphics& g, Button& b, const Colour& bg, bool over, bool down)
{
    auto r = b.getLocalBounds().toFloat().reduced (0.5f);
    auto c = b.getToggleState() ? b.findColour (TextButton::buttonOnColourId) : bg;
    if (over) c = c.brighter (0.15f);
    if (down) c = c.darker (0.2f);
    if (! b.isEnabled()) c = c.withAlpha (0.4f);
    g.setColour (c);
    g.fillRoundedRectangle (r, 6.f);
    g.setColour (Colours::white.withAlpha (0.18f));
    g.drawRoundedRectangle (r, 6.f, 1.f);
}

//==============================================================================
class VoxHaloEditor::Content : public Component, private Timer
{
public:
    explicit Content (VoxHaloProcessor& p) : proc (p)
    {
        for (const auto& grp : groups())
            for (int id : grp.ids)
                colourOf[(size_t) id] = grp.colour;

        for (int i = 0; i < vh::kNumFloat; ++i)
        {
            auto& s = strips[(size_t) i];
            const auto& info = vh::kParams[i];

            s.slider.setSliderStyle (Slider::LinearVertical);
            s.slider.setTextBoxStyle (Slider::TextBoxBelow, false, kColW, 20);
            s.slider.setColour (Slider::trackColourId, colourOf[(size_t) i]);
            s.slider.setTooltip (String (info.tip) + "\n(Double-click to reset)");
            addAndMakeVisible (s.slider);

            s.label.setText (info.name, dontSendNotification);
            s.label.setJustificationType (Justification::centred);
            s.label.setFont (Font (11.f, Font::bold));
            s.label.setInterceptsMouseClicks (false, false);
            addAndMakeVisible (s.label);

            s.att = std::make_unique<AudioProcessorValueTreeState::SliderAttachment> (proc.apvts, info.id, s.slider);
        }

        syncBtn.setButtonText ("SYNC");
        syncBtn.setClickingTogglesState (true);
        syncBtn.setTooltip (vh::kSyncTip);
        addAndMakeVisible (syncBtn);
        syncAtt = std::make_unique<AudioProcessorValueTreeState::ButtonAttachment> (proc.apvts, "sync", syncBtn);

        divBox.addItemList (vh::kDivisions, 1);
        divBox.setTooltip (vh::kDivTip);
        addAndMakeVisible (divBox);
        divAtt = std::make_unique<AudioProcessorValueTreeState::ComboBoxAttachment> (proc.apvts, "division", divBox);

        StringArray names;
        for (int i = 0; i < vh::kNumPresets; ++i)
            names.add (vh::kPresets[i].name);
        presetBox.addItemList (names, 1);
        presetBox.setTooltip ("Choose one of the 20 factory presets.");
        presetBox.setSelectedItemIndex (proc.getCurrentProgram(), dontSendNotification);
        presetBox.onChange = [this] { proc.setCurrentProgram (presetBox.getSelectedItemIndex()); };
        addAndMakeVisible (presetBox);

        prevBtn.setButtonText ("<");
        nextBtn.setButtonText (">");
        prevBtn.setTooltip ("Previous preset");
        nextBtn.setTooltip ("Next preset");
        prevBtn.onClick = [this] { step (-1); };
        nextBtn.onClick = [this] { step (1); };
        addAndMakeVisible (prevBtn);
        addAndMakeVisible (nextBtn);

        setSize (VoxHaloEditor::kW, VoxHaloEditor::kH);
        refreshState();
        startTimerHz (10);
    }

    void paint (Graphics& g) override
    {
        g.setGradientFill (ColourGradient (Colour (0xff1a1f4a), 0.f, 0.f, Colour (0xff080b1c), 0.f, (float) getHeight(), false));
        g.fillAll();

        // soft colour glows
        g.setGradientFill (ColourGradient (kViolet.withAlpha (0.20f), 200.f, 20.f, Colours::transparentBlack, 200.f, 260.f, true));
        g.fillRect (getLocalBounds());
        g.setGradientFill (ColourGradient (kCyan.withAlpha (0.10f), (float) getWidth() - 100.f, (float) getHeight(), Colours::transparentBlack, (float) getWidth() - 100.f, (float) getHeight() - 300.f, true));
        g.fillRect (getLocalBounds());

        // logo: halo ring + wordmark
        g.setGradientFill (ColourGradient (kCyan, 24.f, 16.f, kPink, 62.f, 54.f, false));
        g.drawEllipse (24.f, 16.f, 38.f, 38.f, 5.f);
        g.setColour (Colours::white);
        g.fillEllipse (38.f, 30.f, 10.f, 10.f);

        g.setGradientFill (ColourGradient (Colours::white, 76.f, 14.f, kCyan.brighter (0.3f), 250.f, 50.f, false));
        g.setFont (Font (32.f, Font::bold));
        g.drawText ("VOXHALO", 74, 10, 230, 40, Justification::centredLeft);
        g.setColour (Colours::white.withAlpha (0.6f));
        g.setFont (Font (11.f));
        g.drawText ("VOCAL CHAIN + HYBRID ECHO", 76, 48, 240, 16, Justification::centredLeft);

        // panels
        for (size_t i = 0; i < panels.size(); ++i)
        {
            const auto r = panels[i].toFloat();
            const auto c = groups()[i].colour;
            g.setColour (c.withAlpha (0.08f));
            g.fillRoundedRectangle (r, 12.f);
            g.setColour (c.withAlpha (0.55f));
            g.drawRoundedRectangle (r.reduced (0.5f), 12.f, 1.5f);

            g.setColour (c);
            g.setFont (Font (13.f, Font::bold));
            g.drawText (groups()[i].title, panels[i].getX() + 12, panels[i].getY() + 4, panels[i].getWidth() - 24, 24, Justification::centredLeft);
            g.setColour (c.withAlpha (0.35f));
            g.drawLine (r.getX() + 10.f, r.getY() + 30.f, r.getRight() - 10.f, r.getY() + 30.f, 1.f);
        }

        g.setColour (Colours::white.withAlpha (0.45f));
        g.setFont (Font (11.f));
        g.drawText ("Hover any control for a tip  |  Double-click a slider to reset  |  Drag the bottom-right corner to resize",
                    12, getHeight() - 38, getWidth() - 24, 20, Justification::centred);
    }

    void resized() override
    {
        panels.clear();
        int x = kMargin;

        for (const auto& grp : groups())
        {
            const int cols = (int) grp.ids.size();
            const Rectangle<int> panel (x, kPanelY, cols * kColW + 2 * kPad, kPanelH);
            panels.push_back (panel);

            for (int k = 0; k < cols; ++k)
            {
                auto& s = strips[(size_t) grp.ids[(size_t) k]];
                const int cx = panel.getX() + kPad + k * kColW;
                s.label.setBounds (cx, panel.getY() + 36, kColW, 18);
                s.slider.setBounds (cx, panel.getY() + 58, kColW, panel.getHeight() - 66);
            }
            x += panel.getWidth() + kGap;
        }

        // sync controls sit on the ECHO title row
        const auto& echo = panels[3];
        divBox.setBounds (echo.getRight() - kPad - 66, echo.getY() + 5, 66, 22);
        syncBtn.setBounds (divBox.getX() - 6 - 56, echo.getY() + 5, 56, 22);

        // preset bar
        prevBtn.setBounds (470, 18, 34, 30);
        presetBox.setBounds (510, 18, 260, 30);
        nextBtn.setBounds (776, 18, 34, 30);
    }

private:
    struct Strip
    {
        Slider slider;
        Label label;
        std::unique_ptr<AudioProcessorValueTreeState::SliderAttachment> att;
    };

    void step (int dir)
    {
        const int n = vh::kNumPresets;
        const int idx = (proc.getCurrentProgram() + dir + n) % n;
        presetBox.setSelectedItemIndex (idx, sendNotificationSync);
    }

    void refreshState()
    {
        const bool sync = proc.apvts.getRawParameterValue ("sync")->load() > 0.5f;
        strips[(size_t) vh::pTime].slider.setEnabled (! sync);
        strips[(size_t) vh::pTime].label.setAlpha (sync ? 0.35f : 1.f);
        divBox.setEnabled (sync);
    }

    void timerCallback() override
    {
        refreshState();
        if (presetBox.getSelectedItemIndex() != proc.getCurrentProgram())
            presetBox.setSelectedItemIndex (proc.getCurrentProgram(), dontSendNotification);
    }

    VoxHaloProcessor& proc;
    std::array<Strip, vh::kNumFloat> strips;
    std::array<Colour, vh::kNumFloat> colourOf;
    std::vector<Rectangle<int>> panels;

    TextButton syncBtn, prevBtn, nextBtn;
    ComboBox divBox, presetBox;
    std::unique_ptr<AudioProcessorValueTreeState::ButtonAttachment> syncAtt;
    std::unique_ptr<AudioProcessorValueTreeState::ComboBoxAttachment> divAtt;
};

//==============================================================================
VoxHaloEditor::VoxHaloEditor (VoxHaloProcessor& p) : AudioProcessorEditor (&p)
{
    setLookAndFeel (&laf);
    content = std::make_unique<Content> (p);
    addAndMakeVisible (*content);

    setResizable (true, true);
    setResizeLimits (kW / 2, kH / 2, kW * 2, kH * 2);
    getConstrainer()->setFixedAspectRatio ((double) kW / (double) kH);
    setSize (kW, kH);
}

VoxHaloEditor::~VoxHaloEditor()
{
    content.reset();
    setLookAndFeel (nullptr);
}

void VoxHaloEditor::resized()
{
    if (content != nullptr)
    {
        content->setTransform ({});
        content->setBounds (0, 0, kW, kH);
        content->setTransform (AffineTransform::scale ((float) getWidth() / (float) kW));
    }
}
